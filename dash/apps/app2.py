
import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.express as px
import json

df = pd.read_json("data/keywords.json")
f = open("data/custom.geo.json")
geojson = json.load(f)

countries = df.explode("type")[df.explode("type")["type"] == "country"]
countries = countries.drop_duplicates(subset = ["name"])

de = df[df.country_code == "de"]

color_scale = px.colors.sequential.Redor_r
height = 600

margins = {"t": 0, "b": 0, "r": 0, "l": 0}

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

#
#app = dash.Dash(assets_folder="../assets")

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
                    html.Div(className = "nine columns pretty-container", children = [
                        dcc.Graph(
                            figure = fig2, config = {"displayModeBar": False, "responsive" : False}
                        ),
                    ], style = {"padding": "1%"}),

                    html.Div(className = "three columns pretty-container", children = [
                        html.P("Kartenansicht", className = "title"),
                        html.H5("Karte", className = "header"),
                        html.P("YOLO lorem ipsum")

                    ])
                ]),
            ]),     

        dcc.Tab(
            className = "custom-tab", selected_className = "custom-tab--selected",
            label = "Ländervergleich",
            children = [
                html.Div(className = "row content-container", children = [
                    html.Div(className = "nine columns pretty-container", children = [
                        dcc.Graph(
                            figure = fig1, config = {"displayModeBar": False, "responsive" : False}
                        ),
                    ], style = {"padding": "1%"}),

                    html.Div(className = "three columns pretty-container", children = [
                        html.P("Kartenansicht", className = "title"),
                        html.H5("Karte", className = "header"),
                        html.P("YOLO lorem ipsum")

                    ])
                ]),
        ]),

        dcc.Tab(
            className = "custom-tab", selected_className = "custom-tab--selected",
            label = "Deutschland",
            children = [
                html.Div(className = "row content-container", children = [
                    html.Div(className = "six columns pretty-container", children = [
                        dcc.Graph(
                            figure = fig3, config = {"displayModeBar": False, "responsive" : False}
                        ),
                    ], style = {"padding": "1%"}),

                    html.Div(className = "six columns pretty-container", children = [
                        html.P("Kartenansicht", className = "title"),
                        html.H5("Karte", className = "header"),
                        html.P("YOLO lorem ipsum")

                    ])
                ]),
            ]),


    ]), 

    html.Hr(className = "vertical"),
    
    html.Div(className = "text-container", children = [
        html.H6("Beispiel", className = "title"),

        html.H1("Lorem Ipsum", className = "header"),

        html.P("""Et incidunt molestiae cupiditate totam neque. Pariatur cupiditate illo aut molestias exercitationem 
                oluptatem delectus reprehenderit. Fugit laborum dolorum quia. Est vel laudantium molestias nihil explicabo. 
                Deleniti sit ullam quaerat qui fugit sunt iure quia. Quod aut rerum quaerat architecto vero.

                Ut et iusto odio fugit et error repellendus. Ea officia dolor assumenda voluptatum ut sequi. 
                Aut laborum dignissimos labore esse illo saepe. Cum sapiente rerum suscipit sint et.

                Hic et magnam accusantium et sit. Neque eveniet alias sit aut autem. Molestiae provident nemo commodi est 
                ipsum fuga aut similique.

                Recusandae nostrum perferendis dicta. Sint deleniti voluptatem dicta et. Quod totam excepturi qui molestias. 
                Maiores ullam culpa sit laudantium numquam et accusamus nihil. Nihil illo ipsum et officia soluta sed nobis maiores. 
                Non ea fuga qui quas earum tempore veritatis.""")
    ]),

])

#app.run_server()