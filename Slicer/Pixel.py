# Pixel.py
# Used for creating an interconnected FaceDrawImage
# Interconnecting facedraw images can optimize algorithms

class Pixel:

    def __init__(self, height, width, value, empty=False):
        self.height = height
        self.width = width
        self.value = value
        self.empty = empty
        self.neighbors = []
