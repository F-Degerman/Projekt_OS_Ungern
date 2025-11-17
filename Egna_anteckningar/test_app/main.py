from dash import dcc, html
from dash.dependencies import Input, Output
import dash
from os_analysis import figur_medaljer_per_os

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("OS-dashboard"),
    html.P("Välj land"),
    # TODO Göra om till sporter i dropdown. 
    dcc.Dropdown(
        id="land-dropdown",
        options=[{"label": "Ungern", "value": "HUN"},
                 {"label": "Sverige", "value": "SWE"}],
        value="HUN"
    ),
    dcc.Graph(id="medalj-graf")
])

@app.callback(
    Output("medalj-graf", "figure"),
    Input("land-dropdown", "value")
)
def uppdatera_medalj_graf(valt_land):
    fig = figur_medaljer_per_os(valt_land)
    return fig

if __name__ == "__main__":
    app.run(debug=True)
