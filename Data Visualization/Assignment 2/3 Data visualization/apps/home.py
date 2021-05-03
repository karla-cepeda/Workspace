import dash
import dash_html_components as html
import dash_bootstrap_components as dbc

from app import app

layout = html.Div([
    dbc.Container([
        html.Div([
            
            html.H1("Welcome to Moby Bikes!", className="text-center mb-5 mt-5"),
            html.H3("Final Data Visualisation Project", className="lead"),
            html.P("This APP shows real-time data extracted from the API from the business Moby Bikes, Dublin Ireland. This is a Data Visualization final project delivered on 1st May 2021.", className='lead'),
            dbc.Button("Get started!", color="success", href='/dashboard', className="mr-1"),
            
        ],className='jumbotron'),

    
    
        html.Div([
            
            html.P("The data consists of bike information regarding battery, location, status, and date of rent. MOBY is an innovative Irish start-up company focused on developing and bringing to market a range of electric mobility solutions for cities and individuals.")
            
            ], style={'text-align':'center'}),
    
        html.Div([
            
                 dbc.Row([
                     
                     dbc.Col([
                         
                         dbc.Card(
                             [
                         dbc.CardImg(src="../assets/moby.jpg", top=True),
                         dbc.CardBody(
            [
                
                     html.H4("Access to original dataset and\n\nAPI is available to the public."),
                     dbc.Button("MOBY bikes data", 
                                color="success", 
                                href="https://data.smartdublin.ie/dataset/moby-bikes", 
                                className="mr-1")
                     
                     ])
                         
                         ])
                     
                     ],),
                     
                 
                 dbc.Col([
                     
                     dbc.Card(
                             [
                         dbc.CardImg(src="../assets/github.png", top=True),
                         dbc.CardBody(
            [
                
                     html.H4("Access the code used\n\nto build this dashboard. If needed, request access to d00242569."),
                     dbc.Button("GitHub", 
                                color="success", 
                                href="https://github.com/karla-cepeda/Workspace/tree/master/Data%20Visualization/Assignment%202", 
                                className="mr-1"),
                     
                     ],),
                 
                     ])
                         
                         ])
                 
            
                ],),
        ]),
        
    ], className='container-narrow text-center'),
    
])
    
