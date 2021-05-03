import mysql.connector
import sqlalchemy

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from datetime import datetime, date, timedelta

import plotly.express as px
import plotly.graph_objects as go


import pandas as pd
import numpy as np

from app import app


config = {
     'user': 'tanniest_mybikes',
     'password': 'WNZvC=M^u.pQ',
     'host': 'mx74.hostgator.mx',
     'database': 'tanniest_mybikes',
   }

engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                  format(config['user'], config['password'], 
                                         config['host'], config['database']))


def call_sp(storedp, args):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    
    cursor.callproc(storedp, args)
    
    info_db = None
    desc = None
    
    for result in cursor.stored_results():
        desc = result.description
        info_db = result.fetchall()
        
    cursor.close()
    cnx.close()
    
    cols = list()
    for i in desc:
        cols.append(i[0])
    
    return pd.DataFrame(info_db, columns=cols)


now = datetime.now()

maxhour = now.hour

dictlist = dict()
sliders = [*range(0,maxhour+2)]

for i in sliders:
    dictlist[i] = str(i)+":00"


slidertool = dcc.Slider(
                    id='sliderid',
                    min=min(sliders),
                    max=max(sliders),
                    value=max(sliders),
                    step=1,
                    marks=dictlist,
                    included=False
                )  

layout = html.Div(children=[   
        
        
    
        dbc.Row([
                #Header span the whole row
                #className: Often used with CSS to style elements with common properties.
                
                html.Div(
                    
                html.Button(id='openid',
                        children=[html.Img(src='assets/info-circle-fill.svg', style={'width':'30px'} )],
                        className='position-fixed', style={'right':'10px', 'top':'0', 'z-index':'1000000', 'border': 'none', 'width': 'auto', 'margin': '0', 'padding': '0'}
                        ),
                
                ),
            
                dbc.Tooltip(
                    "Filter your data! If you want to see previous status of bikes, select the hour you want to look into."
                    "Additionally, you can see previous days, fantastic!",
                    target="openid",
                    style={'font-size':'12px'}
                ),
                
                
                
                dbc.Col(html.H1(["Real-Time Bikes"], style={'textAlign': 'center', 'color': 'black', 'margin-bottom': '0px', 'padding':'0'}, className='col-md-auto pl-1 display-4 mb-5 mt-5'), md=4), 
                
                
                                
            ],
            justify="center", className="align-items-center"),
        
        dbc.Row([
            
                dbc.Col([html.H4([dbc.Badge("LIVE", id='liveid', color="danger", className="mr-1"), 
                                 
                                ], style={'padding':'0','padding-top':'30px', 'display':'inline'}),
                        
                        dcc.DatePickerSingle(
                                           id='my-date-picker-single',
                                           min_date_allowed=date(2020, 9, 24),
                                           max_date_allowed=now.date(),
                                           initial_visible_month=now.date(),
                                           date=now.date(),
                                           display_format='DD/MM/YYYY',
                                           style={'display':'inline'}
                                       )
                        
                        ], className = 'col-md-auto p-0'),
                
            
            ],
            justify="center", className="align-items-center"),
    
         dbc.Row([
                #Header span the whole row
                #className: Often used with CSS to style elements with common properties.
                html.P("Filter by hour:"),
                dbc.Col(slidertool, style={'padding-top':'10px'})
                ], style={'margin-top':'10px', 'padding-left':'30px'}),
        
    
        dbc.Row([
                dbc.Col([
                        html.H4("Battery Level per Bike", style={'margin-bottom': '11px','padding-top': '41px','padding-left': '43px', 'display':'in-line'}),
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
                        html.H4("Bike per status", style={'margin-bottom': '11px','padding-top': '41px','padding-left': '43px', 'display':'in-line'}),
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
                        
            
            dcc.Interval(id="interval", interval=100000),
            
            
    ], )



@app.callback(
    [Output(component_id='figtblstatid', component_property='figure'),
     Output(component_id='figtblbatid', component_property='figure'),
     Output(component_id='fig_statusid', component_property='figure'),
     Output(component_id='fig_baterryid', component_property='figure'),
     Output('sliderid', 'max'),
     Output('sliderid', 'min'),
     Output('sliderid', 'marks'),
     Output(component_id='liveid', component_property='color'),
     Output(component_id='interval', component_property='max_intervals'),
     ],
    
    [Input(component_id='sliderid', component_property='value'),
     Input(component_id='interval', component_property='n_intervals'),
     Input(component_id='my-date-picker-single', component_property='date')]
    
)
def update_graphs(valueslder, n_intervals, date):

    bgcolor = "secondary"
    
    now = datetime.now()    
    smax = valueslder
    max_intervals=0
    
    dictlist = None
    sliders = None
    
    if now.date().strftime('%Y-%m-%d') == date:
        
        maxhour = now.hour
        
        if smax > maxhour:
            smax = maxhour
            
        if now.hour == smax:            
            bgcolor = "danger"
            max_intervals=-1
    
        dictlist = dict()
        sliders = [*range(0,maxhour+1)]
        
        for i in sliders:
            dictlist[i] = str(i)+":00"
        
        
        
    else:
        dictlist = dict()
        sliders = [*range(0,24)]
        
        for i in sliders:
            dictlist[i] = str(i)+":00"
        
        
    if now.date().strftime('%Y-%m-%d') == date:
        get_batterystatusbikes_all = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/get_batterystatusbikes_all.csv')
    else:
        date2 = pd.to_datetime(date,format='%Y-%m-%d')
        get_batterystatusbikes_all = call_sp('get_batterystatusbikes_all', (date2.strftime('%d/%m/%Y'),))
        get_batterystatusbikes_all.columns = ['bikeid', 'HarvestTime', 'id', 'name', 'max', 'min','bikeid.1', 'battery', 'ebikestateid', 'name.1']

    get_batterystatusbikes_all['bikeid'] = get_batterystatusbikes_all.bikeid.astype(str)
    get_batterystatusbikes_all['HarvestTime'] = pd.to_datetime(get_batterystatusbikes_all['HarvestTime'])
    get_batterystatusbikes_all.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')
    get_batterystatusbikes_all.sort_values(by=['HarvestTime','bikeid'], ascending=False, inplace=True)
    
    cond = (get_batterystatusbikes_all.HarvestTime.dt.hour <= smax) #& (get_batterystatusbikes_all.HarvestTime.dt.date == now.date())
    
    hourly = get_batterystatusbikes_all.loc[cond]
    
    batteryday = hourly[['bikeid', 'HarvestTime']].groupby(by='bikeid').max()
    batteryday.reset_index(inplace=True)
    
    batteryday = get_batterystatusbikes_all.merge(batteryday)
    
    cond = batteryday.battery == 0 
    batteryday['battery2'] = batteryday.battery
    batteryday.loc[cond, 'battery2'] = -10
    batteryday.loc[~cond, 'battery2'] = batteryday.loc[~cond, 'battery2']+10
        
    batterydaytbl = batteryday.copy()
    batteryday.sort_values(by='battery2', inplace=True)
    batteryday['htstring'] = batteryday.HarvestTime.dt.strftime('%Y-%m-%d %H:%M:%S')
    batteryday.rename(columns={'name':'batteryname'}, inplace=True, errors='ignore')
    
    fig_baterry = px.bar(batteryday, x="battery2", y="batteryname", orientation='h', 
                         color='batteryname',
                         hover_data={'battery2':False, # remove species from hover data
                                     'battery':True,
                                     'htstring':True,
                                     'bikeid':True},
                        labels={
                         "battery2": "",
                         "batteryname": "Status",
                         "htstring": "Last Harvest Time",
                         "bikeid":"Bike ID",
                         "battery":"Battery Level"
                             },                               
                        )
    
    fig_baterry.update_layout(
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
                   align='left'))
    ])
    
    figtblbat.update_layout(
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
                   align='left'))
    ])
    
    figtblstat.update_layout(
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

    
        
    return [figtblstat, figtblbat, fig_status, fig_baterry, max(sliders), min(sliders), dictlist, bgcolor, max_intervals]
    

