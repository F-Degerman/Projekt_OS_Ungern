import pandas as pd
import plotly.express as px

df = pd.read_csv("athlete_events.csv")
noc = pd.read_csv("noc_regions.csv")
df = df.merge(noc, on="NOC", how="left")

hungary = df[df["region"] == "Hungary"]

summer_years = sorted(df[df["Season"] == "Summer"]["Year"].unique())
winter_years = sorted(df[df["Season"] == "Winter"]["Year"].unique())

full_years = pd.concat([
    pd.DataFrame({"Year": summer_years, "Season": "Summer"}),
    pd.DataFrame({"Year": winter_years, "Season": "Winter"})
], ignore_index=True)

hun_participants = (
    hungary.drop_duplicates(subset=["ID", "Year", "Season"])
       .groupby(["Year", "Season"])["ID"]
       .nunique()
       .reset_index(name="Participants")
)

final = full_years.merge(hun_participants, on=["Year", "Season"], how="left")
final["Participants"] = final["Participants"].fillna(0)

fig = px.line(
    final,
    x="Year",
    y="Participants",
    color="Season",
    markers=True,
    title="Antal ungerska deltagare per OS (Summer vs Winter)"
)

fig.update_traces(line_shape="spline")

fig.update_traces(selector=dict(name="Summer"), line=dict(color="green"))
fig.update_traces(selector=dict(name="Winter"), line=dict(color="blue"))

fig.update_xaxes(type="linear")

fig.show()