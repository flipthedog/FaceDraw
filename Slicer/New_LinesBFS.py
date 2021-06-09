# Lines.py
# A revised version of lines, create a series of points connected by lines
# The points are connected based on closest neighbors and randomly

import random

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

        self.height = self.image.shape[0]
        self.width = self.image.shape[1]
        self.connected_image = facedraw_image.connected_image
        self.depth = depth

    def lines(self):

        # points that have already been used for drawing
        used_points = []

        points = []

        for i in range(0, self.width):

            for j in range(0, self.height):

                if self.connected_image[j][i].value > 0:

                    # This means the dot needs to be drawn

                    if not used_points.__contains__([j, i]):

                        points.append([j * self.height_compression, i * self.width_compression])
                        used_points.append([j, i])
                        points = self.neighbor_bfs(points, used_points, self.connected_image[j][i])
                        points.append([-1, -1])


                    # points.append([-1, -1])

        return points

    def neighbor_bfs(self, points, used_points, cell, depth):

        if cell.width == -1 and cell.height == -1:
            # Empty cell
            # points.append([-1, -1])
            return points

        neighbors = cell.neighbors

        draw_neighbors = []
        for neighbor in neighbors:

            if neighbor.value > 0:

                if not used_points.__contains__([neighbor.height, neighbor.width]):
                    draw_neighbors.append(neighbor)

        number_of_neighbors = len(draw_neighbors)

        if number_of_neighbors > 0:
            index = random.randint(0, number_of_neighbors)
            selected_neighbor = draw_neighbors[index - 1]

            points.append([selected_neighbor.height * self.height_compression, selected_neighbor.width * self.width_compression])
            used_points.append([selected_neighbor.height, selected_neighbor.width])
            points = self.neighbor_bfs(points, used_points, selected_neighbor)

        return points
