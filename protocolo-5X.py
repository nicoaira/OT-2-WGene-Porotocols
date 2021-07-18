#!/usr/bin/env python
# coding: utf-8

# In[19]:


from opentrons import protocol_api
import json
import opentrons.execute


# metadata
metadata = {
    'protocolName': 'Prueba3',
    'author': 'Nico',
    'description': 'Protocolo de prueba escrito en python',
    'apiLevel': '2.10'
}


with open('WL_labware/wl_40_wellplate_500ul.json') as labware_file:
     rack_40_500ul = json.load(labware_file)


num_racks = 9



# protocol run function
def run(protocol: protocol_api.ProtocolContext):
    
    
    #Prende la luz
    protocol.set_rail_lights(True)

    

    # labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_1000ul', 10)
    plate = protocol.load_labware('opentrons_6_tuberack_falcon_50ml_conical', 11)


    # Los racks se cargan en una lista.
    # La cantidad de racks cargados depende del numero indicado anteriormente

    racks_500ul = []

    for i in range(1, num_racks+1):
        racks_500ul.append(protocol.load_labware_from_definition(rack_40_500ul, i))
    

    # pipettes
    left_pipette = protocol.load_instrument(
         'p1000_single', 'left', tip_racks=[tiprack])

    # commands
    left_pipette.pick_up_tip()
    left_pipette.well_bottom_clearance.aspirate = 84


    for i in range(num_racks):

        c = 0

        for well in racks_500ul[i].wells()[::2]:
            # De a dos wells a la vez



            left_pipette.aspirate(1000, plate['A1'])
            left_pipette.dispense(440, racks_500ul[i].wells()[c].bottom(15))
            left_pipette.dispense(440, racks_500ul[i].wells()[c+1].bottom(15))
            left_pipette.dispense(120, plate['A1'].top() )

            if left_pipette.well_bottom_clearance.aspirate > 18:
                left_pipette.well_bottom_clearance.aspirate -= 1.65
            else:
                left_pipette.well_bottom_clearance.aspirate = .5

            c += 2

        # A los 18 mm se va a .5. En la documentacion hay acalara que hay que tener
        # cuidado con que tome valores negativos pq se estrella el tip.

    left_pipette.drop_tip()

    #Apaga la luz
    protocol.set_rail_lights(False)



