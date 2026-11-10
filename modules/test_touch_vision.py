from datetime import datetime
from pathlib import Path
import csv
import hashlib
import json
import logging
import math
import re
import time

from dinolite import DinoLiteSession, build_testtouch_image_name

# The canonical-width pipeline exported by the training notebook (section 10). It replaces the old
# unet_predictor.py + delta_regressor_prediction.py code path, which only fits the November2026 models.
# Keep this file next to the checkpoints it was exported with.
import touch_length_inference as vision

logger = logging.getLogger(__name__)

# The FOV (mm across the image width) the models were trained with. It is the last-resort fallback when no valid
# FOV is available (the result is then flagged "check"), and the reference for the "FOV differs from the
# training FOV" warning.
DEFAULT_FOV_MM = 14.128709


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


def _normalized_sha256(path):
    """Hash of a text file that ignores CRLF/LF differences (git checkouts on Windows)."""
    return hashlib.sha256(Path(path).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def load_vision_models(unet_model_path, delta_model_path, device, recipe_path=None,
                       check_module_copy=True):
    """Load the U-Net and length regressor that were exported together.

    delta_model_path keeps its old name for existing callers; it is the length-regressor checkpoint.
    The export folder must contain model_recipe.json next to the checkpoints. It records the input
    layout, image scale and thresholds, and the loader refuses a regressor that does not match.
    """
    unet_model_path = Path(unet_model_path)
    reg_model_path = Path(delta_model_path)

    if recipe_path is None:
        recipe_path = unet_model_path.parent / "model_recipe.json"
    recipe_path = Path(recipe_path)
    if not recipe_path.is_file():
        raise FileNotFoundError(
            f"model_recipe.json not found at {recipe_path}. Copy the WHOLE export folder "
            "(both .pth files, model_recipe.json, touch_length_inference.py) from the training notebook."
        )

    # Guard against running new weights with a different copy of the inference code.
    exported_copy = unet_model_path.parent / "touch_length_inference.py"
    installed_copy = Path(vision.__file__)
    if (check_module_copy and exported_copy.is_file()
            and exported_copy.resolve() != installed_copy.resolve()
            and _normalized_sha256(exported_copy) != _normalized_sha256(installed_copy)):
        raise RuntimeError(
            f"The installed {installed_copy} differs from {exported_copy}, which was exported with these "
            "checkpoints. Copy the exported file over the installed one (or pass check_module_copy=False)."
        )

    models = vision.load_vision_models(unet_model_path, reg_model_path, device, recipe_path)
    models["delta_model"] = models["length_model"]  # old key name, kept for any existing callers
    try:
        recipe = json.loads(recipe_path.read_text())
        models["model_info"] = dict(folder=unet_model_path.parent.name, run_name=recipe.get("run_name"),
                                    created_at=recipe.get("created_at"))
    except Exception:
        models["model_info"] = dict(folder=unet_model_path.parent.name)
    return models


def move_camera_to_test_touch(cq, camera_testtouchpath, test_touch_index, camera_zaxis,
                              camera_cover_port, flood_port, xy_speed=25, z_speed=4, settle_ms=750):
    tt_table = load_test_touch_table(camera_testtouchpath)

    if test_touch_index not in tt_table:
        raise KeyError(f"Camera test-touch index {test_touch_index} not found in {camera_testtouchpath}")

    camx, camy, camz = tt_table[test_touch_index]

    # turn spindle flood port off
    cq.commands.io.digitaloutputset(axis='X', output_num=flood_port, value=0)
    cq.commands.motion.moveabsolute(["X", "Y"], [camx, camy], [xy_speed, xy_speed])
    cq.commands.motion.waitforinposition(["X"])
    cq.commands.motion.waitforinposition(["Y"])
    cq.commands.motion.waitformotiondone(["X"])
    cq.commands.motion.waitformotiondone(["Y"])
    cq.commands.motion.movedelay(["X", "Y"], delay_time=settle_ms)

    # Open camera cover
    cq.commands.io.digitaloutputset(axis='X', output_num=camera_cover_port, value=1)

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


def capture_test_touch_image(cq, test_touch_index, spindle, cuttype, image_output_dir,
                             camera_session_kwargs, camera_cover_port, flood_port, naming):
    """Take the picture, then ALWAYS put the hardware back in its safe state (camera lifted, cover closed,
    flood back on). Returns the capture-result dict, or None if the camera could not take a picture.

    A camera problem (no frame available, camera not opening, SDK error) is logged and does NOT raise, so the
    cuts can carry on. If the picture was saved and only the status query (AMR/FOV) failed, the picture is kept
    and a minimal result with amr=None, fovx_mm=None is returned.
    """
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

    capture_result = None
    started = time.time()
    try:
        with DinoLiteSession(**camera_session_kwargs) as s:
            capture_result = s.capture_image(output_path)
    except Exception as exc:
        # keep the picture only if THIS capture wrote it (an older file with the same name must not be reused)
        if (output_path.is_file() and output_path.stat().st_size > 1024
                and output_path.stat().st_mtime >= started - 1.0):
            capture_result = {"image_path": str(output_path), "image_name": output_path.name,
                              "amr": None, "fovx_mm": None, "stream_width": None, "stream_height": None,
                              "capture_warning": repr(exc)}
            logger.warning("Test touch #%s: the picture was saved but the camera status query failed (%r); "
                           "FOV/AMR are unavailable for it.", test_touch_index, exc)
        else:
            logger.error("Test touch #%s: the camera could not capture an image (%r). No picture was taken.",
                         test_touch_index, exc)

    # Move delay to ensure photo has time to be taken at desired location
    cq.commands.motion.movedelay(["X", "Y", "ZA"], delay_time=3_000)
    # Lift camera up
    cq.commands.motion.moveabsolute(['ZA'], [-15], [10])
    # Close camera cover
    cq.commands.io.digitaloutputset(axis='X', output_num=camera_cover_port, value=0)

    # turn spindle flood port back on
    cq.commands.io.digitaloutputset(axis='X', output_num=flood_port, value=1)
    cq.wait_for_empty()

    return capture_result


def run_ml_on_test_touch_image(image_path, fov_mm, models, threshold=None, overlay_dir=None):
    """Run the exported pipeline on one image.

    threshold=None uses the threshold stored in the model recipe. The returned dict has the same keys as
    before (image_path, fov_mm, unet_result, regressor_result, selected_prediction, overlay_path) plus
    rejected_frame_components and border_review_required.
    """
    return vision.run_ml_on_test_touch_image(
        image_path, fov_mm, models, threshold=threshold, overlay_dir=overlay_dir)


def _touch_label(touch_info):
    """'[SpindleC Thin] ' in front of a log message, so test touch #48 of SpindleB and of SpindleC can be told apart.

    Empty when no spindle was given, in which case the message is exactly what it was before.
    """
    spindle = (touch_info or {}).get("spindle")
    if not spindle:
        return ""
    cuttype = touch_info.get("cuttype")
    return f"[{spindle} {cuttype}] " if cuttype else f"[{spindle}] "


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

    label = _touch_label(touch_info)
    if pred is None:
        logger.info(
            f"{label}Performed test touch #{touch_info['test_touch_index']} | pred_length_mm=None"
        )
    else:
        logger.info(
            f"{label}Performed test touch #{touch_info['test_touch_index']} | "
            f"pred_length_mm={pred['pred_length_mm']:.6f}"
        )

    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)


