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
    outname, comport="COM4",
    dwell_ms_at_depth=0  # set >0 if you want a hardware dwell at depth
):
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

        # 1) Row point: (x, Ystart, Zstart) and wait
        command_queue.commands.motion.moveabsolute(
            axes=["X", "Y", "ZA"], positions=[x, Ystart, Zstart], speeds=[10.0, 10.0, 3.0]
        )
        command_queue.commands.motion.waitformotiondone(["X", "Y", "ZA"])
        command_queue.commands.motion.waitforinposition(["X", "Y", "ZA"])
        command_queue.commands.motion.movedelay("ZA", 2_000)
        

        # 2) Drop to depth and dwell so we can pause and query data points
        
        command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[depth], speeds=[3.0])
        command_queue.commands.motion.waitforinposition(["ZA"])
        command_queue.commands.motion.waitformotiondone(["ZA"])
        command_queue.commands.motion.movedelay("ZA", int(dwell_ms_at_depth))

        command_queue.commands.motion.movedelay(["X", "Y", "ZA"], 4_000)
        
        ser.write(b"RMD0\r\n")  # replace with your gauge's measurement command if needed
        time.sleep(0.05)
        
        sensor = ser.read(2048).decode("utf-8", errors="ignore").strip()

        while True:
            pos = _get_program_pos(controller, axes=("X","Y","ZA"))
            if pos['X'] == x and pos['Y'] == Ystart and pos['ZA'] == depth:
                line = f"{pos['X']}, {pos['Y']}, {pos['ZA']}, {sensor}\n"
                f.write(line)
                f.flush()
                print(f"{pos['X']}, {pos['Y']}, {pos['ZA']}, {sensor}")
                break   # exit while, go to next X
            else:
                time.sleep(0.1)  # tiny delay before re-check
                

        #command_queue.commands.motion.movedelay("ZA", 2_000)
        command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[Zstart], speeds=[7.0])
        command_queue.commands.motion.waitformotiondone(["ZA"])
        command_queue.commands.motion.waitforinposition(["ZA"])
        command_queue.commands.motion.movedelay("X", 4_000)
        command_queue.wait_for_empty()  # ensure retract finished before next X
        
    # Park and end
    command_queue.commands.motion.movedelay("ZA", 3_000)
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[0.0], speeds=[8.0])
    command_queue.commands.motion.waitformotiondone(["ZA"])
    command_queue.commands.motion.waitforinposition(["ZA"])

    command_queue.wait_for_empty()
    controller.runtime.commands.end_command_queue(command_queue)
    f.close()
    ser.close()
 


