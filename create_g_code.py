# Creating the g-code

# image_to_gcode
# Input: image: the grayscale, line image to be converted into g-code commands
# Input: linewidth: The width of the line to be drawn
# Input: raster: Boolean, whether to raster or not
# Input: filename: the name of the file generated
# Go through the picture pixel by pixel
def image_to_gcode(image, linewidth, raster, filename):
    imageWidth = image.shape[0]
    imageHeight = image.shape[1]
    widthCellNumber = imageWidth / linewidth
    heightCellNumber = imageHeight / linewidth

    file = open(filename, str, 2)

    for i in widthCellNumber:

        for j in heightCellNumber:
            if image[]
            file.write()

