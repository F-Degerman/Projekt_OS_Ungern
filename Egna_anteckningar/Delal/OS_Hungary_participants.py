import pandas as pd
import plotly.express as px

df = pd.read_csv("athlete_events.csv")
noc = pd.read_csv("noc_regions.csv")
df = df.merge(noc, on="NOC", how="left")
hun = df[df["region"] == "Hungary"]

summer_years = sorted(df[df["Season"] == "Summer"]["Year"].unique())
winter_years = sorted(df[df["Season"] == "Winter"]["Year"].unique())
#saknad data
missing_summer = [1916, 1940, 1944]
missing_winter = [1940, 1944]

summer_years = sorted(set(summer_years + missing_summer))
winter_years = sorted(set(winter_years + missing_winter))

full_years = pd.concat([
    pd.DataFrame({"Year": summer_years, "Season": "Summer"}),
    pd.DataFrame({"Year": winter_years, "Season": "Winter"})
], ignore_index=True)

hun_participants = (
    hun.drop_duplicates(subset=["ID", "Year", "Season"])
       .groupby(["Year", "Season"])["ID"]
       .nunique()
       .reset_index(name="Participants")
)

final = full_years.merge(hun_participants, on=["Year", "Season"], how="left")
final["Participants"] = final["Participants"].fillna(0)

fig = px.line(
    final.sort_values("Year"),
    x="Year",
    y="Participants",
    color="Season",
    markers=True,
    title="Antal ungerska deltagare per OS (Summer vs Winter)"
)

fig.update_traces(line_shape="spline")
fig.update_xaxes(type="linear")
fig.update_traces(selector=dict(name="Summer"), line=dict(color="orange"))
fig.update_traces(selector=dict(name="Winter"), line=dict(color="turquoise"))

fig.show()
