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
config.read('/data/user_storage/config.ini')
# config.read('config.ini')
rvo = config.get('REACTIVO', 'reactivo')
num_racks = int(config.get('NUM_RACKS', 'num_racks'))
num_tandas = int(config.get('NUM_TANDAS', 'num_tandas'))
primer_tip = config.get('FIRST_TIP', 'tip')
last_tube = config.get('LAST_TUBE', 'tube')
num_falcons = int(config.get('NUM_FALCONS', 'num_falcons'))


if rvo == '5x' or rvo == 'nfw':
    vel_asp= int(config.get('VEL_P1000', 'asp'))
    vel_disp = int(config.get('VEL_P1000', 'disp'))

elif rvo == 'pc' or rvo == '40x':
    vel_asp = int(config.get('VEL_P300', 'asp'))
    vel_disp = int(config.get('VEL_P300', 'disp'))


factor_vel_mov_ot = float(config.get('VEL_OT-2', 'vel_mov_ot'))



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
<<<<<<< HEAD

    p = 0

    for j in range(1, 8):
        for i in string.ascii_uppercase[:4]:
            if p < num_falcons:
                falcons[i+str(j)] = 2500
            else:
                falcons[i+str(j)] = 0

            p += 1
=======
    for i in string.ascii_uppercase[:4]:
        for j in range(1,8):
            falcons[i+str(j)] = 2500
>>>>>>> 80904326f2566e91befb939caaaa7d377eac58ba



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
<<<<<<< HEAD
    altura_base = 8
    altura_limite = 10
    rate_mm_mL = 1.86
    vol_muerto = vol_pipeta*1.4

=======
    altura_base = 12
    altura_limite = 19.1
    rate_mm_mL = 1.86
    vol_muerto = vol_pipeta*1.4
>>>>>>> 80904326f2566e91befb939caaaa7d377eac58ba

elif rvo == '40x':
    vol_limite = 200 # Vol a partir del cual toma desde la base
    altura_base = 2
    altura_limite = 12
    rate_mm_mL = 7.57
    vol_muerto = vol_pipeta*1.4
<<<<<<< HEAD



if rvo == '5x':
    vol_muerto = 1500

elif rvo == 'nfw':
    vol_muerto = 3000

elif rvo == 'pc':
    vol_muerto = 600

elif rvo == '40x':
    vol_muerto = 350
=======
>>>>>>> 80904326f2566e91befb939caaaa7d377eac58ba




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
    pipette.flow_rate.aspirate = vel_asp #controla la velocidad de aspiraci??n, predeterminada
    pipette.flow_rate.dispense = vel_disp  # controla la velocidad de dispensado, predeterminada
<<<<<<< HEAD

    if rvo == '5x' or rvo == 'nfw':
        pipette.flow_rate.blow_out = 80
=======
    pipette.flow_rate.blow_out = 20  # controla la velocidad de expulci??n de flujo, predeterminada
    pipette.starting_tip = tiprack[primer_tip]
    pipette.pick_up_tip()

>>>>>>> 80904326f2566e91befb939caaaa7d377eac58ba

    elif rvo == '5x':
        pipette.flow_rate.blow_out = 40

    elif rvo == '40x' or rvo == 'pc':
        pipette.flow_rate.blow_out = 20

<<<<<<< HEAD


  # controla la velocidad de expulci??n de flujo, predeterminada
    pipette.starting_tip = tiprack[primer_tip]
    pipette.pick_up_tip()




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

=======
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
>>>>>>> 80904326f2566e91befb939caaaa7d377eac58ba

                if vol > vol_limite:
                    pipette.well_bottom_clearance.aspirate = altura_base + ((vol-vol_limite)/1000) * rate_mm_mL
                else:
                    pipette.well_bottom_clearance.aspirate = .5

                while c < wells_per_rack:


