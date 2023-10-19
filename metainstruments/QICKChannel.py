import qcodes as qc
from qcodes.instrument import Instrument, ManualParameter
from qcodes.station import Station
from qcodes.utils.validators import Numbers, MultiType, Ints 
from qick import *
from qick.averager_program import QickSweep
from measurements.protocols import Protocol, NDSweepProtocol, PulseProbeSpectroscopyProtocol, T1Protocol
import numpy as np


class DACChannel(Instrument):
    
    def __init__(self, name: str, channel_number: int, **kwargs):
        '''
        As we initialize the metainstrument, each of the gettable and settable
        parameters are defined and initialized. All parameters receive some
        initial value, but those that initial values corresponding to variables
        that are sweeped over are overwritten.
        '''

        self.isDAC = True
        self.isADC = False
        
        super().__init__(name, label="QICK DAC channel",)
            
        self.sensible_defaults = {
                                   "nqz"          : 1,   # -- First nyquist zone
                                   "pulse_gain"   : 5000,# -- DAC units
                                   "pulse_phase"  : 0,   # -- Degrees
                                   "pulse_freq"   : 500, # -- MHz
                                   "pulse_length" : 10 } # -- us

        self.add_parameter('channel',
                            parameter_class=ManualParameter,
                            label='Channel number',
                            vals = Ints(*[0,6]),
                            initial_value = channel_number)

        self.add_parameter('nqz',
                            parameter_class=ManualParameter,
                            label='Nyquist zone',
                            vals = Ints(1,2),
                            initial_value = 1)

        self.add_parameter('pulse_gain',
                            parameter_class=ManualParameter,
                            label='DAC gain',
                            vals = Numbers(*[0,40000]),
                            unit = 'DAC units',
                            initial_value = 5000)

        self.add_parameter('pulse_freq',
                            parameter_class=ManualParameter,
                            label='NCO frequency',
                            vals = Numbers(*[0,9000]),
                            unit = 'MHz',
                            initial_value = 500)

        self.add_parameter('pulse_phase',
                            parameter_class=ManualParameter,
                            label='Pulse phase',
                            vals = Ints(*[0,360]),
                            unit = 'deg',
                            initial_value = 0)

        self.add_parameter('pulse_length',
                            parameter_class=ManualParameter,
                            label='Pulse length',
                            vals = Numbers(*[0,150]),
                            unit = 'us',
                            initial_value = 10)


class ADCChannel(Instrument):

    def __init__(self, name: str, channel_number: int, **kwargs):
        '''
        As we initialize the metainstrument, each of the gettable and settable
        parameters are defined and initialized. All parameters receive some
        initial value, but those that initial values corresponding to variables
        that are sweeped over are overwritten.
        '''
        
        super().__init__(name, label="QICK ADC channel")

        self.isDAC = False
        self.isADC = True
            
        self.sensible_defaults = {
                                   "nqz"          : 1,   # -- First nyquist zone
                                   "pulse_gain"   : 5000,# -- DAC units
                                   "pulse_phase"  : 0,   # -- Degrees
                                   "pulse_freq"   : 500, # -- MHz
                                   "pulse_length" : 10 } # -- us

        self.add_parameter('channel',
                            parameter_class=ManualParameter,
                            label='Channel number',
                            vals = Ints(*[0,1]),
                            initial_value = channel_number)

        self.add_parameter('nqz',
                            parameter_class=ManualParameter,
                            label='Nyquist zone',
                            vals = Ints(1,2),
                            initial_value = 1)

        self.add_parameter('pulse_gain',
                            parameter_class=ManualParameter,
                            label='DAC gain',
                            vals = Numbers(*[0,40000]),
                            unit = 'DAC units',
                            initial_value = 5000)

        self.add_parameter('pulse_freq',
                            parameter_class=ManualParameter,
                            label='NCO frequency',
                            vals = Numbers(*[0,9000]),
                            unit = 'MHz',
                            initial_value = 500)

        self.add_parameter('pulse_phase',
                            parameter_class=ManualParameter,
                            label='Pulse phase',
                            vals = Ints(*[0,360]),
                            unit = 'deg',
                            initial_value = 0)

        self.add_parameter('pulse_length',
                            parameter_class=ManualParameter,
                            label='Pulse length',
                            vals = Numbers(*[0,150]),
                            unit = 'us',
                            initial_value = 10)

