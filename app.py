from db_functions import *
import datetime
from datetime import datetime as dt


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
                                                )                                                
                                            ]
                                        ),
                                        dcc.Tab(
                                            label='Localidades y Barrios',
                                            value='tab-2',
                                            style=tab_style, 
                                            selected_style=tab_selected_style,
                                            children=[
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column thirtythree_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram1")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column thirtythree_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram2")
                                                            ]
                                                        ),                                                        
                                                        html.Div(
                                                            className='column thirtythree_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram3")
                                                            ]
                                                        )                                                        
                                                    ]
                                                ),
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column thirtythree_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram4")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column thirtythree_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram5", className="fifty_percent")
                                                            ]
                                                        ),                                                      
                                                        html.Div(
                                                            className='column thirtythree_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram6", className="fifty_percent")
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                        ),
                                        dcc.Tab(
                                            label='Época y hora',
                                            value='tab-3',
                                            style=tab_style, 
                                            selected_style=tab_selected_style,
                                            children=[
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column thirtythree_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram7")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column thirtythree_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram8")
                                                            ]
                                                        ),
                                                        html.Div(
                                                            className='column thirtythree_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram9")
                                                            ]
                                                        )                            
                                                    ]
                                                ),
                                                html.Div(
                                                    className='row',
                                                    children=[
                                                        html.Div(
                                                            className='column thirtythree_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram10")
                                                            ]
                                                        ),                                                      
                                                        html.Div(
                                                            className='column sixtysix_perc',
                                                            children=[
                                                                dcc.Graph(id="histogram11")
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
                                                                dcc.Graph(id='histogram12')
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
        dash.dependencies.Output('baq-maps', 'figure'),
        dash.dependencies.Output('histogram0', 'figure'),
        dash.dependencies.Output('histogram1', 'figure'),
        dash.dependencies.Output('histogram2', 'figure'),
        dash.dependencies.Output('histogram3', 'figure'),
        dash.dependencies.Output('histogram4', 'figure'),
        dash.dependencies.Output('histogram5', 'figure'),
        dash.dependencies.Output('histogram6', 'figure'),
        dash.dependencies.Output('histogram7', 'figure'),
        dash.dependencies.Output('histogram8', 'figure'),
        dash.dependencies.Output('histogram9', 'figure'),
        dash.dependencies.Output('histogram10', 'figure'),
        dash.dependencies.Output('histogram11', 'figure'),
        dash.dependencies.Output('histogram12', 'figure'),
    ],
    [
        dash.dependencies.Input('crimetype-dropdown', 'value'),
        dash.dependencies.Input('year-dropdown', 'value'),
        dash.dependencies.Input('borough-dropdown', 'value')
    ]
)
def update_map(crime_type, years, borough):
    n_of_records = 3
    df_filtered,\
    df_crimes_by_barrio,\
    df_crimes_by_crimetype_and_year,\
    df_crimes_by_crimetype_and_localidad,\
    df_crimes_by_localidad,\
    df_crimes_by_localidad_and_year,\
    df_crimes_by_localidad_weekday,\
    df_crime_by_weekday,\
    df_crimes_by_month,\
    df_crimes_by_holiday,\
    df_crimes_by_tipodow = filter_crime(df_crime, crime_type, years, borough)
    
    return create_map(df_filtered),\
           create_line_chart_by_crimetype_and_year( df_crimes_by_crimetype_and_year ),\
           create_bar_chart_by_localidad( df_crimes_by_localidad ),\
           create_line_chart_by_localidad_and_year( df_crimes_by_localidad_and_year ),\
           create_bar_chart_crimestype_by_localidad( df_crimes_by_crimetype_and_localidad, n_of_records ),\
           create_bar_chart_top_barrios_total_crimen( df_crimes_by_barrio, n_of_records ),\
           create_bar_chart_top_barrios_by_ratio( df_crimes_by_barrio, n_of_records ),\
           create_bar_chart_crimes_by_localidad_and_weekday( df_crimes_by_localidad_weekday ),\
           create_bar_chart_crimes_by_weekday( df_crime_by_weekday ),\
           create_bar_char_crimes_by_tipodow( df_crimes_by_tipodow ),\
           create_bar_chart_crimes_by_month( df_crimes_by_month ),\
           create_bar_char_crimes_by_holiday( df_crimes_by_holiday ),\
           create_heatmap_hora_dow(df_filtered),\
           create_heatmap_festividad_localidad(df_filtered)
            

def create_map( df ):
    colors=[ get_color(t) for t in df['impacto'].values]
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
                     marker= dict(
                        color=colors,
                        colorscale=[
                            [0, "#21c7ef"],
                            [0.33, "#76f2ff"],
                            [0.66, "#ff6969"],
                            [1, "#ff1717"],
                        ],
                        size=(df['impacto']**2)/10),
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
    crime_lst = list(set(df["crimen"]))
    for c in crime_lst:
        df_tmp = df[df['crimen']==c]
        data.append(go.Scatter(x=df_tmp['period'], y=df_tmp['total'], name=c))

    return {
        'data' : data,
        'layout': getLayout('Crimenes a lo largo del tiempo', xtickmode='auto')
    }

def create_line_chart_by_localidad_and_year( df ):
    data = []

    # year_lst = sorted(list(set(df["year"])))

    # for year in year_lst:
    #     data.append(go.Bar( orientation='h', y=df[df['year']==year]['localidad'], x=df[df['year']==year]['total'], name=int(year)))

    localidad_lst = list(set(df["localidad"]))
    for loc in localidad_lst:
        df_tmp = df[df['localidad']==loc]
        df_tmp['year'] = df_tmp['year'].apply(lambda field: int(field))
        data.append(go.Scatter(x=df_tmp['year'], y=df_tmp['total'], name=loc))

    return {
        'data' : data,
        'layout': getLayout('Crimenes por localidad a través del tiempo', xtickangle=-90)
    }

def create_bar_chart_crimestype_by_localidad( df, n_of_records ):
    data = []
    localidad_lst = list(set(df["localidad"]))

    for loc in localidad_lst:
        df_tmp = df[df['localidad']==loc]
        #df_tmp['perc'] = (df_tmp['total'] / df_tmp['total'].sum())
        df_tmp['perc'] = df_tmp.apply( lambda row: row['total'] / df[(df['crimen'] == row['crimen'])]['total'].sum(), axis=1)
        df_tmp = df_tmp.sort_values(by='perc', ascending=False)
        data.append(go.Bar(x=df_tmp['crimen'], y=df_tmp['perc'], name=loc ))


    return {
        'data' : data,
        'layout' : getLayout('Tipo de crimen por localidad', xtickangle=-90, ytickformat=',.0%', bar_mode='stack')
    }

def create_bar_chart_crimes_by_localidad_and_weekday( df ):
    data = []

    df['nombre_dia_semana'] = df['dia_semana'].apply( lambda field: DAYS_OF_THE_WEEK[int(field)] )
    
    localidad_lst = list(set(df["localidad"]))  
    for loc in localidad_lst:
        data.append(go.Bar(x=df[df['localidad']==loc]['nombre_dia_semana'], y=df[df['localidad']==loc]['total'], name=loc))

    #dia_semana_lst = list(set(df["dia_semana"]))
    #for dow in dia_semana_lst:
    #    data.append(go.Bar(x=df[df['dia_semana']==dow]['localidad'], y=df[df['dia_semana']==dow]['total'], name=DAYS_OF_THE_WEEK[int(dow)]))

    return {
        'data' : data,
        'layout' : getLayout('Crimenes por día de la semana y localidad')
    }

def create_bar_chart_crimes_by_weekday( df ):
    data = []

    df['nombre_dia_semana'] = df['dia_semana'].apply( lambda field: DAYS_OF_THE_WEEK[int(field)] )
    data.append(go.Bar(x=df['nombre_dia_semana'], y=df['total']))

    return {
        'data' : data,
        'layout': getLayout('Crimenes por día de la semana')
    }    

def create_bar_chart_crimes_by_month( df ):
    data = []

    df['nombre_month'] = df['month'].apply( lambda field: MONTHS[int(field) - 1] )
    data.append(go.Bar(x=df['nombre_month'], y=df['total']))

    return {
        'data' : data,
        'layout': getLayout('Crimenes por mes', xtickangle=-90)
    }

def create_bar_char_crimes_by_holiday( df ):
    data = []

    df = df.sort_values(by='total', ascending=False)
    data.append(go.Bar(x=df['festivo'], y=df['total']))

    return {
        'data' : data,
        'layout': getLayout('Crimenes Días Feriados', xtickangle=-90)
    }



def create_bar_char_crimes_by_tipodow( df ):
    data = []
    df = df.sort_values(by='total', ascending=False)
    data.append(go.Bar(x=df['festivo'], y=df['total']))

    return {
        'data' : data,
        'layout': getLayout('Crimenes por tipo de día')
    }


def create_bar_chart_by_localidad( df ):
    df = df.sort_values(by='total', ascending=False)
    return {
        'data': [
            {'x': df['localidad'], 'y': df['total'], 'type': 'bar'}
        ],
        'layout': getLayout('Crimenes por localidades')
    }

def create_bar_chart_top_barrios_total_crimen(df, n_of_records):
    data = []
    localidad_lst = list(set(df["localidad"]))
    for loc in localidad_lst:
        df_tmp = df[df['localidad']==loc].head(n_of_records).sort_values(by='total', ascending=False)
        data.append(go.Bar(x=df_tmp['barrio'], y=df_tmp['total'], name=loc))

    return {
        'data': data,
        'layout': getLayout(f'Total crimenes Barrios x Localidad (Top {n_of_records})', xtickangle=-90)
    }

def create_bar_chart_top_barrios_by_ratio(df, n_of_records):
    data = []
    localidad_lst = list(set(df["localidad"]))
    for loc in localidad_lst:
        df_tmp = df[df['localidad']==loc].head(n_of_records).sort_values(by='crime_ratio', ascending=False)
        data.append(go.Bar(x=df_tmp['barrio'], y=df_tmp['crime_ratio'], name=loc))

    return {
        'data': data,
        'layout': getLayout(f'Ratio crimen por población Barrios x Localidad (Top {n_of_records})', xtickangle=-90)
    }

def create_heatmap_hora_dow(df):
    df["fecha_hora"] = df["fecha_hora"].apply(lambda x: dt.strptime(x, "%Y-%m-%d %H:%M:%S"))  # String -> Datetime
    df["date_horaampm"] = df["fecha_hora"].apply(lambda x: dt.strftime(x, "%I %p"))  # Datetime -> int(hour) + AM/PM

    df['numero_crimenes'] = 1
    df = df.sort_values('fecha_hora').set_index('fecha_hora')
    

    x_axis = [datetime.time(i).strftime("%I %p") for i in range(24)]  # 24hr time list
    y_axis = DAYS_OF_THE_WEEK

    # Get z value : sum(number of records) based on x, y,

    z = np.zeros((7, 24))
    annotations = []

    for ind_y, day in enumerate(y_axis):
        #filtered_day = df[df['date_dow'] == day]
        filtered_day = df[df['date_dow'] == ind_y]

        for ind_x, x_val in enumerate(x_axis):
            sum_of_record = filtered_day[filtered_day["date_horaampm"] == x_val][
                'numero_crimenes'
            ].sum()
            z[ind_y][ind_x] = sum_of_record

            annotation_dict = dict(
                showarrow=False,
                text="<b>" + str(sum_of_record) + "<b>",
                xref="x",
                yref="y",
                x=x_val,
                y=day,
                font=dict(family="sans-serif"),
            )

            annotations.append(annotation_dict)

    # Heatmap
    hovertemplate = "<b> %{y}  %{x} <br><br> %{z} incidentes"

    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=z,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=False,
            colorscale=[[0, "#5DBCD2"], [1, "#002963"]],
        )
    ]

    layout = dict(
                margin=dict(l=70, b=50, t=50, r=50),
                plot_bgcolor='#323130',
                paper_bgcolor='#323130',        
                modebar={"orientation": "v"},
                font=dict(family="Open Sans", color='#FFFFFF'),
                annotations=annotations,
                xaxis=dict(
                    side="top",
                    ticks="",
                    ticklen=2,
                    tickfont=dict(family="sans-serif"),
                    tickcolor="#FFFFFF",
                ),
                yaxis=dict(
                    side="left", ticks="", tickfont=dict(family="sans-serif"), ticksuffix=" "
                ),
                hovermode="closest",
                showlegend=True
            )
    return {"data": data, "layout": layout}