def dressing_metrology(command_queue, controller, numX, numY, lengthX, lengthY,
                       Xstart, Ystart, Zstart, Zdrop, outname, comport="COM4", lifterSettleTime=0.5):
    """
    Perform a rectangular raster scan over the lens plate and record gauge outputs.

    Parameters
    ----------
    command_queue : Automation1 CommandQueue
        The command queue used to issue motion commands.
    controller : Automation1 Controller
        The controller object used to query axis status.
    numX, numY : int
        Number of X and Y sample points.
    lengthX, lengthY : float
        Total scan length in X and Y [mm].
    Xstart, Ystart : float
        Starting coordinates for the raster [mm].
    Zstart : float
        Reference Z height (safe retract) [mm].
    Zdrop : float
        Probe depth below Zstart for each touch [mm].
    outname : str
        Path to output data file for metrology results.
    comport : str, optional
        Serial COM port for the gauge sensor (default: "COM4").
    lifterSettleTime : float, optional
        Time to wait after probe contact before reading sensor [s].

    Notes
    -----
    - Output file format is always: X, Y, ZA, sensor.
    """

    if os.path.exists(outname):
        print("Metrology File Present, stopping to avoid overwrite")
        return

    command_queue.pause()

    # Enable axes
    for axis in ["X", "Y", "ZA"]:
        command_queue.commands.motion.enable(axis)

    # Retract to Zstart
    command_queue.commands.motion.moveabsolute(
        axes=["ZA"], positions=[Zstart], speeds=[3.0]
    )
    command_queue.commands.motion.waitforinposition(["ZA"])

    # Compute increments
    incdistX = lengthX / (numX - 1) if numX > 1 else 0
    incdistY = lengthY / numY if numY > 0 else 0

    # Move to starting XY
    command_queue.commands.motion.moveabsolute(
        axes=["X", "Y"], positions=[Xstart, Ystart], speeds=[3.0, 3.0]
    )
    command_queue.commands.motion.waitforinposition(["X", "Y"])

    # Open serial port for gauge
    ser = serial.Serial(comport, 9600, timeout=1)
    time.sleep(0.02)

    try:
        with open(outname, "w") as outfile:
            for xcount in range(numX):
                x = Xstart + incdistX * xcount

                # Move to beginning of this X "column"
                command_queue.commands.motion.moveabsolute(
                    axes=["X", "Y"], positions=[x, Ystart], speeds=[3.0, 3.0]
                )
                command_queue.commands.motion.waitforinposition(["X", "Y"])

                for ycount in range(numY):
                    y = Ystart + incdistY * ycount

                    # Move to (x, y)
                    command_queue.commands.motion.moveabsolute(
                        axes=["Y"], positions=[y], speeds=[3.0]
                    )
                    command_queue.commands.motion.waitforinposition(["Y"])

                    # Drop probe
                    command_queue.commands.motion.moveabsolute(
                        axes=["ZA"], positions=[Zstart - Zdrop], speeds=[2.5]
                    )
                    command_queue.commands.motion.waitforinposition(["ZA"])

                    time.sleep(lifterSettleTime)

                    # Reset/read probe
                    ser.write(b"RMD0\r\n")
                    time.sleep(0.02)
                    sensor_reading = ser.read(2048).decode("utf-8").strip()

                    # Query ProgramPositions
                    config = a1.StatusItemConfiguration()
                    for axis in ["X", "Y", "ZA"]:
                        config.axis.add(a1.AxisStatusItem.ProgramPosition, axis)
                    results = controller.runtime.status.get_status_items(config)
                    posvals = {
                        axis: results.axis.get(a1.AxisStatusItem.ProgramPosition, axis).value
                        for axis in ["X", "Y", "ZA"]
                    }

                    # Log: X, Y, ZA, sensor
                    outfile.write(
                        f"{posvals['X']}, {posvals['Y']}, {posvals['ZA']}, {sensor_reading}\n"
                    )

                    # Retract
                    command_queue.commands.motion.moveabsolute(
                        axes=["ZA"], positions=[Zstart], speeds=[3.0]
                    )
                    command_queue.commands.motion.waitforinposition(["ZA"])

    finally:
        try:
            ser.close()
        except Exception:
            pass

        # Retract at end
        command_queue.commands.motion.moveabsolute(
            axes=["ZA"], positions=[Zstart], speeds=[3.0]
        )
        command_queue.commands.motion.waitforinposition(["ZA"])

    command_queue.resume()
    command_queue.wait_for_empty()
    controller.runtime.commands.end_command_queue(command_queue)

    print("Dressing metrology complete.")



