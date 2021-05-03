

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from datetime import datetime, date, timedelta

import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd

import pandas as pd
import numpy as np

from app import app

def split_datelist(x):
    if len(x) == 2:
        return x[1]
    return np.nan


now = datetime.now()

maxhour = now.hour

dictlist = dict()
sliders = [*range(0,maxhour+2)]

for i in sliders:
    dictlist[i] = str(i)+":00"


slidertool = dcc.RangeSlider(
                    id='sliderid',
                    min=min(sliders),
                    max=max(sliders),
                    value=[min(sliders), max(sliders)],
                    step=1,
                    marks=dictlist,
                    allowCross=False,
                    
                    #included=False
                )  

layout = html.Div(children=[   
        
        
    
        dbc.Row([
                #Header span the whole row
                #className: Often used with CSS to style elements with common properties.
                
                html.Div(
                    
                html.Button(id='openid',
                        children=[html.Img(src='assets/info-circle-fill.svg', style={'width':'30px'} )],
                        className='position-fixed', style={'right':'10px', 'z-index':'1000000', 'border': 'none', 'width': 'auto', 'margin': '0', 'padding': '0'}
                        ),
                
                ),
            
                dbc.Tooltip(
                    "Filter your data! Rented bikes are filtered by range, while Status and Battery plots just display the last time data was harvested.",
                    target="openid",
                    style={'font-size':'12px'}
                ),
                
                
                
                dbc.Col(
                    html.H1(["Real-Time Bikes"], style={'textAlign': 'center', 'color': 'black', 'margin-bottom': '0px', 'padding':'0'}, className='display-4 mb-5 mt-5'
                            
                ), md=4), 
                dbc.Col(
                    html.H4(dbc.Button("LIVE", color="danger", className="mr-1"), style={'padding':'0','padding-top':'30px'}), md=1)
                
                
            ],
            justify="center"),
        
    
         dbc.Row([
                #Header span the whole row
                #className: Often used with CSS to style elements with common properties.
                html.P("Filter by hour:"),
                dbc.Col(children=[slidertool], style={'padding-top':'10px'})
                ], style={'margin-top':'10px', 'padding-left':'30px'}),
        
        

        dbc.Row([
                dbc.Col([
                        html.H4("Number of rentals per Bike", style={'margin-bottom': '11px','padding-top': '41px','padding-left': '43px', 'display':'in-line'}),
                    ],md=12), 
            ]),
    
    
        dbc.Row([
            dbc.Col(
                html.Div([
                            
                            
                            
                            dcc.Graph(
                                   id='figid',
                                   
                               ),
                            
                            
                            
                         ],#style={'width': '80%', 'margin-left': '10%','display': 'inline-block'}
                    ),md=8
                ),
            
            dbc.Col(
                html.Div([
                    dcc.Graph(
                            id='figtblid',
                            
                        ),
                    
                    html.Div(id='Totalfigid', style={'padding-top':'20px'}),
                    
                ])
                , md=4),                    
            
            ]),
    
    
        dbc.Row([
                dbc.Col([
                        html.H4("Battery status per Bike", style={'margin-bottom': '11px','padding-top': '41px','padding-left': '43px', 'display':'in-line'}),
                    ],md=12), 
            ]),
    
            dbc.Row([
            dbc.Col(
                html.Div([
                            
                            
                            
                            dcc.Graph(
                               id='fig_baterryid',
                                   config={
                                        'displayModeBar': False
                                    }
                               
                           ),
                            
                         ],#style={'width': '80%', 'margin-left': '10%','display': 'inline-block'}
                    ),md=8
                ),
            
            dbc.Col(
                html.Div([
                    dcc.Graph(
                            id='figtblbatid',
                            
                        ),
                    
                ])
                , md=4),                    
            
            ]),
            
            
            
    
        dbc.Row([
                dbc.Col([
                        html.H4("Status per Bike", style={'margin-bottom': '11px','padding-top': '41px','padding-left': '43px', 'display':'in-line'}),
                    ],md=12), 
            ]),
    
            dbc.Row([
            dbc.Col(
                html.Div([
                            
                            
                            
                            dcc.Graph(
                               id='fig_statusid',
                                   config={
                                        'displayModeBar': False
                                    }
                               
                           ),
                            
                         ],#style={'width': '80%', 'margin-left': '10%','display': 'inline-block'}
                    ),md=8
                ),
            
            dbc.Col(
                html.Div([
                    dcc.Graph(
                            id='figtblstatid',
                            
                        ),
                    
                ])
                , md=4),                    
            
            ]),
                        
            
            dcc.Interval(id="interval", interval=100000)
            
    ], )



