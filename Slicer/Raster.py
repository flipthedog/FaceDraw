# Raster.py
# A type of slicing algorithm, takes in a facedrawimage and returns
# a toolpath that can be written to G-code.
# A raster basically will put down a point at every single pixel

class Raster():

    def __init__(self, facedraw_image):
        """
        Constructor, create the Raster object
        """

        self.facedraw_image = facedraw_image

        self.x_compression = self.facedraw_image.max_bed_width / \
            self.facedraw_image.width_number
        self.y_compression = self.facedraw_image.max_bed_height / \
            self.facedraw_image.height_number

        self.height = facedraw_image.shape[0]
        self.width = facedraw_image.shape[1]

        print("Height: ", self.height, "Width: ", self.width)


    def raster(self):

        # Empty array of points which will turn into G-code moves
        points = []

        for i in range(0, self.width):

            for j in range(0, self.height):

                if self.image[j][i] > 0:

                    # This means the dot needs to be drawn

                    x_compression = self.facedraw_image.max_bed_width / self.facedraw_image.width_number
                    y_compression = self.facedraw_image.max_bed_height / self.facedraw_image.height_number

                    points.append([j * y_compression, i * x_compression])
                    points.append([-1, -1]) # Enter the move command

        return points
