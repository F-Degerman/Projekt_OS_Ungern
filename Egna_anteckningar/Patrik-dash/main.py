import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from pathlib import Path
import hashlib as hl
import numpy as np

# PATH
root_dir = Path(__file__).parent.parent.parent
path = root_dir/"athlete_events.csv"

# ORIGINAL DATA (ANONYMIZED)
df = pd.read_csv(path)
hun_df = df[df["NOC"] == "HUN"].copy().reset_index().sort_values(by="Year")
hash_df = hun_df["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())
hun_df["Name"] = hash_df
chosen_sports = ["Weightlifting", "Gymnastics", "Fencing", "Figure Skating"]

# GRAPH DATA
## Welcoming graph: copied from Copilot after prompting a px.scatter() with data points in the shape of a smiley
theta = np.linspace(0, 2*np.pi, 100)
head_x = np.cos(theta)
head_y = np.sin(theta)

eye_left_x = [-0.3]
eye_left_y = [0.4]
eye_right_x = [0.3]
eye_right_y = [0.4]

mouth_theta = np.linspace(np.pi/6, 5*np.pi/6, 50)
mouth_x = 0.6 * np.cos(mouth_theta)
mouth_y = -0.6 * np.sin(mouth_theta) + 0.2

smiley_df = pd.DataFrame({
    "x": list(head_x) + eye_left_x + eye_right_x + list(mouth_x),
    "y": list(head_y) + eye_left_y + eye_right_y + list(mouth_y),
    "part": (["head"]*len(head_x) +
             ["eye_left"]*len(eye_left_x) +
             ["eye_right"]*len(eye_right_x) +
             ["mouth"]*len(mouth_x))
})

## Hungary: medals won per sport
most_medals = pd.DataFrame(hun_df.groupby("Sport")["Medal"].value_counts().unstack(fill_value=0).sum(axis=1)).rename(columns={0:"Medals"}).sort_values("Medals", ascending=False)

## Hungary: medals won per Olympics
total_medals = hun_df[["Year", "Season", "Event", "Medal"]].dropna().drop_duplicates(subset=["Year", "Event", "Medal"])
total_medals["ExtraSeason"] = total_medals.apply(lambda row: "Intercalated Games" if row["Year"] == 1906 else ("Winter" if row["Season"] == "Winter" else "Summer"), axis=1)
unique_medals = total_medals.groupby(["Year", "ExtraSeason"])["Medal"].value_counts().unstack().sum(axis=1)
unique_medals_df = unique_medals.reset_index().rename(columns={0: "Medals"})

## Hungary: medals won per Olympics (detailed)
total_medals = hun_df[["Year", "Season", "Event", "Medal"]].fillna({"Medal": "0"}).dropna(subset=["Year", "Event", "Medal"]).drop_duplicates(subset=["Year", "Event", "Medal"])
total_medals["ExtraSeason"] = total_medals.apply(lambda row: "Intercalated Games" if row["Year"] == 1906 else ("Winter" if row["Season"] == "Winter" else "Summer"), axis=1)
unique_medals = total_medals.groupby(["Year", "ExtraSeason"])["Medal"].value_counts().unstack().reset_index()
melted = unique_medals.melt(id_vars=["Year", "ExtraSeason"], value_vars=["Bronze", "Silver", "Gold"], var_name="MedalType", value_name="Count")
melted["YearSeason"] = melted["ExtraSeason"] + " " + melted["Year"].astype(str)

## Hungary: number of events participated in per year
new_df = df[["Name", "Event", "NOC", "Year", "Season"]]
hun_df = new_df[new_df["NOC"] == "HUN"].dropna().drop_duplicates(subset=["Event", "Year"])
grouped_df = pd.DataFrame(hun_df.groupby(["Year", "Season"])["Event"].value_counts().unstack().sum(axis=1)).rename(columns={0:"Events"}).reset_index()

# Zero participants during outlier years
no_events = pd.DataFrame([{"Year": 1916, "Season": "Summer", "Events": 0}, # WW1
                          {"Year": 1920, "Season": "Summer", "Events": 0}, # Banned (WW1)
                          {"Year": 1940, "Season": "Summer", "Events": 0}, # WW2
                          {"Year": 1940, "Season": "Winter", "Events": 0}, # WW2
                          {"Year": 1944, "Season": "Summer", "Events": 0}, # WW2
                          {"Year": 1944, "Season": "Winter", "Events": 0}, # WW2
                          {"Year": 1984, "Season": "Summer", "Events": 0}  # Boycott against the US
                          ])
olympic_events = pd.concat([grouped_df, no_events], ignore_index=True).sort_values(by="Year").reset_index().drop("index", axis=1)

## Hungary: age distribution amongst athletes (1896-2016)
# Only using original data variable: hun_df

## Overall: medal distribution between countries in chosen sports
medal_dist_df = df[["Sport", "Medal", "NOC", "Year", "Event"]].dropna().drop_duplicates(subset=["Year", "Event", "Medal"])
sports_df = medal_dist_df[medal_dist_df["Sport"].isin(chosen_sports)]
medals_df = pd.DataFrame(sports_df.groupby(["NOC", "Sport"])["Medal"].value_counts().unstack().sum(axis=1).astype(int)).reset_index().rename(columns={0:"Medals"})

## Overall: comparison of age distribution in chosen sports
age_dist_df = df[["ID", "Age", "Sport", "NOC", "Year"]].drop_duplicates(subset=["ID", "Age"])
sports_df2 = age_dist_df[age_dist_df["Sport"].isin(chosen_sports)]

# RENDER
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server

# LAYOUT
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src="assets/oslogo.png", className="logo")], 
        className="left-col"), 
        html.Div([
            html.H1("Olympic Dashboard", className="title"), 
            dcc.Dropdown(
                id="hungary-dropdown",
                options=[{"label": "Hungary: medals won per sport", "value": "most_medals"}, 
                        {"label": "Hungary: medals won per Olympics", "value": "olympic_medals"}, 
                        {"label": "Hungary: medals won per Olympics (detailed)", "value": "olympic_medals_d"}, 
                        {"label": "Hungary: number of events participated in per year", "value": "olympic_events"}, 
                        {"label": "Hungary: age distribution of all athletes across time", "value": "hun_age"}, 
                        {"label": "Overall: medal distribution across countries in the chosen sports", "value": "all_medals"}, 
                        {"label": "Overall: age distribution comparison between the chosen sports", "value": "all_age"}], 
                value="", className="dropdown")], 
        className="mid-col"), 
        html.Div([
            html.Img(src="assets/hungaryflag.png", className="flag")], 
        className="right-col")], 
    className="header"), 
    html.Div([
        html.H2("", className="question", id="question")], 
    className="mid-col"), 
    dcc.Graph(id="graph")])

