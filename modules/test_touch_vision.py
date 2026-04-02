from pathlib import Path
import logging

#from dinolite import DinoLiteSession, build_testtouch_image_name
from unet_predictor import load_unet_weights, predict_unet_mask
from delta_regressor_prediction import (
    load_delta_regressor,
    predict_all_touches_from_mask,
    save_prediction_overlay,
)


def load_test_touch_table(path):
    path = Path(path)
    table = {}

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("Spindle"):
                continue

            parts = s.split()
            if len(parts) < 4:
                continue

            try:
                idx = int(parts[0])
                x, y, z = map(float, parts[1:4])
            except ValueError:
                continue

            table[idx] = (x, y, z)

    return table


def load_vision_models(unet_model_path, delta_model_path, device):
    unet_model = load_unet_weights(unet_model_path, device)
    delta_model = load_delta_regressor(delta_model_path, device)

    return {
        "unet_model": unet_model,
        "delta_model": delta_model,
        "device": device,
    }


def move_camera_to_test_touch(cq, camera_testtouchpath, test_touch_index, camera_zaxis,
                              xy_speed=30, z_speed=4, settle_ms=750):
    tt_table = load_test_touch_table(camera_testtouchpath)

    if test_touch_index not in tt_table:
        raise KeyError(f"Camera test-touch index {test_touch_index} not found in {camera_testtouchpath}")

    camx, camy, camz = tt_table[test_touch_index]

    cq.commands.motion.moveabsolute(["X", "Y"], [camx, camy], [xy_speed, xy_speed])
    cq.commands.motion.waitforinposition(["X"])
    cq.commands.motion.waitforinposition(["Y"])
    cq.commands.motion.waitformotiondone(["X"])
    cq.commands.motion.waitformotiondone(["Y"])
    cq.commands.motion.movedelay(["X", "Y"], delay_time=settle_ms)

    cq.commands.motion.moveabsolute([camera_zaxis], [camz], [z_speed])
    cq.commands.motion.waitforinposition([camera_zaxis])
    cq.commands.motion.waitformotiondone([camera_zaxis])
    cq.commands.motion.movedelay([camera_zaxis], delay_time=settle_ms)

    cq.wait_for_empty()

    return {
        "camera_X": camx,
        "camera_Y": camy,
        "camera_Z": camz,
        "test_touch_index": test_touch_index,
    }


def capture_test_touch_image(test_touch_index, spindle, cuttype, image_output_dir,
                             camera_session_kwargs, naming):
    image_output_dir = Path(image_output_dir)
    image_output_dir.mkdir(parents=True, exist_ok=True)

    image_name = build_testtouch_image_name(
        naming["lenstype"],
        naming["lenssurfaceside"],
        naming["orientation"],
        spindle,
        cuttype,
        test_touch_index,
    )
    output_path = image_output_dir / image_name

    with DinoLiteSession(**camera_session_kwargs) as s:
        capture_result = s.capture_image(output_path)

    return capture_result


def run_ml_on_test_touch_image(image_path, fov_mm, models, threshold=0.22, overlay_dir=None):
    image_path = Path(image_path)

    unet_result = predict_unet_mask(
        image_path=image_path,
        model=models["unet_model"],
        device=models["device"],
        threshold=threshold,
    )

    reg_result = predict_all_touches_from_mask(
        raw_image=unet_result["raw_image"],
        binary_mask=unet_result["binary_mask"],
        fov_mm=fov_mm,
        model=models["delta_model"],
        device=models["device"],
        image_name=image_path.stem,
    )

    selected_prediction = None
    overlay_path = None

    if len(reg_result["predictions"]) > 0:
        selected_prediction = max(
            reg_result["predictions"],
            key=lambda p: p["y"]
        )

        max_y = max(p["y"] for p in reg_result["predictions"])
        assert selected_prediction["y"] == max_y, (
            "Selected prediction is not the lowest / most recent touch in the image"
        )

        if overlay_dir is not None:
            overlay_dir = Path(overlay_dir)
            overlay_dir.mkdir(parents=True, exist_ok=True)

            touch_index = selected_prediction["touch_id"]
            overlay_path = overlay_dir / f"{image_path.stem}_overlay.png"

            save_prediction_overlay(
                result=reg_result,
                touch_index=touch_index,
                save_path=str(overlay_path),
            )


    return {
        "image_path": str(image_path),
        "fov_mm": float(fov_mm),
        "unet_result": unet_result,
        "regressor_result": reg_result,
        "selected_prediction": selected_prediction,
        "overlay_path": str(overlay_path) if overlay_path is not None else None,
    }


def append_test_touch_prediction_log(path, touch_info, ml_result):
    log_path = Path(path) / "test_touch.log"

    if log_path.exists() and log_path.stat().st_size > 0:
        with open(log_path, "rb+") as f:
            f.seek(-1, 2)
            last_char = f.read(1)
            if last_char != b"\n":
                f.write(b"\n")

    pred = ml_result["selected_prediction"]

    logger = logging.getLogger("testtouch_prediction_logger")
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    fh = logging.FileHandler(log_path, mode="a")
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    if pred is None:
        logger.info(
            f"Performed test touch #{touch_info['test_touch_index']} | pred_length_mm=None"
        )
    else:
        logger.info(
            f"Performed test touch #{touch_info['test_touch_index']} | "
            f"pred_length_mm={pred['pred_length_mm']:.6f}"
        )

    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


def perform_test_touch_vision_cycle(cq, path, spindle, cuttype, touch_info, vision_config):
    camera_move_result = move_camera_to_test_touch(
        cq=cq,
        camera_testtouchpath=vision_config["camera_testtouchpath"],
        test_touch_index=touch_info["test_touch_index"],
        camera_zaxis=vision_config["camera_zaxis"],
        xy_speed=vision_config.get("camera_xy_speed", 20),
        z_speed=vision_config.get("camera_z_speed", 10),
        settle_ms=vision_config.get("camera_settle_ms", 500),
    )

    capture_result = capture_test_touch_image(
        test_touch_index=touch_info["test_touch_index"],
        spindle=spindle,
        cuttype=cuttype,
        image_output_dir=vision_config["image_output_dir"],
        camera_session_kwargs=vision_config["camera_session_kwargs"],
        naming=vision_config["naming"],
    )

    ml_result = run_ml_on_test_touch_image(
        image_path=capture_result["image_path"],
        fov_mm=capture_result["fovx_mm"],
        models=vision_config["models"],
        threshold=vision_config.get("unet_threshold", 0.22),
        overlay_dir=vision_config.get("overlay_dir", None),
    )

    append_test_touch_prediction_log(
        path=path,
        touch_info=touch_info,
        ml_result=ml_result,
    )

    return {
        "touch_info": touch_info,
        "camera_move_result": camera_move_result,
        "capture_result": capture_result,
        "ml_result": ml_result,
    }
