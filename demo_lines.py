from Slicer import FaceDrawImage, New_LinesDFS, New_LinesBFS, Writer
from ImageProcessing import process_image
from Viewer import Viewer

import time

import matplotlib as mpl

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

# INSTRUCTIONS
# 1. Change the filename field below
# 2. Change the printer configuration below
# 3. Run the Script

# Your filename here
# filename = 'dog.jpg'

filename = 'initial.png'

# Printer configuration
bed_height = 220
bed_width = 280
bed_size = [bed_height, bed_width]  # The size of your printer bed
travelrate = 2000
drawrate = 750
# The feedrate of your x-y moves

z_hop = 3.0  # The total Z-hop between each dot (mm)
z_tune = 0.0  # Tune the Z-axis

# Take the picture
# takepicture.take_picture(filename) # Uncomment this if you want to take a picture

# open the image
cv_image = process_image.openImage(filename, show=True)

facedraw_image = FaceDrawImage.FaceDrawImage(cv_image, bed_size, line_width=0.5, show=True)

# facedraw_image.__str__()

start_time = time.time()

lines = New_LinesDFS.Lines(facedraw_image, 15)

points = lines.lines()

print(f'Took {time.time() - start_time} seconds to run')
print(f'Generated {len(points)} moves')


Writer.points_moves_to_gcode(
    filename, points, travelrate, drawrate, bed_size, z_hop=z_hop, z_tune=z_tune)

viewer = Viewer.Viewer(points)
viewer.create_2d_moves()
viewer.plot_moves(max_x=bed_width, max_y= bed_height)
