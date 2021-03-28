import dash 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


uri = os.environ.get("DATABASE_URL")  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


server = Flask(__name__)

app = dash.Dash(__name__, suppress_callback_exceptions=True, 
    server = server,
    meta_tags=[{
      'name': 'viewport',
      'content': 'width=device-width, initial-scale=1.0'
    }])

app.server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.server.config['SQLALCHEMY_DATABASE_URI'] = uri #'postgresql//code@localhost/test'


db = SQLAlchemy(app.server)
engine = db.engine


#from the index.py file
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