# CALLBACK
@app.callback(
    Output("graph", "figure"), 
    Output("question", "children"), 
    Input("hungary-dropdown", "value")
)
def update_graph(selected_value):
    ## Welcoming smiley
    if selected_value in [None, ""]:
        question="Please choose a topic from the dropdown menu!"
        fig = px.scatter(smiley_df, x="x", y="y", color="part", color_discrete_sequence=["darkgreen"])
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1), showlegend=False, height=650, paper_bgcolor="#f9f9f9")
        fig.for_each_trace(lambda trace: trace.update(marker=dict(size=40)) if trace.name in ["eye_left", "eye_right"] else ())
        fig.for_each_trace(lambda trace: trace.update(marker=dict(size=15)) if trace.name in ["head", "mouth"] else ())
        return fig, question
    
    ## Hungary: medals won per sport
    elif selected_value == "most_medals":
        question = "In which sports has Hungary earned the most medals?"
        fig = px.bar(
            data_frame=most_medals,
            x=most_medals.index, 
            y="Medals", 
            title="Hungary: medals won per sport", 
            subtitle="1896-2016", 
            color=most_medals.index, 
            text_auto=True)
        fig.update_layout(height=650, paper_bgcolor="#f9f9f9")
        return fig, question
    
    ## Hungary: medals won per Olympics
    elif selected_value == "olympic_medals":
        question = "How many medals has Hungary won at each Olympics and why are medal counts for some years missing?"
        fig = px.bar(
            data_frame=unique_medals_df,
            x="Year", 
            y="Medals", 
            title="Hungary: medals won per Olympics", 
            subtitle="Team medals counts as one medal", 
            color="ExtraSeason", 
            barmode="group", 
            color_discrete_map={"Summer": "orange", "Winter": "blue", "Intercalated Games": "red"})
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=1.15, xanchor="right", x=1), 
                          legend_title_text="", bargap=0.02, height=650, paper_bgcolor="#f9f9f9")
        fig.update_xaxes(dtick=4, ticklabelposition="outside left", tickangle=-45)
        return fig, question
    
    ## Hungary: medals won per Olympics (detailed)
    elif selected_value == "olympic_medals_d":
        question = "What year did Hungary win the most (gold) medals?"
        fig = px.bar(
            data_frame=melted,
            x="YearSeason", 
            y="Count", 
            title="Hungary: medals won per Olympics (detailed)", 
            subtitle="Team medals counts as one medal", 
            color="MedalType", 
            barmode="stack", 
            color_discrete_map={"Gold": "orange", "Silver": "grey", "Bronze": "sienna"}, 
            labels={"Count": "Medals", "YearSeason": "Olympics"}, 
            text_auto=True)
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=1.15, xanchor="right", x=1, traceorder="reversed"), 
                          legend_title_text="Medal:", bargap=0.02, height=650, paper_bgcolor="#f9f9f9")
        fig.update_xaxes(ticklabelposition="outside left", tickangle=-45)
        fig.update_traces(textangle=0)
        return fig, question
    
    ## Hungary: number of events participated in per year
    elif selected_value == "olympic_events":
        question = "How many events did Hungary participate in from year to year?"
        fig = px.line(
            olympic_events, 
            x="Year", 
            y="Events", 
            title="Hungary: number of events participated in per year", 
            subtitle="Years: 1896-2016", 
            range_x=[1892, 2020], 
            range_y=[0, grouped_df["Events"].max()+15], 
            line_shape="spline", 
            color="Season", 
            color_discrete_map={"Summer": "orange", "Winter": "blue"})
        fig.update_xaxes(dtick=2, ticklabelposition="outside left", tickangle=-45)
        return fig, question

    ## Hungary: age distribution amongst athletes (1896-2016)
    elif selected_value == "hun_age":
        question = "What is the age span and distribution of all Hungarian athletes across these 120 years?"
        fig = px.histogram(
            hun_df, 
            x="Age", 
            nbins=50, 
            color_discrete_sequence=["green"], 
            title="Hungary: age distribution of all athletes across time", 
            subtitle="1896-2016", 
            text_auto=True)
        fig.update_xaxes(range=[10,60], dtick=2)
        fig.update_yaxes(title_text="Number of Athletes", range=[0,550])
        fig.update_traces(marker_line_color="white", marker_line_width=1)
        fig.update_layout(height=650, paper_bgcolor="#f9f9f9")
        return fig, question
    
    ## Overall: medal distribution between countries in chosen sports
    elif selected_value == "all_medals":
        question = "How does the medal distribution look between countries in our chosen sports?"
        fig = px.bar(
            medals_df, 
            x="NOC", 
            y="Medals", 
            color="NOC", 
            title="Overall: medal distribution across countries in the chosen sports", 
            subtitle="1896-2016", 
            facet_col="Sport", 
            facet_col_wrap=2, 
            labels={"NOC":"Country", "y": "Medals"})
        fig.update_xaxes(ticklabelposition="outside left", tickangle=-45, dtick=1, tickfont=dict(size=10))
        fig.update_layout(showlegend=False, height=650, paper_bgcolor="#f9f9f9")
        fig.for_each_annotation(lambda title: title.update(text=f"<b>{title.text.split("=")[-1].upper()}</b>"))
        return fig, question

    ## Overall: comparison of age distribution in chosen sports
    elif selected_value == "all_age":
        question = "How does the age distribution look in our chosen sports?"
        fig = px.histogram(
            sports_df2, 
            x="Age", 
            facet_col="Sport", 
            facet_col_wrap=2, 
            nbins=55, 
            color_discrete_sequence=["darkgreen"],
            opacity=0.9, 
            text_auto=True, 
            title="Overall: age distribution comparison between the chosen sports")
        
        fig.update_xaxes(range=[10,sports_df2["Age"].max()], dtick=2)
        fig.update_yaxes(title_text="Number of Athletes", range=[0,420])
        fig.update_traces(marker_line_color="white", marker_line_width=1)
        fig.update_layout(height=650, paper_bgcolor="#f9f9f9")
        fig.for_each_annotation(lambda title: title.update(text=f"<b>{title.text.split("=")[-1].upper()}</b>"))
        return fig, question

if __name__ == "__main__":
    app.run(debug=True)