def lens_metrology(command_queue, controller, circlediam, xstep, ystep, Xcenter, Ycenter, Zstart, moveheight, outname, comport="COM4", lifterSettleTime=0.5):
    """
    Perform lens metrology over a circular region.

    Parameters
    ----------
    command_queue : Automation1 CommandQueue
        The command queue used to issue motion commands.
    controller : Automation1 Controller
        The controller object used to query axis status.
    circlediam : float
        Diameter of the measurement circle [mm].
    xstep : float
        Step size in the X direction [mm].
    ystep : float
        Step size in the Y direction [mm].
    Xcenter : float
        X-coordinate of circle center [mm].
    Ycenter : float
        Y-coordinate of circle center [mm].
    Zstart : float
        Reference Z height (safe retract height), usually 0.0 [mm].
    moveheight : float
        Hover height above wafer before probing [mm].
    outname : str
        Path to output data file for metrology results.
    comport : str, optional
        Serial COM port for the gauge sensor (default: "COM4").
    lifterSettleTime : float, optional
        Time to wait after probe contact before reading sensor [s].
    """

    if os.path.exists(outname):
        print("Metrology File Present, stopping to avoid overwrite")
        return

    command_queue.pause()

    # Enable axes
    for axis in ["X", "Y", "ZA"]:
        command_queue.commands.motion.enable(axis)

    # Return Z to safe start (Z=0)
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[Zstart], speeds=[3.0])
    command_queue.commands.motion.waitforinposition(["ZA"])

    # X start/stop
    xstart = Xcenter - circlediam / 2.0
    xstop = xstart + circlediam
    xval = xstart

    # Pre-position to first line
    command_queue.commands.motion.moveabsolute(
        axes=["X", "Y"], positions=[xstart, Ycenter], speeds=[3.0, 3.0]
    )
    command_queue.commands.motion.waitforinposition(["X", "Y"])

    # Drop to moveheight
    command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[moveheight], speeds=[3.0])
    command_queue.commands.motion.waitforinposition(["ZA"])

    # Open serial port for gauge
    ser = serial.Serial(comport, 9600, timeout=1)
    time.sleep(0.02)

    try:
        with open(outname, "w") as outfile:
            # Loop over X positions
            while xval < xstop:
                # Circle equation for Y bounds
                half = circlediam / 2.0
                yspan = math.sqrt(half**2 - (xval - Xcenter) ** 2)
                ystart = Ycenter - yspan
                ystop = Ycenter + yspan

                yval = ystart
                while yval < ystop:
                    # Conditional zdrop adjustment
                    r_eff = 2 * math.sqrt((xval - Xcenter) ** 2 + (yval - Ycenter) ** 2)
                    if r_eff < 260.0:
                        zdrop = 15.0
                    else:
                        zdrop = 20.0

                    # Move to XY
                    command_queue.commands.motion.moveabsolute(
                        axes=["X", "Y"], positions=[xval, yval], speeds=[3.0, 3.0]
                    )
                    command_queue.commands.motion.waitforinposition(["X", "Y"])

                    # Drop probe
                    command_queue.commands.motion.moveabsolute(
                        axes=["ZA"], positions=[moveheight - zdrop], speeds=[2.5]
                    )
                    command_queue.commands.motion.waitforinposition(["ZA"])

                    time.sleep(lifterSettleTime)

                    # Reset/read the probe
                    ser.write(b"RMD0\r\n")
                    time.sleep(0.02)
                    sensor_reading = ser.read(2048).decode("utf-8").strip()

                    # Query program positions
                    config = a1.StatusItemConfiguration()
                    for axis in ["X", "Y", "ZA"]:
                        config.axis.add(a1.AxisStatusItem.ProgramPosition, axis)
                    results = controller.runtime.status.get_status_items(config)
                    posvals = {
                        axis: results.axis.get(a1.AxisStatusItem.ProgramPosition, axis).value
                        for axis in ["X", "Y", "ZA"]
                    }

                    # Write to file: X, Y, ZA, sensor
                    outfile.write(
                        f"{posvals['X']}, {posvals['Y']}, {posvals['ZA']}, {sensor_reading}\n"
                    )

                    # Retract
                    command_queue.commands.motion.moveabsolute(
                        axes=["ZA"], positions=[moveheight], speeds=[3.0]
                    )
                    command_queue.commands.motion.waitforinposition(["ZA"])

                    yval += ystep

                # Increment X
                xval += xstep

    finally:
        # Ensure cleanup
        try:
            ser.close()
        except Exception:
            pass

        command_queue.commands.motion.moveabsolute(axes=["ZA"], positions=[Zstart], speeds=[3.0])
        command_queue.commands.motion.waitforinposition(["ZA"])

    command_queue.resume()
    command_queue.wait_for_empty()
    controller.runtime.commands.end_command_queue(command_queue)

    print("Lens metrology complete.")


