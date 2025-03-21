import os, sys
import vapoursynth as vs
import havsfunc as haf  # Optional for additional filtering
import mvsfunc as mvf  # For bit depth conversion
import vsTCanny
core = vs.core

sys.path.append(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\Scripts")
import importlib.machinery
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\Dual\L-SMASH-Works\LSMASHSource.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\nnedi3\vsznedi3.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\TTempSmooth\TTempSmooth.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\SVPFlow\svpflow2_vs64.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\SVPFlow\svpflow1_vs64.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\Sangnom\libsangnom.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\RemoveGrainVS\RemoveGrainVS.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\nnedi3\NNEDI3CL.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\nnedi3\libnnedi3.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\mvtools\libmvtools.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\BM3D\BM3D.dll", altsearchpath=True)
mvsfunc = importlib.machinery.SourceFileLoader('mvsfunc', r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\mvsfunc\mvsfunc.py").load_module()
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\MiscFilters\MiscFilters.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\Dual\KNLMeansCL\KNLMeansCL.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\HQDN3D\libhqdn3d.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\fmtconv\fmtconv.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\FluxSmooth\libfluxsmooth.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\Dual\flash3kyuu_deband\flash3kyuu_deband.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\FFT3DFilter\fft3dfilter.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\EEDI3m\EEDI3m.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\EEDI2\EEDI2.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\DFTTest\DFTTest.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\Deblock\Deblock.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\DCTFilter\DCTFilter.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\CTMF\CTMF.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\CAS\CAS.dll", altsearchpath=True)
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\AWarpSharp2\libawarpsharp2.dll", altsearchpath=True)
adjust = importlib.machinery.SourceFileLoader('adjust', r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\Scripts\adjust.py").load_module()
core.std.LoadPlugin(r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\AddGrain\AddGrain.dll", altsearchpath=True)
havsfunc = importlib.machinery.SourceFileLoader('havsfunc', r"F:\Encoding\StaxRip-v2.44.4-x64\Apps\Plugins\VS\Scripts\havsfunc.py").load_module()

clip = core.lsmas.LWLibavSource(r"E:\Anime BDMV\TLRDR\To Love-Ru S03E3 2012 1080p Bluray Hybrid-REMUX AVC DTS-HD MA 2.0 Dual Audio -ZR-.mkv",format="yuv420p16")
clip = havsfunc.santiag(c=clip, opencl=True)
clip = havsfunc.DeHalo_alpha(clip)
clip = core.resize.Bicubic(clip, 1920, 1080)
# Convert to 16-bit for better processing
clip = mvf.Depth(clip, 16)

# Generate edge mask using TCanny (similar to Sobel)
edges = core.tcanny.TCanny(clip, sigma=1.5, mode=1)

# Invert mask so debanding is applied to smooth areas, not edges
mask = core.std.Invert(edges)

# Apply debanding to the full frame
debanded = core.neo_f3kdb.Deband(clip, y=64, cb=64, cr=64, grainy=16, grainc=16)

# Merge original with debanded clip using the mask
final = core.std.MaskedMerge(clip, debanded, mask)
