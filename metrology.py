import automation1 as a1
import time
import numpy as np
import matplotlib.pyplot as plt

import os
import serial
from pathlib import Path
from pprint import pprint

def testtouch_metrology(command_queue, controller, comport="COM4"):
    """
    Execute a metrology raster with absolute moves, 3 mm/s speed, and in-position waits.
    Positions are recorded from ProgramPosition after each measurement.

    Note:
    THIS METROLOGY SCAN IS FOR TEST TOUCHES FOR ALUMINA FILTER ON THE SILICON TEST WAFER

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
