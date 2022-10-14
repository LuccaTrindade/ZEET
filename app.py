import dash
import dash_bootstrap_components as dbc
from login import app as server

app = dash.Dash(
    __name__, 
    suppress_callback_exceptions=True, 
    server=server, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    url_base_pathname='/home/'
)

server = app.server