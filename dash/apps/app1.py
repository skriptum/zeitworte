# %%
# all the import statements
import zeit
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html

from app import app, db, engine



# %%
def plotter(dictionary):
    """ plot a dictionary of type {title : timeseries}"""
    fig = go.Figure()
    colors = [
        "rgba(252, 191, 73, 1)", #yellow
        "rgba(214, 40, 40, 1)",  #red
        "rgba(129, 15, 128, 1)", #purple
        "rgba(22, 88, 177, 1)", #blue
        "rgba(6,85,24,1)", #green
        "rgba(1,43, 61, 1)" #dark
        ]

    for i, (w, ts)  in enumerate(dictionary.items()):
        # ts = api.search_for(k, limit=0, facet_time="1year")
        fig.add_traces(go.Scatter(
            x = ts.index, y = ts.values, 
            mode = "lines", fill = "tozeroy", name = w,
            fillcolor = f"{colors[i][:-2]}0.1)",
            ))


    #styling
    fig.update_layout(
        paper_bgcolor = "#f4f4f4",
        font = {"color":"#181818", "family" : "futura", "size": 13 },
        showlegend = True,
        plot_bgcolor = "#f4f4f4",
        margin = {"t": 0, "b": 0, "l": 0, "r": 0},
        xaxis_title = "Jahr",
        yaxis_title = "Erwähnungen",
        hovermode = "x unified", 
        hoverlabel = {"bgcolor": "white"},
        colorway = colors,
        legend = dict(
            bgcolor = "rgba(0,0,0,0)",
            title = "Legende",
            x = 0, y = 1,
            bordercolor = "#f4f4f4",
            borderwidth = 1,
        ),)


    fig.update_yaxes(ticklabelposition="inside top", title = None,
        gridcolor = "lightgrey", nticks = 4)

    fig.update_xaxes(
        rangeslider_visible=True, ticklabelposition="inside top",
        showspikes = True, spikecolor = "grey", spikethickness = 2, spikemode = "across", 
        spikedash = "solid",
        linecolor = "lightgray",
        showgrid = False,
        title = "Zeitrahmen einstellen",
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1J", step="year", stepmode="backward"),
                dict(count=10, label="10J", step="year", stepmode="backward"),
                dict(label = "alles", step="all")
            ]),
            font = {"size": 8},
            bgcolor = "#f4f4f4",
            activecolor = "#c1c1c1",
            bordercolor = "grey", borderwidth = 1,

            ),
        
        )

    fig.update_traces(
        hovertemplate = "%{y}"
    )

    return fig

# %%
def get_objs(list_of_keywords, time = "1year"):
    """ function to query the database """
    list_of_objs = []

    for w in list_of_keywords:
        query = db.select([table]).filter(table.columns.uri.like(f"%{w}%")).order_by(db.desc(table.columns.results))

        ResultProxy = con.execute(query)
        result = ResultProxy.fetchall()

        series = pd.Series(result[0])
        series.name = series.lexical
        list_of_objs.append(series)
    
    return list_of_objs

#%%
def serializer(dataframe):
    """ function to extract the timeseries and sort them from a pandas DataFrame
    then make a figure from them"""
    sum_dict ={}

    for i in range(len(dataframe)):
        s = dataframe.iloc[i].squeeze()
        name = s.lexical
        results = s.results

        ts = pd.read_json(s.json, typ = "series", orient = "records")
        ts.index = pd.to_datetime(ts.index, unit = "ms")
        
        sum_dict[results] = (name, ts)
        

    #srt the dictionary ascending
    plot_dict = {value[0]:value[1] for key, value in sorted(sum_dict.items(), key=lambda item: item[0], reverse=True)}
    
    return plot_dict

# %%
def object_info(dataframe):
    """ takes a dataframe, returns a list of divs"""

    try:
        width = (100 / len(dataframe) ) -3 #if dataframe has no data
        if width < 23:
            width = 30
    except:
        width = "inherit"

    children = []
    for i in range(len(dataframe)):
        series = dataframe.iloc[i].squeeze()
        div = html.Div(style = {"width": f"{width}%"},className = "preview-box columns pretty-container", children = [
            html.H3(series.lexical, className = "header"),
            html.P(children = [f"{series.results} Artikel"], className = "title"),
            html.P(children = [f"Typus: {series.type}"], className = "title"),
            html.Hr(className = "vertical"),

            html.A(children = [
                    html.P(series.matches["title"], className = "header"),
                    ], href = series.matches["href"], target = "_blank",
                ),

            html.P(series.matches["teaser_text"]),

            # html.Hr(className = "vertical"),
        ]) 
        children.append(div) 

    return children

