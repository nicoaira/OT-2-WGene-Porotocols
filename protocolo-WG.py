from opentrons import protocol_api
import json
import opentrons.execute
import configparser
import math



# metadata
metadata = {
    'protocolName': 'Porotocolo - WGener SARS-CoV-2 RT Detection',
    'author': 'CIBIO-WL (Nicolas Aira y Mariano Depiante)',
    'description': 'Protocolo para el alicuotado de los 4 semielavorados del kit',
    'apiLevel': '2.10'
}


# Info de configuracion

config = configparser.ConfigParser()

config.read('/data/user_storage/config.ini')
rvo = config.get('REACTIVO', 'reactivo')
num_racks = int(config.get('NUM_RACKS', 'num_racks'))
falcons = dict(config.items('VOL_FALCONS'))
primer_tip = config.get('FIRST_TIP', 'tip')

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

elif rvo == 'pc':
    vol_pipeta = 200
    vol_dispensar = 54







# protocol run function
def run(protocol: protocol_api.ProtocolContext):
    
    
    #Prende la luz
    protocol.set_rail_lights(True)

    

    # labware
    if rvo == '5x' or rvo == 'nfw':
        tiprack = protocol.load_labware('opentrons_96_filtertiprack_1000ul', 10)

    elif rvo == '40x' or rvo == 'pc':
        tiprack = protocol.load_labware('opentrons_96_filtertiprack_200ul', 10)

    plate = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 11)


    # Los racks se cargan en una lista.
    # La cantidad de racks cargados depende del numero indicado anteriormente

    racks = []

    for i in range(1, num_racks+1):

        if rvo == 'nfw':
            racks.append(protocol.load_labware('wienerlab_40_reservoir_2000ul', i))

        elif rvo == '5x' or rvo == '40x' or rvo == 'pc':
           racks.append(protocol.load_labware('wienerlab_40_reservoir_500ul', i))
    

    # pipettes
    if rvo == '5x' or rvo == 'nfw':
        pipette = protocol.load_instrument(
            'p1000_single', 'left', tip_racks=[tiprack])

    elif rvo == '40x' or rvo == 'pc':
        pipette = protocol.load_instrument(
            'p300_single', 'right', tip_racks=[tiprack])




    # commands
    pipette.pick_up_tip(tiprack[primer_tip])


    for i in range(num_racks):

        c = 0

        wells_per_rack = len(racks[i].wells())  # para el rack nuestro seria 40

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
                pipette.well_bottom_clearance.aspirate = 16 + ((vol-3750)/1000) * 1.86
            else:
                pipette.well_bottom_clearance.aspirate = .5
                

            while c < wells_per_rack:


                if vol_pipeta >= vol_dispensar:

                    pipette.aspirate(vol_pipeta, plate[falcon])

                    for m in range(vol_pipeta//vol_dispensar):

                        # Chequea que c no genere un OutOfIndex
                        if c+m < wells_per_rack:
                            pipette.dispense(vol_dispensar, racks[i].wells()[c+m].bottom(10))
                        else:
                            pipette.blow_out(plate[falcon])
                            break


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

                            pipette.dispense(vol_dispensar/pasos, racks[i].wells()[c].bottom(10))
                            # Se descuenta el volumen usado del falcon
                        

                    pipette.dispense(vol_pipeta%(vol_dispensar/pasos), plate[falcon].top() )


                    # Volumen utilizado en uL
                    vol_usado = vol_dispensar

                    # Se descuenta el volumen usado del falcon
                    falcons[falcon] -= vol_usado
                    print('Volumen en el falcon', falcon, '>>', falcons[falcon])

                    c += 1




                if pipette.well_bottom_clearance.aspirate > 19.1:
                    pipette.well_bottom_clearance.aspirate -= 1.86 * vol_usado/1000
                else:
                    pipette.well_bottom_clearance.aspirate = .5


                # Chequeo del volumen del falcon antes de repetir cada paso
                if falcons[falcon] < 200 + vol_dispensar*1.1:
                    break
                else:
                    continue

            # A los 18 mm se va a .5. En la documentacion hay acalara que hay que tener
            # cuidado con que tome valores negativos pq se estrella el tip.

    # pipette.drop_tip()
    pipette.return_tip()

    #Apaga la luz
    protocol.set_rail_lights(False)



