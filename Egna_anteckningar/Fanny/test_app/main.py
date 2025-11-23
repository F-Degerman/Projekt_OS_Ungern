from dash import dcc, html
import dash

from os_analysis import figur_gender_trend, get_shared_gender_axis_ranges

app = dash.Dash(__name__)

# Beräkna gemensamma axelgränser en gång
x_range, y_range = get_shared_gender_axis_ranges()

app.layout = html.Div([
    html.H1("Deltagande i OS utifrån kön – Ungern vs Sverige"),

    html.Div([
        dcc.Graph(
            id="hun-gender-graph",
            figure=figur_gender_trend(noc="HUN", x_range=x_range, y_range=y_range)
        ),
        dcc.Graph(
            id="swe-gender-graph",
            figure=figur_gender_trend(noc="SWE", x_range=x_range, y_range=y_range)
        ),
    ], style={"display": "flex", "gap": "20px"})
])

if __name__ == "__main__":
    app.run(debug=True)
