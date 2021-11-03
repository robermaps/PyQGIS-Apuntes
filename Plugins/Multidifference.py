# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessing,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFile,
                       QgsProcessingParameterFolderDestination)
from qgis import processing
import os

class Multidifference(QgsProcessingAlgorithm):
    INPUT = 'INPUT'
    OVERLAY = 'OVERLAY'
    OUTPUT = 'OUTPUT'    
      
    def __init__(self):   ## Lo primero que debemos definir. Es el constructor de la clase (imprescindible)
        super().__init__() 
 
    def name(self):   ## Nombre identificativo de la herramienta (solo números y minúsculas)         
        return "recortemultiple" 
 
    def tr(self, text):   ## Método para que el texto de la interfaz se traduzca (si es posible)        
        return QCoreApplication.translate("Multidifference", text) 
 
    def displayName(self):   ## Nombre que se mostrará al usuario en la interfaz         
        return self.tr("Diferencia múltiple") 
        
    def group(self):   ## Nombre del grupo que contendrá la herramienta en la caja de procesos         
        return self.tr("Scripts de prueba") 

    def groupId(self):   ## Nombre identificativo del grupo (solo números y minúsculas)
        return "scriptsdeprueba"
    
    def shortHelpString(self):   ## Texto descriptivo con las instrucciones de la herramienta         
        return self.tr("Este proceso recorta todos los shapes de un directorio especificando una única capa") 
    
    def helpUrl(self):   ## Enlace que se abrirá al hacer clic sobre el botón de ayuda         
        return "https://programapa.wordpress.com" 
 
    def createInstance(self):   ## Crea una nueva instancia de la clase que estamos creando (imprescindible)          
        return type(self)() 
        
    ## iniciamos la definicion de los parametros
    def initAlgorithm(self, config=None): 
            
            ## capeta con los archivos de entrada
            self.addParameter(QgsProcessingParameterFile(
                self.INPUT, 
                self.tr("Input folder (Required)"),
                behavior = QgsProcessingParameterFile.Folder))
             
            ## capa de tipo poligono que hace de overlay   
            self.addParameter(QgsProcessingParameterFeatureSource(            
                self.OVERLAY,             
                self.tr("Input overlay layer (Required)"), 
                [QgsProcessing.TypeVectorPolygon])) 
            
            ## carpeta de salida de los archivos generados    
            self.addParameter(QgsProcessingParameterFolderDestination(
                self.OUTPUT, 
                self.tr("Output folder (Required)"))) 
                
    def processAlgorithm(self, parameters, context, feedback):

        ## Se recogerán las rutas de entrada y salida introducidas por el usuario de la herramienta en cadenas de texto
        ruta_entrada = self.parameterAsString(parameters, self.INPUT, context)
        ruta_salida = self.parameterAsString(parameters, self.OUTPUT, context)

        ## Se listarán los archivos de la ruta de entrada
        archivos = os.listdir(ruta_entrada)

        ## Se iniciará un bucle que recorrerá todos los archivos de la lista y seleccionará solo los shapes
        for archivo in archivos:
            if os.path.splitext(archivo)[1] == '.shp':
                    
                nombre = os.path.splitext(archivo)[0]   ## el nombre de la capa
                   
                ## construcción de las rutas de entrada y salida 
                capa_input = ruta_entrada + '\\' + archivo
                capa_output = ruta_salida + '\\' + nombre + '_cut.shp'
                     
                ## geoproceso 'difference' que se aplicará a cada shapefile
                processing.run("qgis:difference", {'INPUT': capa_input, 'OVERLAY': parameters['OVERLAY'], 'OUTPUT': capa_output})
