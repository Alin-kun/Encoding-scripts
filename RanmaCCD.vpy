import vapoursynth as vs
import functools
import havsfunc as haf
import kagefunc as kgf
import mvsfunc as mvf
import G41Fun as G41Fun
import adptvgrnMod as adg
import muvsfunc as muv
import descale as ds
import nnedi3_rpow2 as nnd
import vsTAAmbk as taa
from vsutil import depth, get_y
from jvsfunc import denoise
core = vs.core

# Load your source
clip = core.lsmas.LWLibavSource(r"E:\Anime BDMV\Ranma\Ranma - 01 [BDRemux].m2ts", format="YUV420P16")
clip = core.std.Crop(clip, 240, 240, 0, 0)

# Apply CCD (chroma denoising)
#clip = clip[0:105] + clip[2952:3131] + clip[7584:7773] + clip[10724:10873] + clip[18049:18106] + clip[20292:20390] + clip[25596:25774]
clip = denoise.ccd(clip, threshold=25)  # <-- lowercase "ccd"
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

# --- Clone mask for denoising ---
denoise_mask = mask

# --- Apply denoising only in masked (flat) areas BEFORE debanding ---
pre_denoised = G41Fun.mClean(clip, thSAD=400, chroma=False, sharp=10, rn=14, deband=0, depth=0, strength=10)

clip = core.std.MaskedMerge(clip, pre_denoised, denoise_mask)

# Create filtered branch only for non-edge areas (Deband)
filtered = core.neo_f3kdb.Deband(
    clip, range=15, y=64, cb=32, cr=32, grainy=120, grainc=30
)

# Merge with original, preserving edges
merged = core.std.MaskedMerge(clip, filtered, mask)

# Convert to 16-bit and output
bitcon = core.fmtc.bitdepth(merged, bits=16)
bitcon.set_output()
