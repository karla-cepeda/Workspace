
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app

policyp = html.Iframe(src='http://datavis.tanniestudio.com/policyprivacy.html',height=600,width="100%", style={'border':"none"})

layout = html.Div(children=[policyp])