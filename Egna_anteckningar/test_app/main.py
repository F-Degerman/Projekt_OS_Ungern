from dash import dcc, html
from dash.dependencies import Input, Output
import dash

from os_analysis import figur_gender_trend
from os_analysis import figur_age_hist   # kön-grafen

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Statistik: Ungerns deltagande i OS untifrån ett historiskt perspektiv"),

    html.P("Välj land:"),
    dcc.Dropdown(
        id="country-dropdown",
        options=[
            {"label": "Alla länder", "value": "ALL"},
            {"label": "Ungern",      "value": "HUN"},
            {"label": "Sverige",     "value": "SWE"},
        ],
        value="HUN"
    ),

    html.P("Välj område:"),
    dcc.Dropdown(
        id="metric-dropdown",
        options=[
            {"label": "Kön",        "value": "gender"},
            {"label": "Ålder",      "value": "age"},
            {"label": "Deltagande", "value": "participation"},
            {"label": "Medaljer",   "value": "medals"},
        ],
        value="gender"
    ),

    dcc.Graph(id="main-graph")
])

@app.callback(
    Output("main-graph", "figure"),
    Input("country-dropdown", "value"),
    Input("metric-dropdown", "value")
)
def uppdatera_figur(valt_land, vald_metric):
    if vald_metric == "gender":
        return figur_gender_trend(noc=valt_land, season="Summer")
    elif vald_metric == "age":
        return figur_age_hist(noc=valt_land, season="Summer")
    # osv...
    # fallback
    return figur_gender_trend(noc="HUN", season="Summer")

if __name__ == "__main__":
    app.run(debug=True)