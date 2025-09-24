import automation1 as a1
import time
import numpy as np
import matplotlib.pyplot as plt

import os
import serial
from pathlib import Path
from pprint import pprint
import pandas as pd
import re

import sys
sys.path.append('C:\\Users\\UNIVERSITY\\git\\')
sys.path.append('C:\\Users\\UNIVERSITY\\git\\metalens\\')
import metalens
import core_utils as cu 


def check_io_status(controller, port, name, axis='X', execution_task_index=1):
    """
    Check the status of a digital output (flood cooling, spindle cooling, probe, etc.)
    
    Parameters
    ----------
    controller : object
        Automation1 controller instance.
    port : int
        Digital IO output port number.
    name : str, optional
        Human-readable device name for output string (default="Device").
    axis : str
        Axis associated with the digital output. Default is  "X"
    execution_task_index : int, optional
        Task index to query (default=1).
    
    Returns
    -------
    str
        Status message of the given device.
    """
    # Query output state
    current = controller.runtime.commands.io.digitaloutputget(
        axis=axis,
        output_num=port,
        execution_task_index=execution_task_index,
    )

    # Build status message
    if int(current) == 1:
        status = f"{name} is ON"
    elif int(current) == 0:
        status = f"{name} is OFF"
    else:
        status = f"{name} in awkward state. Stop and check hardware."

    return status


def enable_zaxes(controller, cq, z_axes):
    """
    Enable X, Y, and one or more Z axes.

    Args
    ----
    controller : a1.Controller
    cq         : Command queue
    z_axes     : str or list of str  ("ZC" or ["ZA", "ZB"])

    Note: controller and command queue must already be instantiated. 
    """
    print("Queue was initiated on task:", cq.task_index, "capacity:", cq.command_capacity)

    if isinstance(z_axes, str):
        z_axes = [z_axes]

    cq.pause()
    for axis in ["X", "Y"] + z_axes:
        cq.commands.motion.enable(axis)
    print(f"Enabled axes: X, Y, {', '.join(z_axes)}")

    cq.resume()
    cq.wait_for_empty()
    controller.runtime.commands.end_command_queue(cq)


def prepare_zaxes(controller, cq, z_axes, spindle_ports, flood_ports, active_z,
                  z_position=0, z_speed=20, delay_ms=11_000, io_axis='X'):
    """
    Prepare Z axes for cutting: move all Z axes to 0, reset flood cooling status, turn on all spindles,
    and activate flood cooling only for the currently active Z.

    Args
    ----
    controller    : a1.Controller
    cq            : Command queue
    z_axes        : list of str       e.g., ["ZB", "ZC", "ZD"]
    spindle_ports : list of int       spindle DOs (must match z_axes)
    flood_ports   : list of int       flood DOs (must match z_axes)
    active_z      : str               which Z axis should have its flood cooling ON
    z_position    : float             target Z position (mm) for all Zs
    z_speed       : float             move speed (mm/s) for all Zs
    delay_ms      : int               dwell time (ms)
    io_axis       : str               I/O axis context (usually "X")

    Note:
    This includes some dwell times for turning flood cooling off and on in case of lag in general. 
    """
    if isinstance(z_axes, str):
        raise ValueError("z_axes must be a list when using multi-axis prepare")

    if not (len(z_axes) == len(spindle_ports) == len(flood_ports)):
        raise ValueError("z_axes, spindle_ports, and flood_ports must be same length")

    if active_z not in z_axes:
        raise ValueError(f"active_z {active_z} must be one of {z_axes}")

    cq.pause()

    # --- Move all Zs to position ---
    positions = [z_position] * len(z_axes)
    speeds    = [z_speed]    * len(z_axes)
    cq.commands.motion.moveabsolute(z_axes, positions, speeds)
    cq.commands.motion.waitforinposition(z_axes)
    cq.resume()
    cq.wait_for_empty()
    # TODO: should actually query the position of the z axis and have it print that instead
    print(f"Moved {', '.join(z_axes)} to {z_position:.4f} mm. Resetting flood cooling, turning on spindles, and enabling flood for active Z axis, {active_z}.")
    cq.pause()

    # --- Flood OFF for all ---
    for fp in flood_ports:
        cq.commands.io.digitaloutputset(axis=io_axis, output_num=fp, value=0)
        cq.commands.motion.movedelay(z_axes, delay_time=3_000)

    # --- Spindles ON for all ---
    for sp in spindle_ports:
        cq.commands.io.digitaloutputset(axis=io_axis, output_num=sp, value=1)

    # --- Flood ON only for active Z ---
    active_index = z_axes.index(active_z)
    cq.commands.io.digitaloutputset(axis=io_axis, output_num=flood_ports[active_index], value=1)

    # --- Hold dwell ---
    cq.commands.motion.movedelay(["X", "Y"] + z_axes, delay_time=delay_ms)
    cq.resume()
    cq.wait_for_empty()

    #print(f"All spindles ON {spindle_ports}; flood ON for {active_z} (DO {flood_ports[active_index]}).")
    controller.runtime.commands.end_command_queue(cq)
    print("Command queue ended after prepping Z axes.")
    for fp in flood_ports:
        name = f"Flood cooling port {fp}"
        status = check_io_status(controller=controller, port=fp, name=name, axis='X', execution_task_index=1)
        print(status)
    for sp in spindle_ports:
        name = f'Spindle port {sp}'
        status = check_io_status(controller=controller, port=sp, name=name, axis='X', execution_task_index=1)
        print(status)


