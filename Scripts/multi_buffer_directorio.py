## Este script genera nuevas capas con buffers a distintas distancias 
## para cada uno de los archivos .shp que se encuentren en un directorio
##

import os
from qgis.core import *  
from qgis.utils import *

## Lista de capas
ruta = 'C:\\ruta\\'
archivos = os.listdir(ruta)

## Crear carpeta de resultados
if os.path.exists(ruta + "RESULTADOS\\"):
    print("El directorio ya existe")
    resultados = ruta + "RESULTADOS\\"
else:
    os.mkdir(ruta + "RESULTADOS\\")
    print("Directorio creado")
    resultados = ruta + "RESULTADOS\\"

## Bucles
for archivo in archivos:  ## Por cada archivo del directorio
  
    if os.path.splitext(archivo)[1]==".shp":  ## Si son shapefiles...
        capa = QgsVectorLayer(ruta + archivo, os.path.splitext(archivo)[0],"ogr") ## ...cargarlos
        CRS = capa.crs().postgisSrid() ## ...obtener su SRC
        campos = capa.dataProvider().fields() ## obtener sus campos
        id = 0 ## ...iniciar el id
        
        for distancia in range(100, 501, 100): ## Para cada una de las distancias que queremos calcular...
            print('Generando buffer de ' + str(distancia) + ' metros para la capa ' + archivo + ' ...') 
            uri =  "MultiPolygon?crs=epsg:"+ str(CRS) + "&field=id:integer""&index=yes"
            capa_buffers = QgsVectorLayer(uri, "buffers", "memory") ## ...crear una capa temporal
            capa_buffers.startEditing() 
            capa_buffers.dataProvider().addAttributes(campos.toList()) ## ...copiar los campos de la capa de entrada
            
            for f in capa.getFeatures():   ## Por cada una de las entidades de la capa de entrada...
                geom = f.geometry()   ## ...acceder a su geometria
                buffer = geom.buffer(distancia,-1)    ## ...aplicarle un buffer con la distancia que toque
                entidad = QgsFeature()   ## ...crear un objeto feature vacio 
                entidad.setGeometry(buffer)    ## ...añadirle la geometria del buffer
                entidad.setAttributes([id])    ## ...añadirle el valor del objeto id 
                capa_buffers.addFeatures([entidad])    ## ...y copiar la entidad a la capa temporal
                id += 1    ## Aumentar el id al acabar cada paso del bucle
                
            capa_buffers.commitChanges()    ## Guardar los cambios de la capa temporal
            
            ## Guardar la capa temporal en una capa nueva en la carpeta de resultados
            output = resultados+capa.name()+str(distancia)+".shp" 
            QgsVectorFileWriter.writeAsVectorFormat(capa_buffers, output,"UTF-8",capa.crs(), driverName="ESRI Shapefile") 

