import automation1 as a1
import time
import numpy as np
import matplotlib.pyplot as plt

import os
import serial
from pathlib import Path
from pprint import pprint

def _get_program_pos(controller, axes=("X","Y","ZA")):
    cfg = a1.StatusItemConfiguration()
    for ax in axes:
        cfg.axis.add(a1.AxisStatusItem.ProgramPosition, ax)
    res = controller.runtime.status.get_status_items(cfg)
    return {ax: res.axis.get(a1.AxisStatusItem.ProgramPosition, ax).value for ax in axes}

def testtouch_metrology(
    command_queue, controller,
    numX, lengthX,
    Xstart, Ystart, Zstart, Zdrop,
    outname, dwell_ms_at_depth=0, comport="COM4"):
    """
    Y is fixed. For each X:
      - Move to (X, Ystart, Zstart), wait
      - Move ZA to depth, wait
      - wait_for_empty()  <-- ensure we're *actually* at depth
      - pause()           <-- freeze queue; nothing else will move
      - read sensor + positions; print
      - resume(); retract to Zstart; wait; wait_for_empty()
    """
    if os.path.exists(outname):
        print("Metrology File Present, Stopping Motion")
        return
        
    # Step size along X
    incX = 0.0 if numX <= 1 else (lengthX / (numX - 1))
    depth = Zstart - Zdrop

    # Enable axes we use
    for ax in ["X", "Y", "ZA"]:
        command_queue.commands.motion.enable(ax)

    # Move to start (Y fixed)
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[0.0], speeds=[11.0])
    command_queue.commands.motion.waitformotiondone(["ZA"])
    command_queue.commands.motion.waitforinposition(["ZA"])
    command_queue.commands.motion.moveabsolute(axes=["X"], positions=[Xstart], speeds=[15.0])
    command_queue.commands.motion.waitformotiondone(["X"])
    command_queue.commands.motion.waitforinposition(["X"])
    command_queue.commands.motion.moveabsolute(axes=["Y"], positions=[Ystart], speeds=[15.0])
    command_queue.commands.motion.waitformotiondone(["Y"])
    command_queue.commands.motion.waitforinposition(["Y"])

    command_queue.wait_for_empty()  # arrive at start pose

    # Open gauge once
    ser = serial.Serial(comport, 9600, timeout=3)
    time.sleep(0.02)
    f = open(outname, "w")
    for ix in range(numX):
        x = Xstart + incX * ix

        # 1) Row point: (x, Ystart, Zstart) and wait
        command_queue.commands.motion.moveabsolute(
            axes=["X", "Y", "ZA"], positions=[x, Ystart, Zstart], speeds=[10.0, 10.0, 8.0]
        )
        command_queue.commands.motion.waitformotiondone(["X", "Y", "ZA"])
        command_queue.commands.motion.waitforinposition(["X", "Y", "ZA"])
        command_queue.commands.motion.movedelay("ZA", 1_000)
        

        # 2) Drop to depth and dwell so we can pause and query data points
        
        command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[depth], speeds=[3.0])
        command_queue.commands.motion.waitforinposition(["ZA"])
        command_queue.commands.motion.waitformotiondone(["ZA"])
       
        while True:
            pos = _get_program_pos(controller, axes=("X","Y","ZA"))
            if _within(pos['X'], x, 1e-3) and _within(pos['ZA'], depth, 1e-3):
                 # dwell in position
                 command_queue.commands.motion.movedelay(["X", "Y", "ZA"], 1_000)
                 
                 ser.write(b"RMD0\r\n") 
                 sensor = ser.read(2048).decode("utf-8", errors="ignore").strip()
                 line = f"{pos['X']}, {pos['Y']}, {pos['ZA']}, {sensor}\n"
                 f.write(line)
                 f.flush()
                 print(f"{pos['X']}, {pos['Y']}, {pos['ZA']}, {sensor}")
                 break   
            else:
                time.sleep(0.1)  
                
        command_queue.commands.motion.movedelay("ZA", 500)
        command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[Zstart], speeds=[8.0])
        command_queue.commands.motion.waitformotiondone(["ZA"])
        command_queue.commands.motion.waitforinposition(["ZA"])
        command_queue.commands.motion.movedelay("X", 1_000)
        command_queue.wait_for_empty()  # ensure retract finished before next X
        
    # Park and end
    command_queue.commands.motion.movedelay("ZA", 500)
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[0.0], speeds=[8.0])
    command_queue.commands.motion.waitformotiondone(["ZA"])
    command_queue.commands.motion.waitforinposition(["ZA"])

    command_queue.wait_for_empty()
    controller.runtime.commands.end_command_queue(command_queue)
    f.close()
    ser.close()
 

