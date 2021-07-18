>* property **door_closed**
>
>Returns True if the robot door is closed


>* **resume(self)**
>
>Resume a previously-paused protocol


>* **air_gap(self, volume: 'Optional[float]' = None, height: 'Optional[float]' = None) → 'InstrumentContext'¶**
>
>Pull air into the pipette current tip at the current location


>* **blow_out(self, location: 'Union[types.Location, Well]' = None) → 'InstrumentContext'**
>
>Blow liquid out of the tip.
>If dispense is used to completely empty a pipette, usually a small amount of liquid will remain in the tip. This method moves the plunger past its usual stops to fully remove any remaining liquid from the tip. Regardless of how much liquid was in the tip when this function is called, after it is done the tip will be empty.

>*property **current_volume**
>
>The current amount of liquid, in microliters, held in the pipette.

>*property **default_speed**
>
>The speed at which the robot’s gantry moves.
>By default, 400 mm/s. Changing this value will change the speed of the pipette when moving between labware. In addition to changing the default, the speed of individual motions can be changed with the speed argument to InstrumentContext.move_to().

>* **distribute(self, volume: 'Union[float, Sequence[float]]', source: 'Well', dest: 'List[Well]', *args, **kwargs) → 'InstrumentContext'**
>
>Move a volume of liquid from one source to multiple destinations.



>*property **flow_rate**
>
>The speeds (in uL/s) configured for the pipette.
>This is an object with attributes aspirate, dispense, and blow_out holding the flow rates for the corresponding operation.

>* **mix(self, repetitions: 'int' = 1, volume: 'Optional[float]' = None, location: 'Union[types.Location, Well]' = None, rate: 'float' = 1.0) → 'InstrumentContext'**
>
>Mix a volume of liquid (uL) using this pipette, by repeatedly aspirating and dispensing in the same place.


>* **pick_up_tip(self, location: 'Union[types.Location, Well]' = None, presses: 'Optional[int]' = None, increment: 'Optional[float]' = None) → 'InstrumentContext'**
>
>Pick up a tip for the pipette to run liquid-handling commands with
>If no location is passed, the Pipette will pick up the next available tip in its InstrumentContext.tip_racks list.
>The tip to pick up can be manually specified with the location argument. The location argument can be specified in several ways:


>*property **starting_tip**
>
>The starting tip from which the pipette pick up


>* **use_tips(self, start_well: opentrons.protocol_api.labware.Well, num_channels: int = 1)**
>
>Removes tips from the tip tracker.


>* ****
>
>



