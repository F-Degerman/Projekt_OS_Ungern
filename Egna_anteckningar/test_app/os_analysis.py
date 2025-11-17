import pandas as pd

df = pd.read_csv("athlete_events.csv")

def medaljer_per_os(country="HUN"):
    dff = df[df["NOC"] == country]
    medals = dff[dff["Medal"].notna()]
    medal_counts = medals.groupby("Year")["Medal"].count().reset_index()
    return medal_counts  # DataFrame

def figur_medaljer_per_os(country="HUN"):
    import plotly.express as px
    medal_counts = medaljer_per_os(country)
    fig = px.bar(medal_counts, x="Year", y="Medal",
                 title=f"Antal medaljer per OS – {country}")
    return fig
