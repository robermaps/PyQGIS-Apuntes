## Crear un nuevo campo ID autoincrementable en una capa vectorial
##

## Cargar la capa y empezar la edición
capa = QgsVectorLayer(output,nombre,'ogr')
capa.startEditing()
 
## Añadir el nuevo atributo ID
capa.dataProvider().addAttributes([QgsField('ID', QVariant.Int)])
capa.updateFields()
 
## Listar las entidades
entidades = capa.getFeatures()
 
## Iniciar el contador
contador = 0
 
## Bucle que recorre las entidades de la capa cargada
for entidad in entidades:
 
        ## Establecer el valor del atributo ID para la entidad a partir del valor del contador
        entidad['ID'] = contador
 
        ## Actualizar la entidad
        capa.updateFeature(entidad)
 
        ## Aumentar el contador
        contador += 1
 
## Guardar los cambios             
capa.commitChanges()