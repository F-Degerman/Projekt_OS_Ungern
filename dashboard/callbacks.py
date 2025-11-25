import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from graph_data import aim25g_df, final_participants, medals_sport, medals_olympic, medals_olympic_d, hun_top10_sports_52, nation_year, medal_by_sport_sex52, medal_counts_east_noc52, pie_data, gymnastics_gender_all, gender_summary, confetti
from dash import Input, Output

def _style_fig(fig, height=600):
    """ Set height and papercolor for graphs. """
    fig.update_layout(height=height, paper_bgcolor="#f9f9f9")
    return fig

def register_callbacks(app):
    """ Setting up callback functionality between the dropdown menu, the label and the graph. """
    @app.callback(
        Output("graph", "figure"), 
        Output("question", "children"), 
        Input("hungary-dropdown", "value"))

    def update_graph(selected_value):
        """ Updating the graph based on the value recieved from the dropdown menu. """

        ## "AIM25G" scatter
        if selected_value is None:
            question="Please choose a topic from the dropdown menu!"
            
            fig = px.scatter(
                aim25g_df, 
                x="x", 
                y="y", 
                title="Welcome to our presentation!", 
                subtitle="Fanny Degerman, Delal Uca, Adrian Söderberg Skog och Patrik Hellgren")
            fig.update_traces(marker=dict(size=8, color="darkgreen"))
            fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1), showlegend=False)
            return _style_fig(fig), question
                
        ## Hungary: number of participants per year
        elif selected_value == "final_participants":
            question = "How many participants did Hungary have from year to year?"
            fig = px.line(
                final_participants.sort_values("Year"),
                x="Year",
                y="Participants",
                color="Season",
                markers=True,
                title="Hungary: number of participants per year", 
                subtitle="Summer vs. winter", 
                hover_data="City", 
                line_shape="spline")

            fig.update_xaxes(type="linear", dtick=2, ticklabelposition="outside left", tickangle=-45)
            fig.update_traces(selector=dict(name="Summer"), line=dict(color="orange"))
            fig.update_traces(selector=dict(name="Winter"), line=dict(color="blue"))
            return _style_fig(fig), question

        ## Hungary: medals won per Olympics
        elif selected_value == "hun_medals":
            question = "How many medals has Hungary won at each Olympic Game?"
            fig = px.bar(
                medals_olympic,
                x="Year", 
                y="Medals", 
                title="Hungary: medals won per Olympics", 
                subtitle="Team medals count as one medal", 
                color="ExtraSeason", 
                barmode="group", 
                color_discrete_map={"Summer": "orange", "Winter": "blue", "Intercalated Games": "red"})
            fig.update_layout(legend=dict(orientation="h", yanchor="top", y=1.15, xanchor="right", x=1), 
                            legend_title_text="", bargap=0.02)
            fig.update_xaxes(dtick=4, ticklabelposition="outside left", tickangle=-45)
            return _style_fig(fig), question
        
        ## Hungary: medals won per Olympics (detailed)
        elif selected_value == "hun_medals_d":
            question = "What year did Hungary win the most (gold) medals?"
            fig = px.bar(
                medals_olympic_d,
                x="SeasonYear", 
                y="Count", 
                title="Hungary: medals won per Olympics (detailed)", 
                subtitle="Team medals count as one medal", 
                color="MedalType", 
                barmode="stack", 
                color_discrete_map={"Gold": "orange", "Silver": "grey", "Bronze": "sienna"}, 
                labels={"Count": "Medals", "SeasonYear": "Olympics"}, 
                text_auto=True)
            fig.update_layout(legend=dict(orientation="h", yanchor="top", y=1.15, xanchor="right", x=1, traceorder="reversed"), 
                            legend_title_text="Medal:", bargap=0.02)
            fig.update_xaxes(ticklabelposition="outside left", tickangle=-45)
            fig.update_traces(textangle=0)
            return _style_fig(fig), question

        ## Hungary: medals per sport 1952 vs all years
        elif selected_value == "sport_medals":
            question = "In which sports did Hungary win medals during their peak year 1952?"
            fig = make_subplots(rows=1, cols=2, subplot_titles=("1952", "Total"))

            color_map = {
                "Gymnastics": "orchid",
                "Swimming": "steelblue",
                "Fencing": "silver",
                "Athletics": "forestgreen",
                "Wrestling": "firebrick",
                "Canoeing": "darkorange",
                "Shooting": "dimgray",
                "Modern Pentathlon": "gold",
                "Boxing": "brown",
                "Football": "darkred",
                "Figure Skating": "deepskyblue",
                "Water Polo": "navy"}

            fig1 = px.bar(
                hun_top10_sports_52, 
                x="Total", 
                y="Sport", 
                orientation="h", 
                color="Sport", 
                text_auto=True, 
                color_discrete_map=color_map)

            for trace in fig1.data:
                fig.add_trace(trace, row=1, col=1)

            fig2 = px.bar(
                medals_sport,
                x="Medals", 
                y="Sport", 
                orientation="h", 
                color="Sport", 
                text_auto=True, 
                color_discrete_map=color_map)

            for trace in fig2.data:
                fig.add_trace(trace, row=1, col=2)

            fig.update_layout(
                title_text="Hungary: comparison of medals per sport",  
                legend_title_text="Sport", 
                showlegend=False)
            return _style_fig(fig), question

        ## Overall: medal comparison of Eastern European nations 1952
        elif selected_value == "comp_een":
            question = "How did Hungary perform compared to other Eastern European nations in 1952?"
            fig = make_subplots(rows=2, cols=7, 
                                subplot_titles=["Medals 1952"] + list(pie_data["NOC"]), 
                                row_heights=[0.7, 0.3], 
                                column_widths=[1/7, 1/7, 1/7, 1/7, 1/7, 1/7, 1/7], 
                                specs=[[{"type": "bar", "colspan": 7}, None, None, None, None, None, None],
                                       [{"type": "pie"}]*7])

            fig1 = px.bar(
                medal_counts_east_noc52,
                x="Count",
                y="NOC",
                color="Medal",
                color_discrete_map={"Gold": "orange", "Silver": "grey", "Bronze": "sienna"},
                text_auto=True,
                category_orders={"Medal": ["Bronze", "Silver", "Gold"]}, 
                orientation="h")
            fig1.update_traces(textangle=0)

            for trace in fig1.data:
                fig.add_trace(trace, row=1, col=1)

            col = 1
            for noc in pie_data["NOC"].unique():
                noc_df = pie_data[pie_data["NOC"] == noc].iloc[0]
                df_noc = pd.DataFrame({
                    "Category": ["Medals", "Participants"], 
                    "Value": [noc_df["Medals"], noc_df["Participants"]], 
                    "NOC": [noc, noc]})
                
                figx = px.pie(
                    df_noc, 
                    values="Value", 
                    names="Category",
                    color="Category", 
                    color_discrete_map={"Medals": "grey", "Participants": "#004B23"})
                figx.update_traces(rotation=60)
                
                for trace in figx.data:
                    fig.add_trace(trace, row=2, col=col)
                    col += 1

            fig.update_layout(title_text="Medals and medals to participants ratio between Eastern European nations in 1952", barmode="stack")
            return _style_fig(fig), question
        
        ## Overall: correlation between medals and participants
        elif selected_value == "nation_year":
            question = "Is there a correlation between medals and participants?"
            fig = px.scatter(
                nation_year,
                x="Athletes",
                y="Medals",
                color="NOC",
                opacity= 0.7,
                hover_data="Year",
                title="Overall: correlation between medals and participants", 
                subtitle="All countries, all years (correlation: 0.97)")
            return _style_fig(fig), question
        
        ## Hungary: medals grouped by sport and gender 1952
        elif selected_value == "medals_sport_gender":
            question = "How was the medal distribution between genders in 1952?"
            fig = px.bar(
                medal_by_sport_sex52,
                x="Sport",
                y="Total",
                color="Sex",
                color_discrete_map={"M": "#004B23", "F": "#C50000"},
                barmode="group",
                title="Hungary: medals grouped by sport and gender",
                subtitle="1952",
                labels={"Total": "Medals", "Sport": "Sport", "Sex": "Gender"})
            fig.for_each_trace(lambda label: label.update(name="Male" if label.name == "M" else "Female"))
            return _style_fig(fig), question

        ## Gymnastics: gender comparison
        elif selected_value == "gymnastics_gender":
            question = "What does the gender distribution in gymnastics look like?"
            fig = px.pie(
                gymnastics_gender_all, 
                names="Sex", 
                facet_col="Group", 
                facet_row="Period", 
                category_orders={"Group": ["All countries", "Hungary", "Sweden"]}, 
                title="Gymnastics: gender comparison", 
                subtitle="All years vs 1952", 
                color="Sex", 
                color_discrete_map={"M": "#004B23", "F": "#C50000"})
            fig.update_traces(textinfo="label+percent")
            return _style_fig(fig), question
        
        ## Hungary: medal distribution across time based on gender
        elif selected_value == "medal_dist_gender":
            question = "How did women's participation and results in 1952 differ from the surrounding years?"
            fig = go.Figure()
            
            fig.add_bar(
                x=gender_summary["Year_sex"],
                y=gender_summary["Medalists"],
                name="Medalists",
                hovertemplate="Medalists: %{y}<extra></extra>", 
                marker_color="gray")
            
            fig.add_bar(
                x=gender_summary.loc[gender_summary["Sex"]=="F", "Year_sex"],
                y=gender_summary.loc[gender_summary["Sex"]=="F", "Non_medalists"],
                name="Female non-medalists",
                hovertemplate="Female, no medal: %{y}<extra></extra>", 
                marker_color="#C50000")
            
            fig.add_bar(
                x=gender_summary.loc[gender_summary["Sex"]=="M", "Year_sex"],
                y=gender_summary.loc[gender_summary["Sex"]=="M", "Non_medalists"],
                name="Male non-medalists",
                hovertemplate="Male, no medal: %{y}<extra></extra>", 
                marker_color="#004B23")
            
            bar_categories = gender_summary["Year_sex"].unique() 
            index_bar_1952 = [i for i, c in enumerate(bar_categories) if c.startswith("1952")] 

            if index_bar_1952:
                x0 = index_bar_1952[0] - 0.5
                x1 = index_bar_1952[-1] + 0.5
                fig.add_vrect(x0=x0, x1=x1, line_dash="dash")

            fig.update_layout(
                barmode="stack",
                title="Hungary: medal distribution across time based on gender", 
                title_subtitle_text="1924-1968", 
                xaxis_title="Year and gender",
                yaxis_title="Number of participants")
            return _style_fig(fig), question
        
        ## ENDING
        elif selected_value == "ending":
            question = ""
            # NOTE: copied from Copilot after prompting a px.scatter() with exploding confetti in front of a text
            fig = px.scatter(
                confetti,
                x="x",
                y="y",
                color="color",
                animation_frame="frame")
            fig.update_traces(marker=dict(size=12, opacity=0.7, symbol="circle"))
            fig.update_layout(
                showlegend=False,
                plot_bgcolor="#f9f9f9", 
                xaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[-10, 10]),
                yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, range=[-10, 10]),
                annotations=[
                    dict(
                        text="THANK YOU!",
                        x=0, y=0,
                        xref="x", yref="y",
                        showarrow=False,
                        font=dict(size=60, color="#004B23", family="Arial Black"))])
        return _style_fig(fig), question
    