def dressing_metrology(
    command_queue, controller,
    numX, lengthX, numY, lengthY,
    Xstart, Ystart, Zstart, Zdrop,
    outname, comport="COM4"  # set >0 if you want a hardware dwell at depth
):
    """
    For each X and Y:
      - Move to (X, Y, Zstart), wait
      - Move ZA to depth, wait
      - wait_for_empty()  <-- ensure we're *actually* at depth
      - movedelay()           <-- freeze; nothing else will move
      - read sensor + positions; write to file
      - resume(); retract to Zstart; wait; wait_for_empty()
    """
    if os.path.exists(outname):
        print("Metrology File Present, Stopping Motion")
        return
    
    # Step size along X
    incX = 0.0 if numX <= 1 else (lengthX / (numX - 1))
    incY = 0.0 if numY <= 1 else (lengthY / (numY - 1))
    depth = Zstart - Zdrop

    # Enable axes we use
    for ax in ["X", "Y", "ZA"]:
        command_queue.commands.motion.enable(ax)

    # Move to start (Y fixed)
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[0.0], speeds=[8.0])
    command_queue.commands.motion.waitformotiondone(["ZA"])
    command_queue.commands.motion.waitforinposition(["ZA"])
    command_queue.commands.motion.moveabsolute(axes=["X"], positions=[Xstart], speeds=[15.0])
    command_queue.commands.motion.waitformotiondone(["X"])
    command_queue.commands.motion.waitforinposition(["X"])
    command_queue.commands.motion.moveabsolute(axes=["Y"], positions=[Ystart], speeds=[15.0])
    command_queue.commands.motion.waitformotiondone(["Y"])
    command_queue.commands.motion.waitforinposition(["Y"])

    command_queue.wait_for_empty()  # arrive at start pose

    # Open gauge once
    ser = serial.Serial(comport, 9600, timeout=3)
    time.sleep(0.02)
    f = open(outname, "w")
    for ix in range(numX):
        x = Xstart + incX * ix

        command_queue.commands.motion.moveabsolute(
            axes=["X", "ZA"], positions=[x, Zstart], speeds=[10.0, 6.0]
        )
        command_queue.commands.motion.waitformotiondone(["X", "ZA"])
        command_queue.commands.motion.waitforinposition(["X", "ZA"])
        command_queue.commands.motion.movedelay("ZA", 500)
        
        for iy in range(numY):
            y = Ystart + incY * iy
            
            # 2) Drop to depth and dwell so we can pause and query data points
            command_queue.commands.motion.moveabsolute(axes=["Y"], positions=[y], speeds=[10.0])
            command_queue.commands.motion.waitforinposition(["Y"])
            command_queue.commands.motion.waitformotiondone(["Y"])
            command_queue.commands.motion.movedelay("Y", 250) # can change to 1s

            
            command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[depth], speeds=[3.0])
            command_queue.commands.motion.waitforinposition(["ZA"])
            command_queue.commands.motion.waitformotiondone(["ZA"])

            
            while True:
                pos = _get_program_pos(controller, axes=("X","Y","ZA"))
                if _within(pos['X'], x, 1e-3) and _within(pos['Y'], y, 1e-3) and _within(pos['ZA'], depth, 1e-3): 
                    command_queue.commands.motion.movedelay(["X", "Y", "ZA"], 500)
                    ser.write(b"RMD0\r\n")  # replace with your gauge's measurement command if needed
                    sensor = ser.read(2048).decode("utf-8").strip()
                    line = f"{pos['X']}, {pos['Y']}, {pos['ZA']}, {sensor}\n"
                    f.write(line)
                    f.flush()
                    print(f"{pos['ZA']}, {sensor}")
                    #time.sleep(2)
                    break   # exit while, go to next X
                else:
                    time.sleep(0.1)  # tiny delay before re-check
                    
            command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[Zstart], speeds=[7.0])
            command_queue.commands.motion.waitformotiondone(["ZA"])
            command_queue.commands.motion.waitforinposition(["ZA"])
            command_queue.commands.motion.movedelay(["X", "Y"], 500)
            command_queue.wait_for_empty()  # ensure retract finished before next X
        
    # Park and end
    command_queue.commands.motion.movedelay("ZA", 500)
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[0.0], speeds=[8.0])
    command_queue.commands.motion.waitformotiondone(["ZA"])
    command_queue.commands.motion.waitforinposition(["ZA"])

    command_queue.wait_for_empty()
    controller.runtime.commands.end_command_queue(command_queue)
    f.close()
    ser.close()


