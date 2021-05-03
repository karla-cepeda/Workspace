import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import server
from app import app
from apps import home, map_bikes, dashboard, bikes

dash.Dash(__name__)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

FOOTER_STYLE = {
    "position": "fixed",
    "bottom": 0,
    "left": 0,
    "right": 0,
    "height": '3rem',
    "padding": "0.5rem 0.5rem",
    "background-color": "gray",
}

fdivs = [html.P('Data Visualization')]
footer = html.Footer(fdivs, style=FOOTER_STYLE)
navbar = dbc.Nav(
                [
                    dbc.NavLink(children=["Home"], href="/home",  active=True, id="homeid"),
                    dbc.NavLink("Dashboard", href="/dashboard",  active='exact'),
                    dbc.NavLink("Map", href="/map", active="exact"),
                    dbc.NavLink("Bikes", href="/bikes", active="exact"),
                ],
                vertical=True,
                pills=True,
            )
sidebar = html.Div(
                [
                    html.H2("Moby Bikes", className="display-4"),
                    html.Hr(),
                    navbar,
                ],
                style=SIDEBAR_STYLE,
            )
                
content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"), 
    sidebar, 
    content, 
    #footer, 
    #dcc.Interval(id="interval")
])


@app.callback([Output("page-content", "children"), 
               Output("homeid", "active")], [Input("url", "pathname")])
def render_page_content(pathname):
    pathname = pathname.lower()
    if pathname == "/dashboard":
        return [dashboard.layout, "exact"]
    elif pathname == "/map":
        return [map_bikes.layout, "exact"]
    elif pathname == "/bikes":
        return [bikes.layout, "exact"]
    else:
        return [home.layout, True]
        
    
"""
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
            html.Script('''
                        
                $(".summary").on("click", function() {
                  $(this).next().toggleClass("show");
                })
                
                '''
            )
        ]
    )

@app.callback(Output('graph', 'extendData'), [Input('interval', 'n_intervals')])
def update_data(n_intervals):
    index = n_intervals % resolution
    # tuple is (dict of new data, target trace index, number of points to keep)
    return dict(x=[[x[index]]], y=[[y[index]]]), [0], 10
"""

if __name__ == '__main__':
    app.run_server(port=8060, debug=True) #, dev_tools_ui=True, 
              #dev_tools_hot_reload =True, threaded=True)