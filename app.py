import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly import graph_objs as go
import plotly.graph_objects as go

import pandas as pd
import numpy as np

import settings
from db_functions import *
import json

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'backgroundColor': '#31302F',
    'font-color': '#F4FCFA',
    'font-size' : '10px'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'fontWeight': 'bold',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'rgba(255, 255, 255, 0.637)',
    'color': 'black',
    'padding': '6px',
    'font-size' : '10px'
}


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


df_crime = load_crime_data()
df_barrio = load_barrio_dane()
df_crime_type = load_crime_type(df_crime)
df_years = load_years(df_crime)
geo_json = load_baq_polyg()


# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="navbar",
                    children=[
                        html.Div(
                            className="open-slide",
                            children=[
                                html.Button('☰',  id='btn_open_slide')
                            ]
                        ),
                        html.Div(
                            "Criminalidad en Barranquilla (2010-2019)",
                            className="navbar-nav"
                        )
                    ],
                ),
                html.Div(
                    id="side-menu",
                    className="side-nav",
                    children=[
                        html.Button("×",  className="btn-close", id='btn_close_slide'),
                        html.Div(
                            className="row", 
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        dcc.Dropdown(
                                            id='year-selector',
                                            options=[
                                                {'label': year, 'value': year} 
                                                for year in df_years['date_year']
                                            ],
                                            multi=True,
                                            placeholder="Periodo",
                                        )
                                    ]
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        dcc.Dropdown(
                                            id='crimetype-dropdown',
                                            options=[
                                                {'label': crimen, 'value': crimen} 
                                                for crimen in df_crime_type['crimen']
                                            ],
                                            multi=True,
                                            placeholder="Tipo de crimen",
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                # Column for app graphs and plots
                html.Div(
                    id='main',
                    children=[
                        html.Div(
                            className="eight columns div-for-charts bg-grey",
                            children=[
                                dcc.Tabs(
                                    id="tabs-styled-with-inline",
                                    style={
                                        'height': '30px'
                                    },
                                    value='tab-1', 
                                    children=[
                                        dcc.Tab(
                                            label='Mapa', 
                                            value='tab-1',
                                            style=tab_style, 
                                            selected_style=tab_selected_style,
                                            children=[
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                dcc.Graph(
                                                                    id='baq-maps'
                                                                )
                                                            ]
                                                        )                                            
                                                    ]
                                                ),
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            children=[
                                                                dcc.Graph(id="histogram0")
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column_fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram1")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column_fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram2")
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        ),
                                        dcc.Tab(
                                            label='Más información',
                                            value='tab-2',
                                            style=tab_style, 
                                            selected_style=tab_selected_style,
                                            children=[
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column_fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram3")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column_fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram4")
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column_fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram5", className="fifty_percent")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column_fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram6", className="fifty_percent")
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        ),
                                    ]
                                ),
                                html.Div(id='tabs-content-inline'),
                            ]
                        )
                    ],
                ),
            ],
        )
    ]
)
@app.callback (
    [
        dash.dependencies.Output('side-menu', 'style'),
        dash.dependencies.Output('main', 'style'),
    ],
    [
        dash.dependencies.Input('btn_open_slide', 'n_clicks'),
        dash.dependencies.Input('btn_close_slide', 'n_clicks')
    ]
)
def open_close_sidebar(n_clicks1, n_clicks2):
    style_menu = {}
    style_main = {}
    if (n_clicks1 is None): n_clicks1 = 0
    if (n_clicks2 is None): n_clicks2 = 0

    if (n_clicks1 == n_clicks2):
        style_menu = {'width': '0'}
        style_main = {'margin-left': '0'}
    else: 
        style_menu = {'width': '250px'}
        style_main = {'margin-left': '250px'}

    return style_menu, style_main

@app.callback(
    [
        dash.dependencies.Output('baq-maps', 'figure'),
        dash.dependencies.Output('histogram0', 'figure'),
        dash.dependencies.Output('histogram1', 'figure'),
        dash.dependencies.Output('histogram2', 'figure'),
    ],
    [
        dash.dependencies.Input('crimetype-dropdown', 'value'),
        dash.dependencies.Input('year-selector', 'value'),
    ]
)
def update_map(crime_type, years):
    n_of_records = 10
    df_crimes_by_barrio, df_crimes_by_crimetype_and_year = filter_crime(df_crime, crime_type, years)
    
    return create_map(df_crimes_by_barrio),\
           create_line_chart_by_crimetype_and_year(df_crimes_by_crimetype_and_year),\
           create_bar_chart_top_barrios_by_ratio(df_crimes_by_barrio, n_of_records),\
           create_bar_chart_top_barrios_total_crimen(df_crimes_by_barrio, n_of_records)

def create_map( df ):
    return {
        'data': [ go.Choroplethmapbox(
                        geojson=geo_json,
                        locations=df['barrio_id'],
                        z=df['total'],
                        colorscale='blues',
                        colorbar_title="Indicar metrica",
                        text=df['barrio']
                    )
                ],
        'layout': go.Layout(
                        autosize=True,
                        margin=go.layout.Margin(l=0, r=35, t=0, b=0),
                        mapbox_style=settings.mapbox_style,
                        mapbox_accesstoken=settings.mapbox_access_token,
                        mapbox_zoom=11,
                        mapbox_center = settings.BAQ_CENTER_COORD,
                    ),
    }

def create_line_chart_by_crimetype_and_year( df ):
    data = []
    crime_lst = list(set(df["crimen"]))
    for c in crime_lst:
        data.append(go.Scatter(x=df[df['crimen']==c]['year'], y=df[df['crimen']==c]['total'], name=c))

    return {
        'data' : data,
        'layout': go.Layout(
                        plot_bgcolor='#323130',
                        paper_bgcolor='#323130',
                        font_color='#FFFFFF',
                        title='Crimenes a lo largo del tiempo',
                        xaxis=dict(tickmode='linear', dtick=1
                    )
        ) 
    }

def create_bar_chart_top_barrios_total_crimen(df, n_of_records):
    df = df.sort_values(by='total', ascending=False)
    return {
        'data': [
            {'x': df['barrio'].head(n_of_records), 'y': df['total'].head(n_of_records), 'type': 'bar'}
        ],
        'layout': go.Layout(
                        plot_bgcolor='#323130',
                        paper_bgcolor='#323130',
                        font_color='#FFFFFF',
                        title='Top 5 de Barrios - Total crimenes'
                    )
    }

def create_bar_chart_top_barrios_by_ratio(df, n_of_records):
    df = df.sort_values(by='crime_ratio', ascending=False)
    return {
        'data': [
            {'x': df['barrio'].head(n_of_records), 'y': df['crime_ratio'].head(n_of_records), 'type': 'bar'}
        ],
        'layout': go.Layout(
                        plot_bgcolor='#323130',
                        paper_bgcolor='#323130',
                        font_color='#FFFFFF',
                        title='Top 5 de Barrios - Crimen vs Población'
                    )
    }


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')
