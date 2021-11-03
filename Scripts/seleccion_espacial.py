# Este script selecciona entidades de una capa cuando intersectan con otra capa


# Módulos 
from qgis.core import *  
from qgis.utils import *

ruta = 'C:\\ruta\\'

# Cargar capas
capa1 = QgsVectorLayer(ruta+"capa1.shp",'Mi capa 1','ogr')
capa2 = QgsVectorLayer(ruta+"capa2.shp",'Mi capa 2','ogr')

# Lista vacía que almacenará los ID
ids = []

# Bucles de iteración sobre las entidades
for f1 in capa1.getFeatures():
    for f2 in capa2.getFeatures():
          if f1.geometry().intersects(f2.geometry()):
                ids.append(f1.id())  # Actualización de la lista con los ID de las entidades que intersectan

# Seleccion usando el ID
municipios.selectByIds(ids)

