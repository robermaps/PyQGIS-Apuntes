# Este script añade al panel de capas de QGIS 
# todas las capas .shp que se encuentren en la
# carpeta especificada y comprueba si fueron
# cargadas correctamente o no

from qgis.core import *  
from qgis.utils import *
import os

ruta =  'C:\\ruta\\'
lista_ficheros = os.listdir(ruta)
 
for fichero in lista_ficheros:
    nombre = os.path.splitext(fichero)[0]
    extension = os.path.splitext(fichero)[1]
    if extension == '.shp':
        capa_shp = iface.addVectorLayer(ruta + nombre + extension, nombre,'ogr')
        if not capa_shp.isValid():
            print('Error al cargar la capa ' + fichero) 
        else: 
            print('La capa ' + fichero + ' se cargó correctamente')
           
