import pandas as pd
import plotly.express as px


# Ladda in data
athletes = pd.read_csv("athlete_events.csv")
noc = pd.read_csv("noc_regions.csv")

# Slå ihop dataset för att få regionnamn
data = pd.merge(athletes, noc, on="NOC", how="left")

# Sorterar alla unika deltagare
all_unique = data.drop_duplicates(subset=["ID", "Year", "Event"])

# Ungern & Sverige
hungary_unique = (
    data[data["NOC"] == "HUN"]
    .drop_duplicates(subset=["ID", "Year", "Event"])
)

sweden_unique = (
    data[data["NOC"] == "SWE"]
    .drop_duplicates(subset=["ID", "Year", "Event"])
)

# Kön per år (sommar OS)

def figur_gender_trend(noc="HUN", season="Summer"):
    """
    Skapar en plotly-figur som visar antal unika deltagare per år
    i OS för valt land (NOC) och säsong (Summer/Winter), uppdelat på kön.
    """
    dff = all_unique[(all_unique["NOC"] == noc) & (all_unique["Season"] == season)]

    yearly_gender = (
        dff.groupby(["Year", "Sex"])["ID"]
        .nunique()
        .reset_index()
        .rename(columns={"ID": "Antal_deltagare"})
    )

    titel = f"Antal deltagare ({season}-OS) ({noc}) per år och kön"

    fig = px.line(
        yearly_gender,
        x="Year",
        y="Antal_deltagare",
        color="Sex",
        markers=True,
        title=titel
    )

    fig.update_layout(
        xaxis_title="År",
        yaxis_title="Antal deltagare",
        legend_title_text="Kön"
    )
    return fig



def figur_age_hist(noc="HUN", season="Summer"):
    """
    Histogram över åldersfördelning för valt land (NOC) och säsong (Summer/Winter).
    Bygger på all_unique (unika deltaganden).
    """
    dff = all_unique[(all_unique["NOC"] == noc) & (all_unique["Season"] == season)].copy()
    dff = dff[dff["Age"].notna()]  # ta bort rader utan ålder

    if dff.empty:
        # liten fallback om det inte finns data
        fig = px.histogram(title=f"Ingen åldersdata för {noc} – {season}-OS")
        return fig

    age_min = dff["Age"].min()
    age_max = dff["Age"].max()
    nbins = int(age_max - age_min)

    fig = px.histogram(
        dff,
        x="Age",
        nbins=nbins,
        title=f"Åldersfördelning – {noc}, {season}-OS"
    )

    fig.update_xaxes(
        dtick=2,
        tickangle=45,
        title="Ålder"
    )
    fig.update_layout(
        yaxis_title="Antal deltagare"
    )

    return fig
