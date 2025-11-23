import pandas as pd
import hashlib
import plotly.express as px

# load data and merge
df = pd.read_csv("athlete_events.csv")
noc = pd.read_csv("noc_regions.csv")
df = df.merge(noc, on="NOC", how="left")

# target country and figure skating
TARGET_COUNTRY = "Hungary"
country = df[df["region"] == TARGET_COUNTRY]
figure_skating = country[country["Sport"] == "Figure Skating"].copy()

# hash names to anonymize athletes
def hash_name(name):
    if pd.isna(name):
        return name
    return hashlib.sha256(name.encode("utf-8")).hexdigest()

figure_skating["AnonName"] = figure_skating["Name"].apply(hash_name)

# data with only medal winners
figure_skating_medals = figure_skating.dropna(subset=["Medal"])

# medals by event
events = (
    figure_skating_medals.groupby("Event")["Medal"]
    .count()
    .reset_index(name="medals")
    .sort_values("medals", ascending=False)
)
fig1 = px.bar(events, x="Event", y="medals")
fig1.show()

# medals by year
medals_year = (
    figure_skating_medals.groupby("Year")["Medal"]
    .count()
    .reset_index(name="medals")
)
fig2 = px.line(medals_year, x="Year", y="medals", markers=True)
fig2.show()

# age distribution
fig3 = px.histogram(figure_skating.dropna(subset=["Age"]), x="Age", nbins=20)
fig3.show()

# gender distribution
fig4 = px.histogram(figure_skating, x="Sex", color="Sex")
fig4.show()

# top skaters by medal count
top_skaters = (
    figure_skating_medals.groupby("AnonName")["Medal"]
    .count()
    .reset_index(name="medalcount")
    .sort_values("medalcount", ascending=False)
    .head(10)
)

print(top_skaters)
