# Raster.py
# A type of slicing solution, might be interesting
# Rasters the image to create a list of tool paths

# Import Statements
from Slicer import Slicer

class Raster(Slicer):

    def __init__(self, image, feedrate, bed_size, line_width, z_hop=None, z_tune=None):

        Slicer.Slicer.__init__(self, image, feedrate, bed_size, z_hop, z_tune)

        self.line_width = line_width

    # raster()
    # Create a rastering solution for the image
    def raster(self):
        None