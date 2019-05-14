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
    filename = "./GCode/" + filename

    # Check for file existence and overwrite if necessary
    try:
        # File already exists, overwrite it
        # TODO, overwrite the file
        file = open(str(filename), 'w', 1)

    except FileNotFoundError:
        # File does not exist, create it
        print(FileNotFoundError.strerror)
        file = open(str(filename), 'w')

    writeIntroduction(file)
    writeBody(file, lines, max_width, max_height, image_width, image_height, z_tune, z_hop, feedrate)
    writeConclusion(file)
    file.close()

# writeIntroduction()
# Write the introduction and settings of the G-code file
# Input: file: The file to write the introduction to
def writeIntroduction( file):
    # TODO Write the settings to the file
    today = str(_datetime.datetime.today())
    file.write("; Created by FaceDraw on: " + str(today) + "\n")
    file.write("; Find FaceDraw on: http:/github.com/flipthedog/facedraw\n")
    file.write("; Settings: \n")
    file.write("G90") # Absolute mode

# writeConclusion()
# Write the conclusion of the file
# Input: file: the
def writeConclusion( file):
    # TODO write the conclusion of this
    file.write("\n; Find FaceDraw on: http:/github.com/flipthedog/facedraw")
    file.write("\n")
    file.write("; Thanks")

# writeBody()
# Convert an array of points to G-code moves
# Input: file: The file to write the text to
# Input: max_width: The maximum width to move in
# Input: max_height: The maximum height to move in
# Input: z_hop: The height to hop in between draw moves
# Input: lines: An array of lines to be drawn
# Output: None
def writeBody(file, lines, max_width, max_height, image_width, image_height, z_tune=0.0, z_hop=5.0, feedrate=750):
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

        # Go to position
        file.write("\nG1 X" + str(g_code_x) + " Y" + str(g_code_y) + " Z" + str(g_code_z) + " F" + str(feedrate))

        file.write("\nG1 " + "Z" + str(z_tune) + " F500") # Move down the tool head

        g_code_z = z_tune + z_hop

        file.write("\nG1 " + "Z" + str(g_code_z) + " F750") # Move up the tool head