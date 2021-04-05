
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.express as px
import json

from app import app

df = pd.read_json("data/keywords.json")
f = open("data/custom.geo.json")
geojson = json.load(f)

countries = df.explode("type")[df.explode("type")["type"] == "country"]
countries = countries.drop_duplicates(subset = ["name"])

de = df[df.country_code == "de"]

color_scale = px.colors.sequential.Redor_r
height = 600

margins = {"t": 0, "b": 0, "r": 0, "l": 0}

#---------------------------------------------------------------------------------------------------------------------------------
#the figures
#choropleth map
fig1 = px.choropleth_mapbox(
    countries, geojson = geojson, locations="iso_3", featureidkey = "properties.iso_a3", 
    mapbox_style = "carto-positron", color = "score", color_continuous_scale=color_scale,
    height = height, custom_data=["keyword", "score"]
    )
fig1.update_traces(
    marker = {"opacity": 0.5},
    hovertemplate = "<b> %{customdata[0]} </b>: %{customdata[1]}" 
)
fig1.update_mapboxes(
    zoom = 2,
    center = {"lat": 27, "lon": -18},
)

#general figure layouts
fig1.update_layout(
    margin = margins,
    title = None,
    #coloraxis_showscale = False,
    paper_bgcolor = "#f4f4f4",
    plot_bgcolor = "#f4f4f4",
)

fig1.update_coloraxes(colorbar = dict(
    x = 0,
    xpad = 0,
    ypad = 0,
    tickfont = {"color": "white"},
    ticklabelposition = "inside top",
    ticks = "inside",
    tickcolor = "white",
    title = None,
    thickness = 20,
    ticklen = 15,
    nticks = 5,
))

#bubble map
fig2 = px.scatter_mapbox(
        df, lat = "lat", lon = "lon", mapbox_style="carto-positron", custom_data=["keyword"],
        color = "score",size = "score", color_continuous_scale = color_scale,
        height = height
        )
        
fig2.update_mapboxes(
    zoom = 2,
    center = {"lat": 32, "lon": 53},
)
fig2.update_traces(
    hovertemplate = "<b> %{customdata[0]} </b>: %{marker.size}" ,
)

#general figure layout
fig2.update_layout(
    margin = margins,
    title = None,
    paper_bgcolor = "#f4f4f4",
    plot_bgcolor = "#f4f4f4",
)
fig2.update_coloraxes(colorbar = dict(
    x = 0,
    xpad = 0,
    ypad = 0,
    tickfont = {"color": "white"},
    ticklabelposition = "inside top",
    ticks = "inside",
    tickcolor = "white",
    title = None,
    thickness = 20,
    ticklen = 15,
))




#density map
fig3 = px.density_mapbox(de, lat = "lat", lon = "lon", z = "score", mapbox_style="carto-positron",
        color_continuous_scale = color_scale, height=height,custom_data=["keyword"],
        )
fig3.update_mapboxes(
    zoom = 4.5,
)
fig3.update_traces(
    hovertemplate = "<b> %{customdata[0]} </b>: %{z}" ,
)

#general figure 

fig3.update_layout(
    margin = margins,
    title = None,
    paper_bgcolor = "#f4f4f4",
    plot_bgcolor = "#f4f4f4",
)
fig3.update_coloraxes(colorbar = dict(
    x = 0,
    xpad = 0,
    ypad = 0,
    tickfont = {"color": "white"},
    ticklabelposition = "inside top",
    ticks = "inside",
    tickcolor = "white",
    title = None,
    thickness = 20,
    ticklen = 15,
    nticks = 5,
))