def check_axis_status_position(controller, axis):
    """
    Check drive status and program position for a given axis.
    
    Parameters
    ----------
    controller : object
        Automation1 controller instance.
    axis : str
        Axis name (e.g., "ZA", "ZB", "ZC").
    """
    cfg = a1.StatusItemConfiguration()
    cfg.axis.add(a1.AxisStatusItem.AxisStatus, axis)
    cfg.axis.add(a1.AxisStatusItem.ProgramPosition, axis)

    results = controller.runtime.status.get_status_items(cfg)

    # Extract values
    axis_status = results.axis.get(a1.AxisStatusItem.AxisStatus, axis).value
    program_pos  = results.axis.get(a1.AxisStatusItem.ProgramPosition, axis).value

    # Convert drive status to int and mask off camming bit (bit 16)
    camming_bit = int(axis_status) & (1 << 16)

    return {
        "axis": axis,
        "camming_bit": bool(camming_bit),
        "program_position": program_pos,
        "axis_status_raw": int(axis_status)
    }


def read_startend_coords(master_path, camnum):
    df = load_master_table(master_path)

    # make sure camnum is a string with leading zeros like in the file
    camnum_str = str(camnum).zfill(4)

    # filter rows where column 0 == camnum_str
    row = df[df[0] == camnum_str]

    if row.empty:
        raise ValueError(f"camnum {camnum_str} not found in {master_path}")

    # extract x, y, z as scalars
    xstart = row.iloc[0, 1]
    ystart = row.iloc[0, 2]
    zstart = row.iloc[0, 3]
    yend = row.iloc[0, 4]

    return xstart, ystart, zstart, yend
    

def load_master_table(master_path):
    """
    Read Master.txt (or .dat) as whitespace-delimited without headers.
    Keeps column 0 as string so leading zeros aren't lost.
    Returns a DataFrame with columns:
      0 = camnum_str, 1 = X, 2 = Y, 3 = Z, 4 = feed (if present)
    """
    master_path = Path(master_path)
    assert master_path.exists(), f"Master file not found: {master_path}"

    # comment='#' lets you keep notes in the file safely
    df = pd.read_csv(
        master_path,
        sep='\s+',
        header=None,
        comment="#",
        dtype={0: str},      # preserve '0007'
        engine="python",
    )
    # Drop empty rows if any slipped through
    df = df.dropna(how="all")
    
    return df


def iter_cam_paths_from_master(master_path, base_path, cuttype):
    """
    Yields (row_idx, camnum_int, cam_filename, cam_path, row) for each row in Master.txt.
    - camnum_int is the integer form for formatting (7 → '0007')
    - row is the entire pandas row if you want X/Y/Z/feed later
    """
    base_path = Path(base_path)
    df = load_master_table(master_path)
    campaths = []
    for i, row in df.iterrows():
        camnum_str = str(row[0]).strip()

        # Be forgiving: extract digits just in case (e.g., '0007' or '0007,' etc.)
        m = re.search(r"(\d+)", camnum_str)
        if not m:
            print(f"[warn] row {i}: could not parse cam number from '{camnum_str}'")
            continue

        camnum_int = int(m.group(1))  # 7, 12, etc.
        cam_filename = f"CutCam{cuttype}{camnum_int:04d}.Cam"
        cam_path = base_path / cam_filename
        campaths.append(cam_path)

        if not cam_path.exists():
            print(f"[warn] row {i}: missing {cam_path}")
            continue

    return campaths# i, camnum_int, cam_filename, cam_path, row


def loadcampath(master_path, base_path, cuttype, camnum):
    """
    Yields (row_idx, camnum_int, cam_filename, cam_path, row) for each row in Master.txt.
    - camnum_int is the integer form for formatting (7 → '0007')
    - row is the entire pandas row if you want X/Y/Z/feed later
    """
    base_path = Path(base_path)
    df = load_master_table(master_path)
    campaths = []
    for i, row in df.iterrows():
        camnum_str = str(row[0]).strip()

        # Be forgiving: extract digits just in case (e.g., '0007' or '0007,' etc.)
        m = re.search(r"(\d+)", camnum_str)
        if not m:
            print(f"[warn] row {i}: could not parse cam number from '{camnum_str}'")
            continue

        camnum_int = int(m.group(1))  # 7, 12, etc.
        cam_filename = f"CutCam{cuttype}{camnum_int:04d}.Cam"
        cam_path = base_path / cam_filename
        campaths.append(cam_path)

        if not cam_path.exists():
            print(f"[warn] row {i}: missing {cam_path}")
            continue

    return campaths# i, camnum_int, cam_filename, cam_path, row


