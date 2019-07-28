import cv2 as cv
from Slicer import Lines
from Slicer import Writer
from ImageProcessing import process_image

# INSTRUCTIONS:
# 1. Change the filename field below
# 2. Change the printer configuration below
# 3. Run the Script

# Your filename here
filename = 'oma7.jpg'

# Printer configuration
bed_height = 220
bed_width = 280
bed_size = [bed_height, bed_width] # The size of your printer bed
feedrate = 750
# The feedrate of your x-y moves

z_hop = 3.0 # The total Z-hop between each dot (mm)
z_tune = 0.0 # Tune the Z-axis

# Take the picture
# takepicture.take_picture(filename) # Uncomment this if you want to take a picture

# open the image
cv_image = process_image.openImage(filename)

lines = Lines.Slicer(cv_image, bed_size, line_width=1.0)
points = lines.slice()

Writer.points_moves_to_gcode(filename, points, feedrate, z_hop=z_hop, z_tune=z_tune)

cv.waitKey(0)
cv.destroyAllWindows() # delete all windows