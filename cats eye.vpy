import vapoursynth as vs
import functools
import havsfunc as haf
import kagefunc as kgf
import mvsfunc as mvf
import  G41Fun as dgr
import adptvgrnMod as adg
import muvsfunc as muv

core = vs.core

# Load video
clip = core.ffms2.Source(r'E:\Anime BDMV\cats\Cats Eye - 06 [BDRemux].m2ts')
#Conv 16b
clip = core.fmtc.bitdepth(clip,bits=16)

#Chroma Clean
clip = dgr.TemporalDegrain2(clip, degrainTR=1, postFFT=1, postSigma=1,degrainPlane=3)



# Crop 240 pixels from left and right
cropped = clip.std.Crop(left=240, right=240)

# Create mask for local debanding (edges)
def create_local_mask(clip):
    gray = core.std.ShufflePlanes(clip, planes=0, colorfamily=vs.GRAY)
    mask = core.std.Sobel(gray).std.Binarize(150).std.Maximum().std.Minimum()
    return mask

local_mask = create_local_mask(cropped)

# Apply local debanding
deband_local = core.neo_f3kdb.Deband(cropped, range=15, y=64, cb=32, cr=32, grainy=16, grainc=16)
deband_local = core.std.MaskedMerge(cropped, deband_local, local_mask)

# Create mask for global debanding (smooth areas)
def create_global_mask(clip):
    blurred = core.std.BoxBlur(clip, hradius=2, vradius=2)
    mask = core.std.Expr([clip, blurred], expr="x y - abs 8 *").std.Binarize(30)
    return mask

global_mask = create_global_mask(cropped)

# Apply global debanding
deband_global = core.neo_f3kdb.Deband(deband_local, range=20, y=48, cb=24, cr=24, grainy=8, grainc=8)
deband_final = core.std.MaskedMerge(deband_local, deband_global, global_mask)

# Add adaptive grain to prevent banding
deband_grain = adg.adptvgrnMod(cropped, strength=1, size=1.35, luma_scaling=30, sharp=80, static=False, lo=19)
##Resize
resize = muv.SSIM_downsample(deband_grain, 960,720)
## Output final clip
#Conv 16b
bitcon = core.fmtc.bitdepth(resize, bits=16)
bitcon.set_output()
