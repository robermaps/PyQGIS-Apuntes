## Con este script se obtiene la superficie de cada entidad de una primera 
## capa que no coincide espacialmente con ninguna entidad de la segunda capa.
## El resultado se almacena en una capa temporal junto a un ID para cada nueva entidad.
##

from qgis.core import *  
from qgis.utils import *

ruta1 = 'C:\\ruta1'
ruta2 =  'C:\\ruta2'
capa_entrada1 = QgsVectorLayer(ruta1, "entidades_de_entrada", "ogr")
capa_entrada2 = QgsVectorLayer(ruta2, "entidades_de_entrada2", "ogr")
CRS = capa_entrada1.crs().postgisSrid()

uri =  "MultiPolygon?crs=epsg:"+ str(CRS) + "&field=id:integer""&index=yes"
capa_diferencia = iface.addVectorLayer(uri, "diferencias", "memory")

capa_diferencia.startEditing()   
id = 0  

for f1 in capa_entrada1.getFeatures():
    diff_geom = f1.geometry()
    for f2 in capa_entrada2.getFeatures():
        if diff_geom.intersects(f2.geometry()):
            diff_geom = diff_geom.difference(f2.geometry())
    entidad = QgsFeature()
    entidad.setGeometry(diff_geom)
    entidad.setAttributes([id])
    capa_diferencia.addFeatures([entidad])
    id += 1 
capa_diferencia.commitChanges()
