import dash
import dash_core_components as dcc
import dash_html_components as html

#figure

from apps.app2 import fig1 as karten_fig
from apps.app3 import fig  as autoren_fig

layout = html.Div( children = [
    #the words
    html.Div(className = "pretty-container centered", children = [
        dcc.Link(href = "/worte", children = [
            html.H1("Worte", className = "header"),
        ]),
    ]),
    

    #the maps
    html.Div(className = "pretty-container centered", children = [
        dcc.Link(href = "/karten", children = [
            html.H1("Karten", className = "header"),
            dcc.Graph(figure = karten_fig, 
            config = {"responsive": False, "displayModeBar": False}),
        ]),
    ]),

    #the authors
    html.Div(className = "pretty-container centered", children = [
        dcc.Link(href = "/autoren", children = [
            html.H1("Autoren", className = "header"),
            dcc.Graph(figure = autoren_fig, 
            config = {"responsive": False, "displayModeBar": False}),
        ]),
    ]),
   

    #the about
    html.Div(className = "pretty-container centered", children = [
        dcc.Link(href = "/about", children = [
            html.H1("Über die Seite", className = "header"),
        ])
    ]),
])