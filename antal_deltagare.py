import pandas as pd
import plotly.express as px

df = pd.read_csv("athlete_events.csv")
noc = pd.read_csv("noc_regions.csv")
df = df.merge(noc, on="NOC", how="left")

hungary = df[df["region"] == "Hungary"]

deltagare_per_år = (
    hungary.groupby("Year")["ID"]
    .nunique()
    .reset_index(name="Antal deltagare")
)
fig = px.line(
    deltagare_per_år,
    x="Year",
    y="Antal deltagare",
    markers=True,
    title="Antal deltagare från unger per OS"
)
fig.update_xaxes(dtick=4)
fig.show()
