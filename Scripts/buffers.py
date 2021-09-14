# Este script crea un buffer para cada entidad de una capa de entrada 
# y lo amacena en una capa temporal junto a un id
#

from qgis.core import *  
from qgis.utils import *

## Cargar capa vectorial de entrada y obtener su sistema de coordenadas
ruta = 'C:\\ruta\\'
capa_entrada = QgsVectorLayer(ruta, "entidades_de_entrada", "ogr")
CRS = capa_entrada.crs().postgisSrid()

## Creación de capa temporal en la que almacenar los buffers
uri =  "MultiPolygon?crs=epsg:"+ str(CRS) + "&field=id:integer""&index=yes"
capa_buffers = QgsVectorLayer(uri, "buffers", "memory")

capa_buffers.startEditing()   ## Comenzar la edición de la capa temporal
id = 0   ## Valor id que se le asignará a cada nueva entidad

for f in capa_entrada.getFeatures():   ## Bucle para obtener las entidades de la capa  de entrada
     geom = f.geometry()   ## Acceso a la geometría de cada entidad
     buffer = geom.buffer(200,-1)    ## Parámetros del buffer: 200 metros, nº segmentos automático
     entidad = QgsFeature()   ## Creación de objeto de tipo Feature vacío 
     entidad.setGeometry(buffer)    ## Añadirle al objeto la geometría del buffer
     entidad.setAttributes([id])    ## Añadirle al objeto el valor de la variable id
     capa_buffers.addFeatures([entidad])    ## Añadirle a la capa temporal la entidad
     id += 1    ## Aumentar el id al acabar cada paso del bucle

capa_buffers.commitChanges()    ## Guardar los cambios de la capa temporal
