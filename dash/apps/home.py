import dash
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div(children = [
    html.Div(className = "row", children = [
        html.Div(className = "six columns pretty-container", children = [
            dcc.Link("Go to Page 1", href = "/apps/app1")
        ]),

        html.Div(className = "six columns pretty-container", children = [
            dcc.Link("Go to Page 2", href = "/apps/app2")
        ]),
    ]),

    html.Div(className = "row", children = [
        html.Div(className = "six columns pretty-container", children = [
            "C"
        ]),

        html.Div(className = "six columns pretty-container", children = [
            "D"
        ]),

    ]),
], style = {"padding": "5%"})