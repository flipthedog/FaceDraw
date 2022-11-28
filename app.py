# Let's see if we can create a prototype dash front face for FaceDraw

import dash
from dash import Output, Input, html, ctx
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import os
import glob

from Slicer import FaceDrawImage, New_LinesDFS, New_LinesBFS, Writer
from ImageProcessing import process_image
from Viewer import Viewer

from PIL import Image

image_directory = os.getcwd() + '/images/'

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        ]
    ),
    color="dark",
    dark=True,
)

vision_tab = dbc.Card([
                html.H3("Edge Detection Settings"),
                dbc.Input(id="low-th-input", type="number", min=0, max=300, value=100),
                dbc.FormText("Low Threshold Value"),
                dbc.Input(id="high-th-input", type="number", min=100, max=300, value=200),
                dbc.FormText("High Threshold Value"),
                dbc.Input(id="aperture-edge-input", type="number", min=3, max=7, value=3),
                dbc.FormText("Aperture Size Value"),
            ])

drawing_tab = dbc.Card([
                # Drawing/slicer settings
                html.H3("Drawing/Slicing Settings"),
                dcc.Dropdown(options=["DFS", "BFS", "Raster"], value="DFS", id="algorithm-selector"),
                dbc.FormText("Algorithm Selection"),
                dbc.Input(id="line-width", type="number", min=0.1, max=5, value=1),
                dbc.FormText("Line Width"),
                dbc.Input(id="bed-width", type="number", min=0, max=1000, value=200, style={'marginRight': '10px'}),
                dbc.Input(id="bed-height", type="number", min=0, max=1000, value=200),
                dbc.FormText("3D Printer Bed Size"),
                dbc.Checkbox(id="lock-ratio", label="Lock ratio of image on compression", value=True)
            ])

gcode_tab = dbc.Card([
                # Gcode options
                html.H3("GCode Settings"),
                dbc.Input(id="travel-speed", type="number", min=1000, max=5000, value=2000),
                dbc.FormText("Travel Speed (mm/s)"),
                dbc.Input(id="drawrate-speed", type="number", min=100, max=3000, value=750),
                dbc.FormText("Draw Speed (mm/s)"),
                dbc.Input(id="z-hop", type="number", min=0, max=10, value=3),
                dbc.FormText("Z-Hop (mm), amount to go up for travel move"),
                dbc.Input(id="z-tune", type="number", min=-2, max=2, value=0.0),
                dbc.FormText("Z-Tune (mm), amount to go up or down to tune Z-axis"),
            ])

# Main app layout:
app.layout = dbc.Container(
    [
        navbar,
        dbc.Row([
            dbc.Col(dbc.Card([html.Img(id="original-img", src="", alt='Your selected image'), ], ),
                    style={'width': '33%'}),
            dbc.Col(dbc.Card([html.Img(id="processed-img", src="", alt='Your processed image'), ]),
                    style={'width': '33%'}),
            dbc.Col(dbc.Card([html.Img(id="facedraw-img", src="", alt="The final image drawing representation"), ]),
                    style={'width': '33%'})
            ],
            style={'padding': '5px'}
        ),
        dbc.Row([
            # Putting all input for processing here
            dbc.Tabs([
                dbc.Tab(vision_tab, label="Vision"),
                dbc.Tab(drawing_tab, label="Drawing"),
                dbc.Tab(gcode_tab, label="GCode"),
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
    ],

)


@app.callback(
    [Output("filename-selector", "options")],
    [Input("filename-selector", "value")]
)
def update_dropdown(selected_value):
    image_types = ['{}*.png'.format(image_directory), '{}*.jpg'.format(image_directory),
                   '{}*.jpeg'.format(image_directory)]
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
    '''
    Open an image selected by the user
    :param selected_value: str: the filepath selected
    :return: Pillow Object image
    '''
    print("Selected value: ", selected_value)
    if selected_value is not None:
        pillow_image = Image.open(str(selected_value))
        return [pillow_image]
    else:
        return [""]


@app.callback(
    [Output("processed-img", "src"), ],
    [Input("submit-button", "n_clicks"),
     Input("filename-selector", "value"),
     Input("low-th-input", "value"),
     Input("high-th-input", "value"),
     Input("aperture-edge-input", "value")]
)
def create_image(n_clicks, input_value, edge_low_th, edge_high_th, edge_apt):

    options = {
        "edge_low_th": edge_low_th,
        "edge_high_th": edge_high_th,
        "edge_apt": edge_apt
    }

    # print(ctx.triggered_id)

    if ctx.triggered_id == "submit-button":
        print("Trying facedraw generation")

        print("Loading: ", input_value)
        # Printer configuration
        bed_height = 220
        bed_width = 280
        bed_size = [bed_height, bed_width]  # The size of your printer bed
        cv_image = process_image.openImage(str(os.path.basename(input_value)))

        facedraw_image = FaceDrawImage.FaceDrawImage(cv_image, bed_size, options=options, line_width=0.5)

        return [Image.fromarray(facedraw_image.inverted_image)]
    else:
        # print("No update")
        raise dash.exceptions.PreventUpdate


@app.callback(
    [Output("facedraw-img", "src")],
    [Input("create-gcode", "n_clicks"),
     Input("filename-selector", "value"),
     Input("low-th-input", "value"),
     Input("high-th-input", "value"),
     Input("aperture-edge-input", "value"),
     Input("algorithm-selector", "value"),
     Input("line-width", "value"),
     Input("bed-width", "value"),
     Input("bed-height", "value"),
     Input("lock-ratio", "value"),
     Input("travel-speed", "value"),
     Input("drawrate-speed", "value"),
     Input("z-hop", "value"),
     Input("z-tune", "value")]
)
def create_slicer_image(n_clicks, selected_value, edge_low_th, edge_high_th, edge_apt, algorithm_value, line_width,
                        bed_width, bed_height, lock_ratio, travel_speed, drawrate_speed, z_hop, z_tune):

    if ctx.triggered_id == "create-gcode":
        # Only triggers if the user specifically presses the "Generate Gcode" Button
        print("Trying facedraw generation")

        print("Loading: ", selected_value)
        filename = str(os.path.basename(selected_value))
        # Printer configuration
        bed_size = [bed_height, bed_width]  # The size of your printer bed
        travelrate = 2000
        drawrate = 750
        # The feedrate of your x-y moves

        z_hop = 3.0  # The total Z-hop between each dot (mm)
        z_tune = 0.0  # Tune the Z-axis

        cv_image = process_image.openImage(filename)

        facedraw_image = FaceDrawImage.FaceDrawImage(cv_image, bed_size, line_width=line_width)

        lines = New_LinesDFS.Lines(facedraw_image, 15)

        points = lines.lines()

        viewer = Viewer.Viewer(points)
        viewer.create_2d_moves()
        g_code_img = viewer.plot_moves(max_x=bed_width, max_y=bed_height, plot_line_width=line_width)

        Writer.points_moves_to_gcode(
            filename, points, travelrate, drawrate, bed_size, z_hop=z_hop, z_tune=z_tune)

        return [g_code_img]
    else:
        raise dash.exceptions.PreventUpdate


if __name__ == "__main__":
    app.run_server()
