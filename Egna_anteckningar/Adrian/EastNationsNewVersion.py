nation_colors = {
    "BUL" : "#0000FF",
    "HUN" : "#00ff00",
    "POL" : "#f3de00",
    "YUG" : "#7300ff",
    "URS" : "#e40000",
    "ROU" : "#7f4f06",
    "TCH" : "#565656"
}
 
#East nations medals data
East_Nations = ['RUS', 'URS', 'EUN', 'UKR', 'BLR', 'MDA', 'GEO', 'ARM', 'AZE', 'KAZ',
 'UZB', 'KGZ', 'TJK', 'LTU', 'LAT', 'EST',
 'HUN', 'POL', 'ROU', 'BUL', 'ALB', 'YUG', 'SCG', 'SRB', 'CRO', 'SLO',
 'BIH', 'MKD', 'MNE', 'KOS',
 'CZE', 'TCH', 'SVK']
 
df_East_Nations = df[df["NOC"].isin(East_Nations)]
 
df_East_Nations52 = df_East_Nations[df_East_Nations["Year"] == 1952]
 
Unique_Medals_By_EastNoc = df_East_Nations52.drop_duplicates(subset=["NOC", "Sport", "Event", "Medal"])
Medal_Counts_EastNoc52 = Unique_Medals_By_EastNoc.groupby(["NOC", "Medal"]).size().reset_index(name="Count")
 
#East nations medals/athlete data
 
athletes_1952 = (df_East_Nations52.drop_duplicates(subset=["NOC", "ID"])
                     .groupby(["NOC"])
                     .size()
                     .reset_index(name="Athletes"))
medals_1952 = (df_East_Nations52[df_East_Nations52["Medal"].notna()].drop_duplicates(subset=["NOC", "Event", "Medal"])
                   .groupby(["NOC"])
                   .size()
                   .reset_index(name="Medals"))
medals_athletes1952 = athletes_1952.merge(medals_1952, on="NOC", how="left")
medals_athletes1952["Medals"] = medals_athletes1952["Medals"].fillna(0)
medals_athletes1952["Medal per athlete"] = round((medals_athletes1952["Medals"]/medals_athletes1952["Athletes"])*100, 1)
 
#East nations medals figure
 
fig_EN_bar = px.bar(
    Medal_Counts_EastNoc52,
    x="NOC",
    y="Count",
    color="Medal",
    barmode="stack",
    title="East european nations in os 1952",
    labels={"Count":"Number of medals", "NOC":"East european nations"},
    color_discrete_map={'Gold': 'orange', 'Silver': 'grey', 'Bronze': 'sienna'},
    category_orders={"Medal": ["Bronze", "Silver", "Gold"]},
    text_auto=True)
 
#East nations medal/athlete figure
 
fig_EN_scatter = px.scatter(
    medals_athletes1952,
    x= "Athletes",
    y= "Medals",
    color = "NOC",
    size= "Medal per athlete",
    hover_data= ["Medal per athlete"],
    text= "Medal per athlete",
    title= "Medal vs Athletes East block 1952" ,
    color_discrete_map=nation_colors)

fig_EN_scatter.update_traces(
    mode= "markers+text",
    textposition= "top center",
    textfont= dict(size=12),
)
 
fig = make_subplots(rows=1, cols=2, subplot_titles=("Medal count", "Medals vs. athletes ratio"))
 
for trace in fig_EN_bar.data:
    fig.add_trace(trace, row=1, col=1)
 
for trace in fig_EN_scatter.data:
    fig.add_trace(trace, row=1, col=2)


fig.update_xaxes(title_text="Nations", row=1, col=1)
fig.update_xaxes(title_text="Athletes", row=1, col=2)
fig.update_yaxes(title_text="Medals", range=[0, 80])


fig.update_layout(
    showlegend= True,
    title_text= "East bloc nations 1952",
    height=700,
    barmode="stack")

 
fig.show()
 