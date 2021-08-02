from opentrons import protocol_api
import json
import opentrons.execute
import configparser
import math
import string



# metadata
metadata = {
    'protocolName': 'Porotocolo - WGener SARS-CoV-2 RT Detection',
    'author': 'CIBIO-WL (Nicolas Aira y Mariano Depiante)',
    'description': 'Protocolo para el alicuotado de los 4 semielavorados del kit',
    'apiLevel': '2.10'
}


# Info de configuracion

config = configparser.ConfigParser()
config.read('config.ini')
# config.read('/data/user_storage/config.ini')
rvo = config.get('REACTIVO', 'reactivo')
num_racks = int(config.get('NUM_RACKS', 'num_racks'))
primer_tip = config.get('FIRST_TIP', 'tip')
last_tube = config.get('LAST_TUBE', 'tube')

#### Carga de los tubos con el reactivo a alicuotar

if rvo == '5x' or rvo == 'nfw' or rvo == 'pc':
    falcons = dict(config.items('VOL_FALCONS'))

    # Procesamos el diccionario para que sea mas facil correrlo
    # Pasamos el volumen de los falcons a uL

    falcons = {k.upper(): int(v) * 1000 for (k, v) in falcons.items()}

elif rvo == '40x':
    falcons = {}
    for i in string.ascii_uppercase[:4]:
        for j in range(1,8):
            falcons[i+str(j)] = 1500



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


#### Parametros geometricos de los tubos con los reactivos

if rvo == '5x' or rvo == 'nfw' or rvo == 'pc':
    vol_limite = 3750  # Vol a partir del cual toma desde la base
    altura_base = 16
    rate_mm_mL = 1.86
    vol_muerto = 200 + vol_dispensar*1.1

elif rvo == '40x':
    vol_limite = 300 # Vol a partir del cual toma desde la base
    altura_base = 8
    rate_mm_mL = 7.57
    vol_muerto = vol_dispensar*1.1




# protocol run function
def run(protocol: protocol_api.ProtocolContext):
    
    
    #Prende la luz
    protocol.set_rail_lights(True)

    

    # labware
    if rvo == '5x' or rvo == 'nfw':
        tiprack = protocol.load_labware('opentrons_96_filtertiprack_1000ul', 10)

    elif rvo == '40x' or rvo == 'pc':
        tiprack = protocol.load_labware('opentrons_96_filtertiprack_200ul', 10)


    if rvo == '5x' or rvo == 'nfw' or rvo == 'pc':
        plate = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 11)

    elif rvo == '40x':
        plate = protocol.load_labware('wiener_28_wellplate_5000ul', 11)


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


    last_tube_obj = racks[-1].wells_by_name()[last_tube]
    print('ULTIMO TUBO>>>',last_tube_obj)

    ##################### PROTOCOLO #####################


    pipette.pick_up_tip(tiprack[primer_tip])



    for i in range(num_racks):

        c = 0

        wells_per_rack = len(racks[i].wells())  # para el rack nuestro seria 40

        for falcon, vol in falcons.items():

            print('FALCON:', falcon, '- VOLUMEN:', vol)

            # Se busca el primer falcon que tenga volumen
            if vol < vol_muerto:
                continue
                # Si el volumen es menor al volumen muerto busca el siguiente falcon
            else:
                pass


            # Configuracion de la altura inicial del tip
            # Toma como punto limite el cono inferior del falcon (aprox 3750uL)
            # A partir de ahi toma desde el fondo

            if vol > vol_limite:
                pipette.well_bottom_clearance.aspirate = altura_base + ((vol-vol_limite)/1000) * rate_mm_mL
            else:
                pipette.well_bottom_clearance.aspirate = .5



            while c < wells_per_rack:


                if vol_pipeta >= vol_dispensar:

                    pipette.aspirate(vol_pipeta, plate[falcon])

                    for m in range(vol_pipeta//vol_dispensar):

                        # Chequea que c no genere un OutOfIndex
                        if c < wells_per_rack:
                            pipette.dispense(vol_dispensar, racks[i].wells()[c].bottom(10))

                            if racks[i].wells()[c] == last_tube_obj:
                                c = wells_per_rack
                            else:
                                c += 1
                        else:
                            pipette.blow_out(plate[falcon])
                            break


                    pipette.dispense(vol_pipeta%vol_dispensar, plate[falcon].top() )


                    # Volumen utilizado en uL
                    vol_usado = vol_dispensar*(vol_pipeta//vol_dispensar)


                    # Se descuenta el volumen usado del falcon
                    falcons[falcon] -= vol_usado



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

                    if racks[i].wells()[c] == last_tube_obj:
                        break
                    else:
                        c += 1



                if pipette.well_bottom_clearance.aspirate > 19.1:
                    pipette.well_bottom_clearance.aspirate -= rate_mm_mL * vol_usado/1000
                else:
                    pipette.well_bottom_clearance.aspirate = .5


                # Chequeo del volumen del falcon antes de repetir cada paso
                if falcons[falcon] < vol_muerto:
                    break
                else:
                    continue

            # A los 18 mm se va a .5. En la documentacion hay acalara que hay que tener
            # cuidado con que tome valores negativos pq se estrella el tip.

    # pipette.drop_tip()
    pipette.return_tip()

    #Apaga la luz
    protocol.set_rail_lights(False)



