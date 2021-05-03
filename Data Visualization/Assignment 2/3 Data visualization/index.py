import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import server
from app import app
from apps import home, map_bikes, dashboard, bikes, rentals

dash.Dash(__name__)

# Style for master page (layout of multipage app)
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


# Menu for access to different pages.
navbar = dbc.Nav(
                [
                    dbc.NavLink(children=["Home"], href="/home",  active='exact', id="homeid", className='success'),
                    dbc.NavLink("Dashboard", href="/dashboard",  active='exact', className='success'),
                    dbc.NavLink("Map", href="/map", active="exact", className='success'),
                    dbc.NavLink("Bikes", href="/bikes", active="exact", className='success'),
                    dbc.NavLink("Rentals", href="/rentals", active="exact", className='success'),
                ],
                vertical=True,
                pills=True,
            )

policyp = html.Div([
                html.A(children=["Privacy Policy"],href='http://datavis.tanniestudio.com/policyprivacy.html', target="_blank", style={'color':'gray', 'font-size':'10px', 'margin-bottom':'5px'})
            ], style={'position': 'absolute', 'bottom': 0, 'width': '100%', 'height': '2.5rem'})

# Structure where the nav bar will be located.
sidebar = html.Div(
                [
                    html.H2("Moby Bikes", className="display-4"),
                    html.Hr(),
                    navbar,
                    policyp
                ],
                style=SIDEBAR_STYLE,
            )

# Content where other pages would be drawn.
content = html.Div(id="page-content", style=CONTENT_STYLE)

# Index layout
app.layout = html.Div([
    dcc.Location(id="url"), 
    sidebar, 
    content, 
])

@app.callback([
    Output("page-content", "children"), Output("homeid", "active"),
    ], 
    [Input("url", "pathname"),])
def render_page_content(pathname):
    pathname = pathname.lower()
    if pathname == "/dashboard":
        return [dashboard.layout, "exact"]
    elif pathname == "/map":
        return [map_bikes.layout, "exact"]
    elif pathname == "/bikes":
        return [bikes.layout, "exact"]
    elif pathname == "/rentals":
        return [rentals.layout, "exact"]
    else:
        return [home.layout, True]


if __name__ == '__main__':
    #app.run_server(port=8060, debug=True)
    app.run_server(debug=False)