#-----------------------------------------------------------------------------
#the layout
layout = html.Div(children = [
    dcc.Tabs(
        parent_className= "custom-tabs", className = "custom-tabs-container",
        mobile_breakpoint = 0,
        children = [

        dcc.Tab(
            className = "custom-tab", selected_className = "custom-tab--selected",
            label = "Weltkarte",
            children = [
                html.Div(className = "row content-container", children = [
                    #sidenotes
                    html.Div(className = "three columns pretty-container", children = [
                        html.P("Weltkarte der Schlagwörter", className = "title"),
                        html.H5("geographische Schlagworte visualisert", className = "header"),
                        html.P(""" Alle 1600 geographischen Schlagworte der Zeit auf die Karte gebracht.
                        Je größer und heller ein Punkt, desto höher der von der ZEIT vergebene Score. """)

                    ]),

                    #bubble mpa
                    html.Div(className = "nine columns pretty-container", children = [
                        dcc.Graph(
                            figure = fig2, config = {"displayModeBar": False, "responsive" : False}
                        ),
                    ], style = {"padding": "1%"}),

                ]),
            ]),     

        dcc.Tab(
            className = "custom-tab", selected_className = "custom-tab--selected",
            label = "Ländervergleich",
            children = [
                html.Div(className = "row content-container", children = [
                    #sidenotes
                    html.Div(className = "three columns pretty-container", children = [
                        html.P("Kartenansicht", className = "title"),
                        html.H5("Länderkarte", className = "header"),
                        html.P("""Die Zeit sortiert Länder automatisch nach ihrem Score.
                        Diese Karte zeigt die verschiedenen Scores der Meisten Länder der Welt """)

                    ]),

                    #point map
                    html.Div(className = "nine columns pretty-container", children = [
                        dcc.Graph(
                            figure = fig1, config = {"displayModeBar": False, "responsive" : False}
                        ),
                    ], style = {"padding": "1%"}),

                ]),
        ]),

        dcc.Tab(
            className = "custom-tab", selected_className = "custom-tab--selected",
            label = "Deutschland",
            children = [
                html.Div(className = "row content-container", children = [
                    #sidentoes
                    html.Div(className = "six columns pretty-container", children = [
                        html.P("Kartenansicht", className = "title"),
                        html.H5("Deutschland-Karte", className = "header"),
                        html.P("""Auch für Deutschland speziell, in dem die meisten Schlagworte liegen,
                        lässt sich die Verteulung gut darstellen. Insbesondere der Südwesten stich hier hervor""")

                    ]),
                    
                    #deutschland karte
                    html.Div(className = "six columns pretty-container", children = [
                        dcc.Graph(
                            figure = fig3, config = {"displayModeBar": False, "responsive" : False}
                        ),
                    ], style = {"padding": "1%"}),

                ]),
            ]),


    ]), 

    html.Hr(className = "vertical"),
    
    html.Div(className = "text-container", children = [
        html.H6("Kartenansichten", className = "title"),

        html.H1("Schlagwörter der Welt", className = "header"),

        html.P(""" Der Fokus der Zeit liegt vor allem im europäischen Kontext, vor allem im deutschen Raum beispielsweise
        mit Berlin, welches ein Score von 99/100 Punkten hat,
        Jedoch auch bekannte Regionen wie die Ostküste der USA mit New York(97) als auch Südostasien sind hervorgehoben. Regionen,
        die man sonst auch eher aus einem negativen Kontext kennt, wie Syrien(98) oder Irak(95) stehen im Fokus.
        In Deutschland ist vor allem das Ruhrgebiet eine Konzentrationsfläche wie auch der gesamte Südwesten, während Brandenburg 
        und Mecklenburg Vorpommern eher weniger dicht gepunktet sind.

        """),
        #funktionsweise
        html.Div(className = "pretty-container", children = [
            html.H6("Funktionsweise", className = "title"),
            html.P(""" Alle Artikel der Zeit werden mit mehreren Schlagworten versehen, die alle einen Typus wie Ort, Person, Organisation
            bekommen. Bei den Karten werden alle 1600 geographischen Schlagworte mithilfe von Mapbox geocodiert (augrund des Namens den
            Längen- und Breitengrad suchen) und auf eine Karte gebracht. Diese Karte nutzt Kartendaten von Carto und plotly
            """),
         ])
    ]),

])