def flange_metrology(command_queue, controller, numpoints, circlediam, Xcenter, Ycenter,
                     Zstart, moveheight, Zdrop, outname, comport="COM4", lifterSettleTime=0.5):
    """
    Perform flange metrology by probing evenly spaced points around a circle.

    Parameters
    ----------
    command_queue : Automation1 CommandQueue
        The command queue used to issue motion commands.
    controller : Automation1 Controller
        The controller object used to query axis status.
    numpoints : int
        Number of sample points evenly spaced around the flange circle.
    circlediam : float
        Diameter of the measurement circle [mm].
    Xcenter, Ycenter : float
        Coordinates of the circle center [mm].
    Zstart : float
        Reference Z height (safe retract), usually 0.0 [mm].
    moveheight : float
        Safe Z height above wafer surface [mm].
    Zdrop : float
        Probe depth below moveheight for each touch [mm].
    outname : str
        Path to output data file for metrology results.
    comport : str, optional
        Serial COM port for the gauge sensor (default: "COM4").
    lifterSettleTime : float, optional
        Time to wait after probe contact before reading sensor [s].

    Notes
    -----
    - Output file format is always: X, Y, ZA, sensor.
    - Points are distributed evenly on a circle centered at (Xcenter, Ycenter).
    """

    if os.path.exists(outname):
        print("Metrology File Present, stopping to avoid overwrite")
        return

    command_queue.pause()

    # Enable axes
    for axis in ["X", "Y", "ZA"]:
        command_queue.commands.motion.enable(axis)

    # Retract to Zstart
    command_queue.commands.motion.moveabsolute(
        axes=["ZA"], positions=[Zstart], speeds=[3.0]
    )
    command_queue.commands.motion.waitforinposition(["ZA"])

    # Move to center first
    command_queue.commands.motion.moveabsolute(
        axes=["X", "Y"], positions=[Xcenter, Ycenter], speeds=[3.0, 3.0]
    )
    command_queue.commands.motion.waitforinposition(["X", "Y"])

    # Drop to moveheight
    command_queue.commands.motion.moveabsolute(
        axes=["ZA"], positions=[moveheight], speeds=[3.0]
    )
    command_queue.commands.motion.waitforinposition(["ZA"])

    # Open serial port
    ser = serial.Serial(comport, 9600, timeout=1)
    time.sleep(0.02)

    try:
        with open(outname, "w") as outfile:
            dt = 2.0 * math.pi / numpoints

            for pointnum in range(numpoints):
                theta = pointnum * dt
                xval = Xcenter + (circlediam / 2.0) * math.cos(theta)
                yval = Ycenter + (circlediam / 2.0) * math.sin(theta)

                # Move to perimeter point at moveheight
                command_queue.commands.motion.moveabsolute(
                    axes=["X", "Y", "ZA"], positions=[xval, yval, moveheight], speeds=[3.0, 3.0, 3.0]
                )
                command_queue.commands.motion.waitforinposition(["X", "Y", "ZA"])

                # Drop probe
                command_queue.commands.motion.moveabsolute(
                    axes=["ZA"], positions=[moveheight - Zdrop], speeds=[2.5]
                )
                command_queue.commands.motion.waitforinposition(["ZA"])

                time.sleep(lifterSettleTime)

                # Reset/read probe
                ser.write(b"RMD0\r\n")
                time.sleep(0.02)
                sensor_reading = ser.read(2048).decode("utf-8").strip()

                # Query ProgramPositions
                config = a1.StatusItemConfiguration()
                for axis in ["X", "Y", "ZA"]:
                    config.axis.add(a1.AxisStatusItem.ProgramPosition, axis)
                results = controller.runtime.status.get_status_items(config)
                posvals = {
                    axis: results.axis.get(a1.AxisStatusItem.ProgramPosition, axis).value
                    for axis in ["X", "Y", "ZA"]
                }

                # Log: X, Y, ZA, sensor
                outfile.write(
                    f"{posvals['X']}, {posvals['Y']}, {posvals['ZA']}, {sensor_reading}\n"
                )

                # Retract
                command_queue.commands.motion.moveabsolute(
                    axes=["ZA"], positions=[moveheight], speeds=[3.0]
                )
                command_queue.commands.motion.waitforinposition(["ZA"])

    finally:
        try:
            ser.close()
        except Exception:
            pass

        # Retract to Zstart
        command_queue.commands.motion.moveabsolute(
            axes=["ZA"], positions=[Zstart], speeds=[3.0]
        )
        command_queue.commands.motion.waitforinposition(["ZA"])

    command_queue.resume()
    command_queue.wait_for_empty()
    controller.runtime.commands.end_command_queue(command_queue)

    print("Flange metrology complete.")


