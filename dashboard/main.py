import dash
import dash_bootstrap_components as dbc
from layout import set_layout
from callbacks import register_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO], title="Hungarian Olympics")
app.layout = set_layout()
server = app.server

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
