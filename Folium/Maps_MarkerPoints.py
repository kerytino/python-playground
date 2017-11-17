# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 11:37:51 2017
Map with the information of the 10 most populated cities in Spain
Extract information from wikipedia and google maps

@author: srodriguezl
"""

import folium
import pandas as pd
from pygeocoder import Geocoder 
import os 
import time # to make time sleep

os.chdir("D:/github/python-playground/")

data = pd.read_html("https://es.wikipedia.org/wiki/Anexo:Municipios_de_Espa%C3%B1a_por_poblaci%C3%B3n",header = 0)
citiesPopulation = data[0]
citiesPopulation10 = citiesPopulation.iloc[0:10,]

res = []
for i in citiesPopulation10.loc[:,"Nombre"]:
    latlong = Geocoder.geocode(i + ", España").coordinates
    res.append(latlong)
    time.sleep(7)   # It seems that api google maps prefers not very fast requests

resdf = pd.DataFrame(res,columns=["lat","long"],index = citiesPopulation10.Nombre)
resdf.to_csv("LatLong10citiesSpain.csv")

#############################
# 1st option --> icon color 
# The possible values are: ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']

colors = ["black","darkred","red","lightred","orange","darkpurple","cadetblue","darkblue","blue","lightblue"]
# Empty map
m = folium.Map(location=[38,-6],tiles ="Stamen Terrain",zoom_start= 5, no_wrap = False) # all these values are not neccesaries you have by default values

for i in range (0,len(citiesPopulation10)):
    df = citiesPopulation.iloc[i,1:].to_frame(name = str(i+1) + " posicion")
    
    html = df.to_html()
    htmlPopUp = folium.Popup(html)
   
    folium.Marker(location=[res[i][0],res[i][1]], popup = htmlPopUp, 
                  icon =folium.Icon(color=colors[i],icon_color="blue")).add_to(m)
    
m.save("PopulationSpain10cities_colorIcon.html")              
              
#############################
# 2nd option --> icon 
m = folium.Map(location=[38,-6],tiles ="Mapbox Bright",zoom_start= 5, no_wrap = False) # all these values are not neccesaries you have by default values
icon_image = "population_sign.png"
for i in range (0,len(citiesPopulation10)):
    df = citiesPopulation.iloc[i,1:].to_frame(name = str(i+1) + " posicion")
    
    html = df.to_html()
    htmlPopUp = folium.Popup(html)
   
    folium.Marker(location=[res[i][0],res[i][1]], popup = htmlPopUp, 
                  icon = folium.features.CustomIcon(icon_image)).add_to(m)
    
m.save("PopulationSpain10cities_sign.html")              
  