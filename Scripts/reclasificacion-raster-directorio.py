## Este script reclasifica por intervalos todos los archivos TIF de un directorio
## y almacena los resultados en capas nuevas dentro de una carpeta de resultados
##

import os
from qgis.core import *  ## Modulo fundamental
from PyQt5.QtCore import * 
from PyQt5.QtGui import * 
from qgis.analysis import *   ##  Herramientas de analisis raster
from qgis.gui import * 
from qgis.utils import *

## Lista de capas
ruta = 'C:\\ruta\\'
archivos = os.listdir(ruta)

## Crear carpeta de resultados
carpeta = 'RESULTADOS_CALCULADORA\\'
if os.path.exists(ruta + carpeta):
    print("El directorio ya existe")
    resultados = ruta + carpeta
else:
    os.mkdir(ruta + carpeta)
    print("Directorio creado")
    resultados = ruta + carpeta

## Bucles
for archivo in archivos:  ## Por cada archivo del directorio
    if os.path.splitext(archivo)[1]==".tif":  ## Si son tif...
        nombre = os.path.splitext(archivo)[0]
        print('Reclasificando ' + nombre) 
        mi_raster = QgsRasterLayer(ruta + archivo, nombre)
        
        ## Parametros
        tipo = 'GTiff' 
        extension = mi_raster.extent()
        filas = mi_raster.height()
        columnas = mi_raster.width()
        expresion = '( capa1@1 < 100 )  * 1 +  ( capa1@1 >= 100 AND capa1@1 < 500 ) * 2 +  ( capa1@1 >= 500 AND capa1@1 < 1000 ) * 3  +  ( capa1@1  >=  1000 )  * 4'  
        capa_salida =  resultados + nombre + '_reclass.tif' ## Ruta con el nombre de la capa de salida y la extension
        capas_entrada = []  ## Lista vacia que almacenara los objetos de entrada

        ## Capa 1
        capa1 = QgsRasterCalculatorEntry() ## Crear el objeto de entrada
        capa1.ref = 'capa1@1'  ## Crear referencia para la expresion
        capa1.raster = mi_raster  ## Seleccion de la capa  
        capa1.bandNumber = 1  ## Definir el nº de banda a usar
        capas_entrada.append(capa1)   ## Añadir a la lista vacia

        ## CALCULADORA RASTER##
        ## Creacion del objeto con los valores calculados
        calculos = QgsRasterCalculator(expresion, capa_salida, tipo, extension, columnas, filas, capas_entrada)

        ## Escritura de la capa de salida
        calculos.processCalculation()
    
