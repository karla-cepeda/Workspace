# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 08:34:24 2021

@author: acjimenez
"""
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import math

from app import app

from datetime import datetime, date, timedelta

import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd

import pandas as pd
import numpy as np

colors = {
    'background': '#fff',
    'text': 'black'
}

colors2 = {'1':'#636EFA','2':'#EF553B','3':'#00CC96','4':'#AB63FA', '5':'#FFA15A', '0':'#1c1cbd'}

controls = dbc.Form(
    [
        dbc.FormGroup(
            [
                dcc.Dropdown(
                    id="typeStatus",
                    options=[
                        {"label": "Location", "value": "0"},
                        {"label": "Status", "value": "1"},
                        {"label": "Battery", "value": "2"},
                        
                    ],
                    value="0",
                    searchable=False,
                    style={'width':'200px', 'margin-right':'10px'}
                ),
            ],
            className="mr-3"
        ),
        dbc.FormGroup(
            [
                dcc.Dropdown(
                    id='select_status_bike',
                    searchable=False,
                    style={'width':'600px'}
                    
                ),
            ],
            className="mr-3"
        ),
        
    ],
    
)

list_options = html.Div(id='mylist')

graph = dcc.Graph(
                id='mapchart'
            )



layout = html.Div(style={'backgroundColor': colors['background']},children=[
    #dbc.Container([
        dbc.Row([
            
            html.Div(
            
            html.Button(id='openid',
                        children=[html.Img(src='assets/info-circle-fill.svg', style={'width':'30px'} )],
                        className='position-fixed', style={'right':'10px', 'z-index':'1000000', 'border': 'none', 'width': 'auto', 'margin': '0', 'padding': '0'}),
            
            
            ),
            
            dbc.Tooltip(
                "Remember: Bikes not located are plotted in the map by the last GPS locations, but there are also no historical GPS data for some bikes. Check out the table below!",
                target="openid",
                style={'font-size':'12px'}
            ),
            
            
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            
            
                dbc.Col(
                    html.H1(["Real-Time Map"], style={'textAlign': 'center', 'color': 'black', 'margin-bottom': '0px', 'padding':'0'}, className='display-4 mb-5 mt-5'
                            
                ), md=4), 
                dbc.Col(
                    html.H4(dbc.Badge("LIVE", color="danger", className="mr-1",), style={'padding':'0','padding-top':'30px'}), md=1)
                
                
            ],
            justify="center"),
            
            
        dbc.Row([
            dbc.Col(
                controls   
                ,md=12)
            
            ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                            
                            graph,
                            dcc.Interval(id="interval", interval=100000)
                         ],#style={'width': '80%', 'margin-left': '10%','display': 'inline-block'}
                    ),md=10
                ),
            
            dbc.Col(
                html.Div([
                list_options,])
                , md=2)                      
            
        ]),
        html.Div(children=[
            
            html.H4("List of Bikes"),
            dcc.Graph(id='loctblid',)
            
            ], style={'padding-top':'30px'}
                 
            ),
        dcc.ConfirmDialog(
            id='confirm',            
        ),
            
        #], style={'margin-left':'10px'}, className='mx-auto'),
      
])

@app.callback(
    [Output(component_id='select_status_bike', component_property='options'),
     Output(component_id='select_status_bike', component_property='value'),
     Output(component_id='select_status_bike', component_property='multi'),
     ],
    [Input(component_id='typeStatus', component_property='value'),]

)
def update_graphs(typedist):
        
    if not typedist:
        typedist = 0 
    
    options_ = None
    default = None
    multi=False
    if int(typedist) == 0:
        options_ = [
                        {'label': 'On', 'value': '1'},
                        {'label': 'No Located', 'value': '0'},
                        {'label': 'All bikes', 'value': '2'},
                   ]
        default = "2"
        
    elif int(typedist) == 1:
        options_ = [
                        {'label': 'Warning - is in move and not rented', 'value': '1'},
                        {'label': 'Normal', 'value': '2'},
                        {'label': 'Firmware Upgrade', 'value': '3'},
                        {'label': 'Switched Off', 'value': '4'},
                        {'label': 'Laying on the ground', 'value': '5'},
                        
                    ]
        default = ["1","2","3","4","5"]
        multi=True
    elif int(typedist) == 2:
        options_ = [
                        {'label': 'Perfect', 'value': '1'},
                        {'label': 'Good', 'value': '2'},
                        {'label': 'Warning', 'value': '3'},
                        {'label': 'Dead', 'value': '4'},
                        
                    ]
        default = ["1","2","3","4"]
        multi=True
        

    
    
    return [options_, default, multi]


@app.callback(
    [Output(component_id='mapchart', component_property='figure'),
     Output('confirm', 'display'),
     Output('confirm', 'message'),
     Output('mylist', 'children'),
     Output('loctblid', 'figure'),
     
     ],
    
    [Input(component_id='select_status_bike', component_property='value'),
     Input(component_id='typeStatus', component_property='value'),
     Input(component_id='interval', component_property='n_intervals'),]
)
def update_graphs(checkbox, typedist, n_intervals):

    #print(n_intervals)

    message = ""
    display = False
    figtblbat = None
    
    #divtblid = {'display':'none'}

    if not checkbox:
        return dash.no_update
        
    mapbox_access_token = "pk.eyJ1Ijoia2FybGljIiwiYSI6ImNrbml0bjdiZTNzZ2wybm54bjZjaW94dWcifQ.0EFv4tUJhKocrOErV4IDQg"
    lastgps = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/lastgps.csv')
    mobyarea = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/mobyarea.csv')
    lastgps.Located.fillna(0, inplace=True)
    lastgps['Located'] = lastgps.Located.astype(int)
    
    lastgps['Latitude'] = lastgps['Latitude'].apply(lambda x: round(x,4))
    lastgps['Longitude'] = lastgps['Longitude'].apply(lambda x: round(x,4))
    
    df = None
    col = None
    mylist=[]
    if int(typedist) == 0:
        
        col = 'Located'
        if int(checkbox) != 2:            
            df = lastgps[lastgps[col].astype(int) == int(checkbox)]
        else:
            df = lastgps
        
        if len(df) == 0 and int(checkbox) == 0:
            message = "All bikes are located."
            display = True
        
        """
         {'label': 'On', 'value': '1'},
         {'label': 'No Located', 'value': '0'},
         {'label': 'All bikes', 'value': '2'},
        """
        mylist = html.Ul([
                            html.Li("On", className='circle', style={'background': colors2['1'],'color':'black',
                                'list-style':'none','text-indent': '17px'}),
                            html.Li("No Located", className='circle', style={'background': colors2['0'],'color':'black',
                                'list-style':'none','text-indent': '17px','white-space':'nowrap'}),                            
                        ], style={'border-bottom': 'solid 3px', 'border-color':'#00FC87','padding-top': '6px', 'margin-left':'10px', 'margin-right':'10px', 'margin-top':'10px'})
        
        
        data = None
           
        if int(checkbox) == 0:
            
            data = lastgps[lastgps.Located == 0]
            data['date2'] = lastgps.LastGPSTime
            data.date2.fillna('1900-01-01', inplace=True)
            data.date2 = pd.to_datetime(data.date2)
            
            data.sort_values(by=['date2'], inplace=True, ascending=False)
                 
            #divtblid = {'display':'block'}
        elif int(checkbox) == 1:
            
            data = lastgps[lastgps.Located == 1]
            data['date2'] = lastgps.LastGPSTime
            data.date2.fillna('1900-01-01', inplace=True)
            data.date2 = pd.to_datetime(data.date2)
            
            data.sort_values(by=['date2'], inplace=True, ascending=False)
                 
            #divtblid = {'display':'block'}
             
        else:
            
            data = lastgps.copy()
            data['date2'] = lastgps.LastGPSTime
            data.date2.fillna('1900-01-01', inplace=True)
            data.date2 = pd.to_datetime(data.date2)
            
            data.sort_values(by=['date2'], inplace=True, ascending=False)
             
            
        figtblbat = go.Figure(data=[go.Table(
            columnwidth = [20,15,20,15,15],
            header=dict(values=['Last Time GPS', 'Bike ID', 'Latitude', 'Longitude', "Located"],
                        fill_color='royalblue',
                        font=dict(color='white', size=12),
                        align='left'),
            cells=dict(values=[data.LastGPSTime.fillna("No available"),
                               data.BikeID,                        
                               data.Longitude.fillna(0),
                               data.Latitude.fillna(0),
                               np.where(data.Located==1,"Yes", "No")
                               ],
                       #fill_color='white',
                       align='left'))
        ])
        
        figtblbat.update_layout(
            #autosize=True,
            #width=200,
            height=400,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=0
            ),
            paper_bgcolor="White",
        )
        
        df = data.copy()
                
                
    elif int(typedist) == 1:
        col = 'EBikeStateID'
        
        #if int(checkbox) != 6:
            #df = lastgps[lastgps[col].astype(int) == int(checkbox)]
        
        data =[]
        for j in checkbox:
            data.append(lastgps[lastgps[col].astype(int) == int(j)])

        df = pd.DataFrame(np.concatenate(data), columns=lastgps.columns)
        
        #print(df)
        #print(df.columns)
        
        """
                        {'label': 'In move - not rented', 'value': '1'},
                        {'label': 'Normal', 'value': '2'},
                        {'label': 'Firmware Upgrade', 'value': '3'},
                        {'label': 'Switched Off', 'value': '4'},
                        {'label': 'Laying on the ground', 'value': '5'},
        """              
        
        mylist = html.Ul([
                        html.Li("In move - not rented", className='circle', style={'background': colors2['1'],'color':'black',
                            'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
                        html.Li("Normal", className='circle', style={'background': colors2['2'],'color':'black',
                            'list-style':'none','text-indent': '17px','white-space':'nowrap'}),            
                        html.Li("Firmware Upgrade", className='circle', style={'background': colors2['3'],'color':'black',
                            'list-style':'none','text-indent': '17px','white-space':'nowrap'}),            
                        html.Li("Switched Off", className='circle', style={'background': colors2['4'],'color':'black',
                            'list-style':'none','text-indent': '17px','white-space':'nowrap'}), 
                        html.Li("Laying on the ground", className='circle', style={'background': colors2['5'],'color':'black',
                            'list-style':'none','text-indent': '17px','white-space':'nowrap'}), 
                    ], style={'border-bottom': 'solid 3px', 'border-color':'#00FC87','padding-top': '6px', 'margin-left':'10px', 'margin-right':'10px', 'margin-top':'10px'})
       
        #else:
        #    df = lastgps
        
        
        if len(df) == 0:
            message = "No bikes with indicated status."
            display = True
            
            
        figtblbat = go.Figure(data=[go.Table(
            columnwidth = [20,15,20,15,15],
            header=dict(values=['Last Time Harvested', 'Bike ID', 'Latitude', 'Longitude', "Status", "Located"],
                        fill_color='royalblue',
                        font=dict(color='white', size=12),
                        align='left'),
            cells=dict(values=[df.HarvestTime.fillna("No available"),
                               df.BikeID,                                         
                               df.Longitude.fillna(0),
                               df.Latitude.fillna(0),
                               df.nameebs,
                               np.where(df.Located==1,"Yes", "No")
                               ],
                       #fill_color='white',
                       align='left'))
        ])
        
        figtblbat.update_layout(
            #autosize=True,
            #width=200,
            height=400,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=0
            ),
            paper_bgcolor="White",
        )    
        
    
    elif int(typedist) == 2:
        
        col = 'batteryid'
        
        #if int(checkbox) != 6:
            #df = lastgps[lastgps[col].astype(int) == int(checkbox)]
        
        data =[]
        for j in checkbox:
            data.append(lastgps[lastgps[col].astype(int) == int(j)])

        df = pd.DataFrame(np.concatenate(data), columns=lastgps.columns)
        
        
        mylist = html.Ul([
                        html.Li("Perfect", className='circle', style={'background': colors2['1'],'color':'black',
                            'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
                        html.Li("Good", className='circle', style={'background': colors2['2'],'color':'black',
                            'list-style':'none','text-indent': '17px','white-space':'nowrap'}),            
                        html.Li("Warning", className='circle', style={'background': colors2['3'],'color':'black',
                            'list-style':'none','text-indent': '17px','white-space':'nowrap'}),            
                        html.Li("Dead", className='circle', style={'background': colors2['4'],'color':'black',
                            'list-style':'none','text-indent': '17px','white-space':'nowrap'}), 
                    ], style={'border-bottom': 'solid 3px', 'border-color':'#00FC87','padding-top': '6px', 'margin-left':'10px', 'margin-right':'10px', 'margin-top':'10px'})
       
        
        if len(df) == 0:
            message = "No bikes with indicated status."
            display = True
            
            
        figtblbat = go.Figure(data=[go.Table(
            columnwidth = [20,15,20,15,15, 10, 10],
            header=dict(values=['Last Time Harvested', 'Bike ID','Latitude', 'Longitude',  "Battery", "Level", "Located"],
                        fill_color='royalblue',
                        font=dict(color='white', size=12),
                        align='left'),
            cells=dict(values=[df.HarvestTime.fillna("No available"),
                               df.BikeID,          
                               df.Longitude.fillna(0),
                               df.Latitude.fillna(0),
                               df.name,
                               df.Battery,
                               np.where(df.Located==1,"Yes", "No")
                               ],
                       #fill_color='white',
                       align='left'))
        ])
        
        figtblbat.update_layout(
            #autosize=True,
            #width=200,
            height=400,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=0
            ),
            paper_bgcolor="White",
        )  
    
    #print(df.iloc[5:, :])
    
    textmap = list()
    
    if len(df) > 0:
    
        values = lastgps[col].unique()
            
        for i in values:
            cond = (df[col] == i)
            df.loc[cond,'colors'] = colors2[str(int(i))]
        
        
        for i in range(0,len(df)):
        #    print(len(df))
        #    print(i)
        #    print(df.loc[i,:])
            textmap.append('Bike ID = ' + str(df.reset_index().loc[i, 'BikeID']))
        
        
    else:
        
        df['colors'] = None
     

    fig_map = go.Figure(    
        go.Scattermapbox(
            lat=df.Latitude,
            lon=df.Longitude,
            
            marker=go.scattermapbox.Marker(
                size=9,
                color=df['colors'],
            ),
            text=textmap,
            showlegend=False
        ))
    
    fig_map.add_trace(    
        go.Scattermapbox(
            mode = "lines", fill = "toself", 
            fillcolor='rgba(26,150,65,0.2)',
            lon = mobyarea.Longitude,
            lat = mobyarea.Latitude,
            showlegend=False,
            hoverinfo='none',))
    
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
            #showlegend=False
        ),
        margin = {'l':0, 'r':0, 'b':0, 't':0},
        
        geo_scope='europe')
    
    fig_map.data = fig_map.data[::-1]
            
    return [fig_map, display, message, [mylist], figtblbat]