def expected_test_touch_image_path(spindle, cuttype, test_touch_index, vision_config):
    """Where the capture step saves the image for this test touch.

    Uses the same name builder and the same pieces as capture_test_touch_image (lens type, lens surface side,
    orientation, spindle, cut type, test touch index), so the two can never disagree.
    """
    naming = vision_config["naming"]
    image_name = build_testtouch_image_name(
        naming["lenstype"],
        naming["lenssurfaceside"],
        naming["orientation"],
        spindle,
        cuttype,
        test_touch_index,
    )
    return Path(vision_config["image_output_dir"]) / image_name


def wait_for_image_file(image_path, timeout_s=10.0, poll_s=0.25, min_bytes=1024):
    """Return the image path once the file exists, is not trivially small, and has stopped growing.

    Raises FileNotFoundError (with a hint about similar names in the folder) if it never appears, or OSError
    if it exists but is still empty/changing when the time is up.
    """
    image_path = Path(image_path)
    deadline = time.monotonic() + float(timeout_s)
    last_size = -1
    size = None
    while True:
        if image_path.is_file():
            size = image_path.stat().st_size
            if size >= min_bytes and size == last_size:
                return image_path
            last_size = size
        if time.monotonic() >= deadline:
            break
        time.sleep(poll_s)

    folder = image_path.parent
    if not folder.is_dir():
        raise FileNotFoundError(f"The image folder does not exist: {folder}")
    if not image_path.is_file():
        match = re.search(r"testtouch(\d+)", image_path.name)
        similar = sorted(p.name for p in folder.glob(f"*testtouch{match.group(1)}*"))[:5] if match else []
        hint = f" Similar files in that folder: {similar}" if similar else ""
        raise FileNotFoundError(f"Image not found after {timeout_s} s: {image_path}.{hint}")
    raise OSError(f"Image {image_path} is incomplete or still being written "
                  f"(size {size} bytes after {timeout_s} s)")


