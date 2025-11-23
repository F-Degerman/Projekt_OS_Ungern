import pandas as pd
from load_data import load_anonymized_data

# Load dataset
df = load_anonymized_data()

# Hungarian data
hun_df = df[df["NOC"] == "HUN"].copy().reset_index().sort_values(by="Year")

# Graph data
## Welcoming graph
## NOTE: copied from Copilot after prompting a px.scatter() with data points in the shape of "AIM25G"
def letter_to_points(letter_pattern, x_offset=0, y_offset=0, scale=2):
    points = []
    for y, row in enumerate(letter_pattern):
        for x, char in enumerate(row):
            if char == "#":
                # Skala upp punkterna
                for dx in range(scale):
                    for dy in range(scale):
                        points.append({
                            "x": (x*scale + dx) + x_offset,
                            "y": -(y*scale + dy) + y_offset
                        })
    return points

patterns = {
    "A": [
        " ### ",
        "#   #",
        "#   #",
        "#####",
        "#   #",
        "#   #",
        "#   #",
    ],
    "I": [
        "#####",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "#####",
    ],
    "M": [
        "#   #",
        "## ##",
        "# # #",
        "#   #",
        "#   #",
        "#   #",
        "#   #",
    ],
    "2": [
        "#####",
        "    #",
        "    #",
        "#####",
        "#    ",
        "#    ",
        "#####",
    ],
    "5": [
        "#####",
        "#    ",
        "#    ",
        "#####",
        "    #",
        "    #",
        "#####",
    ],
    "G": [
        "#####",
        "#    ",
        "#    ",
        "#  ##",
        "#   #",
        "#   #",
        "#####",
    ],
}

x_offset = 0
all_points = []
for char in "AIM25G":
    pts = letter_to_points(patterns[char], x_offset=x_offset, scale=2)
    all_points.extend(pts)
    x_offset += 7 * 2

aim25g_df = pd.DataFrame(all_points)

## Hungary: number of participants per year
summer_years = sorted(df[df["Season"] == "Summer"]["Year"].unique())
winter_years = sorted(df[df["Season"] == "Winter"]["Year"].unique())

missing_summer = [1916, 1940, 1944]
missing_winter = [1940, 1944]

summer_years = sorted(set(summer_years + missing_summer))
winter_years = sorted(set(winter_years + missing_winter))

full_years = pd.concat([
    pd.DataFrame({"Year": summer_years, "Season": "Summer"}),
    pd.DataFrame({"Year": winter_years, "Season": "Winter"})
], ignore_index=True)

hun_participants = (
    hun_df.drop_duplicates(subset=["ID", "Year", "Season"])
       .groupby(["Year", "Season"])["ID"]
       .nunique()
       .reset_index(name="Participants"))

final_participants = full_years.merge(hun_participants, on=["Year", "Season"], how="left")
final_participants["Participants"] = final_participants["Participants"].fillna(0)

## Hungary: medals won per sport
unique_medals_sport = (hun_df[["Year", "Event", "Sport", "Medal"]]
                        .dropna()
                        .drop_duplicates(subset=["Year", "Event", "Medal"]))
medals_sport = (pd.DataFrame(unique_medals_sport
                        .groupby("Sport")["Medal"]
                        .value_counts()
                        .unstack()
                        .sum(axis=1))
                        .rename(columns={0:"Medals"})
                        .sort_values("Medals", ascending=False))

## Hungary: medals won per Olympics
unique_medals_olympic = (hun_df[["Year", "Event", "Season", "Medal"]]
                        .dropna(subset=["Year", "Event", "Medal"])
                        .drop_duplicates(subset=["Year", "Event", "Medal"]))
unique_medals_olympic["ExtraSeason"] = unique_medals_olympic.apply(lambda row: "Intercalated Games" if row["Year"] == 1906 else ("Winter" if row["Season"] == "Winter" else "Summer"), axis=1)
medals_olympic = (unique_medals_olympic.groupby(["Year", "ExtraSeason"])["Medal"]
                        .value_counts()
                        .unstack()
                        .sum(axis=1)
                        .reset_index()
                        .rename(columns={0: "Medals"}))

