import dash
import dash_core_components as dcc
import dash_html_components as html

#figure

from apps.app2 import fig1 as karten_fig
from apps.app3 import fig  as autoren_fig

layout = html.Div( style = {"padding": "5%"}, children = [
    html.Div(className = "row", children = [
        #the words
        html.Div(className = "six columns pretty-container", children = [
            dcc.Link(href = "/worte", children = [
                html.H1("Worte", className = "header"),
            ]),
        ]),
    ]),

    #the maps
    html.Div(className = "row", children = [
        html.Div(className = "six columns pretty-container", children = [
            dcc.Link(href = "/karten", children = [
                html.H1("Karten", className = "header"),
                dcc.Graph(figure = karten_fig, 
                config = {"responsive": False, "displayModeBar": False}),
            ]),
        ]),
    ]),

    html.Div(className = "row", children = [
        #the authors
        html.Div(className = "six columns pretty-container", children = [
            dcc.Link(href = "/autoren", children = [
                html.H1("Autoren", className = "header"),
                dcc.Graph(figure = autoren_fig, 
                config = {"responsive": False, "displayModeBar": False}),
            ]),
        ]),
    ]),

    html.Div(className = "row", children = [
        #the about
        html.Div(className = "six columns pretty-container", children = [
            dcc.Link(href = "/about", children = [
                html.H1("Über die Seite", className = "header"),
            ])
        ]),
    ]),
])