def _read_capture_log_rows(csv_path):
    """Rows of tt_camera_capture_log.csv as dicts. Comma, tab or semicolon separated (a copy pasted out of a
    spreadsheet is tab separated), tolerant of a BOM and of stray spaces in the header."""
    text = Path(csv_path).read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines:
        return []
    header = lines[0]
    delimiter = max([",", "\t", ";"], key=header.count)
    rows = []
    for row in csv.DictReader(lines, delimiter=delimiter):
        rows.append({str(k).strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items() if k})
    return rows


def _read_fov_from_capture_log(csv_path, image_name):
    """Last fovx_mm recorded for this image name in the capture log, or None."""
    found = None
    for row in _read_capture_log_rows(csv_path):
        name = str(row.get("image_name", "")).replace("\\", "/").rsplit("/", 1)[-1]
        if name == image_name:
            try:
                found = float(row["fovx_mm"])
            except (KeyError, TypeError, ValueError):
                pass
    return found


def resolve_fov_mm(image_path, vision_config, capture_result=None):
    """Return (fov_mm, source) for an image.

    Order:
      1. vision_config["fov_override_mm"]: a number (every image) or a dict such as {"Wedge_90deg": 14.128709}
         whose keys are looked for in the image file name.
      2. the camera's reading from this capture (capture_result["fovx_mm"]);
      3. the capture log CSV (vision_config["capture_log_path"], by default tt_camera_capture_log.csv in
         image_output_dir): the last record for this image name, so a value corrected by hand is picked up;
      4. the fallback vision_config.get("fov_fallback_mm", DEFAULT_FOV_MM), reported as "fallback default"
         (set fov_fallback_mm=None to raise instead).
    A value outside fov_valid_range_mm (default 5-40 mm), such as the 391 mm that a failed query once logged,
    is treated as missing.
    """
    name = Path(image_path).name
    lo, hi = vision_config.get("fov_valid_range_mm", (5.0, 40.0))

    def _valid(value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            return None
        return value if math.isfinite(value) and lo <= value <= hi else None

    override = vision_config.get("fov_override_mm")
    if isinstance(override, dict):
        for key, value in override.items():
            if key in name:
                return float(value), f"config override ({key})"
    elif override is not None:
        return float(override), "config override"

    reading = None if capture_result is None else capture_result.get("fovx_mm")
    if reading not in (None, ""):
        valid = _valid(reading)
        if valid is not None:
            return valid, "camera reading"
        logger.warning("Camera FOV reading %r for %s is outside %s-%s mm; ignoring it", reading, name, lo, hi)

    log_path = vision_config.get("capture_log_path")
    if log_path is None and vision_config.get("image_output_dir"):
        candidate = Path(vision_config["image_output_dir"]) / "tt_camera_capture_log.csv"
        log_path = candidate if candidate.is_file() else None
    if log_path:
        try:
            logged = _read_fov_from_capture_log(log_path, name)
        except OSError as exc:
            logger.warning("Could not read the capture log %s (%r)", log_path, exc)
            logged = None
        valid = None if logged is None else _valid(logged)
        if valid is not None:
            return valid, "capture log"

    fallback = vision_config.get("fov_fallback_mm", DEFAULT_FOV_MM)
    if fallback is None:
        raise ValueError(f"No valid FOV for {name} (camera reading, capture log and override all missing).")
    logger.warning("No valid FOV for %s; using the default %s mm", name, fallback)
    return float(fallback), "fallback default"


def assess_prediction(ml_result, vision_config, fov_mm=None, fov_source=None):
    """Plain-language check of one result. It never changes the value that is logged; it says whether to look.

    Settings (all optional): plausible_length_mm=(2.0, 8.0), min_touches=4, max_regressor_mask_gap_mm=0.5.
    """
    lo, hi = vision_config.get("plausible_length_mm", (2.0, 8.0))
    min_touches = vision_config.get("min_touches", 4)
    max_gap = vision_config.get("max_regressor_mask_gap_mm", 0.5)
    selected = ml_result["selected_prediction"]
    n_touches = len(ml_result["regressor_result"]["predictions"])

    if selected is None:
        return dict(status="no_touch", reasons=["no touch detected"], n_touches=n_touches)

    reasons = []
    ignored = ml_result.get("detached_bottom_touches") or []
    if ignored:
        reasons.append(f"{len(ignored)} short detection(s) far below the stack were ignored")
    if ml_result.get("border_review_required"):
        reasons.append("a frame-edge detection below the selected touch was dropped")
    if fov_source == "fallback default":
        reasons.append(f"no valid FOV was available; the default {DEFAULT_FOV_MM} mm was used")
    if fov_mm is not None:
        trained = vision_config.get("fov_trained_mm", DEFAULT_FOV_MM)
        deviation = fov_mm / trained - 1.0
        if abs(deviation) > vision_config.get("fov_deviation_warn", 0.10):
            reasons.append(f"FOV {fov_mm:.2f} mm differs from the training FOV {trained:.2f} mm by {100 * deviation:+.0f}%; "
                           "this is outside the setup the models were trained on")
    length = selected["pred_length_mm"]
    if not lo <= length <= hi:
        reasons.append(f"length {length:.2f} mm is outside the plausible range {lo}-{hi} mm")
    if n_touches < min_touches:
        reasons.append(f"only {n_touches} touches detected")
    if abs(length - selected["seg_length_mm"]) > max_gap:
        reasons.append(f"regressor {length:.2f} mm and mask length {selected['seg_length_mm']:.2f} mm differ by more than {max_gap} mm")
    return dict(status="check" if reasons else "ok", reasons=reasons, n_touches=n_touches)


def write_test_touch_detail_log(path, touch_info, image_path, fov_mm, fov_source, ml_result, assessment, models=None,
                                capture_result=None):
    """One JSON line per test touch in test_touch_detail.jsonl (next to test_touch.log). Never raises."""
    try:
        selected = (ml_result or {}).get("selected_prediction")
        record = dict(
            time=datetime.now().isoformat(timespec="seconds"),
            spindle=touch_info.get("spindle"),
            cuttype=touch_info.get("cuttype"),
            test_touch_index=touch_info["test_touch_index"],
            image=Path(image_path).name,
            fov_mm=fov_mm,
            fov_source=fov_source,
            status=assessment["status"],
            reasons=assessment["reasons"],
            n_touches=assessment.get("n_touches"),
            selected_y_px=None if selected is None else round(float(selected["y"]), 1),
            mask_mm=None if selected is None else round(float(selected["seg_length_mm"]), 4),
            regressor_mm=None if selected is None else round(float(selected["pred_length_mm"]), 4),
            model=(models or {}).get("model_info"),
            camera_fov_mm=(capture_result or {}).get("fovx_mm"),     # None while the FOV/AMR query is unavailable
            camera_amr=(capture_result or {}).get("amr"),
            stream_size=[(capture_result or {}).get("stream_width"), (capture_result or {}).get("stream_height")],
        )
        with open(Path(path) / "test_touch_detail.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        logger.exception("Could not write test_touch_detail.jsonl (test_touch.log is unaffected)")


def _vision_step(path, touch_info, image_path, vision_config, capture_result=None, fov_mm=None):
    """Check the image is on disk, resolve the FOV, run the models, assess, and write both logs."""
    models = vision_config["models"]
    index = touch_info["test_touch_index"]
    try:
        image_path = wait_for_image_file(image_path, timeout_s=vision_config.get("image_wait_s", 10.0))
        if fov_mm is not None:
            fov_mm, fov_source = float(fov_mm), "argument"
        else:
            fov_mm, fov_source = resolve_fov_mm(image_path, vision_config, capture_result)

        ml_result = run_ml_on_test_touch_image(
            image_path=image_path,
            fov_mm=fov_mm,
            models=models,
            threshold=vision_config.get("unet_threshold"),   # None -> threshold from model_recipe.json
            overlay_dir=vision_config.get("overlay_dir", None),
        )
        assessment = assess_prediction(ml_result, vision_config, fov_mm=fov_mm, fov_source=fov_source)
        for reason in assessment["reasons"]:
            logger.warning("%sTest touch #%s: %s (%s)", _touch_label(touch_info), index, reason, image_path)
        append_test_touch_prediction_log(path=path, touch_info=touch_info, ml_result=ml_result)
        write_test_touch_detail_log(path, touch_info, image_path, fov_mm, fov_source, ml_result, assessment, models,
                                    capture_result=capture_result)
        return dict(image_path=str(image_path), fov_mm=fov_mm, fov_source=fov_source,
                    ml_result=ml_result, assessment=assessment)
    except Exception as exc:
        if vision_config.get("on_vision_error", "raise") != "log_none":
            raise
        logger.exception("%sTest touch #%s: the vision step failed; logging pred_length_mm=None", _touch_label(touch_info), index)
        ml_result = {"selected_prediction": None, "error": repr(exc)}
        assessment = dict(status="error", reasons=[repr(exc)], n_touches=None)
        append_test_touch_prediction_log(path=path, touch_info=touch_info, ml_result=ml_result)
        write_test_touch_detail_log(path, touch_info, image_path, fov_mm, "n/a", ml_result, assessment, models,
                                    capture_result=capture_result)
        return dict(image_path=str(image_path), fov_mm=fov_mm, fov_source="n/a",
                    ml_result=ml_result, assessment=assessment)


def record_no_image(path, touch_info, reason, camera_config=None):
    """Record a test touch that has no measurement because there is no image (camera problem, missing file).

    Writes pred_length_mm=None to test_touch.log and a status="no_image" line to test_touch_detail.jsonl,
    so every test touch has an entry. Returns the assessment dict.
    """
    if not touch_info.get("spindle") and (camera_config or {}).get("spindle"):
        touch_info = {**touch_info, "spindle": camera_config["spindle"]}
    ml_result = {"selected_prediction": None, "error": reason}
    assessment = dict(status="no_image", reasons=[reason], n_touches=None)
    append_test_touch_prediction_log(path=path, touch_info=touch_info, ml_result=ml_result)
    write_test_touch_detail_log(path, touch_info, "", None, "n/a", ml_result, assessment,
                                (camera_config or {}).get("models"))
    logger.warning("%sTest touch #%s: %s; logged pred_length_mm=None", _touch_label(touch_info),
                   touch_info["test_touch_index"], reason)
    return assessment


def _already_predicted(log_dir):
    """Image names that already have a line in test_touch_detail.jsonl in this folder."""
    detail = Path(log_dir) / "test_touch_detail.jsonl"
    done = set()
    if detail.is_file():
        for line in detail.read_text(encoding="utf-8").splitlines():
            try:
                done.add(json.loads(line).get("image"))
            except ValueError:
                pass
    return done


def predict_from_capture_log(capture_log_path, vision_config, log_dir, spindle=None, cuttype=None, only_new=True):
    """Predict for the rows of tt_camera_capture_log.csv, the capture log the cutting loop appends to.

    Useful to catch up on images that were captured without models loaded, or to re-run after correcting an FOV in
    the CSV. log_dir is the folder for test_touch.log / test_touch_detail.jsonl: a single folder, a dict
    {spindle: folder} (spindles share test-touch numbers, so give each its own), or a function row -> folder.
    The last row for an image name wins. only_new skips images already in that folder's detail log. If a row's
    image_path does not exist (for example the CSV was copied off the lab PC) the image is looked for next to the CSV.
    Returns one result dict per image processed.
    """
    capture_log_path = Path(capture_log_path)
    latest = {}
    for row in _read_capture_log_rows(capture_log_path):
        if spindle and row.get("spindle") != spindle:
            continue
        if cuttype and row.get("cuttype") != cuttype:
            continue
        if row.get("image_name"):
            latest[row["image_name"]] = row

    config = dict(vision_config)
    config.setdefault("on_vision_error", "log_none")
    results = []
    for image_name, row in latest.items():
        folder = log_dir(row) if callable(log_dir) else (log_dir[row["spindle"]] if isinstance(log_dir, dict) else log_dir)
        folder = Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        if only_new and image_name in _already_predicted(folder):
            continue
        image_path = Path(row["image_path"]) if row.get("image_path") else capture_log_path.parent / image_name
        if not image_path.is_file() and (capture_log_path.parent / image_name).is_file():
            image_path = capture_log_path.parent / image_name
        touch_info = {"test_touch_index": int(float(row["test_touch_index"])),
                      "spindle": row.get("spindle"), "cuttype": row.get("cuttype")}
        capture_like = {"image_path": str(image_path), "fovx_mm": row.get("fovx_mm"), "amr": row.get("amr")}
        step = _vision_step(folder, touch_info, image_path, config, capture_result=capture_like)
        results.append({"touch_info": touch_info, "row": row, **step})
    return results


def predict_test_touch_from_saved_image(path, spindle, cuttype, touch_info, vision_config, fov_mm=None):
    """Predict for a test touch whose image is already on disk (no camera move, no capture).

    The image path is rebuilt from the same naming pieces the capture step uses. fov_mm=None resolves the
    FOV from vision_config (override, then capture_log_path).
    """
    touch_info = {**touch_info, "spindle": spindle, "cuttype": cuttype}
    image_path = expected_test_touch_image_path(spindle, cuttype, touch_info["test_touch_index"], vision_config)
    step = _vision_step(path, touch_info, image_path, vision_config, capture_result=None, fov_mm=fov_mm)
    return {"touch_info": touch_info, "camera_move_result": None, "capture_result": None, **step}


def predict_test_touch_from_capture(path, spindle, cuttype, touch_info, camera_config, capture_result=None):
    """The step the alumina cutting loop calls right after tt_cameracapture().

    camera_config is the same dict tt_cameracapture() already receives, plus "models" (from load_vision_models) and
    any of the optional keys listed in resolve_fov_mm / assess_prediction / _vision_step. capture_result is
    camera_result["capture_result"]; if it is None the image path is rebuilt from the naming pieces instead.

    A vision problem must never abort a cutting run, so unless the config says otherwise a failure is logged
    (pred_length_mm=None plus the reason in test_touch_detail.jsonl) and the cut continues.
    Returns None when no models were provided.
    """
    touch_info = {**touch_info, "spindle": spindle, "cuttype": cuttype}
    if camera_config.get("models") is None:
        logger.warning("No vision models in camera_config; skipping the prediction for test touch #%s",
                       touch_info["test_touch_index"])
        return None
    vision_config = dict(camera_config)
    vision_config.setdefault("on_vision_error", "log_none")
    if capture_result is not None:
        image_path = capture_result["image_path"]
    else:
        image_path = expected_test_touch_image_path(spindle, cuttype, touch_info["test_touch_index"], vision_config)
    step = _vision_step(path, touch_info, image_path, vision_config, capture_result=capture_result)
    return {"touch_info": touch_info, "capture_result": capture_result, **step}


def perform_test_touch_vision_cycle(cq, path, spindle, cuttype, touch_info, vision_config):
    """Move the camera, capture, then predict (used by the lens-cutting flow). Same move/capture helpers as
    tt_cameracapture(); vision_config needs camera_testtouchpath, camera_zaxis, flood_port, image_output_dir,
    camera_session_kwargs, naming and models."""
    touch_info = {**touch_info, "spindle": spindle, "cuttype": cuttype}
    camera_move_result = move_camera_to_test_touch(
        cq=cq,
        camera_testtouchpath=vision_config["camera_testtouchpath"],
        test_touch_index=touch_info["test_touch_index"],
        camera_zaxis=vision_config["camera_zaxis"],
        camera_cover_port=vision_config.get("camera_cover_port", 4),
        flood_port=vision_config.get("flood_port"),
        xy_speed=vision_config.get("camera_xy_speed", 20),
        z_speed=vision_config.get("camera_z_speed", 4),
        settle_ms=vision_config.get("camera_settle_ms", 750),
    )

    capture_result = capture_test_touch_image(
        cq=cq,
        test_touch_index=touch_info["test_touch_index"],
        spindle=spindle,
        cuttype=cuttype,
        image_output_dir=vision_config["image_output_dir"],
        camera_session_kwargs=vision_config["camera_session_kwargs"],
        camera_cover_port=vision_config.get("camera_cover_port", 4),
        flood_port=vision_config.get("flood_port"),
        naming=vision_config["naming"],
    )

    if capture_result is None:
        assessment = record_no_image(path, touch_info, "camera could not capture an image", vision_config)
        return {
            "touch_info": touch_info,
            "camera_move_result": camera_move_result,
            "capture_result": None,
            "ml_result": {"selected_prediction": None, "error": "camera could not capture an image"},
            "assessment": assessment,
            "fov_mm": None,
            "fov_source": "n/a",
        }

    step = _vision_step(path, touch_info, capture_result["image_path"], vision_config, capture_result=capture_result)

    return {
        "touch_info": touch_info,
        "camera_move_result": camera_move_result,
        "capture_result": capture_result,
        "ml_result": step["ml_result"],
        "assessment": step["assessment"],
        "fov_mm": step["fov_mm"],
        "fov_source": step["fov_source"],
    }
