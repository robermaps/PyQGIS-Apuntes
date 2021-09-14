# Este script permite seleccionar entidades de una capa aplicando 2 filtros:
# -- filtro de selección espacial basado en el extent de otra capa 
# -- filtro de selección por atributos con una expresion SQL
#
# El resultado se almacena en una capa nueva.
#

# Importación de módulos
from qgis.core import *  
from qgis.utils import *

ruta = 'C:\\ruta\\'

# Cargar capas
capa = QgsVectorLayer(ruta+'nombre_capa.shp','Mi capa','ogr')
AOI = QgsVectorLayer(ruta+'nombre_capa2.shp','Area de interes','ogr').extent() 

# Filtro atributos
expresion = QgsExpression('SQL')
filtro = QgsFeatureRequest(expresion) 

# Filtro epacial
filtro.setFilterRect(AOI)
seleccion = capa.getFeatures(filtro)

# Selección de entidades 
ids = [i.id() for i in seleccion]
capa.selectByIds(ids)

# Guardar la selección en una capa nueva tomando el nombre y el SRC de la capa original
QgsVectorFileWriter.writeAsVectorFormat(capa, ruta+capa.name()+'_seleccion.shp', 'UTF-8', capa.crs(), driverName="ESRI Shapefile", onlySelected = True)
