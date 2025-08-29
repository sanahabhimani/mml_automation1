import automation1 as a1
import time
import numpy as np
import matplotlib.pyplot as plt

import os
import serial
from pathlib import Path
from pprint import pprint

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




def check_axis_drive_position(controller, axis):
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
    cfg.axis.add(a1.AxisStatusItem.DriveStatus, axis)
    cfg.axis.add(a1.AxisStatusItem.ProgramPosition, axis)

    results = controller.runtime.status.get_status_items(cfg)

    # Extract values
    drive_status = results.axis.get(a1.AxisStatusItem.DriveStatus, axis).value
    program_pos  = results.axis.get(a1.AxisStatusItem.ProgramPosition, axis).value

    # Convert drive status to int and mask off camming bit (bit 16)
    camming_bit = int(drive_status) & (1 << 16)

    print(f"[diag] {axis} camming bit set? {'Yes' if camming_bit else 'No'}")
    print(f"[diag] {axis} ProgramPosition = {program_pos:.4f} mm")

    return {
        "axis": axis,
        "camming_bit": bool(camming_bit),
        "program_position": program_pos,
        "drive_status_raw": int(drive_status)
    }


def enable_metrologyprobe(controller, state, output_num=0, axis="X", execution_task_index=1):
    """
    Enable or disable the metrology probe, then confirm state.

    Parameters
    ----------
    controller : object
        Automation1 controller instance.
    state : str
        Either "on" or "off".
    output_num : int
        Digital IO output port where the probe is connected. Default 0.
    axis : str
        Axis name (e.g., "X"). Default "X".
    execution_task_index : int
        The Task window in the Automation1 software suite to execute the command.
    """

    state = state.lower()
    if state == "on":
        value = 1
    elif state == "off":
        value = 0
    else:
        raise ValueError("state must be 'on' or 'off'")

    # Set the output
    controller.runtime.commands.io.digitaloutputset(
        axis=axis,
        output_num=output_num,
        value=value,
        execution_task_index=execution_task_index,
    )

    # Read back the output state
    current = controller.runtime.commands.io.digitaloutputget(
        axis=axis,
        output_num=output_num,
        execution_task_index=execution_task_index,
    )

    # Build human-readable status
    if int(current) == 1:
        status = "Metrology probe is ON"
    elif int(current) == 0:
        status = "Metrology probe is OFF"
    else:
        status = "Metrology probe in awkward state. Stop and check hardware."

    return status

# TODO: Each cam file step: loads --> syncs to camming bit to turn camming state on --> unsyncs after cam file final point 
# --> frees the camming table --> then next camming file which is also known as the next row in the Master.txt file and starts again

