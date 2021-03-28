import dash 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import configparser

c = configparser.ConfigParser()
c.read("config.ini")
uri = c.get("Postgres", "URI")

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