def create_heatmap_festividad_localidad(df):
    df['numero_crimenes'] = 1
    #df = df.sort_values('fecha_hora').set_index('fecha_hora')
    
    x_axis = list(set(df['crimen']))
    y_axis = list(set(df['localidad']))

    z = np.zeros((len(y_axis), len(x_axis)))
    annotations = []

    for ind_y, loc in enumerate(y_axis):
        filtered_loc = df[df['localidad'] == loc]

        for ind_x, x_val in enumerate(x_axis):
            sum_of_record = filtered_loc[filtered_loc["crimen"] == x_val]['numero_crimenes'].sum()
            z[ind_y][ind_x] = sum_of_record

            annotation_dict = dict(
                showarrow=False,
                text="<b>" + str(sum_of_record) + "<b>",
                xref="x",
                yref="y",
                x=x_val,
                y=loc,
                font=dict(family="sans-serif"),
            )

            annotations.append(annotation_dict)

    # Heatmap
    hovertemplate = "<b> %{y}  %{x} <br><br> %{z} incidentes"

    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=z,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=False,
            colorscale=[[0, "#5DBCD2"], [1, "#002963"]],
        )
    ]

    layout = dict(
                margin=dict(l=70, b=50, t=50, r=50),
                plot_bgcolor='#323130',
                paper_bgcolor='#323130',        
                modebar={"orientation": "v"},
                font=dict(family="Open Sans", color='#FFFFFF'),
                annotations=annotations,
                xaxis=dict(
                    side="top",
                    ticks="",
                    ticklen=2,
                    tickfont=dict(family="sans-serif"),
                    tickcolor="#FFFFFF",
                ),
                yaxis=dict(
                    side="left", ticks="", tickfont=dict(family="sans-serif"), ticksuffix=" "
                ),
                hovermode="closest",
                showlegend=True
            )
    return {"data": data, "layout": layout}


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')