# Let's see if we can create a prototype dash front face for FaceDraw

import dash
from dash import Output, Input, html, ctx
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import os
import glob
import io

from Slicer import FaceDrawImage, New_LinesDFS, New_LinesBFS, Writer
from ImageProcessing import process_image
from Viewer import Viewer

from PIL import Image

image_directory = os.getcwd() + '/images/'

print(image_directory)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col(dbc.Card([html.Img(id="original-img", src="", alt='Your selected image'),],), style={'width': '33%'}),
            dbc.Col(dbc.Card([html.Img(id="processed-img", src="", alt='Your processed image'),]), style={'width': '33%'}),
            dbc.Col(dbc.Card([html.Img(id="facedraw-img", src="", alt="The final image drawing representation"),]), style={'width': '33%'})
        ]),
        dbc.Row([
           # Putting all input for processing here
            dbc.Card([
                html.H3("Edge Detection Settings"),
                dbc.Input(id="low-th-input", type="number", min=0, max=300, value=100),
                dbc.FormText("Low Threshold Value"),
                dbc.Input(id="high-th-input", type="number", min=100, max=300, value=200),
                dbc.FormText("High Threshold Value"),
                dbc.Input(id="aperture-edge-input", type="number", min=0, max=10, value=3),
                dbc.FormText("Aperture Size Value"),
            ]),
            dbc.Card([
                html.H3("Drawing/Slicing Settings"),
                dcc.Dropdown(options=["DFS", "BFS", "Raster"], value="DFS", id="algorithm-selector"),
                dbc.FormText("Algorithm Selection"),
                dbc.Input(id="line-width", type="number", min=0.1, max=5, value=1),
                dbc.FormText("Line Width"),
                dbc.Input(id="bed-width", type="number", min=0, max=1000, value=200, style={'marginRight': '10px'}),
                dbc.Input(id="bed-height", type="number", min=0, max=1000, value=200),
                dbc.FormText("3D Printer Bed Size"),
                dbc.Checkbox(id="lock-ratio", label="Lock ratio of image on compression", value=True)
                # Drawing/slicer settings
                # Algorithm selection
                # line width
                # max bed width, max bed height
                # lock ratio

            ])
        ]),
        dbc.Row([
            dbc.Container([
                dcc.Dropdown(id="filename-selector", placeholder="Select your picture", options={}),
                dbc.Button("Generate Processed", id="submit-button", className="me-2", n_clicks=0),
                dbc.Button("Generate GCode", id="create-gcode", className="me-2", n_clicks=0)
                ]
            )
        ]),
    ]
)

@app.callback(
    [Output("filename-selector", "options")],
    [Input("filename-selector", "value")]
)
def update_dropdown(selected_value):
    image_types = ['{}*.png'.format(image_directory), '{}*.jpg'.format(image_directory), '{}*.jpeg'.format(image_directory)]
    all_images = []
    list_of_images = [all_images.extend(glob.glob(e)) for e in image_types]

    print(all_images)
    options = []
    for image in all_images:
        options.append({"label": str(image), "value": str(image)})

    return [options]

@app.callback(
    [Output("original-img", "src")],
    [Input("filename-selector", "value")]
)
def update_image(selected_value):
    print("Selected value: ", selected_value)
    if selected_value is not None:
        pillow_image = Image.open(str(selected_value))
        return [pillow_image]
    else:
        return [""]


@app.callback(
    [Output("processed-img", "src"), ],
    [Input("submit-button", "n_clicks"),
     Input("filename-selector", "value")]
)
def create_image(n_clicks, input_value):
    # print(ctx.triggered_id)

    if ctx.triggered_id == "submit-button":
        print("Trying facedraw generation")

        print("Loading: ", input_value)
        # Printer configuration
        bed_height = 220
        bed_width = 280
        bed_size = [bed_height, bed_width]  # The size of your printer bed
        travelrate = 2000
        drawrate = 750
        # The feedrate of your x-y moves

        z_hop = 3.0  # The total Z-hop between each dot (mm)
        z_tune = 0.0  # Tune the Z-axis

        cv_image = process_image.openImage(str(os.path.basename(input_value)))

        facedraw_image = FaceDrawImage.FaceDrawImage(cv_image, bed_size, line_width=0.5)

        return [Image.fromarray(facedraw_image.inverted_image)]
    else:
        print("No update")
        return [""]

@app.callback(
    [Output("facedraw-img", "src")],
    [Input("create-gcode", "n_clicks"),
     Input("filename-selector", "value")]
)
def create_slicer_image(n_clicks, selected_value):

    if ctx.triggered_id == "create-gcode":
        print("Trying facedraw generation")

        print("Loading: ", selected_value)
        filename = str(os.path.basename(selected_value))
        # Printer configuration
        bed_height = 220
        bed_width = 280
        bed_size = [bed_height, bed_width]  # The size of your printer bed
        travelrate = 2000
        drawrate = 750
        # The feedrate of your x-y moves

        z_hop = 3.0  # The total Z-hop between each dot (mm)
        z_tune = 0.0  # Tune the Z-axis

        cv_image = process_image.openImage(filename)

        facedraw_image = FaceDrawImage.FaceDrawImage(cv_image, bed_size, line_width=1)

        lines = New_LinesDFS.Lines(facedraw_image, 15)

        points = lines.lines()

        viewer = Viewer.Viewer(points)
        viewer.create_2d_moves()
        g_code_img = viewer.plot_moves(max_x=bed_width, max_y=bed_height)

        Writer.points_moves_to_gcode(
            filename, points, travelrate, drawrate, bed_size, z_hop=z_hop, z_tune=z_tune)

        return [g_code_img]
    else:
        print("No update")
        return [""]

if __name__ == "__main__":
    app.run_server()
