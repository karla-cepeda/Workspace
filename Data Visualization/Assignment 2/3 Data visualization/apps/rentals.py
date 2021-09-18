
import mysql.connector
import sqlalchemy

import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from datetime import datetime, date

import plotly.express as px
import plotly.graph_objects as go


import pandas as pd

from app import app

# Credentials to connect to database for historical data
#   data from files are just for real-time information for easy upgrading when refreshing page
config = {
     'user': '', # Change
     'password': '', # Change
     'host': '', # Change
     'database': '', # Change
   }

engine = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                  format(config['user'], config['password'], 
                                         config['host'], config['database']))

def call_sp(storedp, args):
    # Connect to database to get data
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

# global variables
now = datetime.now()
maxhour = now.hour
dictlist = dict()
sliders = [*range(0,maxhour+2)]

# create marks for slider
for i in sliders:
    dictlist[i] = str(i)+":00"

slidertool = html.Div(
    
                [dcc.RangeSlider(
                    id='rsliderid',
                    min=min(sliders),
                    max=max(sliders),
                    value=[min(sliders), max(sliders)],
                    marks=dictlist,
                    allowCross=False,
                    
                )])

layout = html.Div(children=[
    dbc.Row([
        html.Div(
            html.Button(id='openid',
                        children=[html.Img(src='assets/info-circle-fill.svg', style={'width':'30px'} )],
                        className='position-fixed', style={'right':'10px', 'top':'0', 'z-index':'1000000', 'border': 'none', 'width': 'auto', 'margin': '0', 'padding': '0'}),
            ),
        dbc.Tooltip("Filter your data! Rented bikes are filtered by range, while Status and Battery plots just display the last time data was harvested.",
                    target="openid",
                    style={'font-size':'12px'}),
        dbc.Col(html.H1(["Real-Time Rentals"], 
                        style={'textAlign': 'center', 'color': 'black', 'margin-bottom': '8px !important', 'padding':'0'}, 
                        className='col-md-auto pl-1 display-4 mb-5 mt-5'), md=4), 
        ], justify="center", className="align-items-center"),
    dbc.Row([
        dbc.Col([html.H4([dbc.Badge("LIVE", id='liveid2', color="danger", className="mr-1"),], style={'padding':'0','padding-top':'30px', 'display':'inline'}),
                 dcc.DatePickerSingle(id='my-date-picker-single',
                                      min_date_allowed=date(2020, 9, 24),
                                      max_date_allowed=now.date(),
                                      initial_visible_month=now.date(),
                                      date=now.date(),
                                      display_format='DD/MM/YYYY',
                                      style={'display':'inline'})
                 ], className = 'col-md-auto p-0'),
        ], justify="center"),
    dbc.Row([
        html.P("Filter by hour:"),
        dbc.Col(slidertool, style={'padding-top':'10px'})
        ], style={'margin-top':'10px', 'padding-left':'30px'}),
    dbc.Row([
        dbc.Col([html.H4("Number of rentals per Bike", style={'margin-bottom': '11px','padding-top': '41px','padding-left': '43px', 'display':'in-line'}),],md=12), 
        ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                dcc.Graph(id='figid',),
                ],),md=8
            ),
        dbc.Col(
            html.Div([
                dcc.Graph(id='figtblid',),
                html.Div(id='Totalfigid', style={'padding-top':'20px'}),
                ]), md=4),                    
        ]),
    dbc.Row([
        dbc.Col([
            html.H4("Rented Bikes", style={'margin-bottom': '11px','padding-top': '41px','padding-left': '43px', 'display':'in-line'}),
            html.Div([
                dcc.RadioItems(id="radioitemid",
                               options=[
                                    {'label': 'Every 5 minuts', 'value': '5T'},
                                    {'label': 'Hourly', 'value': 'H'},
                                ],
                               value='H',
                               labelStyle={'display': 'inline-block', 'margin-left':'10px', 'margin-right':'5px'}),
                dbc.Checklist(options=[{"label": "Cumulative", "value": 1},],
                              value=[],
                              id="switch-input",
                              switch=True,), 
                ], style={'padding-left': '43px'})],md=12), 
        ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                dcc.Graph(id='figcummulatives',
                          #config={'displayModeBar': False}
                          ),
                ],),md=12
            ),
        ]),
    dcc.Interval(id="interval2", interval=100000),
    ], 
)


