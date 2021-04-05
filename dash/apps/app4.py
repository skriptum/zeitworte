import dash_core_components as dcc
import dash_html_components as  html

layout = html.Div(children = [
    html.Div(className = "container", children = [
        html.Div(className = "pretty-container", children = [
            html.H6("Über", className = "title"),
            html.H1("Wer macht das", className = "header"),
            html.P("Willkommen Lorem "),
        ])
    ])
])