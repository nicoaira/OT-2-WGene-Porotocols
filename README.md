# OT-2-WGene-Porotocols

El programa consta de dos partes. Por un lado esta la interfaz gráfica (GUI), que permite al operario cargar las configuraciones del protocolo al servidor del Opentrons. Y, por otro lado, el archivo protocolo-WG.py que es el protocolo en si que lee el robot.

La interfaz grafica se encarga de subir un archivo config.ini al servidor del OT-2, el cual posee todos los parámentros de la corrida a llevarse a cabo. Este archivo se guarda en una ubicación que perdura en el servidor del Opetrons (data/user_storage), de la cual el protocolo-WG.py lee los parámetros necesarios.
