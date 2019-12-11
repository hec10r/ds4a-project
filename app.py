from db_functions import *


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


df_crime = load_crime_data()
df_crime_type = load_crime_type(df_crime)
df_years = load_years(df_crime)
df_localidad = load_localidad(df_crime)

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
                            className="navbar-nav",
                            children=[
                                html.Img(id='logo', src=app.get_asset_url("img/window.png"), className='navbar-nav', style={"text-align": "right"}),
                                html.P("Criminalidad en Barranquilla (2010-2019) - Team 4 - BAQ", className='navbar-nav')
                            ]
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
                                            id='year-dropdown',
                                            options=[
                                                {'label': year, 'value': year} 
                                                for year in df_years['date_year']
                                            ],
                                            multi=True,
                                            value=[2018, 2019],
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
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        dcc.Dropdown(
                                            id='borough-dropdown',
                                            options=[
                                                {'label': localidad, 'value': localidad} 
                                                for localidad in df_localidad['localidad']
                                            ],
                                            multi=True,
                                            placeholder='Localidad',
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
                                            label='Información general', 
                                            value='tab-1',
                                            style=tab_style, 
                                            selected_style=tab_selected_style,
                                            children=[
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(
                                                                    id='baq-maps'
                                                                )
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="line_crimealongtime")
                                                            ]
                                                        )                                 
                                                    ]
                                                ),
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="bar_total_localidad")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="line_fecha_localidad")
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="hm_crimen_localidad")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="bar_tipo_crimen_localidad")
                                                            ]
                                                        )
                                                    ]
                                                )                                                
                                            ]
                                        ),
                                        dcc.Tab(
                                            label='Localización y tiempo',
                                            value='tab-2',
                                            style=tab_style, 
                                            selected_style=tab_selected_style,
                                            children=[
                                                html.Div(
                                                    className='row',
                                                    children=[                                             
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="bar_crimen_barrio_localidad")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="bar_crimen_barrio_localidad_ratio")
                                                            ]
                                                        ),                                                   
                                                    ]
                                                ),
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="bar_crimen_mes")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="bar_crimenes_dia_semana")
                                                            ]
                                                        )
                                                    ]
                                                ),
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="hm_crimenes_dia_semana_localidad")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="hm_crimenes_dia_semana_hora")
                                                            ]
                                                        )   
                                                    ]
                                                )
                                            ]
                                        ),
                                        dcc.Tab(
                                            label='Festividades',
                                            value='tab-3',
                                            style=tab_style, 
                                            selected_style=tab_selected_style,
                                            children=[
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="hm_festividad_hora")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column fifty_perc',
                                                            children=[
                                                                dcc.Graph(id="hm_festividad_localidad")
                                                            ]
                                                        )                                              
                                                    ]
                                                ),
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column hundred_perc',
                                                            children=[
                                                                dcc.Graph(id='hm_festividad_critico')
                                                            ]
                                                        )  
                                                    ]
                                                )
                                            ]
                                        )
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
        dash.dependencies.Output('baq-maps', 'figure'), #Tab 1
        dash.dependencies.Output('line_crimealongtime', 'figure'), #Tab 1
        dash.dependencies.Output('hm_crimen_localidad', 'figure'), #Tab 1
        dash.dependencies.Output('bar_tipo_crimen_localidad', 'figure'), #Tab 1
        dash.dependencies.Output('bar_total_localidad', 'figure'), #Tab 2
        dash.dependencies.Output('line_fecha_localidad', 'figure'), #Tab 2
        dash.dependencies.Output('bar_crimen_barrio_localidad', 'figure'),#Tab 2
        dash.dependencies.Output('bar_crimen_barrio_localidad_ratio', 'figure'),#Tab 2
        dash.dependencies.Output('hm_crimenes_dia_semana_localidad', 'figure'),#Tab 2
        dash.dependencies.Output('bar_crimenes_dia_semana', 'figure'), #Tab 2
        dash.dependencies.Output('bar_crimen_mes', 'figure'),
        dash.dependencies.Output('hm_crimenes_dia_semana_hora', 'figure'),
        dash.dependencies.Output('hm_festividad_hora', 'figure'),
        dash.dependencies.Output('hm_festividad_localidad', 'figure'),
        dash.dependencies.Output('hm_festividad_critico', 'figure'),
    ],
    [
        dash.dependencies.Input('crimetype-dropdown', 'value'),
        dash.dependencies.Input('year-dropdown', 'value'),
        dash.dependencies.Input('borough-dropdown', 'value')
    ]
)
def update_map(crime_type, years, borough):
    n_of_records = 8
    df_filtered,\
    df_crimes_by_barrio,\
    df_crimes_by_crimetype_and_year,\
    df_crimes_by_crimetype_and_localidad,\
    df_crimes_by_localidad,\
    df_crimes_by_localidad_and_year,\
    df_crime_by_weekday,\
    df_crimes_by_month = filter_crime(df_crime, crime_type, years, borough)
    
    return create_map(df_filtered),\
           create_line_chart_by_crimetype_and_year( df_crimes_by_crimetype_and_year ),\
           create_heatmap_crimen_localidad( df_filtered ),\
           create_bar_chart_crimestype_by_localidad( df_crimes_by_crimetype_and_localidad ),\
           create_bar_chart_by_localidad( df_crimes_by_localidad ),\
           create_line_chart_by_localidad_and_year( df_crimes_by_localidad_and_year ),\
           create_bar_chart_top_barrios_total_crimen( df_crimes_by_barrio, n_of_records ),\
           create_bar_chart_top_barrios_by_ratio( df_crimes_by_barrio, n_of_records ),\
           create_heatmap_localidad_dow( df_filtered ),\
           create_bar_chart_crimes_by_weekday( df_crime_by_weekday ),\
           create_bar_chart_crimes_by_month( df_crimes_by_month ),\
           create_heatmap_hora_dow(df_filtered),\
           create_heatmap_festividad_hora( df_filtered ),\
           create_heatmap_festividad_localidad( df_filtered ), \
           create_heatmap_festividad_crimen( df_filtered )
            