def plane_metrology(command_queue, controller, xstep, ystep, circlediam, Xcenter, Ycenter,
                    Zstart, moveheight, Zdrop, outname, comport="COM4", lifterSettleTime=0.5):
    """
    Perform plane metrology by raster scanning within a circular aperture.

    Parameters
    ----------
    command_queue : Automation1 CommandQueue
        The command queue used to issue motion commands.
    controller : Automation1 Controller
        The controller object used to query axis status.
    xstep, ystep : float
        Step sizes in X and Y directions [mm].
    circlediam : float
        Diameter of the circular scan area [mm].
    Xcenter, Ycenter : float
        Center of the measurement circle [mm].
    Zstart : float
        Reference Z height (safe retract), usually 0.0 [mm].
    moveheight : float
        Safe Z height above wafer surface [mm].
    Zdrop : float
        Probe depth below moveheight for each touch [mm].
    outname : str
        Path to output data file for metrology results.
    comport : str, optional
        Serial COM port for the gauge sensor (default: "COM4").
    lifterSettleTime : float, optional
        Time to wait after probe contact before reading sensor [s].

    Notes
    -----
    - Output file format is always: X, Y, ZA, sensor.
    """

    if os.path.exists(outname):
        print("Metrology File Present, stopping to avoid overwrite")
        return

    command_queue.pause()

    # Enable axes
    for axis in ["X", "Y", "ZA"]:
        command_queue.commands.motion.enable(axis)

    # Retract to Zstart
    command_queue.commands.motion.moveabsolute(
        axes=["ZA"], positions=[Zstart], speeds=[3.0]
    )
    command_queue.commands.motion.waitforinposition(["ZA"])

    # Define X scan range
    xstart = Xcenter - circlediam / 2.0
    xstop = xstart + circlediam
    xval = xstart

    # Pre-position to start
    command_queue.commands.motion.moveabsolute(
        axes=["X", "Y"], positions=[xstart, Ycenter], speeds=[3.0, 3.0]
    )
    command_queue.commands.motion.waitforinposition(["X", "Y"])

    # Drop to moveheight
    command_queue.commands.motion.moveabsolute(
        axes=["ZA"], positions=[moveheight], speeds=[3.0]
    )
    command_queue.commands.motion.waitforinposition(["ZA"])

    # Open serial
    ser = serial.Serial(comport, 9600, timeout=1)
    time.sleep(0.02)

    try:
        with open(outname, "w") as outfile:
            while xval < xstop:
                # Circle equation for Y bounds
                half = circlediam / 2.0
                yspan = math.sqrt(half**2 - (xval - Xcenter) ** 2)
                ystart = Ycenter - yspan
                ystop = Ycenter + yspan

                yval = ystart
                while yval < ystop:
                    # Move to Y
                    command_queue.commands.motion.moveabsolute(
                        axes=["Y"], positions=[yval], speeds=[3.0]
                    )
                    command_queue.commands.motion.waitforinposition(["Y"])

                    # Drop probe
                    command_queue.commands.motion.moveabsolute(
                        axes=["ZA"], positions=[moveheight - Zdrop], speeds=[2.5]
                    )
                    command_queue.commands.motion.waitforinposition(["ZA"])

                    time.sleep(lifterSettleTime)

                    # Reset/read probe
                    ser.write(b"RMD0\r\n")
                    time.sleep(0.02)
                    sensor_reading = ser.read(2048).decode("utf-8").strip()

                    # Query ProgramPositions
                    config = a1.StatusItemConfiguration()
                    for axis in ["X", "Y", "ZA"]:
                        config.axis.add(a1.AxisStatusItem.ProgramPosition, axis)
                    results = controller.runtime.status.get_status_items(config)
                    posvals = {
                        axis: results.axis.get(a1.AxisStatusItem.ProgramPosition, axis).value
                        for axis in ["X", "Y", "ZA"]
                    }

                    # Log
                    outfile.write(
                        f"{posvals['X']}, {posvals['Y']}, {posvals['ZA']}, {sensor_reading}\n"
                    )

                    # Retract
                    command_queue.commands.motion.moveabsolute(
                        axes=["ZA"], positions=[moveheight], speeds=[3.0]
                    )
                    command_queue.commands.motion.waitforinposition(["ZA"])

                    yval += ystep

                xval += xstep

    finally:
        try:
            ser.close()
        except Exception:
            pass

        # Retract to Zstart
        command_queue.commands.motion.moveabsolute(
            axes=["ZA"], positions=[Zstart], speeds=[3.0]
        )
        command_queue.commands.motion.waitforinposition(["ZA"])

    command_queue.resume()
    command_queue.wait_for_empty()
    controller.runtime.commands.end_command_queue(command_queue)

    print("Plane metrology complete.")