<<<<<<< HEAD
                    if vol_pipeta >= vol_dispensar:

                        pipette.aspirate(vol_pipeta, plate[falcon])



                        for m in range(vol_pipeta//vol_dispensar):

                            if c < wells_per_rack and vol > vol_muerto:
                                pipette.dispense(vol_dispensar, racks[i].wells()[c].bottom(7), rate = 0.5)
                                pipette.touch_tip(racks[i].wells()[c], radius = 0.60, v_offset = -15 )
=======
                while c < wells_per_rack:


                    if vol_pipeta >= vol_dispensar:

                        pipette.aspirate(vol_pipeta, plate[falcon])



                        for m in range(vol_pipeta//vol_dispensar):

                            if c < wells_per_rack and vol > vol_muerto:
                                pipette.dispense(vol_dispensar, racks[i].wells()[c].bottom(7), rate = 0.5)
                                pipette.touch_tip(racks[i].wells()[c], radius = 0.70, v_offset = -15 )
>>>>>>> 80904326f2566e91befb939caaaa7d377eac58ba
                                pipette.default_speed = 80 * factor_vel_mov_ot
                                protocol.delay(1.2)

                                c_temp = c

                                if racks[i].wells()[c] == last_tube_obj:
                                    c = wells_per_rack  #Para salir del bucle while
                                else:
                                    c += 1
                            else:
<<<<<<< HEAD
                                pipette.default_speed = 300 * factor_vel_mov_ot
                                pipette.blow_out(plate[falcon].bottom(pipette.well_bottom_clearance.aspirate+7))
                                break

                        pipette.default_speed = 300 * factor_vel_mov_ot 
=======
                                pipette.blow_out(plate[falcon])
                                break

                        pipette.default_speed = 300 * factor_vel_mov_ot 
                        # controla la velocidad general del OT2, predeterminada 400mm/s
>>>>>>> 80904326f2566e91befb939caaaa7d377eac58ba

                        pipette.dispense(vol_pipeta%vol_dispensar, plate[falcon].bottom(pipette.well_bottom_clearance.aspirate+7), rate = 0.5)
                        protocol.delay(1.2)
                        pipette.blow_out(plate[falcon].bottom(pipette.well_bottom_clearance.aspirate+7))



                        # Volumen utilizado en uL
                        vol_usado = vol_dispensar*(vol_pipeta//vol_dispensar)


                        # Se descuenta el volumen usado del falcon
                        falcons[falcon] -= vol_usado

<<<<<<< HEAD
                        volumen_actual = 'Volumen remanente en ' + falcon + ' : '+ str(falcons[falcon])
=======
                        volumen_actual = 'VOLUMEN EN FALCON ' + falcon + ' > '+ str(falcons[falcon])
>>>>>>> 80904326f2566e91befb939caaaa7d377eac58ba
                        protocol.comment(volumen_actual)



                    else:
<<<<<<< HEAD

                        pasos = math.ceil(vol_dispensar/vol_pipeta)

                        protocol.comment('Altura de aspirado ' + str(pipette.well_bottom_clearance.aspirate))

                        for m in range(pasos):

                            # Chequeo del volumen del falcon antes de repetir cada paso
                            # if falcons[falcon] < vol_muerto:
                            # #     break
                            # else:
                            pipette.aspirate(vol_pipeta, plate[falcon])
                            pipette.dispense(vol_dispensar/pasos, racks[i].wells()[c].top(-4))
                            pipette.touch_tip(racks[i].wells()[c], radius = 0.70, v_offset = -4 )
                            pipette.dispense(vol_pipeta % (vol_dispensar / pasos), plate[falcon].bottom(pipette.well_bottom_clearance.aspirate+15))


                        # Volumen utilizado en uL
                        vol_usado = vol_dispensar

                        # Se descuenta el volumen usado del falcon
                        falcons[falcon] -= vol_usado
                        protocol.comment('Volumen en falcon ' + falcon + ': ' + str(falcons[falcon]))

                        if racks[i].wells()[c] == last_tube_obj:
                            break
                        else:
                            c_temp = c
                            c += 1




                    if pipette.well_bottom_clearance.aspirate > altura_limite:
                        pipette.well_bottom_clearance.aspirate -= rate_mm_mL * vol_usado/1000
                    else:
                        pipette.well_bottom_clearance.aspirate = .5
=======
>>>>>>> 80904326f2566e91befb939caaaa7d377eac58ba

                        pasos = math.ceil(vol_dispensar/vol_pipeta)


<<<<<<< HEAD
                    # Chequeo del volumen del falcon antes de repetir cada paso

                    all_empty = all([True if v < vol_muerto else False for v in falcons.values()])
                    # Boleano que da True si todos los falcons estan vacios

                    if falcons[falcon] < vol_muerto:


                        if all_empty and num_tandas > 1 and racks[i].wells()[c_temp] != last_tube_obj:
                            protocol.comment('No queda mas volumen para asipirar!')
                            mensaje_tanda = 'Tanda ' + str(t+1) + '/' + str(num_tandas) + ' incompleta!'
                            protocol.comment(msg = mensaje_tanda)
                            protocol.comment(msg = "Chequee cual es el ultimo tubo alicuotado.")
                            protocol.comment('Terminando protocolo!')

                        elif all_empty and num_tandas == 1 and racks[i].wells()[c_temp] != last_tube_obj:
                            protocol.comment(msg = "No se completaron todos lo racks!")
                            protocol.comment(msg = "Chequee cual es el ultimo tubo alicuotado.")
                            protocol.comment('Terminando protocolo!')

                        else:
                            protocol.comment(msg="Falcon vacio, pasando al siguiente...")

                        break

=======
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



>>>>>>> 80904326f2566e91befb939caaaa7d377eac58ba
                    else:
                        continue



<<<<<<< HEAD
        if num_tandas > 1:


            if any([True if v > vol_muerto else False for v in falcons.values()]):

                for l in range(5):
                    protocol.set_rail_lights(False)
                    protocol.delay(1.5)
                    protocol.set_rail_lights(True)

                mensaje_tanda = 'Tanda ' + str(t+1) + '/' + str(num_tandas) + ' completada!'
                protocol.comment(msg = mensaje_tanda)


                if t < num_tandas - 1:
                    mensaje_carga = 'Cargue los ' + str(num_racks) + ' racks nuevos y haga click en "Resume"'
                    protocol.pause(msg = mensaje_carga)

            else:
                protocol.cleanup()
                break



    # cache_volumenes = configparser.ConfigParser()
    # cache_volumenes['VOLUMENES'] = falcons
    #
    # with open('cache_volumenes.ini', 'w') as cache_file:
    #     cache_volumenes.write(cache_file)


=======


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


>>>>>>> 80904326f2566e91befb939caaaa7d377eac58ba


    # pipette.drop_tip()
    pipette.return_tip()

    #Apaga la luz
    protocol.set_rail_lights(False)



