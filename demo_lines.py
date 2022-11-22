from Slicer import FaceDrawImage, New_LinesDFS, New_LinesBFS, Writer
from ImageProcessing import process_image

import matplotlib as mpl

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

# INSTRUCTIONS
# 1. Change the filename field below
# 2. Change the printer configuration below
# 3. Run the Script

# Your filename here
filename = 'dog.jpg'

# filename = 'initial.png'

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

facedraw_image = FaceDrawImage.FaceDrawImage(cv_image, bed_size, line_width=1, show=True)

# facedraw_image.__str__()

lines = New_LinesDFS.Lines(facedraw_image, 15)

points = lines.lines()

print(points)

Writer.points_moves_to_gcode(
    filename, points, travelrate, drawrate, bed_size, z_hop=z_hop, z_tune=z_tune)


# def convert_points_to_3D(lines):
#
#     output = []
#
#     for i in range(0, len(lines)):
#         point = lines[i]
#
#         if i + 1 < len(lines):
#             # Point = (height, width)
#             g_code_x = point[1]
#             g_code_y = point[0]
#             g_code_z = high_z
#             next_point = lines[i + 1]
#             next_x = next_point[1]
#             next_y = next_point[0]
#
#             if next_x != -1 and next_y != -1:
#
#                 if g_code_x == -1 and g_code_y == -1:
#                     # Do a move command, don't draw
#                     # Move to the next point in the array
#
#                     output.append([next_x, next_y, g_code_z])
#
#                     file.write("\nG1 Z" + str(g_code_z))  # Move up
#                     file.write("\nG1 X" + str(next_x) + " Y" + str(next_y) + " F" + str(
#                         travelrate))  # Move above next point
#                     file.write("\nG1 Z" + str(0) + " F" + str(drawrate))
#
#                 else:
#
#                     file.write(
#                         "\nG1 X" + str(g_code_x) + " Y" + str(g_code_y) + " Z" + str(draw_z) + " F" + str(drawrate))
