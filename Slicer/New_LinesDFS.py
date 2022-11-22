# Lines.py
# A revised version of lines, create a series of points connected by lines
# The points are connected based on closest neighbors and randomly

import random
from . import Pixel

class Lines():

    def __init__(self, facedraw_image, depth):
        """
        Constructor, create the Lines objects
        """

        self.facedraw_image = facedraw_image

        self.width_compression = self.facedraw_image.max_bed_width / \
            self.facedraw_image.width_number

        self.height_compression = self.facedraw_image.max_bed_height / \
            self.facedraw_image.height_number

        print(f"Max facedraw boundaries: H{self.facedraw_image.max_bed_height}, {self.facedraw_image.max_bed_width}")

        self.image = facedraw_image.final_image
        self.height = self.image.shape[0]
        self.width = self.image.shape[1]
        self.connected_image = facedraw_image.connected_image

        self.max_depth = depth

    def lines(self):

        print("Calculating lines")
        # points that have already been used for drawing
        used_points = []

        points = []

        for i in range(0, self.width):

            for j in range(0, self.height):

                if self.connected_image[j][i].value > 0:

                    # This means the dot needs to be drawn

                    points, used_points = self.new_dfs(points, used_points, self.connected_image[j][i], 0)

                    points.append([-1, -1])

        print("Finished calculating, point moves created")

        return points

    def new_dfs(self, points, used_points, cell: Pixel, depth):

        if not used_points.__contains__([cell.height, cell.width]):

            used_points.append([cell.height, cell.width])

            points.append([cell.height * self.height_compression, cell.width * self.width_compression])

            # print(cell.neighbors, cell.height, cell.width)

            for neighbor in cell.neighbors:

                if neighbor.value > 0:

                    if depth < self.max_depth:

                        # We can draw

                        self.new_dfs(points, used_points, neighbor, depth + 1)

                    else:
                        # we have hit maximum depth
                        points.append([-1, -1])
                        return points, used_points

        return points, used_points

    def neighbor_dfs(self, points, used_points, cell, depth):

        if cell.width == -1 and cell.height == -1:
            # Empty cell
            return points, used_points

        # Get all direct neighbors
        neighbors = cell.neighbors

        for neighbor in neighbors:

            if neighbor.value > 0:
                # pixel can be filled

                if not used_points.__contains__([neighbor.height, neighbor.width]):
                    # pixel is not already drawn

                    # add it to list of points to draw
                    points.append([neighbor.height * self.height_compression,
                        neighbor.width * self.width_compression])

                    used_points.append([neighbor.height, neighbor.width])

                    if depth < self.max_depth:

                        # Find the next point to draw
                        points, used_points = self.neighbor_dfs(points, used_points, neighbor, depth + 1)
                    else:

                        points.append([-1, -1])
                        print("hi")
                        return points, used_points
            else:

                # neighbor is a blank pixel

                if depth < self.max_depth:

                    # Check blank pixel's neighbors
                    points, used_points = self.neighbor_dfs(points, used_points, neighbor, depth + 1)

                else:
                    print("hi")

                    points.append([-1, -1])

                    return points, used_points

        return points, used_points
