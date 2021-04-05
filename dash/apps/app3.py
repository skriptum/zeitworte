import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.express as px

from app import app

df = pd.read_csv("../data/names.csv", names = ["names", "count", "gender"], header = 0) #read in the data again


#the figure
fig = px.bar(df, y = "count", color="gender", text = "names",
    color_discrete_sequence = ["#efba32", "#c12e35"], labels = {"m": "männlicher Vorname", "f": "weiblicher Vorname"},
)
fig.update_layout(
        paper_bgcolor = "#f4f4f4",
        font = {"color":"#181818", "family" : "futura", "size": 13 },
        showlegend = True,
        plot_bgcolor = "#f4f4f4",
        margin = {"t": 0, "b": 0, "l": 0, "r": 0},
        hovermode = "x", 
        hoverlabel = {"bgcolor": "white", "bordercolor" : "white", "font_color": "black"},
        legend = dict(
            bgcolor = "rgba(0,0,0,0)",
            title = "Geschlecht",
            x = 0.9, y = 1,
            bordercolor = "rgba(0,0,0,0)",
            borderwidth = 0,
        ),)


fig.update_yaxes(ticklabelposition="outside top", title = None,
        gridcolor = "lightgrey", nticks = 7)

fig.update_xaxes(
    rangeslider_visible=True, range = (-1,10),
    ticklabelposition="outside top",
    showspikes = True, spikecolor = "grey", spikethickness = 2, spikemode = "across", 
    spikedash = "solid",
    linecolor = "lightgray",
    showgrid = False,
    title = "Bereich einstellen",
    )
fig.update_traces(
    hovertemplate = "<b>%{y} %{text}'s</b> <br>Platz: %{x} ",
)

#--------------------------------------------------------------------------------------------------------------------
#the layout

layout = html.Div(children = [
    html.Div(className = "row container", children = [
        #the sidenotes
        html.Div(className = "five columns pretty-container", children = [
            html.H6(className = "title", children = "Autoren"),
            html.H1(className = "header", children = "Die Häufigsten Vornamen der Zeit-Autor:innen"),
            html.P("""Diese Grafik zeigt die häufigsten Vornamen der Zeit Autor:innen. 
            Die Frage ist, ob man bei diesem Geschlechterverhältnis überhaupt noch gendern muss"""),
        ]),

        #the graph
        html.Div(className = "seven columns pretty-container", children = [
            dcc.Graph(
                figure = fig,
                config = {"displayModeBar": False}
            ),
        ]),

    ]),

    html.Hr(className = "vertical"),

    html.Div(className = "text-container", children = [
        html.H6(className = "title", children = "Autoren"),
        html.H1(className = "header", children = "Häufigste Vornamen der Zeit-Autoren"),
        dcc.Markdown("""**Peter** scheint unter Zeit Autoren ein sehr beliebter Vorname, 625 **Peters**
        verzeichnet die Zeit, dicht gefolgt von 564 Autoren mit Namen **Hans**. Erst auf Platz
        40 kommen weibliche Vornamen zum Vorschein, die 143 **Barbaras**, gefolgt auf Platz 51
        von 119 **Julias**. Besonders ausgeglichen ist das Geschlechterverhältnis nicht, ob das an den oft 
        gleichen männlichen Vornamen liegt oder am besonders in der Anfangszeit vorherrschenden Sexismus liegt ? 
        """),

        #funktionsweise
        html.Div(className = "pretty-container", children = [
            html.H6("Funktionsweise", className = "title"),
            html.P(""" Etwa 70.000 Autor:innen haben in den letzten 75 Jahren mindestents einen Artikel für
            die Zeit verfasst. Bereinigt von Fehlern, und die Namen in Vornamen, Zunamen und Nachnamen aufgeteilt
            und nach Häufigkeit sortiert, entsteht diese Grafik. Die Geschlechter der Vornamen wurden dabei händisch 
            sortiert""")
        ])
    ])
])