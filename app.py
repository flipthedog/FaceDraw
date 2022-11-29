# Let's see if we can create a prototype dash front face for FaceDraw

import dash
from dash import Output, Input, html, ctx
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import os
import glob
import time

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
                style={"textDecoration": "none"},
            ),
            dbc.Button("?", id="help"),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        ]
    ),
    color="dark",
    dark=True,
)

vision_tab = dbc.Card([
    html.H3("Edge Detection Settings"),
    html.Div([
        dbc.FormText("Low Threshold Value"),
        dbc.Input(id="low-th-input", type="number", min=0, max=300, value=100, maxlength=20),
        dbc.FormText("High Threshold Value"),
        dbc.Input(id="high-th-input", type="number", min=100, max=300, value=200),
        dbc.FormText("Aperture Size Value"),
        dbc.Input(id="aperture-edge-input", type="number", min=3, max=7, value=3),
    ], style={'width': '33%'}),
], style={'padding': '5px'})

drawing_tab = dbc.Card([
    # Drawing/slicer settings
    html.H3("Drawing/Slicing Settings"),
    dbc.FormText("Algorithm Selection"),
    dcc.Dropdown(options=["DFS", "BFS", "Raster"], value="DFS", id="algorithm-selector"),
    dbc.FormText("Line Width"),
    dbc.Input(id="line-width", type="number", min=0.1, max=5, value=1),
    dbc.FormText("3D Printer Bed Size"),
    dbc.Input(id="bed-width", type="number", min=0, max=1000, value=200,
              style={'marginRight': '10px'}),
    dbc.Input(id="bed-height", type="number", min=0, max=1000, value=200),
    dbc.Checkbox(id="lock-ratio", label="Lock ratio of image on compression", value=True)
], style={'padding': '5px'})

gcode_tab = dbc.Card([
    # Gcode options
    html.H3("GCode Settings"),
    dbc.FormText("Travel Speed (mm/s)"),
    dbc.Input(id="travel-speed", type="number", min=1000, max=5000, value=2000),
    dbc.FormText("Draw Speed (mm/s)"),
    dbc.Input(id="drawrate-speed", type="number", min=100, max=3000, value=750),
    dbc.FormText("Z-Hop (mm), amount to go up for travel move"),
    dbc.Input(id="z-hop", type="number", min=0, max=10, value=3),
    dbc.FormText("Z-Tune (mm), amount to go up or down to tune Z-axis"),
    dbc.Input(id="z-tune", type="number", min=-2, max=2, value=0.0),
], style={'padding': '5px'})

# Main app layout:
app.layout = dbc.Container(
    [
        dcc.Store(id='loaded-file', storage_type='session'),
        dcc.Store(id='generated-gcode-file', storage_type='session'),
        navbar,
        dbc.Row([
            dbc.Col(
                dcc.Loading(id="loading-original-img", type="circle",
                            style={'width': '33%', 'align': 'center', 'justify': 'center'},
                            children=[
                                dbc.Card([html.Img(id="original-img", src="", alt='Your selected image'), ], )
                            ])
                , style={'width': '33%'}),
            dbc.Col(
                dcc.Loading(id="loading-processed-img", type="circle",
                            style={'width': '33%', 'align': 'center', 'justify': 'center'},
                            children=[
                                dbc.Card([html.Img(id="processed-img", src="", alt='Your processed image'), ])
                            ])
                , style={'width': '33%'}),
            dbc.Col(
                dcc.Loading(id="loading-facedraw-img", type="circle",
                            style={'width': '33%', 'align': 'center', 'justify': 'center'},
                            children=[
                                dbc.Card([html.Img(id="facedraw-img", src="",
                                                    alt="The final image drawing representation"), ]),
                                ])
                , style={'width': '33%'})
        ], style={'padding': '5px'}),
        html.Hr(),
        dbc.Row([
            # Putting all input for processing here
                dbc.Tabs(children=[
                    dbc.Tab(vision_tab, label="Image Settings"),
                    dbc.Tab(drawing_tab, label="Drawing Settings"),
                    dbc.Tab(gcode_tab, label="GCode Settings"),
                ], style={'padding': '5px'})

        ]),
        html.Hr(),
        dbc.Row([
            dbc.Container([
                dcc.Dropdown(id="filename-selector", placeholder="Select your picture", options={}),
            ], style={'align': 'center', 'padding': '5px', 'width': '80%'}
            )
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Container(
                [
                    dbc.Button("Generate Processed", id="submit-button", className="me-2", n_clicks=0),
                    dbc.Button("Generate GCode", id="create-gcode", className="me-2", n_clicks=0)
                ]
            )
        ]),
        html.Hr(),
        dbc.Row(
            [
                dbc.Container(
                    [
                        html.H3("Output:"),
                        html.P("Waiting to run...", id="console-output"),
                        html.P("Waiting to run...", id="console-output2"),
                        dbc.Button("Download G-Code File", id="gcode-download-button", disabled=True),
                        dcc.Download(id="gcode-download")
                    ]
                )
            ]
        )
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
    [Output("original-img", "src"),
     Output("console-output", "children"),
     Output("loaded-file", "data")],
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
        return [pillow_image, "Updated image to: " + selected_value, selected_value]
    else:
        return ["", "", ""]


@app.callback(
    [Output("processed-img", "src")],
    [Input("submit-button", "n_clicks"),
     Input("filename-selector", "value"),
     Input("low-th-input", "value"),
     Input("high-th-input", "value"),
     Input("aperture-edge-input", "value")],
    prevent_initial_call=True
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
    [Output("facedraw-img", "src"),
     Output("console-output2", "children"),
     Output("generated-gcode-file", "data"),
     Output("gcode-download-button", "disabled")],
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
     Input("z-tune", "value"),
     ],
    prevent_initial_call=True
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


        start_time = time.time()

        cv_image = process_image.openImage(filename)

        facedraw_image = FaceDrawImage.FaceDrawImage(cv_image, bed_size, line_width=line_width)

        print("Here")
        lines = New_LinesDFS.Lines(facedraw_image, 15)

        points = lines.lines()

        viewer = Viewer.Viewer(points)
        viewer.create_2d_moves()
        g_code_img = viewer.plot_moves(max_x=bed_width, max_y=bed_height, plot_line_width=line_width)

        last_gcode_file = Writer.points_moves_to_gcode(
            filename, points, travelrate, drawrate, bed_size, z_hop=z_hop, z_tune=z_tune)

        total_time = time.time() - start_time
        output_text = f"Created: {str(last_gcode_file)} \n " \
                      f"Total Time: {str(total_time)} seconds \n " \
                      f"Total Moves: {str(len(points))}"

        return [g_code_img, output_text, last_gcode_file, False]
    else:
        raise dash.exceptions.PreventUpdate

@app.callback(
    [Output("gcode-download", "data")],
    [Input("gcode-download-button", "n_clicks"),
     Input("filename-selector", "value"),
     Input("generated-gcode-file", "data")],
    prevent_initial_call=True
)
def return_download(n_clicks, selected_file, gcode_file):

    if gcode_file is not None and ctx.triggered_id == "gcode-download-button":
        with open(gcode_file, 'r') as file:
            data = file.read()

        filename = os.path.splitext(os.path.basename(selected_file))[0] + ".gcode"
        return [dict(content=data, filename=filename)]
    else:
        raise dash.exceptions.PreventUpdate




if __name__ == "__main__":
    app.run_server()