def get_cutcam_coords(campath):
    """
    """
    leader_values = []
    follower_values = []
    
    with open(campath, "r") as f:
        for ln in f:
            s = ln.strip()
            parts = s.replace(",", " ").split()
            if len(parts) < 2:
                continue
            try:
                leader = float(parts[1]) # was 0 
                follower = float(parts[2]) # was 1
            except ValueError:
                print(f"[warn] Skipping non-numeric line: {s}")
                continue
            leader_values.append(leader)
            follower_values.append(follower)
        
            
    return leader_values, follower_values


def cutcamming(controller, cq, path, zaxis, cuttype, safelift, feedspeed, floodport, rot=None):
    """
    path = path straight up to the cutcamming file
    add docstrings here
    """
    path = Path(path)
    assert path.exists(), f"Base path not found: {path}"

    mastername = "Master.txt"
    masterpath = Path(path) / mastername  
    assert masterpath.exists(), f"Master file not found: {masterpath}"

    cu._check_lockfile(path)
    campaths = iter_cam_paths_from_master(master_path=masterpath, base_path=path, cuttype=cuttype)

    if rot:
        cq.commands.motion.moveabsolute(["U"], [rot], [20])
        cq.commands.motion.waitforinposition(["U"])
        cq.commands.motion.waitformotiondone(["U"])
        cq.commands.motion.movedelay(["U"], delay_time=1_000)
    
    am = cq.commands.advanced_motion
    for campath in campaths:
        assert campath.exists(), f"Campath not found: {campath}"
        yvals, zvals = get_cutcam_coords(campath)

        # now set up aerotech camming conditions
        am.cammingfreetable(1) 
        am.cammingloadtablefromarray(
            table_num=1,
            leader_values=yvals,
            follower_values=zvals,
            num_values=len(yvals),
            units_mode=a1.CammingUnits.Primary,               
            interpolation_mode=a1.CammingInterpolation.Linear, 
            wrap_mode=a1.CammingWrapping.NoWrap,               
            table_offset=0.0)
        print('Camming table loaded')

        camnum = Path(campath).stem[-4:]
        xstart, ystart, zstart, yend = read_startend_coords(master_path=masterpath, camnum=camnum)

        
        SPEED_Y  = 20.0  # mm/s
        SPEED_X  = 20.0   
        SPEED_Z = 8.0  # (down to zstart+2)
        # TODO: PRIORITY 1 --- check if we want ZC touch speed to be slower
        SPEED_Z_TOUCH    = 0.1  # (final settle at zstart)
        
        # move to start positions, wait for in position
        cq.commands.motion.moveabsolute(["X", "Y"], [xstart, ystart], [SPEED_Y,  SPEED_X])
        cq.commands.motion.waitforinposition(["Y"])
        cq.commands.motion.waitforinposition(["X"])
        cq.commands.motion.movedelay(["X", "Y"], delay_time=1_500)

        cq.commands.motion.moveabsolute([zaxis], [zstart + 2.0], [SPEED_Z])
        cq.commands.motion.waitforinposition([zaxis])
        cq.commands.motion.moveabsolute([zaxis], [zstart], [SPEED_Z_TOUCH])
        cq.commands.motion.waitforinposition([zaxis])
        cq.commands.motion.waitformotiondone([zaxis])
        
        
        while True:
            statuses = check_axis_status_position(controller=controller, axis=zaxis)
            if statuses['camming_bit'] is False:
                break # in desired state, stop looping
            time.sleep(0.1)  

        cq.commands.advanced_motion.cammingon(
            follower_axis=zaxis,
            leader_axis="Y",
            table_num=1,
            source=a1.CammingSource.PositionCommand,  # leader uses position
            output=a1.CammingOutput.RelativePosition  
        )

        ## TODO: there's gotta be something else we can do with the waitforinposition and wait for move done
        ## TODO: something about InPositionTime value that we might be able to toggle
        while True:
            statuses = check_axis_status_position(controller=controller, axis=zaxis)
            if statuses['camming_bit'] is True:
                print(f"{zaxis} camming bit is True; ready to cut line {camnum}")
                break # in desired state, stop looping
            time.sleep(0.1)  

        # when first cutting a line, for the first 10mm, go at a slower feedspeed, 5mm/s
        cq.commands.motion.moveabsolute(["Y"], [ystart+10], [5.0])
        cq.commands.motion.waitforinposition(["Y"])
        cq.commands.motion.waitformotiondone(["Y"])

        # proceed to cutting the rest of the cut at assigned feedspeed
        cq.commands.motion.moveabsolute(["Y"], [yend], [feedspeed])
        cq.commands.motion.waitforinposition(["Y"])
        cq.commands.motion.waitformotiondone(["Y"])
        cq.commands.motion.movedelay(["Y"], delay_time=1_000)

        am.cammingoff(follower_axis=zaxis) 

        # check that camming bit status is False
        while True:
            statuses = check_axis_status_position(controller=controller, axis=zaxis)
            if statuses['camming_bit'] is False:
                print(f"{zaxis} camming status is off, {camnum} line finished cutting.")
                break # in desired state, stop looping
            time.sleep(0.1)  
        
        # retract ZC and free table 1
        # TODO: PRIORITY 1-- CHECK IF THIS IS THE ONLY PLACE THAT SAFELIFT IS USED IN SOURCE CODE
        cq.commands.motion.moveabsolute([zaxis], [zstart + safelift], [SPEED_Z])
        cq.commands.motion.waitforinposition([zaxis])
        cq.commands.motion.waitformotiondone([zaxis])
        cq.commands.advanced_motion.cammingfreetable(1)
        cq.commands.motion.movedelay([zaxis], delay_time=1_000)

        # drain the queue before we are ready to cut the next line
        cq.wait_for_empty()

    cq.commands.io.digitaloutputset(axis='X', output_num=floodport, value=0)
    cq.commands.motion.moveabsolute([zaxis], [0.0], [11])
    controller.runtime.commands.end_command_queue(cq)

    # --- Flood OFF ---
    

    lockfile = path/'lockfile.lock'
    with open(lockfile, "w") as f:
        f.write("")


