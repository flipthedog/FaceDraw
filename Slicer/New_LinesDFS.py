# Lines.py
# A revised version of lines, create a series of points connected by lines
# The points are connected based on closest neighbors and randomly

import random

class Lines():

    def __init__(self, facedraw_image):
        """
        Constructor, create the Lines objects
        """

        self.image = facedraw_image.final_image
        self.height = self.image.shape[0]
        self.width = self.image.shape[1]
        self.connected_image = facedraw_image.connected_image

    def lines(self):

        # points that have already been used for drawing
        used_points = []

        points = []

        for i in range(0, self.width):

            for j in range(0, self.height):

                if self.connected_image[j][i].value > 0:

                    # This means the dot needs to be drawn

                    if not used_points.__contains__([j, i]):
                        points.append([j, i])
                        used_points.append([j, i])
                        points = self.neighbor_dfs(points, used_points, self.connected_image[j][i])
                        points.append([-1, -1])
                    else:
                        print("Poop")

                    # points.append([-1, -1])

        return points

    def neighbor_dfs(self, points, used_points, cell):

        if cell.width == -1 and cell.height == -1:
            # Empty cell
            # points.append([-1, -1])
            return points

        neighbors = cell.neighbors

        for neighbor in neighbors:

            if neighbor.value > 0:

                if not used_points.__contains__([neighbor.height, neighbor.width]):
                    points.append([neighbor.height, neighbor.width])
                    used_points.append([neighbor.height, neighbor.width])
                    points = self.neighbor_dfs(points, used_points, neighbor)

        return points
