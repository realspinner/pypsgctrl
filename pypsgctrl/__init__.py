## @file
# @brief Public exports for the PSG9080 driver.
"""PSG9080 serial driver. Import public classes directly from pypsgctrl."""
from .channel import Channel
from .device import PSG9080
from .enums import FrequencyUnit, Modulation, TriggerSource, Waveform
from .errors import PSGError, PSGTimeoutError, ProtocolError
from .registers import CHANNEL_REGISTERS, REGISTERS, Register
from .transport import Transport

__version__ = '0.1.1'
__all__ = [
    'PSG9080', 'Channel', 'Waveform', 'FrequencyUnit', 'Modulation',
    'TriggerSource', 'PSGError', 'ProtocolError', 'PSGTimeoutError',
    'Transport', 'Register', 'REGISTERS', 'CHANNEL_REGISTERS', '__version__',
]
