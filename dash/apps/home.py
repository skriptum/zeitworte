import dash
import dash_core_components as dcc
import dash_html_components as html

#figure
from apps.app1 import startup_fig as wort_fig
from apps.app2 import fig2 as karten_fig
from apps.app3 import fig  as autoren_fig


layout = html.Div(children = [
    # html.Div(className = "twelve columns pretty-container", 
    #     children =["a"] , 
    #     style = {"margin-top": "0"}),

    #the pages
    html.Div(className = "text-container", children = [
        #first row
        html.Div(className = "row", children = [
            #the words
            html.Div(className = "six columns pretty-container centered", children = [
                dcc.Link(href = "/worte", children = [
                    html.H1("Worte", className = "header"),
                    dcc.Graph(figure = wort_fig, 
                        config = {"displayModeBar": False, "responsive": True},
                        style = {"height": "90%"}),
                ]),
            ]),
            

            #the maps
            html.Div(className = "six columns pretty-container centered", children = [
                dcc.Link(href = "/karten", children = [
                    html.H1("Karten", className = "header"),
                    dcc.Graph(figure = karten_fig, 
                    config = {"displayModeBar": False, "responsive": True},
                    style = {"height": "90%"}),
                ]),
            ]),
        ]),

        #second row
        html.Div(className = "row", children = [
            #the authors
            html.Div(className = "six columns pretty-container centered", children = [
                dcc.Link(href = "/autoren", children = [
                    html.H1("Autoren", className = "header"),
                    dcc.Graph(figure = autoren_fig, 
                    config = {"responsive": True, "displayModeBar": False},
                    style = {"height": "90%"}),
                ]),
            ]),
        

            #the about
            html.Div(className = "six columns pretty-container centered", children = [
                dcc.Link(href = "/about", children = [
                    html.H1("Über die Seite", className = "header"),
                    dcc.Markdown("""
                        Diese Seite basiert auf der ZEIT-Website Schnittstelle, ist jedoch keineswegs von der Zeit,
                        sondern von einem ...""")
                ]),
            ]),
        ]),
    ]),
]) 