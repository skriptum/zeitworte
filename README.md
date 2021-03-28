# Zeitworte App

a multiPage Web App analysing many different things using the Zeit Online API and the python package. 

### Functions

- Analyse usage of different keyword over time and compare them
- visualize the geographical distribution of keywords using the Mapbox Geocode API
- get interesting information about the Authors who have written for the ZEIT

### Used Technologies

1. Call the *ZEIT API* for every keyword and the score
2. Save everything in a heroku *Postgres Database* using SQLAlchemy
3. Read the Database based on User Input in the *Dash* App
4. get geographical Keyword informatio  via the *Mapbox Geocoding API*
5. plot geographical Keywords using *plotly* and *carto* base maps