def cutalumina(controller, cq, path, zaxis, cuttype, safelift, feedspeed,
               testtouchpath, wearshiftpath, lines_per_test):
    path = Path(path)
    assert path.exists(), f"Base path not found: {path}"

    mastername = "Master.txt"
    masterpath = Path(path) / mastername  
    assert masterpath.exists(), f"Master file not found: {masterpath}"

    # Load wear shift table
    ws_table = load_wear_shift_table(wearshiftpath)

    cu._check_lockfile(path)
    campaths = iter_cam_paths_from_master(master_path=masterpath, base_path=path, cuttype=cuttype)
    
    am = cq.commands.advanced_motion
    for campath in campaths[0:4]:
        assert campath.exists(), f"Campath not found: {campath}"
        
        camnum = Path(campath).stem[-4:]
        camnum_int = int(camnum)
        wearshift = ws_table.get(camnum_int, 0.0)

        # get coordinates, including original non-wear shifted z coordinate
        yvals, zvals = get_cutcam_coords(campath)
        xstart, ystart, zstart_raw, yend = read_startend_coords(master_path=masterpath, camnum=camnum)
        
        # apply wear-shift to camming z-values and zstart value
        zvals_shifted = [z + wearshift for z in zvals]
        zstart = zstart_raw + wearshift
        print(zstart)

    
        # now set up aerotech camming conditions
        am.cammingfreetable(1) 
        am.cammingloadtablefromarray(
            table_num=1,
            leader_values=yvals,
            follower_values=zvals_shifted,
            num_values=len(yvals),
            units_mode=a1.CammingUnits.Primary,               
            interpolation_mode=a1.CammingInterpolation.Linear, 
            wrap_mode=a1.CammingWrapping.NoWrap,               
            table_offset=0.0)
        print(f'Camming table loaded for {camnum} file with wear shift = {wearshift}')
        
        SPEED_Y  = 20.0  # mm/s
        SPEED_X  = 20.0   
        SPEED_Z = 12.0  # (down to zstart+2)
        # TODO: PRIORITY 1 --- check if we want ZC touch speed to be slower
        SPEED_Z_TOUCH    = 0.1  # (final settle at zstart)
        
        # move to start positions, wait for in position
        cq.commands.motion.moveabsolute(["X", "Y"], [xstart, ystart], [SPEED_Y,  SPEED_X])
        cq.commands.motion.waitforinposition(["Y"])
        cq.commands.motion.waitforinposition(["X"])
        cq.commands.motion.movedelay(["X", "Y"], delay_time=1_500)

        cq.commands.motion.moveabsolute([zaxis], [zstart + 2.0], [SPEED_Z])
        cq.commands.motion.waitforinposition([zaxis])
        cq.commands.motion.moveabsolute([zaxis], [zstart+1], [0.5])
        cq.commands.motion.waitforinposition([zaxis])
        cq.commands.motion.waitformotiondone([zaxis])
        
        cq.commands.motion.moveabsolute([zaxis], [zstart+0.5], [0.1])
        cq.commands.motion.waitforinposition([zaxis])
        cq.commands.motion.waitformotiondone([zaxis])
        
        cq.commands.motion.moveabsolute([zaxis], [zstart], [0.01])
        cq.commands.motion.waitforinposition([zaxis])
        cq.commands.motion.waitformotiondone([zaxis])
        
        cq.commands.motion.movedelay([zaxis], delay_time=1_000)
        
        while True:
            statuses = check_axis_status_position(controller=controller, axis=zaxis)
            if statuses['camming_bit'] is False:
                break # in desired state, stop looping
            time.sleep(0.1)  

        cq.commands.advanced_motion.cammingon(
            follower_axis=zaxis,
            leader_axis="Y",
            table_num=1,
            source=a1.CammingSource.PositionCommand,  # leader uses position
            output=a1.CammingOutput.RelativePosition  
        )

        ## TODO: there's gotta be something else we can do with the waitforinposition and wait for move done
        ## TODO: something about InPositionTime value that we might be able to toggle
        while True:
            statuses = check_axis_status_position(controller=controller, axis=zaxis)
            if statuses['camming_bit'] is True:
                print(f"{zaxis} camming bit is True; ready to cut line {camnum}")
                break # in desired state, stop looping
            time.sleep(0.1)  

        # move at slower feespeed for first 10 mm
        cq.commands.motion.moveabsolute(["Y"], [ystart+10], [5])
        cq.commands.motion.waitforinposition(["Y"])
        cq.commands.motion.waitformotiondone(["Y"])
        
        cq.commands.motion.moveabsolute(["Y"], [yend], [feedspeed])
        cq.commands.motion.waitforinposition(["Y"])
        cq.commands.motion.waitformotiondone(["Y"])
        cq.commands.motion.movedelay(["Y"], delay_time=2_000)

        am.cammingoff(follower_axis=zaxis) 

        # check that camming bit status is False
        while True:
            statuses = check_axis_status_position(controller=controller, axis=zaxis)
            if statuses['camming_bit'] is False:
                print(f"{zaxis} camming status is off, {camnum} line finished cutting.")
                break # in desired state, stop looping
            time.sleep(0.1)  
        
        # retract ZC and free table 1
        # TODO: PRIORITY 1-- CHECK IF THIS IS THE ONLY PLACE THAT SAFELIFT IS USED IN SOURCE CODE
        cq.commands.motion.moveabsolute([zaxis], [zstart + safelift], [SPEED_Z])
        cq.commands.motion.waitforinposition([zaxis])
        cq.commands.motion.waitformotiondone([zaxis])
        cq.commands.advanced_motion.cammingfreetable(1)
        cq.commands.motion.movedelay([zaxis], delay_time=2_000)

        # drain the queue before we are ready to cut the next line
        cq.wait_for_empty()


        if (camnum_int + 1) % lines_per_test == 0:
            info = run_alumina_test_touch(
                controller = controller,
                cq=cq,
                camnum=camnum,
                testtouchpath = testtouchpath,
                wearshiftpath=wearshiftpath,
                zaxis=zaxis,
                lines_per_test=lines_per_test,
            )
            print(f"did test touch #{info['test_touch_index']}", info)

        
    cq.commands.motion.moveabsolute([zaxis], [0.0], [15])
    controller.runtime.commands.end_command_queue(cq)

    lockfile = path/'lockfile.lock'
    with open(lockfile, "w") as f:
        f.write("")


