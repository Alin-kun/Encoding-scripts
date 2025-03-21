import vapoursynth as vs
import functools

core = vs.core

# Load video
clip = core.lsmas.LWLibavSource(r'H:\BDMV\[BDMV][城市猎人第1季][City Hunter][シティ―ハンタ―][BD-BOX Discx7 Fin]\Disc 1\BDMV\STREAM\00004.m2ts',format="yuv420p16")

# Crop 240 pixels from left and right
cropped = clip.std.Crop(left=240, right=240)

# Create mask for local debanding
def create_local_mask(clip):
    gray = core.std.ShufflePlanes(clip, planes=0, colorfamily=vs.GRAY)
    mask = core.std.Sobel(gray).std.Binarize(150).std.Maximum().std.Minimum()
    return mask

local_mask = create_local_mask(cropped)

# Apply local debanding
deband_local = core.neo_f3kdb.Deband(cropped, range=15, y=64, cb=32, cr=32, grainy=16, grainc=16)
deband_local = core.std.MaskedMerge(cropped, deband_local, local_mask)

# Create mask for global debanding
def create_global_mask(clip):
    blurred = core.std.BoxBlur(clip, hradius=2, vradius=2)
    mask = core.std.Expr([clip, blurred], expr="x y - abs 8 *").std.Binarize(30)
    return mask

global_mask = create_global_mask(cropped)

# Apply global debanding
deband_global = core.neo_f3kdb.Deband(deband_local, range=20, y=48, cb=24, cr=24, grainy=8, grainc=8)
deband_final = core.std.MaskedMerge(deband_local, deband_global, global_mask)

# Output
deband_final.set_output()
