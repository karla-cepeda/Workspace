
#import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from datetime import datetime, timedelta

import plotly.express as px
import plotly.graph_objects as go
#import geopandas as gpd

import pandas as pd
from app import app
import numpy as np

# Global values
#colors = ['#636EFA','#EF553B','#00CC96', '#AB63FA', '#FFA15A', '#1c1cbd']
colors = px.colors.qualitative.Plotly
image_filename = 'assets/green_arrow_long.svg'

#encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode() 

layout = html.Div(children=[   
    dbc.Row(children=[
        html.Div(children=[html.Button(id='openid',
                                       children=[html.Img(src='assets/info-circle-fill.svg', style={'width':'30px'} )],
                                       className='position-fixed', style={'right':'10px', 'z-index':'1000000', 'border': 'none', 'width': 'auto', 'margin': '0', 'padding': '0'}
                                       ),]
                 ),
            
            dbc.Tooltip(children=["Welcome to the dashboard!"
                                  " This is just a summary about location and status of bikes."
                                  " For details, access to Map, Bikes and Rentals section."],
                        target="openid",
                        style={'font-size':'12px'}
                        ),
            
            dbc.Col(children=[html.H1("Dashboard", 
                                      style={'textAlign': 'center', 'color': 'black', 'margin-bottom': '0px'}, 
                                      className='display-4'),
                              html.H4("Real-Time Bikes' Status", 
                                      style={'textAlign': 'center', 'color':'gray', 'margin-top': '0px', 'font-size':'20px'}, 
                                      className='display-4')], 
                    className="col-sm-12", md=3
                    ), 
        
            dbc.Col(children=[html.H4(dbc.Badge("LIVE", 
                                                color="danger", 
                                                className="mr-1",), 
                                      style={'padding':'0'})],
                    md=1),
            ], justify="center"),
        
        
    dbc.Row(id='summary', style={'margin-top':'30px'}),
          
    dbc.Row([       
        dbc.Col([
            html.Tbody(
                html.Tr([
                    html.Td(html.H4("Bikes Rented during the day", 
                                    style={'margin-bottom': '11px','padding-left': '14px', 'display':'in-line'}), 
                            style={'margin':'0', 'padding':'0', 'width':'81.5%', 'border':'None'}),
                    html.Td(dbc.Button("Explore Rentals", 
                                       id='goMap', 
                                       href = '/rentals', 
                                       color="primary", 
                                       className="mr-1", ), 
                            style={'margin':'0', 'padding':'0', 'border':'None'}),
                        ], style={'margin':'0', 'padding':'0'}), 
                style={'margin':'0', 'padding':'0'}),
            
            dcc.Graph(id='cumRent',)
            ], className="col-sm-6"),
        
        dbc.Col([
            html.Tbody(
                html.Tr([
                    html.Td(html.H4("Located bikes in map", 
                                    style={'margin-bottom': '11px','display':'in-line', 'margin-bottom':'10px'}), 
                            style={'margin':'0', 'padding':'0', 'width':'84%', 'border':'None', "text-align": "left"}),
                    html.Td(dbc.Button("Explore Map", 
                                       id='goMap', 
                                       href = '/map', 
                                       color="primary", 
                                       className="mr-1", 
                                       style={'margin-bottom':'10px'}), 
                            style={'margin':'0', 'padding':'0', 'border':'None'}),
                    ], style={'margin':'0', 'padding':'0'}), 
                style={'margin':'0', 'padding':'0'}),
                
                
            dcc.Graph(id='mapBikes',),
            ], className="col-sm-6", style={'text-align':'right'}),
        
        ], style={'margin-top':'30px'}),
    
     dbc.Row([       
        dbc.Col([
            html.Tbody(
                html.Tr([
                    html.Td(dbc.Button("Explore Bikes", 
                                       id='goMap', 
                                       href = '/bikes', 
                                       color="primary", 
                                       className="mr-1", ), 
                            style={'margin':'0', 'padding':'0', 'border':'None', 'width':'100%',}),
                        ], style={'margin':'0', 'padding':'0'}), 
                style={'margin':'0', 'padding':'0'}),
            
            ], className="col-sm-auto"),
    ], justify="end"),
        
    
     dbc.Row([
         dbc.Col([
             html.Div([
                 html.H4('Bikes Located', 
                         style={'textAlign': 'center',}),
                
                 dcc.Graph(id='missingbikes',
                           config={'displayModeBar': False}
                           ),
                
                 html.Ul(id='missingbikeslist', 
                         style={'padding-top': '6px', 'margin-left':'50px', 'margin-right':'10px', 'margin-top':'10px'}
                         ),
                ]),
            ], className="col-sm-3"),
        
         dbc.Col([
             html.Div([
                 html.H4('Bikes in area', 
                         style={'textAlign': 'center',}),
            
                 dcc.Graph(id='fig_inarea',
                           config={'displayModeBar': False} 
                           ),
                
                 html.Ul(id='listBikesInArea', 
                         style={'padding-top': '6px', 'margin-left':'50px', 'margin-right':'10px', 'margin-top':'10px'}),
                
                ]),
            ], className="col-sm-3"),
        
         dbc.Col([
             html.Div([
                 html.H4('Status of Bikes', 
                         style={'textAlign': 'center', }),
                
                 dcc.Graph(
                     id='fig_estatus',
                     config={'displayModeBar': False}),
                
                 html.Ul(id='statusbikes', 
                         style={'padding-top': '6px', 'margin-left':'50px', 'margin-right':'10px', 'margin-top':'10px'}),
                 ]),
             ], className="col-sm-3"),
        
        dbc.Col([
            html.Div([
                html.H4('Battery Status', 
                        style={'textAlign': 'center', }),
            
                dcc.Graph(id='fig_battery',
                          config={'displayModeBar': False}),
                
                html.Ul(id='batterybikes', 
                        style={'padding-top': '6px', 'margin-left':'50px', 'margin-right':'10px', 'margin-top':'10px'}),
                ]),
            ], className="col-sm-3"),
        
        ], justify="center", style={'margin-top':'30px'}), 
     
     dcc.Interval(id="interval", interval=100000),
         
    
])



