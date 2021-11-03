## Este script permite buscar manualmente un algoritmo del modulo
## processing de QGIS introduciendo el proveedor y el nombre del algoritmo.
## Si existe coincidencia lo almacena en un objeto listo para ser utilizado
## en una llamada al algoritmo dentro de processing.run().
## 

while True:
    prov_input = QInputDialog.getText(None, "Proveedor" ,"Introduzca el nombre del proveedor (QGIS, SAGA..) : ")
    proveedor = prov_input[0]
    proc_input = QInputDialog.getText(None, "Proceso" ,"Introduzca el nombre del geoproceso : ")
    proceso = proc_input[0]
    try:
        contador = 0
        for alg in QgsApplication.processingRegistry().algorithms():
            if proveedor.upper() in alg.provider().name() and proceso.lower() == alg.name():
                geoproceso = proveedor.lower() + ':' + alg.name()
                print('El geoproceso ' + geoproceso + ' existe')
                contador += 1
            else:
                continue
        if contador == 0:
            print('No se encontro el proveedor o el geoproceso')
            continue
    except:
        print('ERROR')
        break
    else:
        break

parametros = {}    
processing.run(geoproceso, parametros)