def create_map( df ):
    colors=[ get_color(t) for t in df['impacto'].values]
    df['OverText'] = df['crimen'].str.cat(df['barrio'], sep=', ')
    return {
        'data': [ 
                # go.Choroplethmapbox(
                #         geojson=geo_json,
                #         locations=df['barrio_id'],
                #         z=df['total'],
                #         colorscale='blues',
                #         colorbar_title="Indicar metrica",
                #         text=df['barrio']
                #     )
                    go.Scattermapbox(
                     lat=df['latitud'], 
                     lon=df['longitud'], 
                     mode='markers' ,
                     text=df['OverText'],
                     hoverinfo="text",
                     marker= dict(
                        color=colors,
                        colorscale=[
                            [0, "#21c7ef"],
                            [0.33, "#76f2ff"],
                            [0.66, "#ff6969"],
                            [1, "#ff1717"],
                        ],
                        size=df['impacto']/2),
                     opacity=0.8,
                     #colorscale = [[0,'rgb(255, 255, 0)'],[1,'rgb(255, 0, 0)']],
                    ),
                ],
        'layout': go.Layout(
                        margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                        mapbox_style=settings.mapbox_style,
                        mapbox_accesstoken=settings.mapbox_access_token,
                        mapbox_zoom=11,
                        mapbox_center = settings.BAQ_CENTER_COORD,
                    ),
    }

def create_line_chart_by_crimetype_and_year( df ):
    data = []
    crime_lst = sorted(list(set(df["crimen"])), reverse=False)
    for c in crime_lst:
        df_tmp = df[df['crimen']==c]
        data.append(go.Scatter(x=df_tmp['period'], y=df_tmp['total'], name=c))

    return {
        'data' : data,
        'layout': get_layout('Número de crímenes en el tiempo', margin=dict(l=50, b=50, t=50, r=10), xtickmode='auto')
    }

def create_bar_chart_by_localidad( df ):
    df = df.sort_values(by='total', ascending=False)
    return {
        'data': [
            {'x': df['localidad'], 'y': df['total'], 'type': 'bar'}
        ],
        'layout': get_layout('Crímenes por localidad', margin=dict(l=20, b=50, t=80, r=10), xtickangle=0)
    }

def create_line_chart_by_localidad_and_year( df ):
    data = []

    localidad_lst = sorted(list(set(df["localidad"])), reverse=False)
    for loc in localidad_lst:
        df_tmp = df[df['localidad']==loc]
        data.append(go.Scatter(x=df_tmp['period'], y=df_tmp['total'], name=loc))

    return {
        'data' : data,
        'layout': get_layout('Número de crímenes por localidad', margin=dict(l=50, b=50, t=80, r=10), xtickmode='auto')
    }


def create_heatmap_crimen_localidad(df):
    x_axis = sorted(list(set(df['localidad'])), reverse=False)
    y_axis = sorted(list(set(df['crimen'])), reverse=True)

    return create_heatmap(  df, x_axis, y_axis, 'localidad', 'crimen', dict(l=200, b=5, t=120, r=10), title='Mapa de calor crímenes-localidad', xtickangle=0 )

def create_bar_chart_crimestype_by_localidad( df ):
    data = []
    localidad_lst = sorted(list(set(df["localidad"])), reverse=True)

    for loc in localidad_lst:
        df_tmp = df[df['localidad']==loc]
        #df_tmp['perc'] = (df_tmp['total'] / df_tmp['total'].sum())
        df_tmp['perc'] = df_tmp.apply( lambda row: row['total'] / df[(df['crimen'] == row['crimen'])]['total'].sum(), axis=1)
        df_tmp = df_tmp.sort_values(by='crimen', ascending=False)
        data.append(go.Bar(x=df_tmp['perc'], y=df_tmp['crimen'], name=loc, orientation='h' ))


    return {
        'data' : data,
        'layout' : get_layout('Distribución de crímenes según localidad', margin=dict(l=215, b=20, t=80, r=10), xtickformat=',.0%', bar_mode='stack')
    }