@app.callback([
    Output(component_id='cumRent', component_property='figure'),
    Output(component_id='mapBikes', component_property='figure'),
    Output(component_id='missingbikes', component_property='figure'),
    Output(component_id='fig_inarea', component_property='figure'),
    Output(component_id='fig_estatus', component_property='figure'),
    Output(component_id='fig_battery', component_property='figure'),
    Output(component_id='summary', component_property='children'),
    Output(component_id='listBikesInArea', component_property='children'),
    Output(component_id='batterybikes', component_property='children'),
    Output(component_id='statusbikes', component_property='children'),
    Output(component_id='missingbikeslist', component_property='children'),
    ],
    [Input(component_id='interval', component_property='n_intervals'),]
)
def update_graphs(n_intervals):
    
    # global values
    start_date = pd.to_datetime(datetime.today()).ceil('Min')
    flag = timedelta(minutes=60)
    end_date = pd.to_datetime(datetime.today()) - flag
    
    # --------------------------------------------------------
    
    rented_cum = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/rented_cum.csv')
    rented_cum['LastRentalStart'] = pd.to_datetime(rented_cum.LastRentalStart)
    
    miny = np.clip(rented_cum.Total.max()-10,a_min=0, a_max=None)
    
    # Figure for total rents in real-time
    # I am going to zoom in on specific interval but
    # older value (just from current day) could be available.
    rc_fig = px.line(rented_cum, x='LastRentalStart', y='Total',
                                       labels={
                         "Total": "Total",
                         "LastRentalStart": "Last Rental Start",
                             }, 
                                )
    rc_fig.update_xaxes(type="date", range=[end_date, start_date])
    rc_fig.update_yaxes(range=[miny,rented_cum.Total.max()+2])
    rc_fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor="White",
    )
    
    # -----------------------------------------------------
    
    lastgps = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/lastgps.csv')
    lastgps['LastGPSTime'] = pd.to_datetime(lastgps['LastGPSTime'])
    
    # download point to draw moby area
    mobyarea = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/mobyarea.csv')
    # token to download map from mapbox
    mapbox_access_token = "pk.eyJ1Ijoia2FybGljIiwiYSI6ImNrbml0bjdiZTNzZ2wybm54bjZjaW94dWcifQ.0EFv4tUJhKocrOErV4IDQg"
    
    condition = lastgps['Located'] == 1
    locatedbikes = lastgps[condition].copy()
    locatedbikes['color'] = colors[0]
    locatedbikes['Latitude'] = locatedbikes['Latitude'].apply(lambda x: round(x,4))
    locatedbikes['Longitude'] = locatedbikes['Longitude'].apply(lambda x: round(x,4))
    
    # List of bike id to show in map when hovering a point
    textmap = list()
    for i in range(0,len(lastgps)):
        textmap.append('Bike ID = ' + str(lastgps.reset_index().loc[i, 'BikeID']))
    
    # Map to plot latitude and longitude from current bikes' position
    # Draw bikes' location
    fig_map = go.Figure(    
        go.Scattermapbox(
            lat=locatedbikes.Latitude,
            lon=locatedbikes.Longitude,
            mode='markers',
            marker_color = locatedbikes.color,
            marker=go.scattermapbox.Marker(
                    size=9,
            ),
            text=textmap,
            showlegend=False,
            legendgroup = ""
            )
        )
    
    # Draw moby area
    fig_map.add_trace(    
        go.Scattermapbox(
            mode = "lines", fill = "toself", 
            fillcolor='rgba(26,150,65,0.2)',
            lon = mobyarea.Longitude,
            lat = mobyarea.Latitude,
            showlegend=False,
            hoverinfo='none',))
    
    # To center map on Dublin
    fig_map.update_layout(
        hovermode='closest',
        mapbox=dict(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=53.3354,
                lon=-6.26761
            ),
            pitch=0,
            zoom=10,
        ),
        showlegend = False,
        height = 418,
        margin = {'l':0, 'r':0, 'b':0, 't':0},
        geo_scope='europe')
    
    fig_map.data = fig_map.data[::-1]
    
    # -------------------------------------
    
    # Plot pie chart to show summary of the information
    
    #lastgps.loc[(lastgps['Located']==0), 'located_name'] = 'Missing bike'
    #lastgps.loc[(lastgps['Located']==1), 'located_name'] = 'Bike on'
    
    get_location = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/get_location.csv')
    get_batteryStatus = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/get_batteryStatus.csv')
    get_bikestatus = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/get_bikestatus.csv')
    get_inarea = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/get_inarea.csv')
    
    # Show number of located and no located bikes
    fig_missing = px.pie(get_location, 
                         values='total', 
                         names='label', 
                         color='label',
                         labels={"label": "Status",
                                 "total": "Total",
                                 }
                         )
    fig_missing.update(layout_showlegend=False)
    fig_missing.update_layout(
        autosize=True,
        height=200,
        margin=dict(
            l=10,
            r=10,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor="White",
    )
    fig_missing.update_traces(textposition='inside')
    
    # Show number of bikes in or out of moby area
    fig_area = px.pie(get_inarea, 
                      values='total', 
                      names='label', 
                      color='label',
                      labels={"label": "Status",
                              "total": "Total",
                              }
                      )
    fig_area.update(layout_showlegend=False)
    fig_area.update_layout(
        autosize=True,
        height=200,
        margin=dict(
            l=10,
            r=10,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor="White",
    )
    fig_area.update_traces(textposition='inside')
    
    # Show number of bikes per (physical) status
    fig_estatus = px.pie(get_bikestatus, 
                         values='total', 
                         names='name', 
                         color='name',
                         labels={"name": "Status",
                                 "total": "Total",
                                 }
                         )
    fig_estatus.update(layout_showlegend=False)
    fig_estatus.update_layout(
        autosize=True,
        height=200,
        margin=dict(
            l=10,
            r=10,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor="White",
    )
    fig_estatus.update_traces(textposition='inside')
    
    # Show number of bikes according to level of battery
    # this was binned by Perfect, Good, Warning and Dead.    
    fig_battery = px.pie(get_batteryStatus, 
                         values='total', 
                         names='name', 
                         color='name',
                         labels={"name": "Status",
                                 "total": "Total",
                                }
                         )
    fig_battery.update(layout_showlegend=False)
    fig_battery.update_layout(
        autosize=True,
        height=200,
        margin=dict(
            l=10,
            r=10,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor="White",
    )
    fig_battery.update_traces(textposition='inside')
    
    
    # Create lists of option for each pie chart    
    listInArea = [
            html.Li(get_inarea.label.unique()[0], 
                    className='circle', 
                    style={'background': colors[0],'color':'black', 'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
            html.Li(get_inarea.label.unique()[1], 
                    className='circle', 
                    style={'background': colors[1],'color':'black', 'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
            html.Li(get_inarea.label.unique()[2], 
                    className='circle', 
                    style={'background': colors[2],'color':'black', 'list-style':'none','text-indent': '17px','white-space':'nowrap'}),                            
        ]

    batterylist = [
            html.Li(get_batteryStatus.name.unique()[0], 
                    className='circle', 
                    style={'background': colors[0],'color':'black', 'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
            html.Li(get_batteryStatus.name.unique()[1], 
                    className='circle', 
                    style={'background': colors[1],'color':'black', 'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
            html.Li(get_batteryStatus.name.unique()[2], 
                    className='circle', 
                    style={'background': colors[2],'color':'black', 'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
            html.Li(get_batteryStatus.name.unique()[3], 
                    className='circle', 
                    style={'background': colors[3],'color':'black', 'list-style':'none','text-indent': '17px','white-space':'nowrap'}), 
        ]
    
    statusbikes = [
            html.Li(get_bikestatus.name.unique()[0], 
                    className='circle', 
                    style={'background': colors[0],'color':'black', 'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
            html.Li(get_bikestatus.name.unique()[1], 
                    className='circle', 
                    style={'background': colors[1],'color':'black', 'list-style':'none','text-indent': '17px','white-space':'nowrap'}),            
            html.Li(get_bikestatus.name.unique()[2], 
                    className='circle', 
                    style={'background': colors[2],'color':'black', 'list-style':'none','text-indent': '17px','white-space':'nowrap'}),            
            html.Li(get_bikestatus.name.unique()[3], 
                    className='circle', 
                    style={'background': colors[3],'color':'black','list-style':'none','text-indent': '17px','white-space':'nowrap'}), 
            html.Li(get_bikestatus.name.unique()[4], 
                    className='circle', 
                    style={'background': colors[4],'color':'black','list-style':'none','text-indent': '17px','white-space':'nowrap'}),
            ]
    
    missingbikeslist = [
            html.Li("On", 
                    className='circle', 
                    style={'background': colors[0],'color':'black','list-style':'none','text-indent': '17px'}),
            html.Li("No Located", 
                    className='circle', 
                    style={'background': colors[1],'color':'black', 'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
            ]
    
    # ----------------------------------------------------------
    
    summary = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/summary.csv')
    
    summ = [dbc.Col([
                html.Div(
                    dbc.Toast([
                        html.Tbody(
                            html.Tr([
                                html.Td(html.Img(src="/assets/bike2.png", 
                                                 height="60px"), 
                                        style={'border': 'none'}),
                                html.Td(html.P(summary.loc[0,'total'], 
                                               className="mb-0"), 
                                        style={'border': 'none', 'font-size':'30px'})],
                                ), style={'width':'100%', 'border': 'none'})
                        ], header=summary.loc[0,'label'], style={'font-size':'18px'},)
                    ),
                ]), 
            
            dbc.Col([
                html.Div(
                    dbc.Toast([
                        html.Tbody(
                            html.Tr([
                                html.Td(html.Img(src="/assets/bike5.png", 
                                                 height="60px"), 
                                        style={'border': 'none'}),
                                html.Td(html.P(summary.loc[1,'total'], 
                                               className="mb-0"), 
                                        style={'border': 'none', 'font-size':'30px'})],
                                ), style={'width':'100%', 'border': 'none'}),
                        ], header=summary.loc[1,'label'], style={'font-size':'18px'},)
                    )
                ]), 
            
            dbc.Col([
                html.Div(
                    dbc.Toast([
                        html.Tbody(
                            html.Tr([
                                html.Td(html.Img(src="/assets/bike1.png", 
                                                 height="60px"), 
                                        style={'border': 'none'}),
                                html.Td(html.P(summary.loc[2,'total'], 
                                               className="mb-0"), 
                                        style={'border': 'none', 'font-size':'30px'})],
                                ), style={'width':'100%', 'border': 'none'}),
                        ], header=summary.loc[2,'label'], style={'font-size':'18px'},)
                    )
                ]), 
            
            dbc.Col([
                html.Div(
                    dbc.Toast([
                        html.Tbody(
                            html.Tr([
                                html.Td(html.Img(src="/assets/bike3.png", 
                                                 height="60px"), 
                                        style={'border': 'none'}),
                                html.Td(html.P(summary.loc[3,'total'], 
                                               className="mb-0"), 
                                        style={'border': 'none', 'font-size':'30px'})],
                                ), style={'width':'100%', 'border': 'none'}),
                        ], header=summary.loc[3,'label'], style={'font-size':'18px'},)
                    )
                ]), 
            
            dbc.Col([
                html.Div(
                    dbc.Toast([
                        html.Tbody(
                            html.Tr([
                                html.Td(html.Img(src="/assets/bike4.png", 
                                                 height="60px"), 
                                        style={'border': 'none'}),
                                html.Td(html.P(summary.loc[4,'total'], 
                                               className="mb-0"), 
                                        style={'border': 'none', 'font-size':'30px'})],
                                ), style={'width':'100%', 'border': 'none'})
                        ], header=summary.loc[4,'label'], style={'font-size':'18px'},)
                    )
                ]),
            ]
    

    return [rc_fig, fig_map, fig_missing, fig_area, fig_estatus, fig_battery, summ, listInArea, batterylist, statusbikes, missingbikeslist]
