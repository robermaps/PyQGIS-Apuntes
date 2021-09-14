## Este script crea una nueva capa que almacena la geometría de las intersecciones entre las entidades de dos capas de entrada, 
## es decir, con la superficie que ambas capas tienen en común. Ambas capas de entrada deberán ser de tipo poligonal.
## Las entidades creadas se almacenan junto a un ID.
## 

## Módulos 
from qgis.core import *  
from qgis.utils import *

## Cargar capas vectoriales de entrada
ruta1 = 'C:\\ruta'
ruta2 =  'C:\\ruta2'
capa_entrada1 = QgsVectorLayer(ruta1, "entidades_de_entrada", "ogr")
capa_entrada2 = QgsVectorLayer(ruta2, "entidades_de_entrada2", "ogr")
CRS = capa_entrada1.crs().postgisSrid()

## Creación de capa temporales en la que almacenar las nuevas geometrías
uri =  "MultiPolygon?crs=epsg:"+ str(CRS) + "&field=id:integer""&index=yes"
capa_intersecciones = iface.addVectorLayer(uri, "intersecciones", "memory")

capa_intersecciones.startEditing()   ## Comenzar la edición de la capa temporal
id = 0   ## Valor id que se le asignará a cada nueva entidad

for f1 in capa_entrada1.getFeatures():   ## Bucle para obtener las entidades de la capa de entrada 1
    for f2 in capa_entrada2.getFeatures():   ## Bucle para obtener las entidades de la capa de entrada 2
        if f1.geometry().intersects(f2.geometry()):
            interseccion_geom = f1.geometry().intersection(f2.geometry())    ## Creación de la geometría de la intersección
            entidad = QgsFeature()    ## Creación de objeto de tipo Feature vacío 
            entidad.setGeometry(interseccion_geom)    ## Añadirle al objeto la geometría de la intersección
            entidad.setAttributes([id])    ## Añadirle al objeto el valor de la variable id
            capa_intersecciones.addFeatures([entidad])    ## Añadirle a la capa temporal la entidad
            id += 1    ## Aumentar el id al acabar cada paso del bucle

capa_intersecciones.commitChanges()    ## Guardar los cambios de la capa temporal
