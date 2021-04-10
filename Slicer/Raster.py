# Raster.py
# A type of slicing algorithm, takes in a facedrawimage and returns
# a toolpath that can be written to G-code.
# A raster basically will put down a point at every single pixel

class Raster():

    def __init__(self, facedraw_image):
        """
        Constructor, create the Raster object
        """

        self.image = facedraw_image
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

                    points.append([j, i])
                    points.append([-1, -1]) # Enter the move command

        return points
