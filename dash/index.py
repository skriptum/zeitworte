
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2, home

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    #head
    html.Div(className = "bare-container top", children = [
        html.A(href = "/", children = [
                #html.Img(src = "./assets/logo.png")
                html.H1("Keine Zeit", className = "header")
        ]),
    ]),

    #content
    html.Div(id='page-content'),

    #footer
    html.Div(className = "bare-container bottom", children = [
        "YOlo"
    ], style = {"border-top": "1px solid #252525"}),
    
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/':
        return home.layout
    else:
        return '404'




if __name__ == '__main__':
    app.run_server(debug=True)