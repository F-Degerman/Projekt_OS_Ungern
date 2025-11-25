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
                    options=[{"label": "1. Hungary: number of participants per year", "value": "final_participants"}, 
                             {"label": "2. Hungary: medals won per Olympics", "value": "hun_medals"}, 
                             {"label": "3. Hungary: medals won per Olympics (detailed)", "value": "hun_medals_d"}, 
                             {"label": "4. Hungary: medals per sport 1952 vs all years", "value": "sport_medals"}, 
                             {"label": "5. Overall: medal comparison of Eastern European nations 1952", "value": "comp_een"}, 
                             {"label": "6. Overall: correlation between medals and participants", "value": "nation_year"}, 
                             {"label": "7. Hungary: medals grouped by sport and gender 1952", "value": "medals_sport_gender"}, 
                             {"label": "8. Overall: gender comparison in gymnastics", "value": "gymnastics_gender"}, 
                             {"label": "9. Hungary: medal distribution across time based on gender", "value": "medal_dist_gender"}, 
                             {"label": "That's all, folks!", "value": "ending"}], 
                className="dropdown")]), 
            html.Div([
                html.Img(src="assets/hungaryflag.png", className="flag")]
        )], className="header"), 
        html.Div([
            html.H2("", className="question", id="question")]), 
        dcc.Graph(id="graph")])