#===========================TAB 2============================
def create_bar_chart_top_barrios_total_crimen(df, n_of_records):
    data = []
    localidad_lst = sorted(list(set(df["localidad"])), reverse=False)
    for loc in localidad_lst:
        df_tmp = df[df['localidad']==loc].sort_values(by='total', ascending=False).head(n_of_records)
        data.append(go.Bar(x=df_tmp['barrio'], y=df_tmp['total'], name=loc))

    return {
        'data': data,
        'layout': get_layout(f'Barrios con más crímenes según localidad (Top {n_of_records})', margin=dict(l=50, b=150, t=80, r=10), xtickangle=-90)
    }


def create_bar_chart_top_barrios_by_ratio(df, n_of_records):
    data = []
    localidad_lst = sorted(list(set(df["localidad"])), reverse=False)
    for loc in localidad_lst:
        df_tmp = df[df['localidad']==loc].sort_values(by='crime_ratio', ascending=False).head(n_of_records)
        data.append(go.Bar(x=df_tmp['barrio'], y=df_tmp['crime_ratio'], name=loc))

    return {
        'data': data,
        'layout': get_layout(f'Ratio de crimen según densidad poblacional', margin=dict(l=50, b=150, t=80, r=10), xtickangle=-90)
    }



def create_bar_chart_crimes_by_weekday( df ):
    data = []

    df['nombre_dia_semana'] = df['dia_semana'].apply( lambda field: DAYS_OF_THE_WEEK[int(field)] )
    data.append(go.Bar(x=df['nombre_dia_semana'], y=df['total']))

    return {
        'data' : data,
        'layout': get_layout('Crímenes por día de la semana', margin=dict(l=50, b=110, t=80, r=10))
    }

def create_heatmap_hora_dow(df):
    x_axis = [datetime.time(i).strftime("%I %p") for i in range(24)]  # 24hr time list 
    y_axis = DAYS_OF_THE_WEEK

    return create_heatmap(  df=df, x_axis=x_axis, y_axis=y_axis, x_column_name='date_horaampm', y_column_name='date_dow', margin=dict(l=70, b=50, t=100, r=50), y_index=True, title='Crímenes día de la semana y hora')


def create_heatmap_localidad_dow(df):
    x_axis = sorted(list(set(df['localidad'])), reverse=False)
    y_axis = DAYS_OF_THE_WEEK

    return create_heatmap(  df=df, x_axis=x_axis, y_axis=y_axis, x_column_name='localidad', y_column_name='date_dow', margin=dict(l=70, b=50, t=50, r=50), y_index=True, title='Crímenes por día de la semana y localidad', xtickangle=0)

#=============TAB 3========================
def create_bar_chart_crimes_by_month( df ):
    data = []

    df['nombre_month'] = df['month'].apply( lambda field: MONTHS[int(field) - 1] )
    data.append(go.Bar(x=df['nombre_month'], y=df['total']))

    return {
        'data' : data,
        'layout': get_layout('Crímenes por mes', margin=dict(l=50, b=110, t=80, r=10), xtickangle=-90)
    }

def create_heatmap_festividad_hora(df):
    x_axis = [datetime.time(i).strftime("%I %p") for i in range(24)]  # 24hr time list
    y_axis = sorted([y for y in list(set(df['festividad'])) if str(y) != 'nan'], reverse=True)

    return create_heatmap(  df, x_axis, y_axis, 'date_horaampm', 'festividad', dict(l=220, b=10, t=180, r=10), height=800, title='Crímenes por festividad y hora', xtickangle=-90)

def create_heatmap_festividad_localidad(df):
    x_axis = sorted(list(set(df['localidad'])), reverse=False)
    y_axis = sorted([y for y in list(set(df['festividad'])) if str(y) != 'nan'], reverse=True)
    
    
    return create_heatmap(  df, x_axis, y_axis, 'localidad', 'festividad', dict(l=220, b=10, t=150, r=25), height=800, title='Crímenes por festividad y localidad', xtickangle=0 )


def create_heatmap_festividad_crimen(df):
    x_axis = sorted(list(set(df['crimen'])), reverse=False)
    y_axis = sorted([y for y in list(set(df['festividad'])) if str(y) != 'nan'], reverse=True)
    
    return create_heatmap(  df, x_axis, y_axis, 'crimen', 'festividad', dict(l=250, b=10, t=280, r=25), height=800, title='Festividades vs Crímenes', xtickangle=-45 )


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')
