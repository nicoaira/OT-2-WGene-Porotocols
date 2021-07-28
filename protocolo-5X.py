from opentrons import protocol_api
import json
import opentrons.execute
import configparser
import math



# Info de configuracion

config = configparser.ConfigParser()

config.read('GUI/config.ini')
rvo = config.get('REACTIVO', 'reactivo')
num_racks = int(config.get('NUM_RACKS', 'num_racks'))
falcons = dict(config.items('VOL_FALCONS'))

# Procesamos el diccionario para que sea mas facil correrlo
# Pasamos el volumen de los falcons a uL

falcons = {k.upper():int(v)*1000 for (k, v) in falcons.items()}

for k,v in falcons.items():
    print(k, '>>',v)



if rvo == '5x':
    vol_pipeta = 1000
    vol_dispensar = 440

elif rvo == '40x':
    vol_pipeta = 200
    vol_dispensar = 55

elif rvo == 'nfw':
    vol_pipeta = 1000
    vol_dispensar = 1850

elif rvo == 'PC':
    vol_pipeta = 200
    vol_dispensar = 54



# metadata
metadata = {
    'protocolName': 'Prueba3',
    'author': 'Nico',
    'description': 'Protocolo de prueba escrito en python',
    'apiLevel': '2.10'
}


with open('WL_labware/wl_40_wellplate_500ul.json') as labware_file:
     rack_40_500ul = json.load(labware_file)





# protocol run function
def run(protocol: protocol_api.ProtocolContext):
    
    
    #Prende la luz
    protocol.set_rail_lights(True)

    

    # labware
    if rvo == '5x' or rvo == 'nfw':
        tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 10)

    elif rvo == '40x' or rvo == 'PC':
        tiprack = protocol.load_labware('opentrons_96_tiprack_200ul', 10)

    plate = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 11)


    # Los racks se cargan en una lista.
    # La cantidad de racks cargados depende del numero indicado anteriormente

    racks_500ul = []

    for i in range(1, num_racks+1):
        racks_500ul.append(protocol.load_labware_from_definition(rack_40_500ul, i))
    

    # pipettes
    if rvo == '5x' or rvo == 'nfw':
        pipette = protocol.load_instrument(
            'p1000_single', 'left', tip_racks=[tiprack])

    elif rvo == '40x' or rvo == 'PC':
        pipette = protocol.load_instrument(
            'p300_single', 'right', tip_racks=[tiprack])    




    # commands
    pipette.pick_up_tip()


    for i in range(num_racks):

        c = 0

        wells_per_rack = len(racks_500ul[i].wells())  # para el rack nuestro seria 40

        for falcon, vol in falcons.items():

            print('FALCON:', falcon, '- VOLUMEN:', vol)

            # Se busca el primer falcon que tenga volumen
            if vol < 200 + vol_dispensar*1.1:
                continue
                # Si el volumen es menor a 1100 uL busca el siguiente falcon
            else:
                pass


            # Configuracion de la altura inicial del tip
            # Toma como punto limite el cono inferior del falcon (aprox 3750uL)
            # A partir de ahi toma desde el fondo

            if vol > 3750:
                pipette.well_bottom_clearance.aspirate = 19.1 + ((vol-3750)/1000) * 1.86
            else:
                pipette.well_bottom_clearance.aspirate = .5

            while c < wells_per_rack:
            # Hay que agregar algo para corroborar que se llene el ultimo well
            # Ya que si c = wells_per_rack se va a romper el loop


            if vol_pipeta >= vol_dispensar:
                pipette.aspirate(vol_pipeta, plate[falcon])
                for m in range(vol_pipeta//vol_dispensar):
                    pipette.dispense(vol_dispensar, racks_500ul[i].wells()[c+m].bottom(10))


                pipette.dispense(vol_pipeta%vol_dispensar, plate[falcon].top() )


                # Volumen utilizado en uL
                vol_usado = vol_dispensar*(vol_pipeta//vol_dispensar)


                # Se descuenta el volumen usado del falcon
                falcons[falcon] -= vol_usado

                # Cantidad de wells que se llenan en cada paso
                c += vol_pipeta//vol_dispensar



            else:
                pasos = math.ceil(vol_dispensar/vol_pipeta)

                pipette.aspirate(vol_pipeta, plate[falcon])
                for m in range(pasos):
                    pipette.dispense(vol_dispensar, racks_500ul[i].wells()[c].bottom(10))

                    # Se descuenta el volumen usado del falcon
                    falcons[falcon] -= vol_dispensar   

                pipette.dispense(vol_pipeta%vol_dispensar, plate[falcon].top() )


                # Volumen utilizado en uL
                vol_usado = vol_dispensar

                # Se descuenta el volumen usado del falcon
                falcons[falcon] -= vol_usado




            if pipette.well_bottom_clearance.aspirate > 19.1:
                pipette.well_bottom_clearance.aspirate -= 1.86 * vol_usado/1000
            else:
                pipette.well_bottom_clearance.aspirate = .5


            # Chequeo del volumen del falcon antes de repetir cada paso
            if falcons[falcon] < 1100:
                break
            else:
                continue

        # A los 18 mm se va a .5. En la documentacion hay acalara que hay que tener
        # cuidado con que tome valores negativos pq se estrella el tip.

    pipette.drop_tip()

    #Apaga la luz
    protocol.set_rail_lights(False)



