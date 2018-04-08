# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 20:13:21 2018

@author: srodriguezl
"""

import requests
import json
import pandas as pd
import time

BASE_URL = "https://opendata.aemet.es/opendata"
APIQUERY={"api_key":APIKEY}
HEADERS = {'cache-control': "no-cache"}

#########################################################################
# Base de datos AEMET: Inventario estaciones
# Empleada para extraer todas los identificadores de las estaciones

estaciones_url = BASE_URL+"/api/valores/climatologicos/inventarioestaciones/todasestaciones"
resp = requests.request("GET",estaciones_url,headers=HEADERS,params=APIQUERY)
print(resp.status_code)
#Si es 200 es que la request ha ido bien.

info = json.loads(resp.text)
info

DATA = json.loads(requests.get(info["datos"]).text)
METADATA = json.loads(requests.get(info["metadatos"]).text)

# Extraigo el listado de todas los id de estacion (indicativo)
list_id_estaciones = [x['indicativo'] for x in DATA] 
nombre_estaciones = [x['nombre'] for x in DATA] 
provincia_estaciones = [x['provincia'] for x in DATA] 
estaciones_meteo = pd.DataFrame(
    {'id': list_id_estaciones,
     'nombre': nombre_estaciones,
     'provincia': provincia_estaciones
    })


#########################################################################
# Base de datos AEMET: Valores climatológicos normales 
# http://www.aemet.es/es/serviciosclimaticos/datosclimatologicos

tempMin= []
tempMax = []
numDiasLluvia = []
numDiasTempMax30 = []
numDiasTempMin0 = []

val_normales_url_base = BASE_URL + "/api/valores/climatologicos/normales/estacion/"
for idestacion in list_id_estaciones: 
    print(idestacion)
    #idestacion = "9434"
    val_normales_url = val_normales_url_base + idestacion
    resp = requests.request("GET",val_normales_url,headers=HEADERS,params=APIQUERY)
    print(resp.status_code)
    if resp.status_code !=200:
        break;
    #Si es 200 es que la request ha ido bien.
    
    info = json.loads(resp.text)
    info
    
    DATA = json.loads(requests.get(info["datos"]).text)
    METADATA = json.loads(requests.get(info["metadatos"]).text)
    
    # Leyendo en el metadata vemos que nos vamos a quedar con el mes 13 (id: mes)
    # y con la siguiente info
    # media temp min: ta_min_md
    # media temp max: ta_max_md
    # media num dias lluvia:  n_llu_md
    # numdiastemp<0: nt_00_md
    # numdiastemp>30: nt_30_md
    if DATA[12]["mes"] != "13" :
        print("no es resumen anual, para estacion" + idestacion)
    tempMin.append(DATA[12]["ta_min_md"])
    tempMax.append(DATA[12]["ta_max_md"])
    numDiasTempMax30.append(DATA[12]["nt_30_md"])
    numDiasTempMin0.append(DATA[12]["nt_00_md"])
    numDiasLluvia.append(DATA[12]["n_llu_md"])
    
    time.sleep(10)

estaciones_meteo["tempMin"] = tempMin
estaciones_meteo["tempMax"] = tempMax
estaciones_meteo["numDiasTempMax30"] = numDiasTempMax30
estaciones_meteo["numDiasTempMin0"] = numDiasTempMin0
estaciones_meteo["numDiasLluvia"] = numDiasLluvia

# mirando directamente en la web ves que hay estaciones que no tienen valores normales asociados
# 
# por lo que decides borrar esos registros.
idborrar = (estaciones_meteo.tempMin == "") & (estaciones_meteo.tempMax == "") & (estaciones_meteo.numDiasTempMax30 == "") & (estaciones_meteo.numDiasTempMin0 == "") & (estaciones_meteo.numDiasLluvia == "")
estaciones_meteo_clean = estaciones_meteo.loc[~idborrar,:]

# Save dataframe csv
estaciones_meteo_clean.to_csv("HistWeather.csv",sep=";",
                              header="True",index="False")

#########################################################################
# Base de datos AEMET: Valores climatologicos diarios 
# --> COMO MAXIMO EN UNA PETICION TE DEVUELVE 31 DÍAS.
# Te presenta para cada estación y para cada día la información que se detalla en METADATA
# velocidad media viento, temp max y min, horas de temp max y min, presiones,....
def formatFecha(year,month=1,day=1,hour=0,minute=0,second=0):
    date = str(year)+"-"
    date += "{:02d}".format(month)+"-"
    date += "{:02d}".format(day)+"T"
    date += "{:02d}".format(hour)+"%3A"
    date += "{:02d}".format(minute)+"%3A"
    date += "{:02d}".format(second)+"UTC"
    return date
#test:
#print(formatFecha(2018))
#print(formatFecha(2018,1,1,23,45,52))


climatologia_url_base=BASE_URL+"/api/valores/climatologicos/diarios/datos/fechaini/{fechaIniStr}/fechafin/{fechaFinStr}/todasestaciones"
climatologia_url = climatologia_url_base.format(fechaIniStr=formatFecha(2015,12,10),fechaFinStr=formatFecha(2015,12,31,23,59,59))

resp = requests.request("GET",climatologia_url,headers=HEADERS,params=APIQUERY)
print(resp.status_code)
info = json.loads(resp.text)
info

DATA = json.loads(requests.get(info["datos"]).text)
METADATA = json.loads(requests.get(info["metadatos"]).text)
DATA

from pandas.io.json import json_normalize
OneMonthData = json_normalize(DATA)