## Hungary: medals won per Olympics (detailed)
unique_medals_olympic_d = (hun_df[["Year", "Event", "Season", "Medal"]]
                        .fillna({"Medal": "0"})
                        .dropna(subset=["Year", "Event", "Medal"])
                        .drop_duplicates(subset=["Year", "Event", "Medal"]))
unique_medals_olympic_d["ExtraSeason"] = unique_medals_olympic_d.apply(lambda row: "Intercalated Games" if row["Year"] == 1906 else ("Winter" if row["Season"] == "Winter" else "Summer"), axis=1)
medals_olympic_d = (unique_medals_olympic_d.groupby(["Year", "ExtraSeason"])["Medal"]
                        .value_counts()
                        .unstack()
                        .reset_index())
melted = medals_olympic_d.melt(id_vars=["Year", "ExtraSeason"], value_vars=["Bronze", "Silver", "Gold"], var_name="MedalType", value_name="Count")
melted["SeasonYear"] = melted["ExtraSeason"] + " " + melted["Year"].astype(str)
medals_olympic_d = melted.drop(["ExtraSeason"], axis=1)

## Hungary: medals per sport 1952
hun_52 = hun_df[hun_df["Year"] == 1952]

unique_medal_event_52 = hun_52.drop_duplicates(subset=["Sport", "Event", "Medal"])
unique_medals_sport_52 = unique_medal_event_52.groupby(["Sport", "Medal"]).size().unstack(fill_value=0)
unique_medals_sport_52["Total"] = unique_medals_sport_52[["Gold", "Silver", "Bronze"]].sum(axis=1)
unique_medals_sport_52.sort_values(by= "Total", ascending=False, inplace=True)

hun_top10_sports_52 = unique_medals_sport_52.reset_index()

## ADRIAN 2


## Gymnastics: gender comparison all years vs 1952
# All years
gymnastics_all = df[df["Sport"] == "Gymnastics"] 
gymnastics_hun = df[(df["Sport"] == "Gymnastics") & (df["NOC"] == "HUN")]
gymnastics_swe = df[(df["Sport"] == "Gymnastics") & (df["NOC"] == "SWE")]

all_gymnastics_group = gymnastics_all.assign(Group="All countries")
hun_gymnastics_group = gymnastics_hun.assign(Group="Hungary")
swe_gymnastics_group = gymnastics_swe.assign(Group="Sweden")

gymnastics_combined = pd.concat([all_gymnastics_group, hun_gymnastics_group, swe_gymnastics_group])
gymnastics_combined["Period"] = "All years"

# 1952
gymnastics_all_1952 = df[(df["Sport"] == "Gymnastics") & (df["Year"] == 1952)]
gymnastics_hun_1952 = df[(df["Sport"] == "Gymnastics") & (df["NOC"] == "HUN") & (df["Year"] == 1952)]
gymnastics_swe_1952 = df[(df["Sport"] == "Gymnastics") & (df["NOC"] == "SWE") & (df["Year"] == 1952)]

all_gymnastics_1952_group = gymnastics_all_1952.assign(Group="All countries")
hun_gymnastics_1952_group = gymnastics_hun_1952.assign(Group="Hungary")
swe_gymnastics_1952_group = gymnastics_swe_1952.assign(Group="Sweden")

gymnastics_1952_combined = pd.concat([all_gymnastics_1952_group, hun_gymnastics_1952_group, swe_gymnastics_1952_group])
gymnastics_1952_combined["Period"] = "1952"

gymnastics_gender_all = pd.concat([gymnastics_combined, gymnastics_1952_combined])

## FANNY 2

## ENDING
# NOTE: copied from Copilot after prompting a px.scatter() with exploding confetti in front of a text
import numpy as np

n_points = 250
n_frames = 30

np.random.seed(42)

x0 = np.zeros(n_points)
y0 = np.zeros(n_points)

angles = np.random.uniform(0, 2*np.pi, n_points)
speeds = np.random.uniform(0.1, 0.5, n_points)
colors = np.random.choice(["red", "orange", "yellow", "green", "blue", "purple", "pink"], n_points)

frames = []
for frame in range(n_frames):
    x = x0 + np.cos(angles) * speeds * frame * 3
    y = y0 + np.sin(angles) * speeds * frame * 3
    df_frame = pd.DataFrame({
        "x": x,
        "y": y,
        "color": colors,
        "frame": frame
    })
    frames.append(df_frame)

confetti = pd.concat(frames)