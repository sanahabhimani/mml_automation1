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
import logging
from datetime import datetime
import metalens
import core_utils as cu

# TODO: Config file for understanding flood cooling and spindle port is 
# TODO: gonna come in so handy

# NOTE: remember to run prepare_axes before this runs
def yz_calibrate(controller, cq, xstart, ystart, zaxis, zstart, numcuts, pitch):

    cq.commands.motion.moveabsolute(["X", "Y"], [xstart, ystart], [20, 20])
    cq.commands.motion.waitforinposition(["Y"])
    cq.commands.motion.movedelay(["X", "Y"], delay_time = 1_000)

    # Z to z_touch + 2 @ z_approach_speed
    cq.commands.motion.moveabsolute([zaxis], [zstart + 5.0], [5])
    cq.commands.motion.waitforinposition([zaxis])

    for cut in range(numcuts):
        print(f'cutting cut number: {cut}')

        # Z to z_touch + 1 @ z_slow_speed
        cq.commands.motion.moveabsolute([zaxis], [z_touch + 2.0], [0.5])
        cq.commands.motion.waitforinposition([zaxis])

        # Z to z_touch @ z_final_speed
        cq.commands.motion.moveabsolute([zaxis], [z_touch+1], [0.1])
        cq.commands.motion.waitforinposition([zaxis])

        cq.commands.motion.moveabsolute([zaxis], [z_touch], [0.01])
        cq.commands.motion.waitforinposition([zaxis])

        # queue-based hold at depth (ms)
        cq.commands.motion.movedelay([zaxis], delay_time=500)

        # then lift up 5mm above 
        cq.commands.motion.moveabsolute([zaxis], [zstart + 5.0], [10])
        cq.commands.motion.waitforinposition([zaxis])

        nextx = xstart + ((cut + 1) * pitch)
        cq.commands.motion.moveabsolute(["X"], [nextx], [2])
        cq.commands.motion.waitforinposition(["X"])
        cq.commands.motion.waitformotiondone(["X"])

        cq.wait_for_empty()

    cq.commands.motion.moveabsolute([zaxis], [0], [10])
    controller.runtime.commands.end_command_queue(cq)






