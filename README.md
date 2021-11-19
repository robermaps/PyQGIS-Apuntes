# Apuntes de PyQGIS

<img src="https://programapa.files.wordpress.com/2021/04/processing_pyqgis.png" width="300" height="200" text-align: center></div>

Por Rober J 

[![](https://img.shields.io/badge/@progra_mapa-white?style=for-the-badge&labelColor=blue&logo=Twitter&logoColor=white)](https://twitter.com/progra_mapa)[![](https://img.shields.io/badge/PrograMapa-grey?style=for-the-badge&logo=wordpress)](https://programapa.wordpress.com)[![](https://img.shields.io/badge/Roberto-blue?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/robertojl)

<br>

<details>
  <summary><strong>Importación de módulos</strong></summary><br>
  
  <p>Al comienzo de un script se debe siempre importar los módulos que vayan a usarse:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
## Módulos imprescindibles con las funciones básicas de QGIS
from qgis.core import *  
from qgis.utils import *

## Si no funcionaran, utilizar los siguientes
from PyQt5.QtCore import *
from PyQt5.QtGui import *

## Módulos recomendables
from qgis.PyQt.QtCore import QSettings, QTranslator, QcoreApplication 
from qgis.PyQt.QtGui import Qicon 
from qgis.PyQt.QtWidgets import QAction, QfileDialog## recomendable

## Módulos útiles de Python
import os
import shutil
import processing
from qgis.analysis import *   ##  Herramientas de analisis raster
</pre></div>
  
  
  <br></details>

## 🛰 Ráster

<details>
  <summary><strong>Cargar capas ráster</strong></summary><br>
  
  <p>Cargar una capa ráster implica crear un objeto QgsRasterLayer que contendrá los datos del archivo ráster. A dicho objeto se le podrán aplicar los distintos métodos de su clase para operar con sus datos.</p>



<p>Hay dos maneras de cargar las capas ráster usando PyQGIS dependiendo de si queremos visualizarlas o no. Si estamos usando Python dentro de QGIS probablemente queramos añadir las capas al panel de capas, pero en caso de usar un IDE externo (VSCode, PyCharm&#8230;) esto no será posible y solo podremos acceder a los datos de las capas sin poder visualizarlas</p>



<p>A diferencia de las capas vectoriales, no será necesario especificar el <strong>proveedor</strong> puesto que para ráster el único disponible es GDAL (Geospatial Data Abstraction Library) y es el equivalente a OGR para datos vectoriales, es decir, admite multitud de formatos ráster como TIFF, IMG&#8230;</p>



<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>


<p><a id="cargar_1"></a></p>


<h3><strong>Cargar y visualizar las capas ráster</strong></h3>



<p>Con el siguiente código, además de cargar en una variable llamada <em>capa_raster </em>los datos de una capa ráster, dicha capa se añadirá al panel de capas de QGIS</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_raster = iface.addRasterLayer('ruta_capa','nombre_capa')
</pre></div>


<p>Esta función no funcionará si trabajamos con PyQGIS en una IDE externa.</p>



<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>


<p><a id="cargar_2"></a></p>


<h3><strong>Cargar solo los datos de las capas ráster</strong></h3>



<p>Con el siguiente código se cargan solo los datos de la capa ráster en una variable nueva llamada <em>capa_raster</em>, de modo que se podrá usar para llevar a cabo geoprocesos pero no se visualizarán. </p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_raster = QgsRasterLayer('ruta_capa','nombre_capa')
</pre></div>


<p>Se puede usar tanto en una IDE como dentro de QGIS si no queremos añadir la capa a la visualización.</p>



<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>


<p><a id="validez"></a></p>


<h3><strong>Comprobar validez de la capa</strong></h3>



<p>Al igual que con los datos vectoriales, debe usarse el <strong>método <em>.isValid()</em></strong> sobre el objeto que guarda la capa. Combinado con una sentencia <em>if</em> podremos generar un mensaje en caso de error:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
if not capa_raster.isValid():
    print("Error al cargar la capa")
</pre></div>

  
  <br></details>

<details>
  <summary><strong>Extraer información de la capa</strong></summary><br>
  
  <p>Una vez cargada la capa ráster en un objeto QgsRasterLayer podremos obtener información de ella a través de distintos métodos:</p>


<p><a id="extension"></a></p>


<h3>Extensión espacial</h3>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_raster.extent()
</pre></div>

<p><a id="tipo"></a></p>


<h3>Tipo de ráster</h3>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_raster.rasterType()
</pre></div>


<p>Podremos obtener 3 resultados:</p>



<ul><li>0 = Escala de grises o indefinido (monobanda) </li><li>1 = Monobanda</li><li>2 = Multibanda</li></ul>


<p><a id="filas_columnas"></a></p>


<h3>Número de filas y columnas</h3>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_raster.width() ## columnas
capa_raster.height() ## filas
</pre></div>

<p><a id="bandas"></a></p>


<h3>Número de bandas</h3>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_raster.bandCount()
</pre></div>

<p><a id="metadatos"></a></p>


<h3>Metadatos</h3>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_raster.metadata()
</pre></div>

<p><a id="valor_pixel"></a></p>


<h3>Valor de un píxel</h3>



<p>El siguiente código usa el <strong>método <em><a href="https://docs.qgis.org/3.16/es/docs/pyqgis_developer_cookbook/raster.html#query-values" target="_blank" rel="noreferrer noopener">.identify()</a></em></strong>  sobre <em><a rel="noreferrer noopener" href="https://qgis.org/pyqgis/3.16/core/QgsRasterDataProvider.html#qgis.core.QgsRasterDataProvider" target="_blank">dataProvider()</a></em>  indicando un objeto QgsPoint. Si es correcto (las coordenadas del punto se encuentran dentro de la extensión espacial del ráster) imprime el valor del píxel que se encuentra en el objeto de tipo <em>QgsIdentifyResult()</em>.</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
coordx = 5000
coordy = -3500
punto = QgsPointXY(coordx, coordy)

valor_pixel = rlayer.dataProvider().identify(punto, QgsRaster.IdentifyFormatValue)

if valor_pixel.isValid():
     print(valor_pixel.results())
</pre></div>


<p>También se puede extraer el valor de un píxel en forma de tupla con el <strong>método <em><a href="https://docs.qgis.org/3.16/es/docs/pyqgis_developer_cookbook/raster.html#query-values" target="_blank" rel="noreferrer noopener">.sample()</a></em></strong> sobre <em><a href="https://qgis.org/pyqgis/3.16/core/QgsRasterDataProvider.html#qgis.core.QgsRasterDataProvider" target="_blank" rel="noreferrer noopener">dataProvider()</a></em>:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
coordx = 5000
coordy = -3500
n_banda = 1
punto = QgsPointXY(coordx, coordy)

valor_pixel, res = capa_raster.dataProvider().sample(punto, n_banda) 
print(valor_pixel)
</pre></div>
  
  <br></details>
  
<details>
  <summary><strong>Calculadora ráster</strong></summary><br>
  
  <p>Las operaciones matemáticas sobre los píxeles de las capas ráster en QGIS se llevan a cabo en la calculadora ráster. En PyQGIS, la función detrás de esta herramienta es <strong><em><a href="https://qgis.org/pyqgis/3.4/analysis/QgsRasterCalculator.html" target="_blank" rel="noreferrer noopener">QgsRasterCalculator()</a></em></strong>. Sus <strong>parámetros</strong> son, por orden:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
QgsRasterCalculator(expresion, capa salida, formato, extension, ancho, alto, capas de entrada)
</pre></div>


<figure class="wp-block-table"><table class="has-fixed-layout"><thead><tr><th>Parámetro</th><th>Descripción</th><th>Tipo de objeto</th></tr></thead><tbody><tr><td>expresión</td><td>Expresión lógica con las operaciones que queremos realizar</td><td>Cadena de texto</td></tr><tr><td>capa de salida</td><td>Ruta con el nombre y la extensión de la capa en la que guardar los resultados</td><td>Cadena de texto</td></tr><tr><td>formato</td><td>Formato de la capa de salida</td><td>Cadena de texto</td></tr><tr><td>extensión</td><td>Coordenadas de la capa de  salida </td><td>QgsRectangle</td></tr><tr><td>ancho (columnas)</td><td>Número de columnas de la capa de  salida </td><td>Entero</td></tr><tr><td>alto (filas)</td><td>Número de filas de la capa de  salida </td><td>Entero</td></tr><tr><td>capas de entrada</td><td>Lista de objetos que almacenan las capas que se usarán en la calculadora</td><td>QgsRasterCalculatorEntry</td></tr></tbody></table></figure>



<p>El proceso para crear la lista con los objetos <a rel="noreferrer noopener" href="https://qgis.org/api/classQgsRasterCalculatorEntry.html" target="_blank">QgsRasterCalculatorEntry</a> junto con el resto de parámetros  y la ejecución de la calculadora es el siguiente:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
## Cargar capas
mi_raster = QgsRasterLayer(ruta, "nombre")
mi_raster2 = QgsRasterLayer(ruta, "nombre2")

## Parametros
tipo = 'GTiff' 
extension = mi_raster.extent()
filas = mi_raster.height()
columnas = mi_raster.width()
expresion =  'capa1@1 * capa2@1'  ## Multiplicar los valores de las dos capas de entrada
capa_salida = 'C:\\ruta\\'  ## Ruta con el nombre de la capa de salida y la extension
capas_entrada = &#91;]  ## Lista vacia que almacenara los objetos de entrada

## CREACION DE ENTRADAS ##
## Capa 1
capa1 = QgsRasterCalculatorEntry() ## Crear el objeto de entrada
capa1.ref = 'capa1@1'  ## Crear referencia para la expresion
capa1.raster = mi_raster  ## Seleccion de la capa  
capa1.bandNumber = 1  ## Definir el nº de banda a usar
capas_entrada.append(capa1)   ## Añadir a la lista vacia

## Capa 2
capa2 = QgsRasterCalculatorEntry()
capa2.ref = 'capa2@1'
capa2.raster = mi_raster2
capa2.bandNumber = 3 
capas_entrada.append(capa2)  

## CALCULADORA RASTER##
## Creacion del objeto con los valores calculados
calculos = QgsRasterCalculator(expresion, capa_salida, tipo, extension, columnas, filas, capas_entrada)

## Escritura de la capa de salida
calculos.processCalculation()
</pre></div>


<p>Si una de las capas de entrada fuese una <strong>capa de máscara</strong>, es decir, con valores 1 y 0, al multiplicarlas recortaríamos la otra capa, pues los píxeles que se multipliquen por 0 perderían su valor.</p>



<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>





<h3><strong>Reclasificación ráster</strong></h3>



<p>El ejemplo anterior toma dos capas de entrada para sumar sus valores, pero podrían usarse más o <strong>usar tan solo una</strong> para reclasificar sus valores y convertir variables continuas en discretas. En tal caso habrá que <strong>adecuar la expresión</strong>:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
## Los pixeles cuyo valor sea mayor a 1000 pasaran a valer 1 y el resto 0
expresion =  'capa@1 &gt; 1000'

## Los pixeles se multiplican por un factor de conversion
expresion = 'capa@1 * 0.7'

## Los pixeles tendran nuevos valores segun el intervalo de datos en el que se encuentren 
expresion = '( capa1@1 &lt; 100 )  * 1 +  ( capa1@1 &gt;= 100 AND capa1@1 &lt; 500 ) * 2 +  ( capa1@1 &gt;= 500 AND capa1@1 &lt; 1000 ) * 3  +  ( capa1@1  &gt;=  1000 )  * 4'
</pre></div>


<p>He dejado un <a rel="noreferrer noopener" href="https://github.com/PrograMapa/PyQGIS/blob/main/reclasificacion_raster_directorio.py" target="_blank">ejemplo completo de reclasificación</a> en GitHub en el que se lleva a cabo la reclasificación por intervalos para todos los TIF de una carpeta.</p>
  
  <br></details>

## 📐 Vectorial  

### Capas

<details>
  <summary><strong>Cargar capas vectoriales</strong></summary><br>
  
  <p>Principalmente existen dos funciones para cargar las capas vectoriales usando PyQGIS dependiendo de si queremos visualizarlas o no. En cualquier caso, lo que se hace es <strong>crear un objeto de tipo QgsVectorLayer</strong>, es decir, un objeto o variable que almacena una capa.</p>



<p>Crear esta clase de objetos es fundamental para poder acceder después a sus entidades, y a partir de ellas a sus atributos y su geometría.</p>






<h4><strong>Cargar y visualizar las capas vectoriales</strong></h4>



<p>Con la función <em>iface.addVectorLayer()</em> además de cargar en una variable nueva<em> </em>los datos de una capa vectorial, dicha capa se añadirá al panel de capas de QGIS. </p>



<p>Esta función no funcionará si trabajamos con PyQGIS en una IDE externa (VSCode, PyCharm&#8230;) .</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_vectorial = iface.addVectorLayer('ruta_capa','nombre_capa','proveedor)
</pre></div>


<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>


<p><a id="cargar_2"></a></p>


<h4><strong>Cargar solo los datos de las capas vectoriales</strong></h4>



<p>Con la función <em>QgsVectorLayer()</em> se cargan solo los datos de la capa vectorial en una variable nueva, de modo que se podrá usar para llevar a cabo geoprocesos pero no se visualizarán. </p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_vectorial = QgsVectorLayer('ruta_capa','nombre_capa','proveedor')
</pre></div>


<p>Se puede usar tanto en una IDE como dentro de QGIS si no queremos añadir la capa a la visualización.</p>

  
  <br></details>
  
<details>
  <summary><strong>Proveedores</strong></summary><br>
  
  <p>El procedimiento para cargar capas vectoriales varía según el proveedor, puesto que el origen de datos varía. En cualquier caso, funcionan igual tanto con <em>QgsVectorLayer()</em> como con <em>iface.addVectorLayer()</em>:</p>



<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>



<h4><strong>OGR</strong></h4>



<p>Es el proveedor para las capas vectoriales de los tipos de archivo más comunes (.shp, .kml o .geojson) y suele usarse para utilizar archivos que se encuentran en el sistema de archivos de nuestro ordenador.</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_vectorial = QgsVectorLayer('ruta_capa','nombre_capa','ogr')
</pre></div>


<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>



<h4 class="has-text-align-left"><strong>postgres</strong></h4>



<p>Sirve para cargar información vectorial almacenada en bases de datos de PostgreSQL o PostGIS.</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
# Conectar con la base de datos
uri = QgsDataSourceUri()
uri.setConnection("host", "puerto", "nombre_database", "usuario", "contraseña") 

# Selección del esquema, la tabla y el campo que contiene la geometría
uri.setDataSource("esquema", "tabla", "campo_geometría") 

# Cargar la capa
capa = QgsVectorLayer(uri.uri(), "Nombre_capa", "postgres")
</pre></div>


<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>



<h4 class="has-text-align-left"><strong>MySQL</strong></h4>



<p>Para conectar con una base de datos de tipo MySQL se debe usar otro proveedor como OGR:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
# Conectar con la base de datos
uri = "MySQL:nombre_database,host=nombre_host,port=numero_puerto,user=nombre_usuario,password=contraseña|layername=nombre_tabla"

# Cargar la capa
capa = QgsVectorLayer(uri,"Nombre_capa","ogr" ),"Nombre_capa","ogr"
</pre></div>


<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>



<h4 class="has-text-align-left"><strong>WFS</strong></h4>



<p>Para cargar servicios WFS (Web Feature Services) habrá que indicar una URL como origen de los datos</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
uri = "URL del servicio WFS"
capa = QgsVectorLayer(uri, "Nombre_capa", "WFS")
</pre></div>


<p>Estos servicios también pueden cargarse usando el módulo de Python <strong>urllib</strong>:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
import urllib
params = {
'service': 'WFS', 
'version': '1.0.0', 'request': 'petición', 
'typename': 'nombre_capa', 'srsname': "EPSG:XXXX"
} 
uri = 
'ruta_servicio?'+urllib.parse.unquote(urllib.parse.ur
lencode(params))

capa = QgsVectorLayer(uri, "Nombre_capa", "WFS")
</pre></div>


<p>Los servicios WFS están estandarizados por la OGC (Open Geospatial Consortium) y todos poseen los siguientes tipos de <strong>peticiones</strong>:</p>



<ul><li>GetCapabilities &#8211; obtener metadatos</li><li>GetFeature &#8211; obtener entidades</li><li>DescribeFeatureType &#8211; obtener esquema XML de los servicios del servidor del WFS</li></ul>



<p class="has-light-green-cyan-background-color has-background">⚠ En QGIS 2 el proveedor que debe especificarse al cargar capas WFS debe ser OGR</p>



<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>



<h4 class="has-text-align-left"><strong>CSV</strong></h4>



<p>Se puede también cargar archivos CSV o de texto delimitado indicando el caracter separador (espacios, comas, puntos, punto y comas&#8230;) y las columnas de las coordenadas X e Y</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
uri = 
"ruta_archivo.extensión?delimiter={}&xField={}
&yField={}".format("delimitador", "nombre_campoX", "nombre_campoY") 
capa = QgsVectorLayer(uri, "layer name you like", "delimitedtext")
</pre></div>


<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>



<h4><strong>memory</strong></h4>



<p>Las capas &#8216;memory&#8217; son capas temporales y vacías que solo existen mientras se ejecuta un script. Son útiles porque nos evita el andar creando archivos innecesarios y actúan como un lienzo en blanco en el que almacenar nuevas geometrías. </p>



<p>En el ejemplo se especifica que la capa temporal sea de tipo multipolígono, su SRC 25830, la <strong>creación de un campo</strong> id de tipo entero y la creación del índice espacial:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
uri =  "MultiPolygon?crs=epsg:25830"+"&field=id:integer""&index=yes"
capa = iface.addVectorLayer(uri, "capa_temporal", "memory")
</pre></div>


<p>Al haber usado <em>iface.addVectorLayer()</em>, la capa temporal se cargará al panel de capas de QGIS y duraría hasta que cerráramos la sesión. Para <strong>guardar la capa temporal como capa nueva</strong> hay que usar la función <em>QgsVectorFileWriter.writeAsVectorFormat()</em></p>


  
  <br></details>
  
<details>
  <summary><strong>Validez de la capa</strong></summary><br>
  
  <p>Para saber si una capa espacial se ha cargado correctamente se debe usar el <strong>método <em>.isValid()</em></strong> sobre dicha capa. Lo que hace es devolver un booleano en el que True significa que la capa es correcta y False si no lo es.</p>



<p>Lo que suele hacerse es combinarlo con estructuras de control <em>if &#8211; else </em> para obtener un mensaje según si se ha cargado bien o no:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa = QgsVectorLayer('ruta_capa','nombre_capa','proveedor')
if not capa.isValid():
      print('Error al cargar la capa') 
else: 
      print('La capa se cargó correctamente')
</pre></div>
  
  <br></details>
  
<details>
  <summary><strong>Capa activa</strong></summary><br>
  
  <p>Consiste en seleccionar una capa que pasa a ser la &#8216;capa activa&#8217; para que sea el objetivo de alguna herramienta de QGIS. </p>



<p>La instrucción siguiente crea una variable que contendrá los datos de la capa que se encuentra activa en QGIS. Esto significa que:</p>



<ul><li>solo podremos utilizar la capa activa si utilizamos Python dentro de QGIS (no funciona en IDEs externos)</li><li>los datos de la variable creada cambiarán según la capa que establezcamos como activa</li></ul>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa = iface.activelayer()
</pre></div>


<p>Vale tanto para capas vectoriales como ráster y solo puede haber una capa activa a la vez. </p>

  
  <br></details>
  
<details>
  <summary><strong>Copiar capas</strong></summary><br>
  
  <p>Para copiar capas tendremos que cargar la capa que queramos copiar y usarla como valor de entrada en la función de escritura de capas vectoriales: </p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa = QgsVectorLayer('ruta_capa','nombre_capa','proveedor')
CRS = capa.crs()
ruta_salida = 'C:\\ruta\\nombre.extension'
QgsVectorFileWriter.writeAsVectorFormat(capa, ruta_salida, CRS, driverName = 'ESRI Shapefile')
</pre></div>


<p>En la <a rel="noreferrer noopener" href="https://qgis.org/pyqgis/master/core/QgsVectorFileWriter.html" target="_blank">documentación oficial</a> hay más información acerca de la escritura de archivos vectoriales.</p>



<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>


<p><a id="entidades_geometrias"></a></p>


<h2 class="has-text-align-center"><strong>Entidades y geometrías</strong></h2>



<p>Las capas espaciales vectoriales se componen de entidades: objetos geométricos que representan fenómenos territoriales. Cada uno de estos objetos ocupa un registro en la tabla de atributos de dicha capa, y entre estos atributos se encuentra la geometría del objeto.</p>



<p>En PyQGIS se distinguen dos clases de variables para estos elementos:</p>



<ul><li>Variables de tipo <strong>QgsFeature</strong> que almacenan las entidades de una capa</li><li>Variables de tipo <strong>QgsGeometry</strong> que almacenan la geometría de las entidades</li></ul>


  
  <br></details>

### Entidades y geometrías

<details>
  <summary><strong>QgsFeature</strong></summary><br>
  
  <p>Para trabajar con la información vectorial es necesario crear un objeto que indexe las entidades de una capa cargada previamente. Dicho objeto será de <strong>tipo QgsFeature,</strong> y para obtenerlo se debe usar el método <em>.getFeatures()</em> sobre un objeto QgsVectorLayer.</p>



<p>Sin embargo, para poder acceder a cada una de esas entidades indexadas será necesario <strong>iterar sobre ellas</strong>:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_vectorial = QgsVectorLayer('capa.shp','nombre_capa','ogr')  ## Objeto Layer
features = capa_vectorial.getFeatures()  ## Objeto Feature

# Con esto ya podríamos iterar sobre las entidades de la capa usando estructuras de control para obtener 
# información de cada una de ellas:
for entidad in features:
     print(entidad.id())   ## ver el identificador
     print(entidad.attributes())   ## ver los valores de todos los campos
     print(entidad&#91;0])   ## ver el valor de la primera columna usando el índice de posición
     print(entidad&#91;'nombre'])   ## ver el valor de la columna usando su nombre
     print(entidad.geometry())   ## ver la geometría

</pre></div>


  
  <br></details>
  
<details>
  <summary><strong>QgsGeometry</strong></summary><br>
  
  <p>Una vez accedemos a las entidades podemos extraer su geometría para obtener información en base a ella como puede ser el área, la longitud o el perímetro de nuestras entidades.</p>



<p>Para ello es necesario crear una nueva <strong>variable de tipo QgsGeometry</strong> que almacene la geometría recogida por el método .geometry() sobre cada entidad y <strong>aplicarle un método</strong> compatible con el <a href="https://programapa.wordpress.com/2020/11/06/tipos-de-datos-espaciales/">tipo de geometría</a>:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_vectorial = QgsVectorLayer('capa.shp','nombre_capa','ogr')
features = capa_vectorial.getFeatures()
for entidad in features:
    geom = entidad.geometry()  ## Creación del objeto con la geometría
    print(geom.area())   ## ver el área de una geometría de tipo polígono
    print(geom.length())   ## ver la longitud de una geometría de tipo línea o el perímetro si es de tipo polígono
    print(geom.asPoint())   ## ver las coordenadas de una geometría de tipo punto
</pre></div>


<p>Además, la geometría es también el <strong>producto de los geoprocesos</strong>, que nos permitirán generar geometrías nuevas a partir de las existentes.</p>


  
  <br></details>

### Selecciones

<details>
  <summary><strong>Por atributos</strong></summary><br>
  
  <p>La selección de entidades según sus atributos o <strong>consultas temáticas</strong> consiste en seleccionar aquellas entidades cuyos atributos coincidan con nuestra consulta.</p>



<p>Para ello se crean <strong>expresiones SQL</strong> con la función <em>QgsExpression()</em> para usarlas en una petición mediante la función <em>QgsFeatureRequest()</em>. Dicha petición se emplea para <strong>acceder a la geometría</strong> de aquellas entidades cuyos atributos casen con la consulta.</p>



<p>En el siguiente ejemplo se seleccionan de una capa con ríos aquellos de longitud superior a 100 km para luego iterar sobre ellos:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_vectorial = QgsVectorLayer('rios.shp','red_fluvial','ogr')

# Creación de variable con la expresión SQL 
expresion = QgsExpression('longitud_km &gt; 100')

# Creación de variable que almacene la expresión como una consulta 
peticion = QgsFeatureRequest(expresion)

# Bucle para iterar solo sobre las entidades que coincidan con la petición
for entidad in capa_vectorial.getFeatures(peticion):
      # operaciones a llevar a cabo con cada río
     
</pre></div>


<p>Otra forma es <strong>seleccionar entidades según su id</strong> usando el método <em>.selectByIds()</em>. Esto resulta útil pues </p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa_rios = QgsVectorLayer('rios.shp','red_fluvial','ogr')

# Creación de variable con la expresión SQL 
expresion = QgsExpression('longitud_km &gt; 100')

# Creación de variable que almacene la expresión como una consulta 
peticion = QgsFeatureRequest(expresion)

# Obtención de entidades
entidades = capa_rios.getFeatures(peticion)

# Creación de lista con los ID de los ríos seleccionados
lista_id = &#91;rio.id() for rio in entidades]

# Selección de ríos a partir de los ID de la lista
capa_rios.selectByIds(lista_id)
</pre></div>

  
  <br></details>
  
<details>
  <summary><strong>Por localización</strong></summary><br>
  
  <p>La selección por localización o <strong>consultas espaciales</strong> consisten en seleccionar aquellas entidades que cumplen con algún tipo de <a href="https://programapa.wordpress.com/2020/11/13/relaciones-espaciales/">relación topológica</a>, es decir, necesitaremos hacer uso de la geometría de las entidades para llevarlas a cabo.</p>



<p>En PyQGIS podemos hacerlo de dos maneras:</p>



<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>


<p><a id="filtro_espacial"></a></p>


<h4><strong>Estableciendo un filtro espacial</strong></h4>



<p>Esto es, utilizar una AOI (Area de Interés) para seleccionar todo aquello que se encuentre dentro de ella. La AOI podemos obtenerla de varias maneras, como tomando el &#8216;extent&#8217; o recuadro delimitador de una capa (sus coordenadas X e Y máximas y mínimas) o dibujándola nosotros mismos.</p>



<p>En el siguiente ejemplo se utiliza como AOI el &#8216;extent&#8217; de una capa para que se seleccionen las entidades de otra capa:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
# Cargar la capa de la que seleccionar las entidades
capa = QgsVectorLayer('capa1.shp','Mi capa','ogr')

# Crear área de interés usando el 'extent' de otra capa
AOI = QgsVectorLayer('capa2.shp','Area de interes','ogr').extent() 

# Aplicar la AOI como filtro usando el método .setFilterRect() sobre una petición 
peticion = QgsFeatureRequest() 
peticion.setFilterRect(AOI)

# Bucle que itera sobre las entidades que se encuentran dentro de la AOI para obtener su ID
for entidad in capa.getFeatures(peticion):
    print(feature.id())
</pre></div>


<p>En este ejemplo la petición estaba vacía, pero se puede <strong>combinar filtros espaciales con consultas de atributos</strong> para obtener solo algunas entidades de entre todas las que se encuentren en la AOI. En el siguiente ejemplo se obtiene solo entidades de uso de suelo urbano dentro del filtro espacial:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
# Cargar la capa de la que seleccionar las entidades
capa = QgsVectorLayer('capa1.shp','Mi capa','ogr')

# Crear área de interés usando el 'extent' de otra capa
AOI = QgsVectorLayer('capa2.shp','Area de interes','ogr').extent() 

# Expresión para seleccionar los polígonos de usos urbanos
expresion = QgsExpression('USO ILIKE \'%urbano%\'')

# Petición para quedarnos solo con lo indicado en la expresión
usos_urbanos = QgsFeatureRequest(expresion) 

# Filtro para seleccionar solo las entidades de nuestra AOI
usos_urbanos.setFilterRect(AOI)

# Bucle que itera sobre las entidades que se encuentran dentro de la AOI para obtener su ID
for entidad in capa.getFeatures(usos_urbanos):
    print(feature.id())
</pre></div>


<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>


<p><a id="relaciones_espaciales"></a></p>


<h4><strong>Estableciendo relaciones espaciales entre capas</strong></h4>



<p>Consiste en quedarnos con aquellas entidades de una capa que cumplen algún tipo de <a href="https://programapa.wordpress.com/2020/11/13/relaciones-espaciales/">relación espacial</a> con las entidades de otra capa: se encuentran dentro, fuera, tocando, ocupando el mismo espacio&#8230;</p>



<p>Para ello tenemos que <strong>acceder a la geometría</strong> de las entidades de las capas y <strong>usar métodos de la <a rel="noreferrer noopener" href="https://qgis.org/api/classQgsGeometry.html" target="_blank">clase geometry</a></strong> sobre dichas geometrías para comprobar las relaciones espaciales:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
# Cargar la capa de la que seleccionar las entidades
capa1 = QgsVectorLayer("capa1.shp",'Mi capa','ogr')

# Cargar una segunda capa con la que comprobar las relaciones espaciales
capa2 = QgsVectorLayer("capa2.shp",'Mi capa 2','ogr')

# Bucles de iteración sobre las entidades
for f1 in capa1.getFeatures():      # Bucle que itera sobre la geometría de las entidades de la capa 1
    for f2 in capa2.getFeatures():      # Bucle para iterar sobre la geometría decada entidad de la capa 2 por cada una de la capa 1
          if f1.geometry().intersects(f2.geometry()):      # Estructura if para comprobar si hay intersección entre las entidades
                print(f1.id(),'intersects',f2.id())     # Acción a realizar si se cumple dicha relación
</pre></div>


<p>En el ejemplo anterior se ha usado el método para averiguar si existe intersección, pero hay muchos más <strong>predicados espaciales</strong><em> </em>como pueden ser:</p>



<figure class="wp-block-table"><table class="has-fixed-layout"><tbody><tr><td>geometría1.intersects(geometría2)</td><td>averiguar si existe intersección entre las geometrías</td></tr><tr><td>geometría1.disjoints(geometría2)</td><td>averiguar si no existe intersección </td></tr><tr><td>geometría1.contains(geometría2) </td><td>averiguar si la geometría 1 contiene a la geometría 2</td></tr><tr><td>geometría1.crosses(geometría2) </td><td>averiguar si la geometría 1 cruza en algún punto con la geometría 2</td></tr></tbody></table></figure>



<p>Recomiendo el <a rel="noreferrer noopener" href="https://programapa.wordpress.com/2020/11/13/relaciones-espaciales/" target="_blank">post sobre relaciones espaciales</a> para conocerlas más a fondo.</p>


  
  <br></details>
  
<details>
  <summary><strong>Guardar en capa nueva</strong></summary><br>
  
  <p>Para crear capas vectoriales nuevas hay que usar la función <em><strong>QgsVectorFileWriter.writeAsVectorFormat()</strong></em> indicando dentro de los paréntesis los siguientes parámetros, por orden:</p>



<figure class="wp-block-table"><table class="has-fixed-layout"><tbody><tr><td>Datos</td><td>Una variable u objeto de tipo QgsVectorLayer, es decir, la variable que contiene los datos que queremos guardar en la capa nueva</td></tr><tr><td>Ruta + nombre + extensión</td><td>La ruta junto con el nombre del archivo a guardar y su extensión</td></tr><tr><td>Codificación</td><td>La codificación de caracteres para esta capa: utf-8, latin1, iso&#8230;</td></tr><tr><td>SRC</td><td>Sistema de coordenadas asociado a la capa nueva</td></tr><tr><td>Formato</td><td>Tipo de capa o archivo que estamos creando: shapefile, geojson, kml&#8230;</td></tr><tr><td>Modo</td><td>Especificar si en el parámetro datos estamos usando entidades seleccionadas (True/False)</td></tr></tbody></table></figure>



<p>Por ejemplo, con el siguiente código se guarda en una capa nueva una selección de usos del suelo que se encuentran dentro del &#8216;extent&#8217; de otra capa. </p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
from qgis.core import *  
from qgis.utils import *

ruta = 'C:\\ruta\\'

# Crear los filtros espacial y de atributos
capa1 = QgsVectorLayer(ruta+'usos.shp','Mi capa','ogr')
capa2 = QgsVectorLayer(ruta+'aoi.shp','Area de interes','ogr').extent() 
expresion = QgsExpression('USO ILIKE  \'%urbano%\')
usos_urbanos = QgsFeatureRequest(expresion) 
usos_urbanos.setFilterRect(capa2)
seleccion = capa.getFeatures(usos_urbanos)

# Selección de entidades
ids = &#91;i.id() for i in seleccion]
capa1.selectByIds(ids)

# Guardar la selección en una capa nueva tomando el nombre y el SRC de la capa original
QgsVectorFileWriter.writeAsVectorFormat(capa1, ruta+capa.name()+'_nuevo.shp', 'UTF-8', capa1.crs(), driverName="ESRI Shapefile", onlySelected = True)
</pre></div>
  
  <br></details>

### Editar campos y atributos 
 
<details>
  <summary><strong>Añadir campos</strong></summary><br>
  
  <p>Los atributos de las capas vectoriales se organizan en forma de tabla, en la que cada columna es un campo y cada fila una entidad. Por tanto, los valores de los campos para cada fila serán los atributos de dicha fila.</p>



<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>


<p><a id="añadir_campos"></a></p>


<h3 class="has-text-align-center"><strong>Añadir campos</strong></h3>



<h4><strong>&#8211; Creando capas temporales</strong></h4>



<p>Se pueden crear campos al crear capas temporales<strong>.</strong> El siguiente ejemplo crea un campo de cada tipo (text, integer, double y date) en una nueva capa temporal<em> (Fuente: Geoinnova)</em>: </p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
URI = 
"MultiPolygon?field=id:integer&index=yes&field=decimal:double&field=tex 
to:string&field=fecha:date"
capa_temporal = iface.addVectorLayer(URI,"temp", "memory")
</pre></div>


<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>



<h4><strong>&#8211; Nuevos campos en capas ya existentes</strong></h4>



<p>También pueden crearse campos en capas ya existentes activando la edición de dicha capa y encadenando los siguientes métodos de la <a href="https://qgis.org/pyqgis/master/core/QgsVectorLayer.html" target="_blank" rel="noreferrer noopener">clase QgsVectorLayer</a>: </p>



<p class="has-text-align-center"><em>capa.dataProvider().addAttributes([QgsField])</em></p>



<ol><li>método .dataProvider()  ## para modificar tablas de atributos</li><li>método .addAttributes([lista_objetos_QgsField]) ## para añadir nuevos campos</li></ol>



<p>Los <strong>objetos de tipo campo o QgsField</strong> se crean con la siguiente sintaxis:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
QgsField("nombre_campo", QVariant.Text)  ## cadenas de texto 
QgsField("nombre_campo", QVariant.Integer)  ## numeros enteros
QgsField("nombre_campo", QVariant.Double)  ## numeros decimales 
QgsField("nombre_campo", QVariant.Date)  ## valores de tipo fecha 
</pre></div>


<p>Al completo, el procedimiento sería el siguiente:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
## Cargar la capa
capa = iface.addVectorLayer('ruta_capa','nombre_capa','proveedor)

## Comenzar la edición
capa.startEditing()

## Añadir nuevos campos
capa.dataProvider().addAttributes(&#91;QgsField("texto", QVariant.String), 
QgsField("entero", QVariant.Int), QgsField("decimal", 
 QVariant.Double),QgsField("fecha", QVariant.Date)])

## Actualizar campos 
capa.updateFields()
capa.commitChanges()
</pre></div>


<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>



<h4><strong>&#8211; Copiar campos a capas nuevas</strong></h4>



<p>Para ello habrá que obtener un objeto de la <a href="https://qgis.org/pyqgis/3.2/core/Field/QgsField.html" target="_blank" rel="noreferrer noopener">clase QgsField</a> con los campos de la capa de la que queremos copiar dichos campos. Después solo habrá que crear una capa nueva, activar su edición y copiarle dichos campos:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
## Cargar capa
capa = iface.addVectorLayer('ruta_capa','nombre_capa','proveedor)

## Obtener su sistema de coordenadas
crs = capa.crs().postgisSrid()

## Listar los campos de la capa cargada
campos = capa.dataProvider().fields()  ## Obtención de campos

## Crear capa temporal 
URI = "MultiPolygon?crs=epsg:"+str(crs)
nueva_capa = iface.addVectorLayer('URI','nueva','memory')

## Copiar los campos de la capa cargada a la nueva capa a través de la lista
nueva_capa.startEditing()
nueva_capa.dataProvider().addAttributes(campos.toList())
nueva_capa.commitChanges()
</pre></div>

<h4><strong>&#8211; Crear campos id autoincrementables</strong></h4>



<p>Una de las operaciones más comunes en cuanto a la creación de nuevos campos es crear IDs que identifiquen de forma única a cada entidad:</p>

  <div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
## Cargar la capa y empezar la edición
capa = QgsVectorLayer(output,nombre,'ogr')
capa.startEditing()

## Añadir el nuevo atributo ID
capa.dataProvider().addAttributes(&#91;QgsField('ID', QVariant.Int)])
capa.updateFields()

## Listar las entidades
entidades = capa.getFeatures()

## Iniciar el contador
contador = 0

## Bucle que recorre las entidades de la capa cargada
for entidad in entidades:

        ## Establecer el valor del atributo ID para la entidad a partir del valor del contador
        entidad&#91;'ID'] = contador

        ## Actualizar la entidad
        capa.updateFeature(entidad)

        ## Aumentar el contador
        contador += 1

## Guardar los cambios             
capa.commitChanges()
</pre></div>
  
  <br></details>
  
  
<details>
  <summary><strong>Modificar atributos</strong></summary><br>
  
  <p>Con el método <strong>.<em>setAttributes([])</em> </strong>podemos actuar sobre un objeto de tipo entidad <strong>en el momento de crearla</strong>, es decir, cuando generamos nuevos objetos de la <a href="https://qgis.org/pyqgis/3.2/core/Feature/QgsFeature.html#qgis.core.QgsFeature.setAttributes" target="_blank" rel="noreferrer noopener">clase QgsFeature</a>:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
## cargar capa
capa = iface.addVectorLayer('ruta_capa','nombre_capa','proveedor)

## lista con los valores
lista_valores = &#91;30, 40, 60]

## bucle para generar varias entidades
for f in range(1,10):
     
     ## nueva entidad
     entidad = QgsFeature()

     ## asignar los valores a las columnas
     entidad.setAttributes(lista_valores) 

     ## añadir la nueva entidad a la capa
     capa.addFeatures(&#91;entidad])

capa.commitChanges()
</pre></div>


<p>La lista de valores para la nueva entidad <strong>sigue el orden de posición de los campos</strong>. Si se quisiera cambiar, por ejemplo, la tercera columna, habría que dejar vacías las posiciones 0 y 1 de la lista.</p>



<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>


<p>Mediante <em><strong>.changeAttributeValue()</strong></em> actuamos sobre un objeto de la <a rel="noreferrer noopener" href="https://qgis.org/pyqgis/master/core/QgsVectorLayer.html" target="_blank">clase QgsVectorLayer</a><em>,</em> es decir, sobre una capa indicando el id de la fila y la posición de la columna en la que actuar:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa = iface.addVectorLayer('ruta_capa','nombre_capa','proveedor)
capa.startEditing()
nuevo_valor = 50
id_entidad = 3
id_campo = 0
capa.changeAttributeValue(id_entidad, id_campo, nuevo_valor)
capa.commitChanges()
</pre></div>
  
  <br></details>
  
<details>
  <summary><strong>Editar geometrías</strong></summary><br>
  
  <p>La edición de geometrías implica operar sobre los objetos <strong>QgsGeometry</strong>, es decir, la geometría de las entidades, para borrarlas, modificarlas o añadir nuevas geometrías que se deriven de algún geoproceso sobre ellas.</p>



<p>Por ejemplo, al hacer un buffer tomamos las geometrías de una capa y se les aplica un geoproceso que genera nuevos polígonos en base a un valor de distancia que indicamos en la función. Esos nuevos polígonos deben almacenarse en otra capa que se encuentre en edición.</p>



<p>Para comenzar a editar las geometrías es necesario <strong>activar la edición</strong> de la capa de entrada, y al finalizar la edición deben <strong>guardarse los cambios</strong>:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
capa = QgsVectorLayer('capa1.shp','Mi capa','ogr')  # Objeto tipo layer con los datos de la capa
capa.startEditing()  # Activación de la edición de la capa
## Geoprocesos ##
capa.commitChanges()  # Guardar los cambios
</pre></div>


<p>Los principales <strong>métodos para editar la geometría</strong> de una capa son:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
objeto_qgsfeature.setGeometry(nueva_geometría)  ## Establecer la geometría de una entidad
objeto_qgsvectorlayer.addFeatures(&#91;objeto_qgsfeature])  ## Añadir la entidad a una capa
</pre></div>


<p>A diferencia de las selecciones, los resultados de los geoprocesos deben almacenarse en capas nuevas que se encuentren en edición, ya que estamos hablando de geometrías nuevas que deben almacenarse en algún lado. </p>



<p>A continuación tenéis ejemplos con distintos geoprocesos básicos:</p>



<h3 class="has-text-align-center"><strong>Buffer</strong></h3>



<p>El buffer o área de influencia se calcula tomando una geometría y aplicándole el <strong>método <em>.buffer()</em></strong> junto a una serie de parámetros (<a rel="noreferrer noopener" href="https://qgis.org/api/classQgsGeometry.html" target="_blank">ver la documentación oficial</a>). </p>



<p>El procedimiento para llevarlo a cabo consiste en iterar sobre las geometrías de las entidades de la capa, en este caso para que se aplique el buffer a cada una de ellas y la geometría resultante se almacene en un objeto QgsFeature que pase a formar parte de una capa temporal. Además, se crea un contador para darle un ID a cada buffer que se cree:</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
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
     entidad.setAttributes(&#91;id])    ## Añadirle al objeto el valor de la variable id
     capa_buffers.addFeatures(&#91;entidad])    ## Añadirle a la capa temporal la entidad
     id += 1    ## Aumentar el id al acabar cada paso del bucle

capa_buffers.commitChanges()    ## Guardar los cambios de la capa temporal
</pre></div>


<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>


<p><a id="intersect"></a></p>


<h3 class="has-text-align-center"><strong>Intersección</strong></h3>



<p>En el caso de la intersección, el <strong>método</strong> a aplicar sobre los objetos QgsGeometry es <em><strong>.intersection()</strong></em> (<a rel="noreferrer noopener" href="https://qgis.org/api/classQgsGeometry.html" target="_blank">ver la documentación oficial</a>)</p>



<p>No debe confundirse con el método <em>.intersect()</em>, porque a diferencia de éste ahora estaremos generando geometrías nuevas, es decir, objetos de la clase QgsGeometry.</p>



<p>Con el siguiente código se crea una capa nueva con la geometría de las intersecciones entre las entidades de dos capas de entrada, es decir, con la superficie que ambas capas tienen en común (por tanto deberán ser dos capas de tipo poligonal):</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
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
            entidad.setAttributes(&#91;id])    ## Añadirle al objeto el valor de la variable id
            capa_intersecciones.addFeatures(&#91;entidad])    ## Añadirle a la capa temporal la entidad
            id += 1    ## Aumentar el id al acabar cada paso del bucle

capa_intersecciones.commitChanges()    ## Guardar los cambios de la capa temporal
</pre></div>


<div style="height:20px;" aria-hidden="true" class="wp-block-spacer"></div>


<p><a id="diferencia"></a></p>


<h3 class="has-text-align-center"><strong>Diferencia</strong></h3>



<p>Con la diferencia obtendríamos la superficie de cada entidad de una primera capa que no coincide espacialmente con ninguna entidad de la segunda capa. El procedimiento es casi igual que con la intersección (necesario que las capas sean polígonos):</p>


<div class="wp-block-syntaxhighlighter-code "><pre class="brush: python; title: ; notranslate" title="">
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
    entidad.setAttributes(&#91;id])
    capa_diferencia.addFeatures(&#91;entidad])
    id += 1 
capa_diferencia.commitChanges()
</pre></div>


<p>En este caso, lo que se hace es crear un objeto con la geometría de cada entidad de la primera capa y modificarlo o &#8216;recortarlo&#8217; con las geometrías de las entidades de la segunda capa. Después, la geometría resultante es almacenada en la capa temporal junto a su id.</p>


  
  <br></details>
