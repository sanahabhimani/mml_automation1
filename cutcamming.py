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



## STEP A: Setup & Constants
base_path = Path(r"C:\Users\UNIVERSITY\Desktop\RunData\Automation1_TEST\SpindleC\CutCammingThin")
cuttype     = "Thin"                # Equivalent to #define cuttype "Thin"
mastername  = "Master.txt"          # The list of cuts
lockname    = "lockfile.lock"       # Lockfile to prevent re-running

safelift = 10.0
lifter_settle_s = 2 # originally 0.5s 
feedspeed = 12.0

# Build full file paths (Path objects)
master_path = base_path / mastername

cu._check_lockfile(base_path)

## STEP B: Initial Motions, Digital Output (DO) --- Turn Spindle/Flood Cooling On

# First Command Queue Begins Here:
# start a queue with capacity 64, and block if full
cq = controller.runtime.commands.begin_command_queue(task=1, command_capacity=64, should_block_if_full=True)
print("Queue started on task:", cq.task_index, "capacity:", cq.command_capacity)
cq.pause()
# Enable axes
for axis in ["X", "Y", "ZC"]:
    cq.commands.motion.enable(axis)

cq.commands.motion.moveabsolute(["ZC"], [-0.0005], [20.0])
cq.commands.motion.waitforinposition(["ZC"])
cq.resume()
cq.wait_for_empty()

print("Pausing command queue after enabling axes and moving Z stage to 0. Next step is to turn on spindle and flood cooling.")
cq.pause()
io_axis = "X"

cq.commands.io.digitaloutputset(axis=io_axis,  output_num=10, value=1) #spindle C
cq.commands.io.digitaloutputset(axis=io_axis, output_num=6,  value=1) # flood cooling port 6
cq.commands.motion.movedelay(["X","Y","ZC"], delay_time=11_000)  # 11 s
cq.resume()   
cq.wait_for_empty()
print("Ending command queue in task window after doing initial setup of positions and turning spindle and flood cooling on.")
controller.runtime.commands.end_command_queue(cq)

## Check ZC Drive Status (can turn into a function)













## checks Master.txt file
assert master_path.exists(), f"Master file not found: {master_path}"
print("[step C] Found Master.txt:", master_path)

with open(master_path, "r") as f:
    lines = [ln.strip() for ln in f if ln.strip()]

print(f"[step C] Read {len(lines)} line(s) from Master.txt.")
if lines:
    print(" first line →", lines[0])

# parse the first cut definition
# AeroBasic FILEREAD expected 5 numeric values per row
# camnum  xvalue  ystart  zstart  yend
row0 = lines[0].split()
assert len(row0) >= 5, f"Expected ≥5 fields, got {len(row0)}: {row0}"

camnum  = int(row0[0])
xvalue  = float(row0[1])
ystart  = float(row0[2])
zstart  = float(row0[3])
yend    = float(row0[4])

print(f"[step C] camnum={camnum}, x={xvalue}, ystart={ystart}, zstart={zstart}, yend={yend}")

## build the cam table file name for this row and check it exists
cam_filename = f"CutCam{cuttype}{camnum:04d}.Cam"
cam_path     = base_path / cam_filename

print("[step C] Cam file:", cam_path)
if not cam_path.exists():
    raise IOError(f"Cam file not found: {cam_path}")

## Main Loop over Master.txt Rows
assert cam_path.exists(), f"Cam file not found: {cam_path}"
print("[step D] Using cam file:", cam_path)

with open(cam_path, "r") as f:
    shown = 0
    for ln in f:
        s = ln.strip()
        if not s or s.startswith(("#",";")):
            continue
        print(" cam>", s)
        shown += 1
        if shown >= 5:
            break


## leader and follower values 
leader_values = []
follower_values = []

with open(cam_path, "r") as f:
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


