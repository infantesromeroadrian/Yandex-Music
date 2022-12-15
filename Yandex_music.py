

# Contexto:
#En este proyecto compararemos las preferencias musicales de las ciudades de Springfield y Shelbyville. Se examinarán datos reales de Y.Music para comprobar las hipótesis que se exponen a continuación y comparar el uso de los usuarios de estas dos ciudades.


#Hipótesis:

#La actividad de los usuarios difiere según el día de la semana y dependiendo de la ciudad.

#las hipotesis que vamos a formular seran:

#Los lunes por la mañana, los habitantes de Springfield escuchan mas pop que los habitantes de Shelbyville.
#Los oyentes de Springfield y Shelbyville tienen preferencias distintas. En Springfield prefieren el pop mientras que en Shelbyville hay más aficionados al rap.
#%% md
# 2.0 IMPORTACION DE LIBRERIAS
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as np
#%% md
# 2.1 LECTURA DE DATOS
#%%
music = pd.read_csv('/Users/adrianinfantesromero/Desktop/AIR/Work/GitHub/Practicum/Music/music_project_en.csv')
music.head()
#%%
music.info()
#%% md
## 2.2 COMPROBACION DE DATOS NULOS
#%% md
CATEGORICOS
#%%
music.isnull().sum()
#%%
music['Track'].describe()
#%%
music['artist'].describe()
#%%
music['genre'].value_counts()
#%%
music['  City  '].value_counts()
#%%
music.columns
#%%
# quiero sustituir los valores nulos de la columna genre por los 10 generos mas escuchados
# primero vamos a ver cual es el genero mas escuchado

music['genre'].value_counts().head(10)
#%%
# ahora vamos a sustituir los valores nulos por los 10 generos mas escuchados de manera proporcional a la cantidad de veces que se escuchan

music['genre'].fillna(music['genre'].value_counts().index[0], inplace=True)

music['genre'].fillna(music['genre'].value_counts().index[1], inplace=True) # esto lo hago porque el primer genero es pop y el segundo es rock, y no quiero que se repitan los generos

music['genre'].fillna(music['genre'].value_counts().index[2], inplace=True)

music['genre'].fillna(music['genre'].value_counts().index[3], inplace=True)

music['genre'].fillna(music['genre'].value_counts().index[4], inplace=True)

music['genre'].fillna(music['genre'].value_counts().index[5], inplace=True)

music['genre'].fillna(music['genre'].value_counts().index[6], inplace=True)

music['genre'].fillna(music['genre'].value_counts().index[7], inplace=True)

music['genre'].fillna(music['genre'].value_counts().index[8], inplace=True)

music['genre'].fillna(music['genre'].value_counts().index[9], inplace=True)

# ahora vamos a ver si se han sustituido los valores nulos
#%%
music['genre'].isnull().sum()
#%% md
#El resto de datos nulos no los podemos reemplazar de una manera logica como genre ya que hay demasiados valores diferentes.
#%% md
# 3.0 PROCESAMIENTO DE TABLAS
#%%
music.rename(columns={'  City  ':'City_name'}, inplace=True)
#%%
music.columns = music.columns.str.lower()
#%%
music['time'].unique()
#%%
music['time'].value_counts()
#%%
music['time'] = pd.to_datetime(music['time'], format='%H:%M:%S')
#%%
music['time'] = music['time'].dt.time
#%%
music['time'] = music['time'].astype(str).str[0:2].astype(int)
#%%
music['time_of_day'] = music['time'].apply(lambda x: 'morning' if x >= 6 and x < 12 else 'afternoon' if x >= 12 and x < 18 else 'evening' if x >= 18 and x < 24 else 'night')
#%%
music
#%% md
# 4.0 ANALISIS DE DATOS
#%% md
## DATOS SIMPLES
#%%
music.groupby(['day'])['time'].count().reset_index().sort_values('time', ascending=False).reset_index(drop=True)
#%%
music['day'].value_counts().plot(kind='bar')
#%%
music.groupby('city_name')['city_name'].count()
#%%
music['city_name'].value_counts().plot(kind='bar')
#%%
music.groupby('time_of_day')['time_of_day'].count()
#%%
music['time_of_day'].value_counts().plot(kind='bar')
#%%
music['genre'].value_counts().plot(kind='bar', figsize=(20,10), fontsize=10, width=0.5)
#%% md
## DATOS COMPLEJOS
#%%
music.groupby(['day', 'time_of_day'])['time_of_day'].count().unstack().plot(kind='line', figsize=(20,10), fontsize=20)
#%% md
#Aqui ya tenemos datos de mayor calidad:
#- Observamos que independientemente de los dias el patron es el mismo por la tarde se escucha mas musica.
#- En 2o luegar por la noche.
#- En 3o lugar durante la mañana se escucha menos que en cualquier otro momento del dia.

