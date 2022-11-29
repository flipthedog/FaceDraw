# Writer.py
# For converting slicer results into a gcode file

import _datetime
import os

# # image_to_gcode
# # Input: image: the grayscale, line image to be converted into g-code commands
# # Input: linewidth: The width of the line to be drawn
# # Input: raster: Boolean, whether to raster or not
# # Input: filename: the name of the file generated
# # Go through the picture pixel by pixel
# def points_to_gcode(fullfilename, points, feedrate, z_hop=None, z_tune=None):
#     """
#     Convert a list of points to G-code.
#     :param filename: [str] The name of the file to be created
#     :param points: [x, y] The list of points
#     :param feedrate: [mm/s] The feedrate of the Gcode
#     :param z_hop: [mm] Total distance to hop in z between moves
#     :param z_tune: [mm] Tuning parameter
#     :return: None
#     """
#
#     filename, file_ext = os.path.splitext(fullfilename)
#
#     filename = "./GCode/" + filename + str(".gcode")
#
#     # Check for file existence and overwrite if necessary
#
#     try:
#         # File already exists, overwrite it
#         file = open(str(filename), 'w', 1)
#
#     except FileNotFoundError:
#         # File does not exist, create it
#         print(FileNotFoundError.strerror)
#         file = open(str(filename), 'w')
#
#     # Write to the file
#     write_introduction(file, filename) # Write an introduction to the file
#     write_body(file, points, z_tune, z_hop, feedrate) # Write the G-code commands to the file
#     write_conclusion(file, filename) # Write the conclusion to the file
#     file.close() # Close the file

# image_to_gcode
# Go through the picture pixel by pixel
def points_moves_to_gcode(fullfilename, points, travelrate, drawrate, bed_size, z_hop=None, z_tune=None):
    """
    Convert a list of points to G-code.
    :param filename: [str] The name of the file to be created
    :param points: [x, y] The list of points
    :param feedrate: [mm/s] The feedrate of the Gcode
    :param z_hop: [mm] Total distance to hop in z between moves
    :param z_tune: [mm] Tuning parameter
    :return: None
    """

    if max(list(zip(*points))[0]) > bed_size[0]:
        raise Exception("Due to an error, some points fall outside of the maximum height bed-size")
    elif max(list(zip(*points))[1]) > bed_size[1]:
        raise Exception("Due to an error, some points fall outside of the maximum width bed-size")
    else:
        print("Verified that no points fall outside bed size")

    filename, file_ext = os.path.splitext(fullfilename)

    subdir = "./GCode/"
    filename = subdir + filename + str(".gcode")

    if not os.path.exists(subdir):
        # Create GCode folder if it does not exist already
        os.makedirs(subdir)

    try:
        # Check for file existence and overwrite if necessary
        try:
            # File already exists, overwrite it
            file = open(str(filename), 'w', 1)

        except FileNotFoundError:
            # File does not exist, create it
            print(FileNotFoundError.strerror)
            file = open(str(filename), 'w')
    except:
        file = open(str(filename + str(".gcode")), 'w')

    # Write to the file
    write_introduction(file, filename) # Write an introduction to the file
    write_body2(file, points, z_tune, z_hop, travelrate, drawrate) # Write the G-code commands to the file
    write_conclusion(file, filename) # Write the conclusion to the file
    file.close() # Close the file

    return file.name

def write_introduction(file, filename):
    """
    Write the introduction to a Gcode file
    :param file: The file to write to
    :return: None
    """
    today = str(_datetime.datetime.today())
    file.write("; " + str(filename))
    file.write("; Created by FaceDraw on: " + str(today) + "\n")
    file.write("; Find FaceDraw on: http:/github.com/flipthedog/facedraw\n")
    file.write("; Settings: \n")
    file.write("G90") # Absolute mode


def write_conclusion(file, fullfilename):
    """
    Write a conclusion to a Gcode file
    :param file: The file to write to
    :return: None
    """
    file.write("\n; Find FaceDraw on: http:/github.com/flipthedog/facedraw")
    file.write("\n")
    file.write("; Thanks")


    print("Operation complete!")
    print("File saved to:", fullfilename)

# writeBody()
# Convert an array of points to G-code moves
# Input: file: The file to write the text to
# Input: max_width: The maximum width to move in
# Input: max_height: The maximum height to move in
# Input: z_hop: The height to hop in between draw moves
# Input: lines: An array of lines to be drawn
# Output: None
def write_body(file, lines, z_tune=0.0, z_hop=5.0, feedrate=750):
    # Assumptions: All the points are in order representing a path

    file.write("\n; This image consists of " + str(len(lines)) + " dots")

    # Iterate through all the points in the line
    for point in lines:
        # Point = (height, width)
        g_code_x = point[0]
        g_code_y = point[1]

        g_code_z = z_tune + z_hop

        # Go to position
        file.write("\nG1 X" + str(g_code_x) + " Y" + str(g_code_y) + " Z" + str(g_code_z) + " F" + str(feedrate))

        file.write("\nG1 " + "Z" + str(z_tune) + " F500") # Move down the tool head

        g_code_z = z_tune + z_hop

        file.write("\nG1 " + "Z" + str(g_code_z) + " F750") # Move up the tool head

def write_body2(file, lines, z_tune=0.0, z_hop=5.0, travelrate=1500, drawrate=750):
    file.write("\n; This image consists of " + str(len(lines)) + " separate points")

    high_z = z_tune + z_hop
    draw_z = z_tune

    # Iterate through all the points in the array of points
    for i in range(0, len(lines)):
        point = lines[i]

        if i + 1 < len(lines):
            # Point = (height, width)
            g_code_x = point[1]
            g_code_y = point[0]
            g_code_z = high_z
            next_point = lines[i + 1]
            next_x = next_point[1]
            next_y = next_point[0]

            if next_x != -1 and next_y != -1:

                if g_code_x == -1 and g_code_y == -1:
                    # Do a move command, don't draw
                    # Move to the next point in the array

                    file.write("\nG1 Z" + str(g_code_z))  # Move up
                    file.write("\nG1 X" + str(next_x) + " Y" + str(next_y) + " F" + str(travelrate)) # Move above next point
                    file.write("\nG1 Z" + str(0) + " F" + str(drawrate))

                else:

                    file.write("\nG1 X" + str(g_code_x) + " Y" + str(g_code_y) + " Z" + str(draw_z) + " F" + str(drawrate))
