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

# Funktion för köns-trend figur (SWE & HUN). Gemensamma axelgränser. 

def figur_gender_trend(noc="HUN", x_range=None, y_range=None):
    """
    Antal unika deltagare per år i OS (alla säsonger),
    för valt land (NOC), uppdelat på kön.
    """
    dff = all_unique[all_unique["NOC"] == noc]

    yearly_gender = (
        dff.groupby(["Year", "Sex"])["ID"]
        .nunique()
        .reset_index()
        .rename(columns={"ID": "Antal_deltagare"})
    )

    fig = px.line(
        yearly_gender,
        x="Year",
        y="Antal_deltagare",
        color="Sex",
        markers=True,
        title=f"Antal deltagare per år och kön – {noc} (alla OS)"
    )

    # Om vi fått in gemensamma axelgränser: använd dem
    if x_range is not None:
        fig.update_xaxes(range=x_range)
    if y_range is not None:
        fig.update_yaxes(range=y_range)

    fig.update_layout(
        xaxis_title="År",
        yaxis_title="Antal deltagare",
        legend_title_text="Kön"
    )
    return fig

# Beräknar gemensam x- och y-axelrange för Ungern + Sverige, så att graferna får samma skala.
def get_shared_gender_axis_ranges():

    dff = all_unique[all_unique["NOC"].isin(["HUN", "SWE"])]

    yearly_gender = (
        dff.groupby(["Year", "Sex"])["ID"]
        .nunique()
        .reset_index()
    )

    x_min = yearly_gender["Year"].min()
    x_max = yearly_gender["Year"].max()
    y_max = yearly_gender["ID"].max()

    x_range = [x_min - 1, x_max + 1]
    y_range = [0, y_max * 1.1]

    return x_range, y_range
