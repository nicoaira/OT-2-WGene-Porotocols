# OT-2-WGene Porotocol Designer
___

![alt text](https://i.ibb.co/SmfhkrS/logo.png?raw=true "Logo")

___

## interfaz gráfica (GUI):

Permite al operario cargar las configuraciones del protocolo al servidor del Opentrons.

### Pantalla prinicipal
<img src="https://i.ibb.co/Wt7cT04/MAIN.png" width=40% height=40%>

### Configuraciones avanzadas
<img src="https://i.ibb.co/g3m3gfs/avanzadas.png" width=40% height=40%>

### Configuraciones de protocolo (caso RT Mix)
<img src="https://i.ibb.co/K9SbYNq/protocolo.png" width=40% height=40%>

___

## Protocolo OT-2:

El OT-2 puede correr protocolos escritos en Python. Para esto existe una API de Opentrons, cuya documentación puede encontrarse en este [link](https://docs.opentrons.com/OpentronsPythonAPIV2.pdf). 
En este caso y para facilitar la experiencia del operador, se creó un único protocolo flexible que puede ejecutar el alicuotado de cualquiera de los reactivos, según los parámetros ingresados en la etapa de configuración con la GUI.

La interfaz gráfica se encarga de subir el archivo config.ini al servidor del OT-2, el cual posee todos los parámentros de la corrida a llevarse a cabo. Este archivo se guarda en una ubicación que perdura en el servidor del OT-2 (data/user_storage), de la cual el protocolo-WG.py lee los parámetros necesarios.

___

## OT-2

<img src="https://img.medicalexpo.es/images_me/photo-g/116739-14574775.webp" width=50% height=50%>

Para información adicional de Opentrons, visite su [sitio oficial](https://opentrons.com). 