def run_alumina_test_touch(
    controller,
    cq,
    camnum,
    testtouchpath,
    wearshiftpath,
    zaxis,
    lines_per_test,
):
    camnum = int(camnum)

    tt_table = load_test_touch_table(testtouchpath)
    ws_table = load_wear_shift_table(wearshiftpath)

    tt_index = camnum // lines_per_test
    print('tt index', tt_index)
    if tt_index not in tt_table:
        raise KeyError(f"Test-touch index {tt_index} not found in {test_touch_file}")

    ttx, tty, ttz = tt_table[tt_index]
    wear_shift = ws_table.get(camnum, 0.0)
    z_touch = ttz + wear_shift

    # XY
    cq.commands.motion.moveabsolute(["X", "Y"], [ttx, tty], [20, 20])
    cq.commands.motion.waitforinposition(["X"])
    cq.commands.motion.waitforinposition(["Y"])
    cq.commands.motion.movedelay(["X", "Y"], delay_time = 1_000)

    # Z to z_touch + 2 @ z_approach_speed
    cq.commands.motion.moveabsolute([zaxis], [z_touch + 2.0], [10])
    cq.commands.motion.waitforinposition([zaxis])

    # Z to z_touch + 1 @ z_slow_speed
    cq.commands.motion.moveabsolute([zaxis], [z_touch + 1.0], [0.5])
    cq.commands.motion.waitforinposition([zaxis])

    # Z to z_touch @ z_final_speed
    cq.commands.motion.moveabsolute([zaxis], [z_touch+0.5], [0.05])
    cq.commands.motion.waitforinposition([zaxis])
    
    cq.commands.motion.moveabsolute([zaxis], [z_touch], [0.01])
    cq.commands.motion.waitforinposition([zaxis])

    # queue-based hold at depth (ms)
    cq.commands.motion.movedelay([zaxis], delay_time=500)

    # retract to Z = 0
    cq.commands.motion.moveabsolute([zaxis], [0.0], [20])
    cq.commands.motion.waitforinposition([zaxis])
    cq.commands.motion.movedelay(['ZC'], delay_time=2_000)

    # X out
    # TODO: UNCOMMENT THIS OUT PRIORITY 1
    #cq.commands.motion.moveabsolute(["X"], [-270], [20]) 
    #cq.commands.motion.waitforinposition(["X"])

    return {
        "camnum": camnum,
        "test_touch_index": tt_index,
        "X": ttx, "Y": tty,
        "Z_test_touch_raw": ttz,
        "wear_shift": wear_shift,
        "Z_touch_final": z_touch,
    }


