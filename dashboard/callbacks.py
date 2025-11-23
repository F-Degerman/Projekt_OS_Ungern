import plotly.express as px
from graph_data import aim25g_df, final_participants, medals_sport, medals_olympic, medals_olympic_d, gymnastics_combined, gymnastics_1952_combined, confetti
from dash import Input, Output

def _style_fig(fig, height=650):
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
                line_shape="spline")

            fig.update_xaxes(type="linear", dtick=2, ticklabelposition="outside left", tickangle=-45)
            fig.update_traces(selector=dict(name="Summer"), line=dict(color="orange"))
            fig.update_traces(selector=dict(name="Winter"), line=dict(color="blue"))
            return _style_fig(fig), question

        ## Hungary: medals won per sport
        elif selected_value == "hun_most_medals":
            question = "In which sports has Hungary earned the most medals?"
            fig = px.bar(
                data_frame=medals_sport,
                x=medals_sport.index, 
                y="Medals", 
                title="Hungary: medals won per sport", 
                subtitle="Team medals count as one medal", 
                color=medals_sport.index, 
                text_auto=True)
            return _style_fig(fig), question
        
        ## Hungary: medals won per Olympics
        elif selected_value == "hun_medals":
            question = "How many medals has Hungary won at each Olympics and why are medal counts for some years missing?"
            fig = px.bar(
                data_frame=medals_olympic,
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
                data_frame=medals_olympic_d,
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

        ## Adrian 1


        ## Adrian 2

        
        ## Gymnastics: gender comparison
        elif selected_value == "gymnastics_gender":
            question = "What does the gender distribution in gymnastics look like?"
            fig = px.pie(
                gymnastics_combined, 
                names="Sex", 
                facet_col="Group", 
                category_orders={"Group": ["All countries", "Hungary", "Sweden"]}, 
                title="Gymnastics: gender comparison", 
                subtitle="All years, all countries", 
                color="Sex", 
                color_discrete_map={"M": "#004B23", "F": "#C50000"})
            fig.update_traces(textinfo="label+percent")
            return _style_fig(fig), question
        
        ## Gymnastics: gender comparison 1952
        elif selected_value == "gymnastics_gender_1952":
            question = "How was the gender distribution in gymnastics in 1952?"
            fig = px.pie(
                gymnastics_1952_combined, 
                names="Sex", 
                facet_col="Group", 
                category_orders={"Group": ["All countries", "Hungary", "Sweden"]}, 
                title="Gymnastics: gender comparison in 1952", 
                subtitle="Summer Olympics in Helsinki, Finland", 
                color="Sex", 
                color_discrete_map={"M": "#004B23", "F": "#C50000"})
            fig.update_traces(textinfo="label+percent")
            return _style_fig(fig), question
        
        ## ENDING
        elif selected_value == "ending":
            question = "Thank you for listening!"
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