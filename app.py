import os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_table
import constants
from dash.dependencies import Input, Output
from sqlalchemy import create_engine


db_host = os.environ.get('HOST')
db_name = os.environ.get('DB_NAME')
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASS')

connection_string = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(connection_string)

# df = pd.read_sql('select * from table', engine.connect())

app = dash.Dash(__name__,meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],)


def build_graph_title(title):
    return html.P(className="graph-title", children=title)


app.layout = html.Div(
    children=[
        html.Div(
            id="top-row",
            children=[
                html.Div(
                    className="row",
                    id="top-row-header",
                    children=[
                        html.Div(
                            id="header-container",
                            # children=[
                            #     build_banner(),
                            #     html.P(
                            #         id="instructions",
                            #         children="Select data points from the well map, ternary map or bar graph to "
                            #         "visualize cross-filtering to other plots. Selection could be done by "
                            #         "clicking on individual data points or using the lasso tool to capture "
                            #         "multiple data points or bars. With the box tool from modebar, multiple "
                            #         "regions can be selected by holding the SHIFT key while clicking and "
                            #         "dragging.",
                            #     ),
                            #     build_graph_title("Select Operator"),
                            #     dcc.Dropdown(
                            #         id="operator-select",
                            #         options=[
                            #             {"label": i, "value": i}
                            #             for i in df["op"].unique().tolist()
                            #         ],
                            #         multi=True,
                            #         value=[
                            #             df["op"].unique().tolist()[0],
                            #             df["op"].unique().tolist()[1],
                            #         ],
                            #     ),
                            # ],
                        )
                    ],
                ),
                html.Div(
                    className="row",
                    id="top-row-graphs",
                    children=[
                        # Well map
                        html.Div(
                            id="well-map-container",
                            children=[
                                build_graph_title("Well Map"),
                                dcc.RadioItems(
                                    id="mapbox-view-selector",
                                    options=[
                                        {"label": "basic", "value": "basic"},
                                        {"label": "satellite", "value": "satellite"},
                                        {"label": "outdoors", "value": "outdoors"},
                                        {
                                            "label": "satellite-street",
                                            "value": "mapbox://styles/mapbox/satellite-streets-v9",
                                        },
                                    ],
                                    value="basic",
                                ),
                                dcc.Graph(
                                    id="well-map",
                                    figure={
                                        "layout": {
                                            "paper_bgcolor": "#192444",
                                            "plot_bgcolor": "#192444",
                                        }
                                    },
                                    config={"scrollZoom": True, "displayModeBar": True},
                                ),
                            ],
                        ),
                        # Ternary map
                        html.Div(
                            id="ternary-map-container",
                            children=[
                                html.Div(
                                    id="ternary-header",
                                    children=[
                                        build_graph_title(
                                            "Shale Mineralogy Composition"
                                        ),
                                        dcc.Checklist(
                                            id="ternary-layer-select",
                                            options=[
                                                {
                                                    "label": "Well Data",
                                                    "value": "Well Data",
                                                },
                                                {
                                                    "label": "Rock Type",
                                                    "value": "Rock Type",
                                                },
                                            ],
                                            value=["Well Data", "Rock Type"],
                                        ),
                                    ],
                                ),
                                dcc.Graph(
                                    id="ternary-map",
                                    figure={
                                        "layout": {
                                            "paper_bgcolor": "#192444",
                                            "plot_bgcolor": "#192444",
                                        }
                                    },
                                    config={
                                        "scrollZoom": True,
                                        "displayModeBar": False,
                                    },
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="row",
            id="bottom-row",
            children=[
                # Formation bar plots
                html.Div(
                    id="form-bar-container",
                    className="six columns",
                    children=[
                        build_graph_title("Well count by formations"),
                        dcc.Graph(id="form-by-bar"),
                    ],
                ),
                html.Div(
                    # Selected well productions
                    id="well-production-container",
                    className="six columns",
                    children=[
                        build_graph_title("Individual well annual production"),
                        dcc.Graph(id="production-fig"),
                    ],
                ),
            ],
        ),
    ]
)


if __name__ == '__main__':
    app.run_server(debug=True)
