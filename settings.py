import os

#Get and set DB credentialss
DB_HOST = os.environ.get('DASH_DB_HOST') or "nps-demo-instance.cofzod1dtat2.us-east-2.rds.amazonaws.com"
DB_NAME = os.environ.get('DASH_DB_NAME') or "ds4a_final"
DB_USER = os.environ.get('DASH_DB_USER') or "final_project"
DB_PASS = os.environ.get('DASH_DB_PASS') or "*m0yTEP3XP0H"

BAQ_CENTER_COORD = {"lat": 10.989849, "lon": -74.802680}


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoiYW1vcmVuby0iLCJhIjoiY2syZmprYXhxMGw2NzNsdDh0ajd0bGlpMyJ9.ikx1XJYapG9NpoSOYkskog"
mapbox_style = "mapbox://styles/amoreno-/ck2qdgwdn0jvd1cpcbn7kxaw7"


## Agregar un registro en el log si no se encuentra alguna de las variables
if not all([DB_HOST, DB_NAME, DB_USER, DB_PASS]):
    print('Variable de entorno no decladaras.. ')