from dash import dcc, html

def set_layout():
    
    return html.Div([
        html.Div([
            html.Div([
                html.Img(src="assets/oslogo.png", className="logo")]), 
            html.Div([
                html.H1("Olympic Dashboard", className="title"), 
                dcc.Dropdown(
                    id="hungary-dropdown",
                    options=[{"label": "Hungary: number of participants per year", "value": "final_participants"}, 
                             {"label": "Hungary: medals won per sport", "value": "hun_most_medals"}, 
                             {"label": "Hungary: medals won per Olympics", "value": "hun_medals"}, 
                             {"label": "Hungary: medals won per Olympics (detailed)", "value": "hun_medals_d"}, 
                             {"label": "Hungary: medals per sport 1952", "value": "sport_medals_1952"}, 

                             {"label": "Gymnastics: gender comparison", "value": "gymnastics_gender"}, 
                             
                             {"label": "That's all, folks!", "value": "ending"}], 
                className="dropdown")]), 
            html.Div([
                html.Img(src="assets/hungaryflag.png", className="flag")]
        )], className="header"), 
        html.Div([
            html.H2("", className="question", id="question")]), 
        dcc.Graph(id="graph")])