def lens_metrology(
    command_queue, controller,
    circlediam, xstep, ystep,
    Xcenter, Ycenter,
    Zstart, moveheight,
    outname, comport="COM4",
    dwell_ms_at_depth=500  # ms, mirrors Aerobasic lifterSettleTime
):
    """
    Lens metrology: raster scan across a circular aperture.
    Mirrors Aerobasic structure but uses dressing_metrology-style sequencing.

    Output: X, Y, ZA, sensor
    """

    if os.path.exists(outname):
        print("Metrology File Present, stopping to avoid overwrite")
        return

    R = circlediam / 2.0

    # Enable axes
    for ax in ["X", "Y", "ZA"]:
        command_queue.commands.motion.enable(ax)

    # Safe starting pose
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[Zstart], speeds=[8.0])
    command_queue.commands.motion.waitforinposition(["ZA"])
    command_queue.commands.motion.moveabsolute(axes=["X","Y"], positions=[Xcenter, Ycenter], speeds=[15.0,15.0])
    command_queue.commands.motion.waitforinposition(["X","Y"])
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[moveheight], speeds=[8.0])
    command_queue.commands.motion.waitforinposition(["ZA"])
    command_queue.wait_for_empty()

    # Open gauge + file
    ser = serial.Serial(comport, 9600, timeout=3)
    time.sleep(0.02)
    f = open(outname, "w")

    # --- X raster loop ---
    xstart = Xcenter - R
    xstop  = Xcenter + R
    xval   = xstart

    while xval < xstop:  # "<" to mirror Aerobasic undershoot
        arg = R**2 - (xval - Xcenter)**2
        if arg < 0:
            xval += xstep
            continue

        yspan  = math.sqrt(arg)
        ystart = Ycenter - yspan
        ystop  = Ycenter + yspan
        yval   = ystart

        # --- Y loop ---
        while yval < ystop:  # "<" like Aerobasic
            # Conditional zdrop
            r_eff = 2 * math.sqrt((xval - Xcenter)**2 + (yval - Ycenter)**2)
            zdrop = 15.0 if r_eff < 260.0 else 20.0
            depth = moveheight - zdrop

            print(f"({xval:.3f}, {yval:.3f}) zdrop={zdrop}")

            # Move XY
            command_queue.commands.motion.moveabsolute(
                axes=["X","Y"], positions=[xval, yval], speeds=[10.0,6.0]
            )
            command_queue.commands.motion.waitforinposition(["X","Y"])
            command_queue.commands.motion.movedelay(["X","Y"], 2000)

            # Drop to depth
            command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[depth], speeds=[3.0])
            command_queue.commands.motion.waitforinposition(["ZA"])

            # dwell at depth
            command_queue.commands.motion.movedelay(["X","Y","ZA"], dwell_ms_at_depth)

            # Read gauge
            ser.write(b"RMD0\r\n")
            sensor = ser.read(2048).decode("utf-8", errors="ignore").strip()

            # while True pose check (like dressing/plane)
            while True:
                pos = _get_program_pos(controller, axes=("X","Y","ZA"))
                if (_within(pos['X'], xval, 1e-3) and
                    _within(pos['Y'], yval, 1e-3) and
                    _within(pos['ZA'], depth, 1e-3)):
                    command_queue.commands.motion.movedelay(["X", "Y", "ZA"], 500)
                    ser.write(b"RMD0\r\n")
                    sensor = ser.read(2048).decode("utf-8", errors="ignore").strip()
                    line = f"{pos['X']}, {pos['Y']}, {pos['ZA']}, {sensor}\n"
                    f.write(line)
                    f.flush()
                    print(f"{pos['ZA']}, {sensor}")
                    break
                else:
                    time.sleep(0.1)

            # Retract
            command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[moveheight], speeds=[7.0])
            command_queue.commands.motion.waitforinposition(["ZA"])
            command_queue.commands.motion.movedelay(["X","Y"], 3000)
            command_queue.wait_for_empty()

            yval += ystep

        xval += xstep

    # Park and end
    command_queue.commands.motion.movedelay("ZA", 1000)
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[Zstart], speeds=[8.0])
    command_queue.commands.motion.waitforinposition(["ZA"])
    command_queue.wait_for_empty()
    controller.runtime.commands.end_command_queue(command_queue)
    f.close()
    ser.close()