def run_test_touch(
    controller,
    cq,
    camnum,
    testtouchpath,
    zaxis,
    lines_per_test,
    zshift = None,
    rot = None
):
    """
    Lines per test arg tells us how many lines we wanna cut between test touches

    can also add a rotation argument for this function too should we need it
    default can be rot = None

    This is for running within the cutlens function for when we wanna cut high frequency lenses and are going by batches of 
    100-200 cuts. Similar to alumina but blade doesn't wear with silicon the same way so we'll put in raw z corrections to make
    based on these test touches that are run when running the cuts
    rot = the rotation angel to do the test touch on 

    NOTE THAT THIS FUNCTION DOES NOT END THE QUEUE AS IT WORKS INSIDE OTHER FUNCTIONS. IMPORTANT WARNING TO STATE

    """
    camnum = int(camnum)

    tt_table = load_test_touch_table(testtouchpath)

    tt_index = camnum // lines_per_test
    print('tt index', tt_index)
    if tt_index not in tt_table:
        raise KeyError(f"Test-touch index {tt_index} not found in {testtouchpath}")

    ttx, tty, ttz = tt_table[tt_index]
    if zshift:
        z_touch = ttz + zshift
    else:
        z_touch = ttz

    # XY
    cq.commands.motion.moveabsolute(["X", "Y"], [ttx, tty], [20, 20])
    cq.commands.motion.waitforinposition(["X"])
    cq.commands.motion.waitforinposition(["Y"])
    cq.commands.motion.movedelay(["X", "Y"], delay_time = 1_000)

    if rot is not None:
        cq.pause()
        cq.commands.motion.moveabsolute(axes=["U"], positions=[rot], speeds=[20])
        cq.commands.motion.waitforinposition(["U"])
        cq.commands.motion.waitformotiondone(["U"])
        cq.commands.motion.movedelay(["U"], delay_time=1_000)
        cq.resume()

    # Z to z_touch + 2 @ z_approach_speed
    cq.commands.motion.moveabsolute([zaxis], [z_touch + 2.0], [10])
    cq.commands.motion.waitforinposition([zaxis])

    # Z to z_touch + 1 @ z_slow_speed
    cq.commands.motion.moveabsolute([zaxis], [z_touch + 1.0], [0.5])
    cq.commands.motion.waitforinposition([zaxis])

    # Z to z_touch @ z_final_speed
    cq.commands.motion.moveabsolute([zaxis], [z_touch+0.5], [0.05])
    cq.commands.motion.waitforinposition([zaxis])
    
    cq.commands.motion.moveabsolute([zaxis], [z_touch], [0.01])
    cq.commands.motion.waitforinposition([zaxis])

    # queue-based hold at depth (ms)
    cq.commands.motion.movedelay([zaxis], delay_time=500)

    # retract to Z = 0
    cq.commands.motion.moveabsolute([zaxis], [0.0], [20])
    cq.commands.motion.waitforinposition([zaxis])
    cq.commands.motion.movedelay(['ZC'], delay_time=500)

    # X out
    cq.commands.motion.moveabsolute(["X"], [-275], [30]) 
    cq.commands.motion.waitforinposition(["X"])

    return {
        "camnum": camnum,
        "test_touch_index": tt_index,
        "X": ttx, "Y": tty,
        "Z_test_touch_raw": ttz,
        "wear_shift": wear_shift,
        "Z_touch_final": z_touch,
    }


