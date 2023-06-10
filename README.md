# Encoding-scripts
Aici voi posta scripturile de encoding folosite de mine
 ------------Chestii Generale------------
 Debicubic(720, 480, b=0, c=1) #Downscale facut la rezolutia la care a fost produs anime-ul
nnedi3x_rpow2(rfactor=2, cshift="Spline36Resize",fwidth=960, fheight=720)#upscale facut la rezolutie de 720p, asa se evita diferite artefacte aparute in urma upscale-ului facut la rezolutia de master a blu ray-ului, se elimina aliasingul si ceva ringing/mosquito noise - downscale facut la un bluray care a fost produs 480p (anime-uri din 98-09 in mare parte)