@app.callback(
    [Output(component_id='figtblstatid', component_property='figure'),
     Output(component_id='figtblbatid', component_property='figure'),
     Output(component_id='fig_statusid', component_property='figure'),
     Output(component_id='fig_baterryid', component_property='figure'),
     Output(component_id='figtblid', component_property='figure'),
     Output(component_id='figid', component_property='figure'),
     Output('sliderid', 'max'),
     Output('sliderid', 'min'),
     Output('sliderid', 'value'),
     Output('sliderid', 'marks'),
     Output('Totalfigid', 'children'),],
    
    [Input(component_id='sliderid', component_property='value'),
     Input(component_id='interval', component_property='n_intervals'),]
    
)
def update_graphs(valueslder, n_intervals):
    
    now = datetime.now()
    
    print(n_intervals)
    print(valueslder)
    
    smin = valueslder[0]
    smax = valueslder[1]
    
    BikesRented = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/BikesRented.csv')
    BikesRented.drop(columns=['Unnamed: 0'], inplace=True)
    BikesRented.LastRentalStart = pd.to_datetime(BikesRented.LastRentalStart)
    
    BikesRented['date'] = BikesRented['LastRentalStart'].dt.date
    BikesRented['time'] = BikesRented['LastRentalStart'].dt.time
    BikesRented['hour'] = BikesRented['LastRentalStart'].dt.hour
    
    BikesRented.sort_values(by='LastRentalStart', ascending=False, inplace=True)
    
    cond = (BikesRented.LastRentalStart.dt.hour >= smin) & (BikesRented.LastRentalStart.dt.hour < smax)
    rentedtoday = BikesRented[cond].copy()
    
    countbikes = rentedtoday.groupby(by='BikeID').count().copy()
    countbikes.reset_index(inplace=True)
    countbikes.drop(columns=['time', 'hour', 'date'], inplace=True)
    countbikes.columns=['BikeID', 'Total']
    
    maxbikes = rentedtoday[['LastRentalStart', 'BikeID']].groupby(by=['BikeID']).max()
    maxbikes.reset_index(inplace=True)
    
    countbikes = countbikes.merge(maxbikes)
    countbikes['ltrstring'] = countbikes.LastRentalStart.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    my_color = ['rgb(237, 102, 93)']
    
    fig = px.bar(countbikes, y='Total', x='BikeID',
                 # add text labels to bar
                 text='Total', 
                 color_discrete_sequence=my_color, 
                 #color='',
                 #title='Number of Rents by Bike',
                 # Add country and life Exp info to hover text
                 hover_data=['BikeID', 'ltrstring'],
                 # change labels
                 labels={'Total':'Number of times rented','BikeID':'Bike Identifier','ltrstring':'Last Time Rented'})
    #update text to be number format rounded with unit and outside 
    fig.update_xaxes(type="category", range=[-1, 19])
    fig.update_yaxes(range=[0,countbikes.Total.max()+1])
    #fig.update_yaxes(type="linear", range=[0,lastinfo.total.max()+2])
    fig.update_traces(texttemplate='', textposition='outside')
    #fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    
    fig.update_layout(
        #autosize=True,
        #width=200,
        #height=200,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor="White",
    )
    
    
    figtbl = go.Figure(data=[go.Table(
        columnwidth = [50,20],
        header=dict(values=['Last Rental Start', 'Bike ID'],
                    fill_color='royalblue',
                    font=dict(color='white', size=12),
                    align='left'),
        cells=dict(values=[rentedtoday.LastRentalStart.dt.strftime('%Y-%m-%d %H:%M:%S'), rentedtoday.BikeID],
                   #fill_color='white',
                   align='left'))
    ])
    
    figtbl.update_layout(
        #autosize=True,
        #width=200,
        height=250,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor="White",
    )
    
       
    cardfigtbl = dbc.Toast(
                [
                    html.Tbody(
                        
                        html.Tr([
                            
                            html.Td(html.Img(src="/assets/bike1.png", height="60px"), style={'border': 'none'}),
                            html.Td(html.P(rentedtoday.BikeID.count(), className="mb-0"), style={'border': 'none', 'font-size':'30px'})],
                    
                    
                    ), style={'width':'100%', 'border': 'none'})
                    
                ],
                header="Total Rents",
                style={'font-size':'18px'},
            )
        
    
    
    """
    get_batterystatusbikes = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/get_batterystatusbikes.csv')
    get_batterystatusbikes['bikeid'] = get_batterystatusbikes.bikeid.astype(str)
    """
    
    get_batterystatusbikes_all = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/get_batterystatusbikes_all.csv')
    get_batterystatusbikes_all['bikeid'] = get_batterystatusbikes_all.bikeid.astype(str)
    get_batterystatusbikes_all['HarvestTime'] = pd.to_datetime(get_batterystatusbikes_all['HarvestTime'])
    get_batterystatusbikes_all.drop(columns=['Unnamed: 0'], inplace=True)
    get_batterystatusbikes_all.sort_values(by=['HarvestTime','bikeid'], ascending=False, inplace=True)
    
    cond = (get_batterystatusbikes_all.HarvestTime.dt.hour < smax) & (get_batterystatusbikes_all.HarvestTime.dt.date == now.date())
    
    hourly = get_batterystatusbikes_all.loc[cond]
    
    batteryday = hourly[['bikeid', 'HarvestTime']].groupby(by='bikeid').max()
    batteryday.reset_index(inplace=True)
    
    batteryday = get_batterystatusbikes_all.merge(batteryday)
    
    cond = batteryday.battery == 0 
    batteryday['battery2'] = batteryday.battery
    batteryday.loc[cond, 'battery2'] = -10
    batteryday.loc[~cond, 'battery2'] = batteryday.loc[~cond, 'battery2']+10
    
    #batteryday.sort_values(by=['battery'], inplace=True)
    
    batterydaytbl = batteryday.copy()
    batteryday.sort_values(by='battery2', inplace=True)
    batteryday['htstring'] = batteryday.HarvestTime.dt.strftime('%Y-%m-%d %H:%M:%S')
    
    fig_baterry = px.bar(batteryday, x="battery2", y="name", orientation='h', 
                         color='name',
                         hover_data={'battery2':False, # remove species from hover data
                                     'battery':True,
                                     'htstring':True,
                                     'bikeid':True},
                        labels={
                         "battery2": "",
                         "name": "Status",
                         "htstring": "Last Harvest Time",
                         "bikeid":"Bike ID",
                         "battery":"Battery Level"
                             },                               
                        )
    
    fig_baterry.update_layout(
        #autosize=True,
        #width=200,
        #height=200,
        xaxis=dict(
            showticklabels=False,
        ),
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor="White",
    )
    
    
    maxstatus = hourly[['bikeid', 'HarvestTime']].groupby(by='bikeid').max()
    maxstatus.reset_index(inplace=True)
    
    countstatustbl = get_batterystatusbikes_all.merge(maxstatus)
    
    countstatus = countstatustbl[['bikeid', 'name.1']].groupby(by='name.1').count()
    countstatus.reset_index(inplace=True)
    countstatus.columns=['name', 'total']
    
    
    get_cat_statusbikes = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/get_cat_statusbikes.csv')
    
    countstatus = get_cat_statusbikes.merge(countstatus, how='left')
    countstatus.fillna(0, inplace=True)
    countstatus.total = countstatus.total.astype(int)
    
    fig_status = px.bar(countstatus, x="name", y="total", orientation='v',
                        color='name',
                        labels={
                         "total": "Number of bikes",
                         "name": "Status",
                             })
    fig_status.update_layout(
        #autosize=True,
        #width=200,
        #height=200,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor="White",
    )
    
    
    figtblbat = go.Figure(data=[go.Table(
        columnwidth = [30,15,20,15],
        header=dict(values=['Last Time Harvested', 'Bike ID', 'Status',  'Battery'],
                    fill_color='royalblue',
                    font=dict(color='white', size=12),
                    align='left'),
        cells=dict(values=[batterydaytbl.HarvestTime.dt.strftime('%Y-%m-%d %H:%M:%S'),
                           batterydaytbl.bikeid,                        
                           batterydaytbl.name,
                           batterydaytbl.battery,
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
    
    
    
    figtblstat = go.Figure(data=[go.Table(
        columnwidth = [30,15,20,15],
        header=dict(values=['Last Time Harvested', 'Bike ID', 'Status'],
                    fill_color='royalblue',
                    font=dict(color='white', size=12),
                    align='left'),
        cells=dict(values=[countstatustbl.HarvestTime.dt.strftime('%Y-%m-%d %H:%M:%S'),
                           countstatustbl.bikeid,                        
                           countstatustbl['name.1'],                       
                           ],
                   #fill_color='white',
                   align='left'))
    ])
    
    figtblstat.update_layout(
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

    maxhour = now.hour
    
    dictlist = dict()
    sliders = [*range(0,maxhour+2)]
    
    for i in sliders:
        dictlist[i] = str(i)+":00"
        
    
    
        
    return [figtblstat, figtblbat, fig_status, fig_baterry, figtbl, fig, max(sliders), min(sliders), [smin, smax], dictlist, cardfigtbl]
    