def flange_metrology(
    command_queue, controller,
    numpoints, circlediam, Xcenter, Ycenter,
    Zstart, moveheight, Zdrop,
    outname, comport="COM4",
    dwell_ms_at_depth=500  # ms, mirrors lifterSettleTime in Aerobasic
):
    """
    Flange metrology: evenly spaced points around a circle.
    Mirrors Aerobasic structure, but uses dressing_metrology-style sequencing.

    Output: X, Y, ZA, sensor
    """
    if os.path.exists(outname):
        print("Metrology File Present, stopping to avoid overwrite")
        return

    R = circlediam / 2.0
    depth = moveheight - Zdrop

    # Enable axes
    for ax in ["X", "Y", "ZA"]:
        command_queue.commands.motion.enable(ax)

    # Safe starting pose
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[Zstart], speeds=[8.0])
    command_queue.commands.motion.waitforinposition(["ZA"])
    command_queue.commands.motion.moveabsolute(axes=["X","Y"], positions=[Xcenter, Ycenter], speeds=[15.0, 15.0])
    command_queue.commands.motion.waitforinposition(["X","Y"])
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[moveheight], speeds=[8.0])
    command_queue.commands.motion.waitforinposition(["ZA"])
    command_queue.wait_for_empty()

    # Open gauge + file
    ser = serial.Serial(comport, 9600, timeout=3)
    time.sleep(0.02)
    f = open(outname, "w")

    # Loop over flange points
    dt = 2.0 * math.pi / numpoints
    for pointnum in range(numpoints):
        theta = pointnum * dt
        xval = Xcenter + R * math.cos(theta)
        yval = Ycenter + R * math.sin(theta)

        print(f"Point {pointnum}: {xval:.3f}, {yval:.3f}")

        # Move XY @ moveheight
        command_queue.commands.motion.moveabsolute(
            axes=["X","Y","ZA"], positions=[xval, yval, moveheight], speeds=[10.0, 10.0, 6.0]
        )
        command_queue.commands.motion.waitforinposition(["X","Y","ZA"])
        command_queue.commands.motion.movedelay(["X","Y"], 2000)

        # Drop to depth
        command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[depth], speeds=[3.0])
        command_queue.commands.motion.waitforinposition(["ZA"])
        command_queue.commands.motion.waitformotiondone(["ZA"])

        
        
        # while True pose check (like dressing_metrology)
        while True:
            pos = _get_program_pos(controller, axes=("X","Y","ZA"))
            if (_within(pos['X'], xval, 1e-3) and
                _within(pos['Y'], yval, 1e-3) and
                _within(pos['ZA'], depth, 1e-3)):

                # dwell at depth
                command_queue.commands.motion.movedelay(["X","Y","ZA"], 500)

                # read probe 
                ser.write(b"RMD0\r\n")
                sensor = ser.read(2048).decode("utf-8", errors="ignore").strip()
                line = f"{pos['X']}, {pos['Y']}, {pos['ZA']}, {sensor}\n"

                # write to file
                f.write(line)
                f.flush()
                print(f"{pos['ZA']}, {sensor}")
                break
            else:
                time.sleep(0.1)

        # Retract
        command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[moveheight], speeds=[7.0])
        command_queue.commands.motion.waitforinposition(["ZA"])
        command_queue.commands.motion.movedelay(["X","Y"], 3000)
        command_queue.wait_for_empty()

    # Park and end
    command_queue.commands.motion.movedelay("ZA", 1000)
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[Zstart], speeds=[8.0])
    command_queue.commands.motion.waitforinposition(["ZA"])
    command_queue.wait_for_empty()
    controller.runtime.commands.end_command_queue(command_queue)
    f.close()
    ser.close()


