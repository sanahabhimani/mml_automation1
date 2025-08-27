import automation1 as a1
import time
import numpy as np
import matplotlib.pyplot as plt

import os
import serial
from pathlib import Path
from pprint import pprint

def testtouch_metrology(command_queue, controller, numX, numY, lengthX, lengthY,
                        Xstart, Ystart, Zstart, Zdrop, outname, comport="COM4", lifterSettleTime=0.5):
    """
    Execute a test-touch metrology scan.

    This routine performs a linear raster in X while holding Y fixed,
    probing the surface at shallow Z depths for alumina filter test touches
    on a silicon test wafer. Probe readings and axis positions are recorded.

    Parameters
    ----------
    command_queue : Automation1 CommandQueue
        The command queue used to issue motion commands.
    controller : Automation1 Controller
        The controller object used to query axis status.
    numX : int
        Number of X steps in the raster scan.
    numY : int
        Number of Y steps in the raster scan.
    lengthX : float
        Total scan length in X [mm].
    lengthY : float
        Total scan length in Y [mm].
    Xstart : float
        Starting X coordinate for the scan [mm].
    Ystart : float
        Starting Y coordinate for the scan [mm].
    Zstart : float
        Reference Z height for the probe [mm].
    Zdrop : float
        Depth below Zstart to probe at each point [mm].
    outname : str
        Path to output data file for metrology results.
    comport : str, optional
        Serial COM port for the gauge sensor (default: "COM4").
    lifterSettleTime : float, optional
        Time to wait after probe contact before reading sensor [s].

    Notes
    -----
    - Output file format is always: X, Y, ZA, sensor.
    - Probe readings are taken at Z = (Zstart - Zdrop).
    """

    if os.path.exists(outname):
        print("Metrology File Present, Stopping Motion")
        return

    incdistX = lengthX / (numX - 1)
    incdistY = lengthY

    command_queue.pause()
    # Enable axes
    for axis in ["X", "Y", "ZA"]:
        command_queue.commands.motion.enable(axis)

    # Zero Z stacks (absolute 0.0)
    command_queue.commands.motion.moveabsolute(
        axes=["ZA"], positions=[0.0], speeds=[3.0]
    )
    command_queue.commands.motion.waitforinposition(['ZA'])

    command_queue.commands.motion.moveabsolute(
        axes=["X"], positions=[-275], speeds=[3.0]
    )

    command_queue.commands.motion.waitforinposition(['X'])

    command_queue.commands.motion.moveabsolute(
        axes=["Y"], positions=[-520], speeds=[3.0]
    )

    command_queue.commands.motion.waitforinposition(['Y'])

    # Open serial for the probe (pyserial)
    ser = serial.Serial(comport, 9600, timeout=1)
    time.sleep(0.02)

    try:
        with open(outname, "w") as outfile:
            for xcount in range(numX):
                x = Xstart + incdistX * xcount
                y = Ystart
                print('x', x, 'y', y)

                command_queue.commands.motion.movedelay(["X", "Y", "ZA"], 10000)
                # Move to row start (X, Y, ZA = Zstart)
                command_queue.commands.motion.moveabsolute(
                    axes=["X", "Y", "ZA"],
                    positions=[x, y, Zstart],
                    speeds=[3.0, 3.0, 3.0]
                )
                command_queue.commands.motion.waitforinposition(['X','Y','ZA'])
                for ycount in range(numY):
                    y = Ystart + incdistY * ycount

                    # Y to next strip position
                    command_queue.commands.motion.moveabsolute(
                        axes=["Y"], positions=[y], speeds=[3.0]
                    )
                    command_queue.commands.motion.waitforinposition(['X','Y','ZA'])

                    # Probe down to measurement depth
                    command_queue.commands.motion.moveabsolute(
                        axes=["ZA"],
                        positions=[Zstart - Zdrop],
                        speeds=[3.0]
                    )
                    command_queue.commands.motion.waitforinposition(['ZA'])

                    # Let the lifter/probe settle
                    time.sleep(lifterSettleTime)

                    # Reset/read the probe
                    ser.write(b"RMD0\r\n")
                    time.sleep(0.02)
                    sensor_reading = ser.read(2048).decode("utf-8").strip()

                    # --- Hardcoded axis-position query (ProgramPosition) ---
                    config = a1.StatusItemConfiguration()
                    for axis in ["X", "Y", "ZA"]:
                        config.axis.add(a1.AxisStatusItem.ProgramPosition, axis)
                    results = controller.runtime.status.get_status_items(config)
                    posvals = {
                        axis: results.axis.get(a1.AxisStatusItem.ProgramPosition, axis).value
                        for axis in ["X", "Y", "ZA"]
                    }
                    # -------------------------------------------------------

                    # Retract probe to Zstart
                    command_queue.commands.motion.moveabsolute(
                        axes=["ZA"], positions=[Zstart], speeds=[3.0]
                    )
                    command_queue.commands.motion.waitforinposition(['X','Y','ZA'])

                    # Log: X, Y, ZA, sensor
                    outfile.write(f"{posvals['X']}, {posvals['Y']}, {posvals['ZA']}, {sensor_reading}\n")

    finally:
        # Close sensor port no matter what
        try:
            ser.close()
        except Exception:
            pass

        # Return Z to safe height
        command_queue.commands.motion.moveabsolute(
            axes=["ZA"], positions=[0.0], speeds=[3.0]
        )
        command_queue.commands.motion.waitforinposition(['X','Y','ZA'])

    command_queue.resume()
    command_queue.wait_for_empty()
    controller.runtime.commands.end_command_queue(cq)

    print("Metrology Done.")


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

