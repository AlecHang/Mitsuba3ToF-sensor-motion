import sys, os
sys.path.append('../')
import mitsuba as mi
import matplotlib.pyplot as plt
#print(mi.variants())

mi.set_variant('llvm_rgb')
#mi.set_variant('scalar_rgb')


scene =  mi.load_file("test.xml")

params = mi.traverse(scene)

#params['PerspectiveCamera.film.size'] = [640, 320]
#params['PerspectiveCamera.shutter_open_time'] = 0.5
#params.update()

image = mi.render(scene, spp=512)

#mi.Bitmap(image).write('dining-room.exr')
mi.util.write_bitmap('blur-1.png', mi.Bitmap(image))

plt.axis("off")
plt.imshow(image ** (1.0 / 2.2)); # approximate sRGB tonemapping
#params
