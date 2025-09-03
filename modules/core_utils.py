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


def enable_axes(controller, cq, z_axes):
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

    print(f"Moved {', '.join(z_axes)} to {z_position:.4f} mm. Resetting flood cooling, turning on spindles, and enabling flood for {active_z}.")
    cq.pause()

    # --- Flood OFF for all ---
    for fp in flood_ports:
        cq.commands.motion.movedelay(z_axes, delay_time=11_000)
        cq.commands.io.digitaloutputset(axis=io_axis, output_num=fp, value=0)

    # --- Spindles ON for all ---
    for sp in spindle_ports:
        cq.commands.io.digitaloutputset(axis=io_axis, output_num=sp, value=1)

    # --- Flood ON only for active Z ---
    active_index = z_axes.index(active_z)
    time.sleep(5)
    cq.commands.motion.movedelay(z_axes, delay_time=11_000)
    cq.commands.io.digitaloutputset(axis=io_axis, output_num=flood_ports[active_index], value=1)

    # --- Hold dwell ---
    cq.commands.motion.movedelay(["X", "Y"] + z_axes, delay_time=delay_ms)
    cq.resume()
    cq.wait_for_empty()

    print(f"All spindles ON {spindle_ports}; flood ON for {active_z} (DO {flood_ports[active_index]}).")
    controller.runtime.commands.end_command_queue(cq)
    print("Command queue ended after prepping Z axes.")



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

def read_starting_coords(master_path, camnum):
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

    return xstart, ystart, zstart
    

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



def cutcamming(controller, cq, path, zaxis, cuttype, safelift, feedspeed):
    path = Path(path)
    assert path.exists(), f"Base path not found: {path}"
    mastername = "Master.txt"
    masterpath = Path(path) / mastername   # ensure it's a Path

    assert masterpath.exists(), f"Master file not found: {masterpath}"

    cu._check_lockfile(path)

    # i feel like cutcamming needs to be one function that just focuses on the one campath and we loop over it?
    campaths = iter_cam_paths_from_master(master_path, base_path, cuttype)
    for campath in campaths[0:1]:
        assert campath.exists(), f"Campath not found: {campath}"
        #print(campath)
        yvals, zvals = get_cutcam_coords(campath)
        
        #print(len(yvals), len(zvals))
        
        # now set up motion
        am = cq.commands.advanced_motion
        am.cammingfreetable(1) # clear table 1 in case something is loaded in that table
        am.cammingloadtablefromarray(
            table_num=1,
            leader_values=leader_values,
            follower_values=follower_values,
            num_values=len(leader_values),
            units_mode=a1.CammingUnits.Primary,               # follower is position vs leader
            interpolation_mode=a1.CammingInterpolation.Linear, # typical for .Cam
            wrap_mode=a1.CammingWrapping.NoWrap,               # NOWRAP
            table_offset=0.0)
        print('Camming table loaded')

        camnum = Path(campath).stem[-4:]
        xstart, ystart, zstart = read_starting_coords(master_path=master_path, camnum=camnum)

        # slow, safe test speeds
        SPEED_Y_TRAVERSE  = 20.0   # mm/s
        SPEED_X_TRAVERSE  = 20.0   # mm/s
        SPEED_ZC_APPROACH = 4.0   # mm/s  (down to zstart+2)
        SPEED_ZC_TOUCH    = 0.1   # mm/s  (final settle at zstart)
        
        
        
        # move y to start position, wait for in position
        cq.commands.motion.moveabsolute(["X", "Y"], [xstart, ystart], [SPEED_Y_TRAVERSE,  SPEED_X_TRAVERSE])
        cq.commands.motion.waitforinposition(["Y"])
        cq.commands.motion.waitforinposition(["X"])
        cq.commands.motion.movedelay(["X", "Y"], delay_time=1_000)

        cq.commands.motion.moveabsolute(["ZC"], [zstart + 2.0], [SPEED_ZC_APPROACH])
        cq.commands.motion.waitforinposition(["ZC"])
        cq.commands.motion.moveabsolute(["ZC"], [zstart], [SPEED_ZC_TOUCH])
        cq.commands.motion.waitforinposition(["ZC"])
        cq.commands.motion.waitformotiondone(["ZC"])
        
        
        while True:
            statuses = check_axis_status_position(controller=controller, axis='ZC')
            if statuses['camming_bit'] is False:
                break # in desired state, stop looping
            time.sleep(0.1)  

        ### here is where it yells at me 
        cq.commands.advanced_motion.cammingon(
            follower_axis=zaxis,
            leader_axis="Y",
            table_num=1,
            source=a1.CammingSource.PositionCommand,                    # leader uses position
            output=a1.CammingOutput.RelativePosition  # matches CAMSYNC ...,1
        )

        ### here is where it yells at me because ZC was still moving down but this just looped through it so damn fast
        ### there's gotta be something else we can do with the waitforinposition and wait for move done
        ## something about InPositionTime value that we might be able to toggle
        while True:
            statuses = check_axis_status_position(controller=controller, axis='ZC')
            if statuses['camming_bit'] is True:
                break # in desired state, stop looping
            time.sleep(0.1)  
        controller.runtime.commands.end_command_queue(cq)
        #assert statuses['camming_bit'] == True, f"Camming bit not set to True, but {zaxis} camming was just commanded to be on."
    

# TODO: Each cam file step: loads --> syncs to camming bit to turn camming state on --> unsyncs after cam file final point 
# --> frees the camming table --> then next camming file which is also known as the next row in the Master.txt file and starts again

