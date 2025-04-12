import vapoursynth as vs
import functools
import havsfunc as haf
import kagefunc as kgf
import mvsfunc as mvf
import  G41Fun as dgr
import adptvgrnMod as adg
import muvsfunc as muv
import finesharp as finesharp

core = vs.core


# Load video
clip = core.lsmas.LWLibavSource(r'H:\BDMV\Ranma Blu-ray BOX\SET1\DISC1\BDMV\STREAM\Ranma - 01 [BDRemux].m2ts',format="yuv420p16")
clip = haf.EdgeCleaner(clip)
#Conv 16b
clip = core.std.Crop(clip,240,240,0,0)
clip = core.fmtc.bitdepth(clip,bits=16)
#clip = clip[0:261] + clip[4532:5169] + clip[12920:13069] + clip[18240:18425] + clip[26292:26329] + clip[27228:27265]


#Chroma Clean
#clip = core.knlm.KNLMeansCL(clip, d=1, a=1, h=4, device_type='auto',channels="UV")



# Crop 240 pixels from left and right
cropped = clip.std.Crop(left=0, right=0)
# Local Debanding Mask (Targets Fine Banding)
local_mask = core.std.Prewitt(clip).std.Binarize(3000).std.Inflate().std.Inflate()

# Global Debanding Mask (Targets Larger Areas)
global_mask = core.std.Prewitt(clip).std.Binarize(1000).std.Deflate().std.Deflate()

# Apply neo_f3kdb debanding with different strengths
local_debanded = core.neo_f3kdb.Deband(clip, y=64, cb=64, cr=64, grainy=82, grainc=82).std.MaskedMerge(clip, local_mask)
global_debanded = core.neo_f3kdb.Deband(clip, y=80, cb=64, cr=64, grainy=82, grainc=82).std.MaskedMerge(clip, global_mask)

# Merge both debanding passes
clip = core.std.Merge(local_debanded, global_debanded)

# Add adaptive grain to prevent banding
grain = adg.adptvgrnMod(clip, strength=1, size=1.35, luma_scaling=20, sharp=80, static=False, lo=19)

##Resize
resize = muv.SSIM_downsample(grain, 960,720)
## Output final clip
#Conv 16b
bitcon = core.fmtc.bitdepth(resize, bits=16)

bitcon.set_output()
