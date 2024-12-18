from header import *

readout_pulse.length.set(0.2e-6)
readout_adc.length.set(1e-6)

qi.set_macro_list(
    [
        Trigger(qi, readout_adc, t=0),
        PlayPulse(qi, readout_pulse),
    ]
)

qi.hard_avgs.set(1)
qi.soft_avgs.set(100)

qi.run(
    Measurement(station=station, name=Path(__file__).name[:-3]),
    acquisition_mode="decimated",
)