#Por otro lado tambien tenermos los dias en grafica:
#- Siendo los Viernes los dias que mas se escucha.
#- Los Lunes en 2a posicion
#- Los miercoles observamos una caida drastica en el consumo de musica.
#%%
music.groupby(['day', 'city_name'])['city_name'].count().unstack().plot(kind='line', figsize=(20,10), fontsize=20)
#%% md
#Vemos los siguientes datos:
#- La ciudad de Springfield escucha mucha mas musica que la ciudad de Springfield
#- Tienen comportamientos totalmente diferenciados mientras que Springfield esucha el pico de musica los viernes y Lunes, Shelbyville es totalmente lo contrario esos mismos dias ellos tienen su punto mas bajo.
#- Los miercoles son el dia que menos musica escuhan los habitantes de la ciudad de Springfield mientras que en Shelbyville es el pico de musica.
#%% md
# 5.0 FORMULACION HIPOTESIS
#%% md
## 5.1 PRIMERA HIPOTESIS

#Vamos a formular hipotesis:

#- Los lunes por la mañana, los habitantes de Springfield escuchan mas pop que los habitantes de Shelbyville.

#- Primero hipotesis nula: los lunes por la mañana, los habitantes de Springfield escuchan la misma cantidad de pop que los habitantes de Shelbyville

#- Hipotesis alternativa: los lunes por la mañana, los habitantes de Springfield escuchan mas pop que los habitantes de Shelbyville

#- El valor alpha que vamos a establecer es de 0.05

#Vamos a hacer un test de chi cuadrado:


#Primero vamos a ver la cantidad de veces que escuchan musica los habitantes de Springfield y Shelbyville en cada momento del dia
#%%
music.groupby(['day', 'time_of_day', 'city_name'])['time_of_day'].count().unstack().apply(lambda x: x/x.sum()*100, axis=1).plot(kind='line', figsize=(20,10), fontsize=20, linewidth=5, markersize=20, marker='o')
#%% md
#Por otro lado vamos a analizar exactamente la cantidad de veces que escuchan pop en cada momento del dia ambas ciudades.
#%%
music.groupby(['city_name', 'time_of_day', 'genre'])['time_of_day'].count().unstack().apply(lambda x: x/x.sum()*100, axis=1)['pop'].plot(kind='bar', figsize=(20,10), fontsize=20)
#%% md
#Teniendo en cuenta que el valor alpha es de 0.05.

#El valor de Springfield es de 0.5, y que el valor de Shelbyville es de 0.4, podemos decir que la hipotesis nula es falsa, y que la hipotesis alternativa es verdadera, por lo que podemos decir que los lunes por la mañana, los habitantes de Springfield escuchan mas pop que los habitantes de Shelbyville.
#%% md
# 6.0 INSIGHTS
#%% md
#- Los viernes y lunes son los dias que mas se escucha musica.
#- En springfield se escucha mas musica que en shelbyville.
#- En las tardes y las noches se escuha mas musica que en la mañana.
#- El genero mas escuchado es el pop.
#- La dinamica de springfield es que el viernes es el pico de musica y va decayendo hastal el miercoles.
#- Mientras que en shelbyville es a la inversa.