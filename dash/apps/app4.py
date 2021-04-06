import dash_core_components as dcc
import dash_html_components as  html

layout = html.Div(children = [
    html.Div(className = "text-container", children = [
        html.H6("Über", className = "title"),
        html.H1("Die ZEITWorte Seite", className = "header"),
        dcc.Markdown("""
        Diese Seite basiert auf der ZEIT-Website Schnittstelle, ist jedoch keineswegs von der Zeit,
        sondern von einem interessierten Leser, der anlässlich des 75ten Geburtstages der Zeit ein bisschen
        herumprobieren wollte. 

        Anhand der Daten, die die Zeit zur Verfügung stellt, lässt sich einiges ablesen, beispielsweise über die
        Autoren als auch die Themenauswahl, die so betrieben wird.
        """),
        html.Div(className = "pretty-container", children = [
            html.H6("Technische Funktionsweise", className = "title"),
            dcc.Markdown(""" 
            Die Zeit stellt für Interessierte eine Programmier Schnittstelle (**Content API**) bereit, über die man allerlei
            Metadaten abfragen kann, beispielsweise welche Schlagwörter es alles so gibt und wie viele (etwa 16.000).

            Alle Schlagwörter wurden in eine Datenbank (**PostgreSQL**) eingespeist, die auf Servern von Heroku läuft.

            Auf diese Datenbank greift dann wiederum diese Website zu und visualisiert sie mithilfe von **plotly** in **python**.
            Bei den Karten gibt es einen Zwischenschritt, dort werden geographische Schlagwörter mithilfe der
            Geocoding API von **Mapbox** den entsprechenden Koordinaaten zugeordnet und auf Kartendaten von **Carto**
            geplottet.

            Die ganze Website ist in Python in **Dash** geschrieben und läuft auf Servern von **Heroku**
            """)
        ])
    ])
])