@app.callback(
    [Output(component_id='figid', component_property='figure'),
     Output(component_id='figtblid', component_property='figure'),
     Output(component_id='Totalfigid', component_property='children'),
     Output(component_id='figcummulatives', component_property='figure'),
     Output('rsliderid', 'max'),
     Output('rsliderid', 'min'),
     Output('rsliderid', 'marks'),
     Output(component_id='liveid2', component_property='color'),
     Output(component_id='interval2', component_property='max_intervals'),
     ],
    
    [Input(component_id='rsliderid', component_property='value'),
     Input(component_id='interval2', component_property='n_intervals'),
     Input('my-date-picker-single', 'date'),
     Input('radioitemid', 'value'),
     Input("switch-input", 'value')]
    
)
def update_graphs(valueslder, n_intervals, date, radioitem, checklist_value):
    
    # global variables for method
    bgcolor = "secondary"
    now = datetime.now()    
    smin = valueslder[0]
    smax = valueslder[1]
    max_intervals=0
    dictlist = dict()
    sliders = None
    
    # If it is same date
    if now.date().strftime('%Y-%m-%d') == date:
        
        maxhour = now.hour
        if smax > maxhour+1:
            smax = maxhour+1
            
        # if it has a different hour greather than curr hour
        if now.hour+1 == smax:            
            bgcolor = "danger"
            max_intervals=-1
            
        # new range of time
        sliders = [*range(0,maxhour+2)]
        for i in sliders:
            dictlist[i] = str(i)+":00"
        
    else:
        # set new range of time
        sliders = [*range(0,24)]
        for i in sliders:
            dictlist[i] = str(i)+":00"
        
    if now.date().strftime('%Y-%m-%d') == date:
        # looking for current data, go into FTP and read csv
        BikesRented = pd.read_csv(r'https://mydata.tanniestudio.com/datasets/BikesRented.csv')
    else:
        # Looking for historical data, connect to db
        date2 = pd.to_datetime(date,format='%Y-%m-%d')
        BikesRented = call_sp('BikesRented', (date2.strftime('%d/%m/%Y'),))
        BikesRented.columns = ['LastRentalStart', 'BikeID']

    BikesRented.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')
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
    countbikes.sort_values(by=['Total','BikeID'], inplace=True, ascending=False)
    
    my_color = ['rgb(237, 102, 93)']
    
    # plot bar plot to show number of times a bike has been rented.    
    fig = px.bar(countbikes, y='Total', x='BikeID',
                 text='Total', 
                 color_discrete_sequence=my_color, 
                 hover_data=['BikeID', 'ltrstring'],
                 labels={'Total':'Number of times rented','BikeID':'Bike Identifier','ltrstring':'Last Time Rented'})
    fig.update_xaxes(type="category", range=[-1, 19])
    fig.update_yaxes(range=[0,countbikes.Total.max()+1])
    fig.update_traces(texttemplate='', textposition='outside')    
    fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0
        ),
        paper_bgcolor="White",
    )
    
    # Plot table to see data
    figtbl = go.Figure(data=[go.Table(
        columnwidth = [50,20],
        header=dict(values=['Last Rental Start', 'Bike ID'],
                    fill_color='royalblue',
                    font=dict(color='white', size=12),
                    align='left'),
        cells=dict(values=[rentedtoday.LastRentalStart.dt.strftime('%Y-%m-%d %H:%M:%S'), rentedtoday.BikeID],
                   align='left'))
    ])
    figtbl.update_layout(
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

    # Show total of times bikes were rented
    cardfigtbl = dbc.Toast([
        html.Tbody(
            html.Tr([
                html.Td(html.Img(src="/assets/bike1.png", height="60px"), style={'border': 'none'}),
                html.Td(html.P(rentedtoday.BikeID.count(), className="mb-0"), style={'border': 'none', 'font-size':'30px'})],
            ), style={'width':'100%', 'border': 'none'})
        ], header="Total Rents", style={'font-size':'18px'},)
    
    
    # Prepare data for cummulative plot
    rentedtoday['rentals'] = 1
    
    if radioitem is None:
        radioitem = '5T'

    df_ = rentedtoday.set_index('LastRentalStart')[['rentals']].resample(radioitem).sum().reset_index()
    
    if len(checklist_value) == 1:
        col1 = 'cumul'
        df_[col1] = df_.rentals.cumsum()
    else:
        col1 = 'rentals'
    
    rc_fig = px.line(df_, 
                     x='LastRentalStart', 
                     y=col1,
                     labels={"rentals": "Bikes rented",
                             "LastRentalStart": "Last Rental Start",}, 
                     #config={'displayModeBar': True}
                     )    
    #rc_fig.update_xaxes(type="date", range=[BikesRented.LastRentalStart.min(), BikesRented.LastRentalStart.max()])
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
    
    return [fig, figtbl, cardfigtbl, rc_fig,  max(sliders), min(sliders), dictlist, bgcolor, max_intervals]
    

