## @file
# @brief Channel settings and frequency/output properties.
from __future__ import annotations

from .enums import FrequencyUnit
from .errors import ProtocolError
from .registers import CHANNEL_REGISTERS, Register, _reg, _encode, _decode

def _parameter(name):
    return property(lambda self: self.get(name), lambda self, value: self.set(name, value),
                    doc=f'{name}: physical value; see CHANNEL_REGISTERS.')


## @brief Parameters of one channel; use PSG9080.ch1, ch2, or channel().
class Channel:
    ## @brief Create a channel object; normally constructed by PSG9080.
    # @param device Parent PSG9080 instance.
    # @param number Channel number 1 or 2; this constructor does not validate it.
    def __init__(self, device, number):
        self.device, self.number = device, number

    def _register(self, name):
        reg = CHANNEL_REGISTERS[name]
        return Register(reg.code + self.number - 1, reg.scale, reg.offset,
                        reg.minimum, reg.maximum)

    ## @brief Read a CHANNEL_REGISTERS parameter.
    # @param name Channel parameter name; frequency/enabled are separate properties.
    # @return Decimal in physical units.
    # @exception PSGTimeoutError Incomplete response or expired timeout.
    # @exception ProtocolError Unexpected device response.
    # @exception ValueError Invalid input value.
    # @exception KeyError Unknown parameter name.
    def get(self, name):
        reg = self._register(name)
        return _decode(reg, self.device.read_raw(reg.code))

    ## @brief Write a channel parameter after validating its value.
    # @param name CHANNEL_REGISTERS parameter name.
    # @param value Number, Decimal, IntEnum, or numeric string in physical units.
    # @exception PSGTimeoutError Incomplete response or expired timeout.
    # @exception ProtocolError Unexpected device response.
    # @exception ValueError Invalid input value.
    # @exception KeyError Unknown parameter name.
    def set(self, name, value):
        reg = self._register(name)
        raw = _encode(reg, value)
        if name == 'waveform' and not (0 <= int(raw) <= 21 or 101 <= int(raw) <= 199):
            raise ValueError('Waveform must be 0..21 or 101..199')
        self.device.write_raw(reg.code, raw)

    ## @brief Select an arbitrary waveform by slot number.
    # @param slot Integer in 1..99; sends waveform code 100 + slot.
    # @exception PSGTimeoutError Incomplete response or expired timeout.
    # @exception ProtocolError Unexpected device response.
    # @exception ValueError Invalid input value.
    def set_arbitrary_waveform(self, slot):
        raw = _encode(_reg(0, minimum=1, maximum=99), slot)
        self.set('waveform', 100 + int(raw))

    ## @brief Set frequency in Hz using the chosen display units.
    # @param hz Nonnegative frequency in Hz; MAXF depends on the device.
    # @param display_unit FrequencyUnit; mHz/uHz scaling follows the document and is not hardware-verified.
    # @exception PSGTimeoutError Incomplete response or expired timeout.
    # @exception ProtocolError Unexpected device response.
    # @exception ValueError Invalid input value.
    def set_frequency(self, hz, *, display_unit=FrequencyUnit.HZ):
        unit = FrequencyUnit(display_unit)
        # 0..2 select display units; documented examples retain millihertz
        # ticks. For mHz/uHz, the document shows ticks per selected unit.
        scale = {0: 1000, 1: 1000, 2: 1000, 3: 1000000, 4: 1000000000}[unit]
        self.device.write_raw(12 + self.number,
                              _encode(_reg(0, scale=scale), hz), int(unit))

    ## @brief Read/write frequency in Hz; property assignment selects FrequencyUnit.HZ.
    # @return Decimal when reading.
    # @exception PSGTimeoutError Incomplete response or expired timeout.
    # @exception ProtocolError Unexpected device response.
    # @exception ValueError Invalid input value.
    @property
    def frequency(self):
        fields = self.device.read_raw(12 + self.number)
        if len(fields) != 2:
            raise ProtocolError('Frequency response requires value and unit')
        try:
            unit = FrequencyUnit(int(fields[1]))
        except ValueError as exc:
            raise ProtocolError('Unknown frequency unit') from exc
        scale = {0: 1000, 1: 1000, 2: 1000, 3: 1000000, 4: 1000000000}[unit]
        return _decode(_reg(0, scale=scale), fields[:1])

    ## @brief Read/write frequency in Hz; property assignment selects FrequencyUnit.HZ.
    # @param hz When writing: nonnegative frequency in Hz.
    # @return Decimal when reading.
    # @exception PSGTimeoutError Incomplete response or expired timeout.
    # @exception ProtocolError Unexpected device response.
    # @exception ValueError Invalid input value.
    @frequency.setter
    def frequency(self, hz):
        self.set_frequency(hz)

    ## @brief Read/write output state; writing preserves the other channel state.
    # @return bool when reading.
    # @exception PSGTimeoutError Incomplete response or expired timeout.
    # @exception ProtocolError Unexpected device response.
    # @exception ValueError Invalid input value.
    @property
    def enabled(self):
        return bool(self.device.get('outputs')[self.number - 1])

    ## @brief Read/write output state; writing preserves the other channel state.
    # @param value When writing: bool or 0/1.
    # @return bool when reading.
    # @exception PSGTimeoutError Incomplete response or expired timeout.
    # @exception ProtocolError Unexpected device response.
    # @exception ValueError Invalid input value.
    @enabled.setter
    def enabled(self, value):
        encoded = _encode(_reg(10, maximum=1), value)
        with self.device._lock:
            states = list(self.device.get('outputs'))
            states[self.number - 1] = encoded
            self.device.set('outputs', *states)


    ## @brief Waveform code: 0..21 or 101..199; arbitrary waveform 01 has code 101.
    # @return Decimal when reading.
    # @exception ValueError Invalid value when writing.
    waveform = _parameter("waveform")

    ## @brief Amplitude in Vpp, 0.001 V step; maximum depends on the device.
    # @return Decimal when reading.
    # @exception ValueError Invalid value when writing.
    amplitude = _parameter("amplitude")

    ## @brief Offset in V, 0.01 V step; minimum -10 V.
    # @return Decimal when reading.
    # @exception ValueError Invalid value when writing.
    offset = _parameter("offset")

    ## @brief Duty cycle in percent, 0..100, 0.01% step.
    # @return Decimal when reading.
    # @exception ValueError Invalid value when writing.
    duty = _parameter("duty")

    ## @brief Phase in degrees, 0..359.99, 0.01 degree step.
    # @return Decimal when reading.
    # @exception ValueError Invalid value when writing.
    phase = _parameter("phase")

    ## @brief Internal modulation frequency in Hz, 0..1000000, 0.001 Hz step.
    # @return Decimal when reading.
    # @exception ValueError Invalid value when writing.
    modulation_frequency = _parameter("modulation_frequency")

    ## @brief AM depth in percent, 0..200, 0.1% step.
    # @return Decimal when reading.
    # @exception ValueError Invalid value when writing.
    am_depth = _parameter("am_depth")

    ## @brief FM deviation in Hz, 0.1 Hz step.
    # @return Decimal when reading.
    # @exception ValueError Invalid value when writing.
    fm_deviation = _parameter("fm_deviation")

    ## @brief FSK frequency in Hz, 0.1 Hz step.
    # @return Decimal when reading.
    # @exception ValueError Invalid value when writing.
    fsk_frequency = _parameter("fsk_frequency")

    ## @brief PM deviation in degrees, 0..359.9, 0.1 degree step.
    # @return Decimal when reading.
    # @exception ValueError Invalid value when writing.
    pm_deviation = _parameter("pm_deviation")

    ## @brief Pulse width in seconds, 0..0.4, 1 ns step.
    # @return Decimal when reading.
    # @exception ValueError Invalid value when writing.
    pulse_width = _parameter("pulse_width")

    ## @brief Pulse period in seconds, 0..4, 10 ns step.
    # @return Decimal when reading.
    # @exception ValueError Invalid value when writing.
    pulse_period = _parameter("pulse_period")
