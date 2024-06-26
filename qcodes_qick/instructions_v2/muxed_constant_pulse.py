from __future__ import annotations

from typing import TYPE_CHECKING

from qcodes.parameters import ManualParameter
from qcodes.validators import Ints
from qcodes.validators import Sequence as SequenceValidator

from qcodes_qick.instruction_base_v2 import QickInstruction
from qcodes_qick.muxed_dac import MuxedDacChannel
from qcodes_qick.parameters import SecParameter

if TYPE_CHECKING:
    from qcodes_qick.instruments import QickInstrument
    from qcodes_qick.protocol_base_v2 import HardwareSweep, SweepProgram


class MuxedConstantPulse(QickInstruction):
    """Frequency-multiplexed rectangular pulse.

    Parameters
    ----------
    parent : QickInstrument
        Make me a submodule of this QickInstrument.
    dac : MuxedDacChannel
        The DAC channel to use.
    name : str
        My unique name.
    **kwargs : dict, optional
        Keyword arguments to pass on to InstrumentBase.__init__.
    """

    def __init__(
        self,
        parent: QickInstrument,
        dac: MuxedDacChannel,
        name="MuxedConstantPulse",
        **kwargs,
    ):
        super().__init__(parent, dacs=[dac], name=name, **kwargs)
        assert isinstance(dac, MuxedDacChannel)

        self.length = SecParameter(
            name="length",
            instrument=self,
            label="Pulse length",
            initial_value=10e-6,
            channel=self.dacs[0],
        )
        self.tone_nums = ManualParameter(
            name="tone_nums",
            instrument=self,
            label="List of tone numbers to generate",
            initial_value=[0],
            vals=SequenceValidator(Ints(0, len(self.dacs[0].tones) - 1)),
        )

    def initialize(self, program: SweepProgram):
        """Add initialization commands to a program.

        Parameters
        ----------
        program : SweepProgram
        """
        program.add_pulse(
            ch=self.dacs[0].channel_num,
            name=self.full_name,
            style="const",
            mask=self.tone_nums.get(),
            length=self.length.get() * 1e6,
        )

    def play(self, program: SweepProgram):
        """Append me to a program.

        Parameters
        ----------
        program : SweepProgram
        """
        program.pulse(ch=self.dacs[0].channel_num, name=self.full_name, t="auto")

    def add_sweep(self, program: SweepProgram, sweep: HardwareSweep):
        """Add a sweep over one of my parameters to a program.

        Parameters
        ----------
        program : SweepProgram
        sweep: HardwareSweep
        """
        raise NotImplementedError(
            f"cannot perform a hardware sweep over {sweep.parameter.name}"
        )