def auswahler(index_list):
    """ take a list, convert it to some boxes in different colors"""
    colors = colors = [
        "rgba(252, 191, 73, 1)", #yellow
        "rgba(214, 40, 40, 1)",  #red
        "rgba(129, 15, 128, 1)", #purple
        "rgba(22, 88, 177, 1)", #blue
        "rgba(6,85,24,1)", #green
        "rgba(1,43, 61, 1)" #dark
        ]
    children = [html.H4("Auswahl (max. 6)", className = "header")]
    for i, name in enumerate(index_list):
        children.append(
            html.Div(className = "auswahl-box", children = [str(name)],
            style = {"border-color": colors[i], "background-color": f"{colors[i][:-2]}0.5)"})
        )
    return html.Div(children)
#%%

#Postgres 
con = engine.connect()
metadata = db.MetaData()
table = db.Table("keyword", metadata, autoload=True, autoload_with=engine)

#the startup selection
startup_df = pd.read_json("data/startup.json") #read the file
startup_plot_dict = serializer(startup_df)
startup_fig = plotter(startup_plot_dict)
startup_text = startup_df.to_json()

# %%


layout = html.Div(children = [
     
    html.Div(className = "row", style = {"padding": "5%", "padding-bottom": "0"},children = [
        #search bar
        html.Div(className = "search-bar pretty-container", children = [
            html.P(id = "number-output1", className = "title", style = {"font-size": "9pt"}),

            dcc.Input(
                id = "input1",type = "text", placeholder = "Suche Schlagwörter", value = "",
                style = {"width": "100%"}
            ),
            
            html.Div(id = "search-output1"),
            

        ],style = {"padding-bottom": "0%"}),
        html.Div(style = {"padding-top": "0%"},className = "pretty-container", children = [
            #auswahl
            html.Div(id = "selected-output"),
            html.Button("Zurücksetzen", id = "clear-button1", n_clicks=0),
        ])

    ]),
    html.Div(id = "hidden-div-output", style = {"display": "none"}),
    html.Div(id = "hidden-div-output2", style = {"display": "none"}, 
            children = startup_text,
            ),

    #the graphing
    dcc.Tabs(
        parent_className= "custom-tabs", className = "custom-tabs-container",
        mobile_breakpoint = 0,
        children = [

        #the worte tab
        dcc.Tab(
            className = "custom-tab", selected_className = "custom-tab--selected",
            label = "Zeitworte", children = [
            #the trender
            html.Div(className = "row content-container", children = [
                #article sidenotes
                html.Div(className = "four columns pretty-container", children = [
                    html.H6("Zeitworte", className = "title"),
                    html.H1("ZEITVergleich", className = "header"),
                    html.P("""Durchsuche die 16.000 Schlagworte der Zeit und vergleiche ihre 
                    Nutzung über die letzten Jahrzente. Voreingestellt sind
                    """),
                ]),
                
                #Graph
                html.Div(className = "eight columns pretty-container", children = [

                    dcc.Graph(id = "graph1",
                    config = {"displayModeBar": False, "responsive" : False}
                    ),
                ]),

            ]), 
        ]),

        #the wortanalyse tab
        dcc.Tab(
            className = "custom-tab", selected_className = "custom-tab--selected",
            label = "Wortanalyse", children = [
                html.Div(className = "row content-container", children = [
                    html.Div(id = "output1")
                ])
         
        ]),

        
    ]),
    html.Hr(className = "vertical"),
    
    html.Div(className = "text-container", children = [
        html.H6("Zeitvergleich", className = "title"),

        html.H1("Schlagworte über die Zeit", className = "header"),

        html.P(""" Die Schlagworte der ZEIT, interaktiv visualisiert und nach eigenen Kriterien aussuchbar.
        Die Zeit hat etwa 16.000 Schlagwörter, mit denen sie Artikel versehen, gesammelt über einen Zeitraum von
        75 Jahren. Diese Website macht den interaktiven Vergleich von verwandten oder völlig fremden Schlagwörtern
        möglich, beispielsweise den Kampf zwischen Armin Laschet, Friedrich Merz und Norbert Röttgen und vieles mehr.
        """),
        html.Div(className = "pretty-container", children = [
            html.H6("Funktionsweise", className = "title"),
            html.P(""" Alle 16.000 Schlagwörter sind von der Zeit-Website abgefragt worden, inklusiove der Typen. Daraufhin
            werden Zeitreihen der Schlagwörter erstellt und in einer Datenbank gespeichert, auf die diese Website zugreift.
            Zu jedem Schlagwort wird außerdem ein Artikel ausgewählt, der im zweiten Tab dargestellt wird.
            """)
        ])
    ]),

])


