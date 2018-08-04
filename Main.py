# The main file of the facedraw program
import process_image
import create_g_code

# Opening the image
image_name = 'pap_1.png'
processed_image = process_image.processImage(image_name, False)

create_g_code.image_to_gcode(processed_image, 0.3, True, "test_1.txt")