def cutlens_segments(controller, cq, path, spindle, zaxis, cuttype, safelift, feedspeed,
               testtouchpath, lines_per_test, cut_rot=None, tt_rot=None, zshift=None):
    """
    Cut lens segment mimic the cut alumina but instead of a wearshift file path it's given 
    a zcorrection file path 

    Ultimately, this function won't be necessary if we're generating wearshift files that 
    are just 1 value all the way down the line if we're using the same code that generates wear
    shift files and just stating that the blade wear is 0

    path is path to CutCamming{cuttype} path; i.e., the thinking involved for the new z shifts
    is done outside of this function for simplicity's sake (in shiftZ_silicon from metalens modules)
    cut_rot is the rotation that we do our cuts on
    tt_rot is the rotation that we need to do our test touch rotation on 

    spindle is string for path concatenation: 'SpindleC'
    zshift is any z correction we applied from shiftZ_silicon metalens function
    """
    path = Path(path)
    assert path.exists(), f"Base path not found: {path}"
    cutpath = path / spindle / f"CutCamming{cuttype}/" 

    mastername = "Master.txt"
    masterpath = cutpath / mastername
    assert masterpath.is_file(), f"Master file not found: {masterpath}"
    
    cu._check_lockfile(path)
    campaths = iter_cam_paths_from_master(master_path=masterpath, base_path=cutpath, cuttype=cuttype)

    
    cq.pause()
    cq.commands.motion.moveabsolute([zaxis], [0], [5])
    cq.commands.motion.waitforinposition([zaxis])
    cq.commands.motion.waitformotiondone([zaxis])
    cq.commands.motion.movedelay([zaxis], delay_time=500)

    cq.resume()
    if cut_rot:
        cq.commands.motion.moveabsolute(["U"], [cut_rot], [20])
        cq.commands.motion.waitforinposition(["U"])
        cq.commands.motion.waitformotiondone(["U"])
        cq.commands.motion.movedelay(["U"], delay_time=1_000)

    
    
    am = cq.commands.advanced_motion
    for campath in campaths:
        assert campath.exists(), f"Campath not found: {campath}"
        
        camnum = Path(campath).stem[-4:]
        camnum_int = int(camnum)

        yvals, zvals = get_cutcam_coords(campath)
        xstart, ystart, zstart, yend = read_startend_coords(master_path=masterpath, camnum=camnum)

        # now set up aerotech camming conditions
        am.cammingfreetable(1) 
        am.cammingloadtablefromarray(
            table_num=1,
            leader_values=yvals,
            follower_values=zvals,
            num_values=len(yvals),
            units_mode=a1.CammingUnits.Primary,               
            interpolation_mode=a1.CammingInterpolation.Linear, 
            wrap_mode=a1.CammingWrapping.NoWrap,               
            table_offset=0.0)
        
        SPEED_Y  = 20.0  # mm/s
        SPEED_X  = 20.0   
        SPEED_Z = 12.0  # (down to zstart+2)

        SPEED_Z_TOUCH    = 0.1  # (final settle at zstart)
        
        # move to start positions, wait for in position
        cq.commands.motion.moveabsolute(["X", "Y"], [xstart, ystart], [SPEED_Y,  SPEED_X])
        cq.commands.motion.waitforinposition(["Y"])
        cq.commands.motion.waitforinposition(["X"])
        cq.commands.motion.movedelay(["X", "Y"], delay_time=400)


        cq.commands.motion.moveabsolute([zaxis], [zstart + 2.0], [SPEED_Z])
        cq.commands.motion.waitforinposition([zaxis])
        cq.commands.motion.moveabsolute([zaxis], [zstart+1], [0.5])
        cq.commands.motion.waitforinposition([zaxis])
        cq.commands.motion.waitformotiondone([zaxis])
        
        cq.commands.motion.moveabsolute([zaxis], [zstart], [0.1])
        cq.commands.motion.waitforinposition([zaxis])
        cq.commands.motion.waitformotiondone([zaxis])
        cq.commands.motion.movedelay([zaxis], delay_time=500)
        cq.wait_for_empty()
        
        while True:
            statuses = check_axis_status_position(controller=controller, axis=zaxis)
            if statuses['camming_bit'] is False:
                break 
            time.sleep(0.1)  

        cq.commands.advanced_motion.cammingon(
            follower_axis=zaxis,
            leader_axis="Y",
            table_num=1,
            source=a1.CammingSource.PositionCommand,  
            output=a1.CammingOutput.RelativePosition  
        )


        while True:
            statuses = check_axis_status_position(controller=controller, axis=zaxis)
            if statuses['camming_bit'] is True:
                print(f"{zaxis}: ready to cut line {camnum}")
                break 
            time.sleep(0.1)  

        # move at slower feedspeed [feedspeed of 5] for first 10 mm 
        # temporarily changed to 20 -- 9/24/25
        cq.commands.motion.moveabsolute(["Y"], [ystart+20], [5])
        cq.commands.motion.waitforinposition(["Y"])
        cq.commands.motion.waitformotiondone(["Y"])
        
        cq.commands.motion.moveabsolute(["Y"], [yend], [feedspeed])
        cq.commands.motion.waitforinposition(["Y"])
        cq.commands.motion.waitformotiondone(["Y"])
        cq.commands.motion.movedelay(["Y"], delay_time=500)

        am.cammingoff(follower_axis=zaxis) 

        # check that camming bit status is False
        while True:
            statuses = check_axis_status_position(controller=controller, axis=zaxis)
            if statuses['camming_bit'] is False:
                break 
            # TODO: PRIORITY 2 -- GOOD PLACE TO ADD LOGGING
            time.sleep(0.1)  
        
        # retract ZC and free table 1
        # TODO: PRIORITY 1-- CHECK IF THIS IS THE ONLY PLACE THAT SAFELIFT IS USED IN SOURCE CODE
        cq.commands.motion.moveabsolute([zaxis], [zstart + safelift], [SPEED_Z])
        cq.commands.motion.waitforinposition([zaxis])
        cq.commands.motion.waitformotiondone([zaxis])
        cq.commands.advanced_motion.cammingfreetable(1)
        cq.commands.motion.movedelay([zaxis], delay_time=500)

        # drain the queue before we are ready to cut the next line
        cq.wait_for_empty()


        if (camnum_int + 1) % lines_per_test == 0:
            # First ensure that the Zaxis moves to zero as we may have to rotate
            cq.pause()
            cq.commands.motion.moveabsolute([zaxis], [0], [SPEED_Z])
            cq.commands.motion.waitforinposition([zaxis])
            cq.commands.motion.waitformotiondone([zaxis])
            cq.resume()

            info = run_test_touch(
                controller = controller,
                cq=cq,
                camnum=camnum,
                testtouchpath = testtouchpath,
                zaxis=zaxis,
                lines_per_test=lines_per_test,
                rot=tt_rot
            )

            if cut_rot:
                cq.pause()
                cq.commands.motion.moveabsolute(axes=["U"], positions=[cut_rot], speeds=[20])
                cq.commands.motion.waitforinposition(["U"])
                cq.commands.motion.waitformotiondone(["U"])
                cq.commands.motion.movedelay(["U"], delay_time=1_000)
                cq.resume()

            print(f"Performed test touch #{info['test_touch_index']}", info)

        
    cq.commands.motion.moveabsolute([zaxis], [0.0], [11])
    controller.runtime.commands.end_command_queue(cq)

    lockfile = path/'lockfile.lock'
    with open(lockfile, "w") as f:
        f.write("")


