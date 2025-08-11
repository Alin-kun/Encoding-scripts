import vapoursynth as vs
import functools
import havsfunc as haf
import kagefunc as kgf
import mvsfunc as mvf
import G41Fun as dgr
import adptvgrnMod as adg
import muvsfunc as muv
import descale as ds
import nnedi3_rpow2 as nnd
import vsTAAmbk  as taa
from vsutil import depth, get_y



core = vs.core

# Load the source
clip = core.lsmas.LWLibavSource(r'J:\Full Metal Panic Complete Collection\FULLMETALPANIC_S1_D1\BDMV\Full Metal Panic - 01 [BDRemux] [US].mkv', format="yuv420p16")
clip = haf.EdgeCleaner(clip)
clip = core.edgefixer.Continuity(clip, bottom=8)
clip = core.std.Crop(clip,240,240,0,0)
#clip = clip[1510:2146]
# Extract luma for mask creation
luma = core.std.ShufflePlanes(clip, planes=0, colorfamily=vs.GRAY)

# ---- Kirsch edge detector ----
def kirsch(clip):
    matrices = [
        [5, 5, 5, -3, 0, -3, -3, -3, -3],
        [-3, 5, 5, -3, 0, 5, -3, -3, -3],
        [-3, -3, 5, -3, 0, 5, -3, -3, 5],
        [-3, -3, -3, -3, 0, 5, -3, 5, 5],
        [-3, -3, -3, -3, 0, -3, 5, 5, 5],
        [-3, -3, -3, 5, 0, -3, 5, 5, -3],
        [5, -3, -3, 5, 0, -3, 5, -3, -3],
        [5, 5, -3, 5, 0, -3, -3, -3, -3],
    ]
    kirsch_edges = [core.std.Convolution(clip, matrix=m, divisor=1) for m in matrices]
    return core.std.Expr(kirsch_edges, 'x y max z max a max b max c max d max e max')

# ---- Retinex + TCanny edge mask ----
def retinex_edgemask(luma, sigma=1):
    ret = core.retinex.MSRCP(luma, sigma=[50, 200, 350], upper_thr=0.005)
    tcanny = ret.tcanny.TCanny(mode=1, sigma=sigma).std.Minimum(coordinates=[1, 0, 1, 0, 0, 1, 0, 1])
    return core.std.Expr([kirsch(luma), tcanny], 'x y +')

# Generate edge mask and invert it
mask = retinex_edgemask(luma).std.Invert()

# Denoise the entire clip
denoised = core.neo_f3kdb.Deband(clip,range=14 ,y=64, cb=32, cr=32, grainy=100, grainc=100)
#denoised = core.placebo.Deband(clip, planes=1 | 2 | 4, iterations=2, threshold=8.0, radius=26.0, grain=25.0)
#denoised =

# Apply denoise only in non-edge areas
merged = core.std.MaskedMerge(clip, denoised, mask)
convbit = core.resize.Bicubic(merged, format=vs.RGBS)
descaled = core.descale.Debicubic(convbit, 704, 480)

# Resize back to YUV 4:2:0 16bit
convyuv = core.resize.Bicubic(descaled, format=vs.YUV420P16, matrix_s="709")
bit = depth(convyuv, 16)

# Upscale using NNEDI3
res = nnd.nnedi3_rpow2(bit, rfactor=4, kernel="blackman", width=960, height=720)
deh = haf.FineDehalo(res)
# Resize back to YUV 4:2:0 16bit
convyuv2 = core.resize.Bicubic(deh, format=vs.YUV420P10, matrix_s="709")
convyuv3 = depth(convyuv2, 10)
convyuv3.set_output()