@app.callback(
    dash.dependencies.Output("search-output1", "children"),
    dash.dependencies.Output("number-output1", "children"),
    dash.dependencies.Output("hidden-div-output", "children"),

    dash.dependencies.Input("input1", "value"),
)
def search_database(value):

    #beginning state
    if value == "":
        buttons = [ html.Button("Niet", style = {"display": "none"}, id = f'search_button{i}', n_clicks=0) for i in range(5)]
        return html.Div(children = buttons), "", "{}"

    #query the database
    query = db.select([table]).filter( #SELECT * FROM table WHERE 
        table.columns.lexical.ilike(f"%{value}%"), #lexical LIKE '%word%'
        ).order_by(db.desc(table.columns.results)).limit(5) #ORDER BY results DESC LIMIT 5
    ResultProxy = con.execute(query)
    result = ResultProxy.fetchall() 

    count = len(result)

    #check the reuslts
    if count == 0:
        buttons = [ html.Button("Niet", style = {"display": "none"}, id = f'search_button{i}', n_clicks=0) for i in range(5)]

        return html.Div(children = buttons), "Keine Ergebnisse", "{}"


    #create the dataframe
    df = pd.DataFrame(result, columns=result[0].keys())
    output = []
    for i in range(count):
        row = df.loc[i]
        div = html.Div(children = [
            html.Button(children = row.lexical, id = f'search_button{i}', n_clicks=0, className = "search-box")
        ])
        output.append(div)

    #extra not shown buttons
    for i in range(count, 5, 1):
        output.append(html.Button("Niet", style = {"display": "none"}, id = f'search_button{i}', n_clicks=0))

    if count == 1:
        anzeige = "Das Beste Ergebnis wird angezeigt"
    else:
        anzeige = f"Die Top {count} Ergebnisse werden angezeigt"
    return html.Div(children = output), anzeige, df.to_json()




@app.callback(
    dash.dependencies.Output("graph1", "figure"), #the figure
    dash.dependencies.Output("hidden-div-output2", "children"), #the current selected dataframe store
    dash.dependencies.Output("output1", "children"), #the article overview
    dash.dependencies.Output("selected-output", "children"), #the overview over your selected things

    #buttons
    dash.dependencies.Output("clear-button1", "n_clicks"),  #the clear button

    dash.dependencies.Output("search_button0", "n_clicks"),
    dash.dependencies.Output("search_button1", "n_clicks"),
    dash.dependencies.Output("search_button2", "n_clicks"),
    dash.dependencies.Output("search_button3", "n_clicks"),
    dash.dependencies.Output("search_button4", "n_clicks"),

    # inputs
    dash.dependencies.Input("hidden-div-output", "children"), #the json of the search dataframe
    dash.dependencies.Input("hidden-div-output2", "children"), #json of the of the selected dataframe


    #buttons
    dash.dependencies.Input("search_button0", "n_clicks"),
    dash.dependencies.Input("search_button1", "n_clicks"),
    dash.dependencies.Input("search_button2", "n_clicks"),
    dash.dependencies.Input("search_button3", "n_clicks"),
    dash.dependencies.Input("search_button4", "n_clicks"),

    dash.dependencies.Input("clear-button1", "n_clicks"), #the clear button

)
def get_data(data, selected, btn0, btn1, btn2, btn3, btn4, clear):

    #reading in the search result dataframe
    try:
        df = pd.read_json(data)
    except Exception:
        return None, selected.to_json(), "", "Nichts ausgewählt", clear, btn0, btn1, btn2, btn3, btn4

    #the dataframe for the current selected things
    selected = pd.read_json(selected)

    if btn0 > 0:
        series = df.loc[0]
        selected = selected.append(series.to_frame(name = series.lexical).T)
        btn0 = 0

    elif btn1 > 0:
        series = df.loc[1]
        selected = selected.append(series.to_frame(name = series.lexical).T)
        btn1 = 0
    elif btn2 > 0:
        series = df.loc[2]
        selected = selected.append(series.to_frame(name = series.lexical).T)
        btn2 = 0
    elif btn3 > 0:
        series = df.loc[3]
        selected = selected.append(series.to_frame(name = series.lexical).T)
        btn3 = 0
    elif btn4 > 0:
        series = df.loc[4]
        selected = selected.append(series.to_frame(name = series.lexical).T)
        btn4 = 0

    if clear > 0:
        selected = selected[0:0]
        clear = 0
    
    
    selected = selected.drop_duplicates(subset = "uri").sort_values("results", ascending=False) 
    selected_json = selected.to_json()

    plot_dict = serializer(selected)
    figure = plotter(plot_dict)

    articles = object_info(selected)

    auswahl = auswahler(selected.lexical)


    return figure, selected_json, html.Div(children = articles), auswahl,  clear, btn0, btn1, btn2, btn3, btn4
    