def load_wear_shift_table(path):
    """
    File format assumed:
        camnum   wearshift
    Returns dict[int] -> float
    """
    path = Path(path)
    table = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip() or line.strip().startswith('#'):
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            key = int(float(parts[0]))
            val = float(parts[1])
            table[key] = val
    return table


def load_test_touch_table(path):
    """
    File format assumed:
        index  X  Y  Z
    (1-based index like Aerobasic)
    Returns dict[int] -> (X, Y, Z)
    """
    path = Path(path)
    table = {}
    with path.open('r', encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('Spindle'):
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


def load_test_touch_table(path):
    """
    File format assumed:
        index  X  Y  Z
    (1-based index like Aerobasic)
    Returns dict[int] -> (X, Y, Z)
    """
    path = Path(path)
    table = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip() or line.strip().startswith('Spindle'):
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            x = float(parts[1])
            y = float(parts[2])
            z = float(parts[3])
            table = (x, y, z)
    return table


def testtouch_fromfile(controller, cq, path, zaxis, floodport, rot=None):
    """
    allows us to read in the .txt file that generates a test touch 
    and goes at the speed we care to

    rot: the rotation angle in int form not string
    """

    x, y, z = load_test_touch_table(path)
    print('TT at Location: ', 'X', x, 'Y', y, 'Z', z)

    cq.pause()

    # make sure zaxis is all the way up for the active zaxis
    print("CHECK THAT ALL Z AXES ARE AT 0")
    cq.commands.motion.moveabsolute(axes=[zaxis], positions=[0], speeds=[12])
    cq.commands.motion.waitforinposition([zaxis])
    cq.commands.motion.waitformotiondone([zaxis])
    cq.resume()
    
    cq.pause()
    cq.commands.motion.moveabsolute(axes=["X", "Y"], positions=[x, y], speeds=[20.0, 20.0])
    cq.commands.motion.waitforinposition(["X", "Y"])
    cq.commands.motion.waitformotiondone(["X", "Y"])
    cq.commands.motion.movedelay(["X", "Y"], delay_time=1_000)
    cq.resume()
    
    if rot is not None:
        cq.pause()
        cq.commands.motion.moveabsolute(axes=["U"], positions=[rot], speeds=[30])
        cq.commands.motion.waitforinposition(["U"])
        cq.commands.motion.waitformotiondone(["U"])
        cq.commands.motion.movedelay(["U"], delay_time=1_000)
        cq.resume()

    
    cq.pause()
    # now move in zaxis to test touch location
    cq.commands.motion.moveabsolute(axes=[zaxis], positions=[z+20], speeds=[6])
    cq.commands.motion.waitforinposition([zaxis])
    cq.commands.motion.waitformotiondone([zaxis])
    cq.resume()

    
    cq.pause()
    cq.commands.motion.moveabsolute(axes=[zaxis], positions=[z+10], speeds=[2])
    cq.commands.motion.waitforinposition([zaxis])
    cq.commands.motion.waitformotiondone([zaxis])
    cq.resume()

    cq.pause()
    cq.commands.motion.moveabsolute(axes=[zaxis], positions=[z+5], speeds=[2])
    cq.commands.motion.waitforinposition([zaxis])
    cq.commands.motion.waitformotiondone([zaxis])
    cq.resume()


    cq.pause()
    cq.commands.motion.moveabsolute(axes=[zaxis], positions=[z+1], speeds=[1])
    cq.commands.motion.waitforinposition([zaxis])
    cq.commands.motion.waitformotiondone([zaxis])
    cq.commands.motion.movedelay([zaxis], delay_time=3_000)
    cq.resume()

    
    cq.pause()
    cq.commands.motion.moveabsolute(axes=[zaxis], positions=[z+0.5], speeds=[0.1])
    cq.commands.motion.waitforinposition([zaxis])
    cq.commands.motion.waitformotiondone([zaxis])
    cq.resume()
    
    cq.pause()
    cq.commands.motion.moveabsolute(axes=[zaxis], positions=[z], speeds=[0.01])
    cq.commands.motion.waitforinposition([zaxis])
    cq.commands.motion.waitformotiondone([zaxis])
    cq.commands.motion.movedelay([zaxis], delay_time=500)
    cq.resume()
    
    # move z up to 0 
    cq.pause()
    cq.commands.motion.moveabsolute([zaxis], [0.0], [12])
    cq.resume()

    time.sleep(1)
    cq.wait_for_empty()
    cq.commands.io.digitaloutputset(axis='X', output_num=floodport, value=0)
    controller.runtime.commands.end_command_queue(cq)

    # --- Flood OFF ---

    

    
    return True, print('Test Touch finished, flood cooling turned off')