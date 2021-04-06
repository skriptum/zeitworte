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
from apps import home, app1, app2, app3, app4

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    #head
    html.Div(className = "bare-container top", children = [
        html.A(href = "/", children = [
                #html.Img(src = "./assets/logo.png")
                html.H1("Keine Zeit", className = "header")
        ]),
        dcc.Link("Worte", href = "/worte"), "|", 
        dcc.Link("Autoren", href = "/autoren"), "|", 
        dcc.Link("Karten", href = "/karten"), "|", 
        dcc.Link("Über", href = "/about"), "|", 
    ]),

    #content
    html.Div(id='page-content'),

    #footer
    html.Div(className = "bare-container bottom", children = [
        "YOlo"
    ]),
    
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/worte':
        return app1.layout
    elif pathname == '/karten':
        return app2.layout
    if pathname == '/autoren':
        return app3.layout
    elif pathname == '/':
        return home.layout
    elif pathname == '/about':
        return app4.layout
    else:
        return '404'