def plane_metrology(
    command_queue, controller,
    xstep, ystep, circlediam, Xcenter, Ycenter,
    Zstart, moveheight, Zdrop,
    outname, comport="COM4",
    dwell_ms_at_depth=4000  # ms dwell at depth
):
    """
    Plane metrology ported from Aerobasic structure.
    Outer loop: X values from xstart to xstop in steps of xstep
    For each X, compute Ystart/Ystop from circle equation
    Inner loop: Y values from ystart to ystop in steps of ystep
    At each (x,y), perform dressing_metrology-style move/dwell/read/retract.

    Output file format: X, Y, ZA, sensor
    """
    import os, time, math, serial

    if os.path.exists(outname):
        print("Metrology File Present, Stopping Motion")
        return

    R = circlediam / 2.0
    depth = moveheight - Zdrop

    # Safe starting pose
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[Zstart], speeds=[8.0])
    command_queue.commands.motion.waitforinposition(["ZA"])
    command_queue.commands.motion.moveabsolute(axes=["X"], positions=[Xcenter], speeds=[15.0])
    command_queue.commands.motion.waitforinposition(["X"])
    command_queue.commands.motion.moveabsolute(axes=["Y"], positions=[Ycenter], speeds=[15.0])
    command_queue.commands.motion.waitforinposition(["Y"])
    command_queue.wait_for_empty()

    # Open gauge + file
    ser = serial.Serial(comport, 9600, timeout=3)
    time.sleep(0.02)
    f = open(outname, "w")

    # --- X raster loop ---
    xstart = Xcenter - R
    xstop  = Xcenter + R
    xval   = xstart

    while xval < xstop:  # "<" to mimic Aerobasic undershoot
        # Compute Y span for this X
        arg = R**2 - (xval - Xcenter)**2
        if arg < 0:
            # Outside circle, skip this column
            xval += xstep
            continue

        yspan  = math.sqrt(arg)
        ystart = Ycenter - yspan
        ystop  = Ycenter + yspan
        yval   = ystart

        # --- Y loop ---
        while yval < ystop:  # "<" to mimic Aerobasic undershoot
            print(xval, yval)

            # Move XY at safe height
            command_queue.commands.motion.moveabsolute(
                axes=["X","Y"], positions=[xval, yval], speeds=[10.0, 12.0]
            )
            command_queue.commands.motion.waitforinposition(["X","Y"])
            command_queue.commands.motion.movedelay(["X","Y"], 2000)

            # Drop to depth
            command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[depth], speeds=[3.0])
            command_queue.commands.motion.waitforinposition(["ZA"])

            
            while True:
                pos = _get_program_pos(controller, axes=("X","Y","ZA"))
                if (_within(pos['X'], xval, 1e-3) and
                    _within(pos['Y'], yval, 1e-3) and
                    _within(pos['ZA'], depth, 1e-3)):

                    # dwell at depth
                    command_queue.commands.motion.movedelay(["X","Y","ZA"], 500)

                    # read probe 
                    ser.write(b"RMD0\r\n")
                    sensor = ser.read(2048).decode("utf-8", errors="ignore").strip()
                    line = f"{pos['X']}, {pos['Y']}, {pos['ZA']}, {sensor}\n"

                    # write to file
                    f.write(line)
                    f.flush()
                    print(f"{pos['ZA']}, {sensor}")
                    break
                else:
                    time.sleep(0.1)


            # Retract
            command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[moveheight], speeds=[7.0])
            command_queue.commands.motion.waitforinposition(["ZA"])
            command_queue.commands.motion.movedelay(["X","Y"], 1000)
            command_queue.wait_for_empty()

            yval += ystep
        # end while yval

        xval += xstep
    # end while xval

    # Park and end
    command_queue.commands.motion.movedelay("ZA", 1000)
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[Zstart], speeds=[8.0])
    command_queue.commands.motion.waitforinposition(["ZA"])
    command_queue.wait_for_empty()
    controller.runtime.commands.end_command_queue(command_queue)
    f.close()
    ser.close()


def _within(v, target, tol=1e-3):
    return abs(v - target) <= tol


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

    time.sleep(1) # pause before querying because of latency 

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