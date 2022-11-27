import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib

import io
from PIL import Image

class Viewer:
    """
    Class to manage the drawing and visualization of moves from either Gcode or array of points
    """

    def __init__(self, points):
        self.points = points
        self.to_draw = []

    def create_2d_moves(self):

        lines = self.points

        output = [(lines[0][1], lines[0][0])]
        codes = [Path.MOVETO]

        for i in range(0, len(lines)):
            point = lines[i]

            if i + 1 < len(lines):
                # Point = (height, width)
                g_code_x = point[1]
                g_code_y = point[0]



                if g_code_x != -1 and g_code_y != -1:
                    output.append((g_code_x, g_code_y))
                    codes.append(Path.LINETO)
                else:
                    next_point = lines[i + 1]
                    next_x = next_point[1]
                    next_y = next_point[0]
                    output.append((next_x, next_y))
                    codes.append(Path.MOVETO)

        self.to_draw = [output, codes]
        return output, codes

    def plot_moves(self, max_x, max_y, show=False):

        matplotlib.use('TkAgg')

        fig, ax = plt.subplots()
        path = Path(self.to_draw[0], self.to_draw[1])

        patch = patches.PathPatch(path, fill=False, lw=0.5)
        ax.add_patch(patch)
        ax.set_xlim(-10, max_x + 10)
        ax.set_ylim(-10, max_y + 10)
        ax.invert_yaxis()
        # ax.invert_xaxis()

        if show:
            plt.show()
        else:
            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='png', dpi=450)
            im = Image.open(img_buf)
            return im
