## @file
# @brief Protocol enumerations.
from __future__ import annotations

from enum import IntEnum

## @brief Built-in waveform codes; arbitrary waveforms use slots 1..99.
class Waveform(IntEnum):
    SINE = 0
    SQUARE = 1
    PULSE = 2
    TRIANGLE = 3
    SLOPE = 4
    CMOS = 5
    DC = 6
    PARTIAL_SINE = 7
    HALF_WAVE = 8
    FULL_WAVE = 9
    POSITIVE_LADDER = 10
    NEGATIVE_LADDER = 11
    POSITIVE_TRAPEZOID = 12
    NEGATIVE_TRAPEZOID = 13
    NOISE = 14
    EXPONENTIAL_RISE = 15
    EXPONENTIAL_FALL = 16
    LOGARITHMIC_RISE = 17
    LOGARITHMIC_FALL = 18
    SINKER_PULSE = 19
    MULTI_AUDIO = 20
    LORENZ = 21


## @brief Frequency display unit codes. API frequencies are always in Hz.
class FrequencyUnit(IntEnum):
    HZ = 0
    KHZ = 1
    MHZ = 2
    MILLIHZ = 3
    MHZ_SMALL = 3  # compatibility alias for millihertz
    UHZ = 4


## @brief Modulation type codes for the two channels.
class Modulation(IntEnum):
    AM = 0
    FM = 1
    PM = 2
    ASK = 3
    FSK = 4
    PSK = 5
    PULSE = 6
    BURST = 7


## @brief Trigger sources: key, internal, external AC, or external DC.
class TriggerSource(IntEnum):
    KEY = 0
    INTERNAL = 1
    EXTERNAL_AC = 2
    EXTERNAL_DC = 3
