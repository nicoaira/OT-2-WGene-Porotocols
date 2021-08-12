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
# config.read('/data/user_storage/config.ini')
config.read('config.ini')
rvo = config.get('REACTIVO', 'reactivo')
num_racks = int(config.get('NUM_RACKS', 'num_racks'))
num_tandas = int(config.get('NUM_TANDAS', 'num_tandas'))
primer_tip = config.get('FIRST_TIP', 'tip')
last_tube = config.get('LAST_TUBE', 'tube')


if rvo == '5x' or rvo == 'nfw':
    vel_asp= int(config.get('VEL_P1000', 'asp'))
    vel_disp = int(config.get('VEL_P1000', 'disp'))

elif rvo == 'pc' or rvo == '40x':
    vel_asp = int(config.get('VEL_P300', 'asp'))
    vel_disp = int(config.get('VEL_P300', 'disp'))


factor_vel_mov_ot = float(config.get('VEL_OT-2', 'vel_mov_ot'))


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
            falcons[i+str(j)] = 2500



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
    altura_base = 12
    altura_limite = 19.1
    rate_mm_mL = 1.86
    vol_muerto = vol_pipeta*1.4

elif rvo == '40x':
    vol_limite = 200 # Vol a partir del cual toma desde la base
    altura_base = 2
    altura_limite = 12
    rate_mm_mL = 7.57
    vol_muerto = vol_pipeta*1.4




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


    

    ##################### PROTOCOLO #####################

    pipette.default_speed = 300 * factor_vel_mov_ot #controla la velocidad general del OT2, predeterminada 400mm/s
    pipette.flow_rate.aspirate = vel_asp #controla la velocidad de aspiración, predeterminada
    pipette.flow_rate.dispense = vel_disp  # controla la velocidad de dispensado, predeterminada
    pipette.flow_rate.blow_out = 20  # controla la velocidad de expulción de flujo, predeterminada
    
    pipette.pick_up_tip(tiprack[primer_tip])




    for t in range(num_tandas):


        for i in range(num_racks):

            c = 0

            wells_per_rack = len(racks[i].wells())


            for falcon, vol in falcons.items():

                # Se busca el primer falcon que tenga volumen
                if vol < vol_muerto:
                    continue
                    # Si el volumen es menor al volumen muerto busca el siguiente falcon
                else:
                    pass


                # Configuracion de la altura inicial del tip
                # Toma como punto limite el cono inferior del falcon
                # A partir de ahi toma desde el fondo

                if vol > vol_limite:
                    pipette.well_bottom_clearance.aspirate = altura_base + ((vol-vol_limite)/1000) * rate_mm_mL
                else:
                    pipette.well_bottom_clearance.aspirate = .5



                while c < wells_per_rack:


                    if vol_pipeta >= vol_dispensar:

                        pipette.aspirate(vol_pipeta, plate[falcon])



                        for m in range(vol_pipeta//vol_dispensar):

                            if c < wells_per_rack and vol > vol_muerto:
                                pipette.dispense(vol_dispensar, racks[i].wells()[c].bottom(7), rate = 0.5)
                                pipette.touch_tip(racks[i].wells()[c], radius = 0.70, v_offset = -15 )
                                pipette.default_speed = 80 * factor_vel_mov_ot
                                protocol.delay(1.2)

                                c_temp = c

                                if racks[i].wells()[c] == last_tube_obj:
                                    c = wells_per_rack  #Para salir del bucle while
                                else:
                                    c += 1
                            else:
                                pipette.blow_out(plate[falcon])
                                break

                        pipette.default_speed = 300 * factor_vel_mov_ot 
                        # controla la velocidad general del OT2, predeterminada 400mm/s

                        pipette.dispense(vol_pipeta%vol_dispensar, plate[falcon].bottom(pipette.well_bottom_clearance.aspirate+7), rate = 0.5)
                        protocol.delay(1.2)
                        pipette.blow_out(plate[falcon].bottom(pipette.well_bottom_clearance.aspirate+7))



                        # Volumen utilizado en uL
                        vol_usado = vol_dispensar*(vol_pipeta//vol_dispensar)


                        # Se descuenta el volumen usado del falcon
                        falcons[falcon] -= vol_usado

                        volumen_actual = 'VOLUMEN EN FALCON ' + falcon + ' > '+ str(falcons[falcon])
                        protocol.comment(volumen_actual)



                    else:

                        pasos = math.ceil(vol_dispensar/vol_pipeta)


                        for m in range(pasos):

                            # Chequeo del volumen del falcon antes de repetir cada paso
                            if falcons[falcon] < vol_muerto:
                                break
                            else:
                                pipette.aspirate(vol_pipeta, plate[falcon])
                                pipette.dispense(vol_dispensar/pasos, racks[i].wells()[c].bottom(10))
                                pipette.dispense(vol_pipeta % (vol_dispensar / pasos), plate[falcon].top())



                        # Volumen utilizado en uL
                        vol_usado = vol_dispensar*pasos

                        # Se descuenta el volumen usado del falcon
                        falcons[falcon] -= vol_usado


                        if racks[i].wells()[c] == last_tube_obj:
                            break
                        else:
                            c += 1



                    if pipette.well_bottom_clearance.aspirate > altura_limite:
                        pipette.well_bottom_clearance.aspirate -= rate_mm_mL * vol_usado/1000
                    else:
                        pipette.well_bottom_clearance.aspirate = .5



                    # Chequeo del volumen del falcon antes de repetir cada paso
                    if falcons[falcon] < vol_muerto:

                        if num_tandas > 1 and racks[i].wells()[c_temp] != last_tube_obj:
                            protocol.comment('No queda mas volumen para asipirar!')
                            mensaje_tanda = 'Tanda ' + str(t+1) + '/' + str(num_tandas) + ' incompleta!'
                            protocol.comment(msg = mensaje_tanda)
                            protocol.comment(msg = "Chequee cual es el ultimo tubo alicuotado.")
                            protocol.comment('Terminando protocolo!')

                        elif num_tandas == 1 and racks[i].wells()[c_temp] != last_tube_obj:
                            protocol.comment(msg = "No se completaron todos lo racks!")
                            protocol.comment(msg = "Chequee cual es el ultimo tubo alicuotado.")
                            protocol.comment('Terminando protocolo!')

                        break



                    else:
                        continue





        if num_tandas > 1:




            if any([True if v > vol_muerto else False for v in falcons.values()]):

                for l in range(5):
                    protocol.set_rail_lights(False)
                    protocol.delay(0.5)
                    protocol.set_rail_lights(True)

                mensaje_tanda = 'Tanda ' + str(t+1) + '/' + str(num_tandas) + ' completada!'
                protocol.comment(msg = mensaje_tanda)


                if t < num_tandas - 1:
                    mensaje_carga = 'Cargue los '+str(num_racks)+' racks nuevos y haga click en "Resume"'
                    protocol.pause(msg = mensaje_carga)

            else:
                protocol.cleanup()
                break



    cache_volumenes = configparser.ConfigParser()
    cache_volumenes['VOLUMENES'] = falcons

    with open('cache_volumenes.ini', 'w') as cache_file:
        cache_volumenes.write(cache_file)




    # pipette.drop_tip()
    pipette.return_tip()

    #Apaga la luz
    protocol.set_rail_lights(False)



