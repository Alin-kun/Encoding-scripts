

import vapoursynth as vs
import functools

core = vs.core

# Load video with LWLibavSource
video = core.lsmas.LWLibavSource(r'H:\BDMV\[BDMV][城市猎人第1季][City Hunter][シティ―ハンタ―][BD-BOX Discx7 Fin]\Disc 1\BDMV\STREAM\00004.m2ts',format="yuv420p16")

# Crop 240 pixels from left and right
cropped = video.std.Crop(left=240, right=240)

# Create a mask (example: edge mask, adjust as needed)
mask = core.std.Prewitt(cropped).std.Binarize(40)

# Apply debanding with neo_f3kdb using the mask
# Parameters: (y=64, cb=32, cr=32, grainy=32, grainc=16)
debanded = core.neo_f3kdb.Deband(cropped, y=64, cb=32, cr=32, grainy=32, grainc=16)

# Merge masked areas back (if necessary)
output = core.std.MaskedMerge(debanded, cropped, mask)

# Set output
output.set_output()
