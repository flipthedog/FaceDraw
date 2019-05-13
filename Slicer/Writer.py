# Writer.py
# For converting slicer results into a gcode file

import _datetime

# image_to_gcode
# Input: image: the grayscale, line image to be converted into g-code commands
# Input: linewidth: The width of the line to be drawn
# Input: raster: Boolean, whether to raster or not
# Input: filename: the name of the file generated
# Go through the picture pixel by pixel
def image_to_gcode(filename, lines, feedrate, max_width, max_height, image_width, image_height, z_hop=None, z_tune=None):

    # Check for file existence and overwrite if necessary
    try:
        # File already exists, overwrite it
        # TODO, overwrite the file
        filename = "./GCode/" + filename
        file = open(str(filename), 'w', 1)

    except FileNotFoundError:
        # File does not exist, create it
        # TODO Create a file
        print(FileNotFoundError.strerror)
        file = open(str(filename), 'w+x')

    writeIntroduction(file)
    linetogcode(file, lines, max_width, max_height, image_width, image_height, z_tune, z_hop, feedrate)
    # writeBody(file, image, linewidth)
    writeConclusion(file)

    # cv.imshow("This image", image)
    # cv.waitKey(0)

    file.close()

# writeIntroduction()
# Write the introduction and settings of the G-code file
# Input: file: The file to write the introduction to
def writeIntroduction( file):
    # TODO Write the settings to the file
    today = str(_datetime.datetime.today())
    file.write("; Created by FaceDraw on: " + str(today))
    file.write("\n")
    file.write("; Find FaceDraw on: http:/github.com/flipthedog/facedraw")
    file.write("\n")
    file.write("; Settings: \n")
    file.write("G90")

# writeBody()
# Write the body, actual g-code to the file
# Input: file: The file to write the body to
# Input: image: The image to write the G-code from
# Input: linewidth: The width of the pen-drawing
# Default: 0.3 mm
def writeBody( file, image, linewidth):
    # TODO Write the G-code writing functions

    if linewidth is None:
        linewidth = 0.3

    imageWidth = image.shape[0]
    imageHeight = image.shape[1]
    widthCellNumber = int(imageWidth / linewidth)
    heightCellNumber = int(imageHeight / linewidth)

    print("This is 1,1: " + str(image[1, 1]))
    print("This is 100,100: " + str(image[100, 100]))
    print("This is 155,155: " + str(image[305, 233]))

    for i in range(0, widthCellNumber):

        for j in range(0, heightCellNumber):
            None

# writeConclusion()
# Write the conclusion of the file
# Input: file: the
def writeConclusion( file):
    # TODO write the conclusion of this

    file.write("\n; That is all for now")
    file.write("\n; Find FaceDraw on: http:/github.com/flipthedog/facedraw")
    file.write("\n")
    file.write("; Thanks")

    None

# linetogcode()
# Convert an array of points to G-code moves
# Input: file: The file to write the text to
# Input: max_width: The maximum width to move in
# Input: max_height: The maximum height to move in
# Input: z_hop: The height to hop in between draw moves
# Input: lines: An array of lines to be drawn
# Output: None
def linetogcode(file, lines, max_width, max_height, image_width, image_height, z_tune=0.0, z_hop=5.0, feedrate=750):
    # Assumptions: All the points are in order representing a path

    # Convert to bed coordinates
    width_ratio = max_width / image_width
    height_ratio = max_height / image_height

    file.write("\n; Putting down " + str(len(lines)) + " dots")

    # Iterate through all the points in the line
    for point in lines:
        # Point = (height, width)
        x = point[0]
        y = point[1]
        # print("Pulled: X: ", x, "Y: ", y)

        # The G-code position
        g_code_x = x * width_ratio
        g_code_y = y * height_ratio
        g_code_z = z_tune + z_hop

        file.write("\nG1 X" + str(g_code_x) + " Y" + str(g_code_y) + " Z" + str(g_code_z) + " F" + str(feedrate))

        file.write("\nG1 " + "Z" + str(z_tune) + " F500 ; Move down the toolhead")

        g_code_z = z_tune + z_hop

        file.write("\nG1 " + "Z" + str(g_code_z) + " F750 ; Move up the toolhead")

    file.write("\n; Done drawing lines")