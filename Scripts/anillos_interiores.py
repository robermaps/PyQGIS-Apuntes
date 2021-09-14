## Este script crea un buffer interior para cada entidad de la capa de entrada
## y realiza la diferencia espacial entre ambos para obtener un anillo interior
##

## Módulos
from qgis.core import *  
from qgis.utils import *

## Capa de entrada
ruta = 'C:\\ruta'
capa_entrada = QgsVectorLayer(ruta, "entidades_de_entrada2", "ogr")
CRS = capa_entrada.crs().postgisSrid()

## Capa nueva temporal
uri =  "MultiPolygon?crs=epsg:"+ str(CRS) + "&field=id:integer""&index=yes"
capa_anillos = iface.addVectorLayer(uri, "diferencias", "memory")

## Inicio de la edición y del contador para el campo id
capa_anillos.startEditing()   
id = 0  

for f in capa_entrada.getFeatures():   ## Bucle para iterar sobre las entidades de la capa
    geom = f.geometry()   ## Creación del objeto con la geometría de la entidad
    buffer = geom.buffer(-1000,-1)   ## Creación de buffer interior de 1000m
    diferencia = geom.difference(buffer)   ## Creación de la diferencia entre el buffer interior y la entidad
    entidad = QgsFeature()   ## Creación de la entidad vacía
    entidad.setGeometry(diferencia)   ## Añadir la geometría del anillo a la entidad vacía
    entidad.setAttributes([id])   ## Añadir el id a la entidad
    capa_anillos.addFeatures([entidad])   ## Añadir la entidad a la capa temporal
    id += 1 
    
capa_anillos.commitChanges()   ## Guardar los cambios
