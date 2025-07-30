# This file is auto-generated. Do not edit manually.
from dataclasses import dataclass
from enum import Enum, IntFlag

from pyharp.communication import Device
from pyharp.protocol import MessageType, PayloadType
from pyharp.protocol.messages import HarpMessage




@dataclass
class AnalogDataPayload:
    # The voltage at the output of the ADC channel 0.
    analog_input0: int
    # The quadrature counter value on Port 2
    encoder: int
    # The voltage at the output of the ADC channel 1.
    analog_input1: int


@dataclass
class RgbAllPayload:
    # The intensity of the green channel in the RGB0 LED.
    green0: int
    # The intensity of the red channel in the RGB0 LED.
    red0: int
    # The intensity of the blue channel in the RGB0 LED.
    blue0: int
    # The intensity of the green channel in the RGB1 LED.
    green1: int
    # The intensity of the red channel in the RGB1 LED.
    red1: int
    # The intensity of the blue channel in the RGB1 LED.
    blue1: int


@dataclass
class RgbPayload:
    # The intensity of the green channel in the RGB LED.
    green: int
    # The intensity of the red channel in the RGB LED.
    red: int
    # The intensity of the blue channel in the RGB LED.
    blue: int


class DigitalInputs(IntFlag):
    """
    Specifies the state of port digital input lines.
    """
    NONE = 0x0
    di_port0 = 0x1
    di_port1 = 0x2
    di_port2 = 0x4
    di3 = 0x8


class DigitalOutputs(IntFlag):
    """
    Specifies the state of port digital output lines.
    """
    NONE = 0x0
    do_port0 = 0x1
    do_port1 = 0x2
    do_port2 = 0x4
    supply_port0 = 0x8
    supply_port1 = 0x10
    supply_port2 = 0x20
    led0 = 0x40
    led1 = 0x80
    rgb0 = 0x100
    rgb1 = 0x200
    do0 = 0x400
    do1 = 0x800
    do2 = 0x1000
    do3 = 0x2000


class PortDigitalIOS(IntFlag):
    """
    Specifies the state of the port DIO lines.
    """
    NONE = 0x0
    dio0 = 0x1
    dio1 = 0x2
    dio2 = 0x4


class PwmOutputs(IntFlag):
    """
    Specifies the state of PWM output lines.
    """
    NONE = 0x0
    pwm_do0 = 0x1
    pwm_do1 = 0x2
    pwm_do2 = 0x4
    pwm_do3 = 0x8


class Events(IntFlag):
    """
    Specifies the active events in the device.
    """
    NONE = 0x0
    port_di = 0x1
    port_dio = 0x2
    analog_data = 0x4
    camera0 = 0x8
    camera1 = 0x10


class CameraOutputs(IntFlag):
    """
    Specifies camera output enable bits.
    """
    NONE = 0x0
    camera_output0 = 0x1
    camera_output1 = 0x2


class ServoOutputs(IntFlag):
    """
    Specifies servo output enable bits.
    """
    NONE = 0x0
    servo_output2 = 0x4
    servo_output3 = 0x8


class EncoderInputs(IntFlag):
    """
    Specifies quadrature counter enable bits.
    """
    NONE = 0x0
    encoder_port2 = 0x4


class FrameAcquired(IntFlag):
    """
    Specifies that camera frame was acquired.
    """
    NONE = 0x0
    frame_acqu_ired = 0x1


class MimicOutput(Enum):
    """
    Specifies the target IO on which to mimic the specified register.
    """
    none = 0
    dio0 = 1
    dio1 = 2
    dio2 = 3
    do0 = 4
    do1 = 5
    do2 = 6
    do3 = 7


class EncoderModeConfig(Enum):
    """
    Specifies the type of reading made from the quadrature encoder.
    """
    position = 0
    displacement = 1


class Behavior(Device):
    """
    Behavior class for controlling the device.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read_digital_input_state(self):
        """
        Reads the contents of the DigitalInputState register.

        Returns
        -------
        byte
            Value read from the DigitalInputState register.
        """
        address = 32
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DigitalInputState register: {reply.error_message}")

        return reply.payload

    def read_output_set(self):
        """
        Reads the contents of the OutputSet register.

        Returns
        -------
        ushort
            Value read from the OutputSet register.
        """
        address = 34
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading OutputSet register: {reply.error_message}")

        return reply.payload

    def write_output_set(self, value):
        """
        Writes a value to the OutputSet register.

        Parameters
        ----------
        value : ushort
            Value to write to the OutputSet register.
        """
        address = 34
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing OutputSet register: {reply.error_message}")

    def read_output_clear(self):
        """
        Reads the contents of the OutputClear register.

        Returns
        -------
        ushort
            Value read from the OutputClear register.
        """
        address = 35
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading OutputClear register: {reply.error_message}")

        return reply.payload

    def write_output_clear(self, value):
        """
        Writes a value to the OutputClear register.

        Parameters
        ----------
        value : ushort
            Value to write to the OutputClear register.
        """
        address = 35
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing OutputClear register: {reply.error_message}")

    def read_output_toggle(self):
        """
        Reads the contents of the OutputToggle register.

        Returns
        -------
        ushort
            Value read from the OutputToggle register.
        """
        address = 36
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading OutputToggle register: {reply.error_message}")

        return reply.payload

    def write_output_toggle(self, value):
        """
        Writes a value to the OutputToggle register.

        Parameters
        ----------
        value : ushort
            Value to write to the OutputToggle register.
        """
        address = 36
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing OutputToggle register: {reply.error_message}")

    def read_output_state(self):
        """
        Reads the contents of the OutputState register.

        Returns
        -------
        ushort
            Value read from the OutputState register.
        """
        address = 37
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading OutputState register: {reply.error_message}")

        return reply.payload

    def write_output_state(self, value):
        """
        Writes a value to the OutputState register.

        Parameters
        ----------
        value : ushort
            Value to write to the OutputState register.
        """
        address = 37
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing OutputState register: {reply.error_message}")

    def read_port_dio_set(self):
        """
        Reads the contents of the PortDIOSet register.

        Returns
        -------
        byte
            Value read from the PortDIOSet register.
        """
        address = 38
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading PortDIOSet register: {reply.error_message}")

        return reply.payload

    def write_port_dio_set(self, value):
        """
        Writes a value to the PortDIOSet register.

        Parameters
        ----------
        value : byte
            Value to write to the PortDIOSet register.
        """
        address = 38
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing PortDIOSet register: {reply.error_message}")

    def read_port_dio_clear(self):
        """
        Reads the contents of the PortDIOClear register.

        Returns
        -------
        byte
            Value read from the PortDIOClear register.
        """
        address = 39
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading PortDIOClear register: {reply.error_message}")

        return reply.payload

    def write_port_dio_clear(self, value):
        """
        Writes a value to the PortDIOClear register.

        Parameters
        ----------
        value : byte
            Value to write to the PortDIOClear register.
        """
        address = 39
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing PortDIOClear register: {reply.error_message}")

    def read_port_dio_toggle(self):
        """
        Reads the contents of the PortDIOToggle register.

        Returns
        -------
        byte
            Value read from the PortDIOToggle register.
        """
        address = 40
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading PortDIOToggle register: {reply.error_message}")

        return reply.payload

    def write_port_dio_toggle(self, value):
        """
        Writes a value to the PortDIOToggle register.

        Parameters
        ----------
        value : byte
            Value to write to the PortDIOToggle register.
        """
        address = 40
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing PortDIOToggle register: {reply.error_message}")

    def read_port_dio_state(self):
        """
        Reads the contents of the PortDIOState register.

        Returns
        -------
        byte
            Value read from the PortDIOState register.
        """
        address = 41
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading PortDIOState register: {reply.error_message}")

        return reply.payload

    def write_port_dio_state(self, value):
        """
        Writes a value to the PortDIOState register.

        Parameters
        ----------
        value : byte
            Value to write to the PortDIOState register.
        """
        address = 41
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing PortDIOState register: {reply.error_message}")

    def read_port_dio_direction(self):
        """
        Reads the contents of the PortDIODirection register.

        Returns
        -------
        byte
            Value read from the PortDIODirection register.
        """
        address = 42
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading PortDIODirection register: {reply.error_message}")

        return reply.payload

    def write_port_dio_direction(self, value):
        """
        Writes a value to the PortDIODirection register.

        Parameters
        ----------
        value : byte
            Value to write to the PortDIODirection register.
        """
        address = 42
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing PortDIODirection register: {reply.error_message}")

    def read_port_dio_state_event(self):
        """
        Reads the contents of the PortDIOStateEvent register.

        Returns
        -------
        byte
            Value read from the PortDIOStateEvent register.
        """
        address = 43
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading PortDIOStateEvent register: {reply.error_message}")

        return reply.payload

    def read_analog_data(self):
        """
        Reads the contents of the AnalogData register.

        Returns
        -------
        short[]
            Value read from the AnalogData register.
        """
        address = 44
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading AnalogData register: {reply.error_message}")

        return reply.payload

    def read_output_pulse_enable(self):
        """
        Reads the contents of the OutputPulseEnable register.

        Returns
        -------
        ushort
            Value read from the OutputPulseEnable register.
        """
        address = 45
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading OutputPulseEnable register: {reply.error_message}")

        return reply.payload

    def write_output_pulse_enable(self, value):
        """
        Writes a value to the OutputPulseEnable register.

        Parameters
        ----------
        value : ushort
            Value to write to the OutputPulseEnable register.
        """
        address = 45
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing OutputPulseEnable register: {reply.error_message}")

    def read_pulse_do_port0(self):
        """
        Reads the contents of the PulseDOPort0 register.

        Returns
        -------
        ushort
            Value read from the PulseDOPort0 register.
        """
        address = 46
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseDOPort0 register: {reply.error_message}")

        return reply.payload

    def write_pulse_do_port0(self, value):
        """
        Writes a value to the PulseDOPort0 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseDOPort0 register.
        """
        address = 46
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseDOPort0 register: {reply.error_message}")

    def read_pulse_do_port1(self):
        """
        Reads the contents of the PulseDOPort1 register.

        Returns
        -------
        ushort
            Value read from the PulseDOPort1 register.
        """
        address = 47
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseDOPort1 register: {reply.error_message}")

        return reply.payload

    def write_pulse_do_port1(self, value):
        """
        Writes a value to the PulseDOPort1 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseDOPort1 register.
        """
        address = 47
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseDOPort1 register: {reply.error_message}")

    def read_pulse_do_port2(self):
        """
        Reads the contents of the PulseDOPort2 register.

        Returns
        -------
        ushort
            Value read from the PulseDOPort2 register.
        """
        address = 48
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseDOPort2 register: {reply.error_message}")

        return reply.payload

    def write_pulse_do_port2(self, value):
        """
        Writes a value to the PulseDOPort2 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseDOPort2 register.
        """
        address = 48
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseDOPort2 register: {reply.error_message}")

    def read_pulse_supply_port0(self):
        """
        Reads the contents of the PulseSupplyPort0 register.

        Returns
        -------
        ushort
            Value read from the PulseSupplyPort0 register.
        """
        address = 49
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseSupplyPort0 register: {reply.error_message}")

        return reply.payload

    def write_pulse_supply_port0(self, value):
        """
        Writes a value to the PulseSupplyPort0 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseSupplyPort0 register.
        """
        address = 49
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseSupplyPort0 register: {reply.error_message}")

    def read_pulse_supply_port1(self):
        """
        Reads the contents of the PulseSupplyPort1 register.

        Returns
        -------
        ushort
            Value read from the PulseSupplyPort1 register.
        """
        address = 50
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseSupplyPort1 register: {reply.error_message}")

        return reply.payload

    def write_pulse_supply_port1(self, value):
        """
        Writes a value to the PulseSupplyPort1 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseSupplyPort1 register.
        """
        address = 50
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseSupplyPort1 register: {reply.error_message}")

    def read_pulse_supply_port2(self):
        """
        Reads the contents of the PulseSupplyPort2 register.

        Returns
        -------
        ushort
            Value read from the PulseSupplyPort2 register.
        """
        address = 51
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseSupplyPort2 register: {reply.error_message}")

        return reply.payload

    def write_pulse_supply_port2(self, value):
        """
        Writes a value to the PulseSupplyPort2 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseSupplyPort2 register.
        """
        address = 51
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseSupplyPort2 register: {reply.error_message}")

    def read_pulse_led0(self):
        """
        Reads the contents of the PulseLed0 register.

        Returns
        -------
        ushort
            Value read from the PulseLed0 register.
        """
        address = 52
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseLed0 register: {reply.error_message}")

        return reply.payload

    def write_pulse_led0(self, value):
        """
        Writes a value to the PulseLed0 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseLed0 register.
        """
        address = 52
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseLed0 register: {reply.error_message}")

    def read_pulse_led1(self):
        """
        Reads the contents of the PulseLed1 register.

        Returns
        -------
        ushort
            Value read from the PulseLed1 register.
        """
        address = 53
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseLed1 register: {reply.error_message}")

        return reply.payload

    def write_pulse_led1(self, value):
        """
        Writes a value to the PulseLed1 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseLed1 register.
        """
        address = 53
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseLed1 register: {reply.error_message}")

    def read_pulse_rgb0(self):
        """
        Reads the contents of the PulseRgb0 register.

        Returns
        -------
        ushort
            Value read from the PulseRgb0 register.
        """
        address = 54
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseRgb0 register: {reply.error_message}")

        return reply.payload

    def write_pulse_rgb0(self, value):
        """
        Writes a value to the PulseRgb0 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseRgb0 register.
        """
        address = 54
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseRgb0 register: {reply.error_message}")

    def read_pulse_rgb1(self):
        """
        Reads the contents of the PulseRgb1 register.

        Returns
        -------
        ushort
            Value read from the PulseRgb1 register.
        """
        address = 55
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseRgb1 register: {reply.error_message}")

        return reply.payload

    def write_pulse_rgb1(self, value):
        """
        Writes a value to the PulseRgb1 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseRgb1 register.
        """
        address = 55
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseRgb1 register: {reply.error_message}")

    def read_pulse_do0(self):
        """
        Reads the contents of the PulseDO0 register.

        Returns
        -------
        ushort
            Value read from the PulseDO0 register.
        """
        address = 56
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseDO0 register: {reply.error_message}")

        return reply.payload

    def write_pulse_do0(self, value):
        """
        Writes a value to the PulseDO0 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseDO0 register.
        """
        address = 56
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseDO0 register: {reply.error_message}")

    def read_pulse_do1(self):
        """
        Reads the contents of the PulseDO1 register.

        Returns
        -------
        ushort
            Value read from the PulseDO1 register.
        """
        address = 57
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseDO1 register: {reply.error_message}")

        return reply.payload

    def write_pulse_do1(self, value):
        """
        Writes a value to the PulseDO1 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseDO1 register.
        """
        address = 57
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseDO1 register: {reply.error_message}")

    def read_pulse_do2(self):
        """
        Reads the contents of the PulseDO2 register.

        Returns
        -------
        ushort
            Value read from the PulseDO2 register.
        """
        address = 58
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseDO2 register: {reply.error_message}")

        return reply.payload

    def write_pulse_do2(self, value):
        """
        Writes a value to the PulseDO2 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseDO2 register.
        """
        address = 58
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseDO2 register: {reply.error_message}")

    def read_pulse_do3(self):
        """
        Reads the contents of the PulseDO3 register.

        Returns
        -------
        ushort
            Value read from the PulseDO3 register.
        """
        address = 59
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PulseDO3 register: {reply.error_message}")

        return reply.payload

    def write_pulse_do3(self, value):
        """
        Writes a value to the PulseDO3 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PulseDO3 register.
        """
        address = 59
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PulseDO3 register: {reply.error_message}")

    def read_pwm_frequency_do0(self):
        """
        Reads the contents of the PwmFrequencyDO0 register.

        Returns
        -------
        ushort
            Value read from the PwmFrequencyDO0 register.
        """
        address = 60
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PwmFrequencyDO0 register: {reply.error_message}")

        return reply.payload

    def write_pwm_frequency_do0(self, value):
        """
        Writes a value to the PwmFrequencyDO0 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PwmFrequencyDO0 register.
        """
        address = 60
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PwmFrequencyDO0 register: {reply.error_message}")

    def read_pwm_frequency_do1(self):
        """
        Reads the contents of the PwmFrequencyDO1 register.

        Returns
        -------
        ushort
            Value read from the PwmFrequencyDO1 register.
        """
        address = 61
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PwmFrequencyDO1 register: {reply.error_message}")

        return reply.payload

    def write_pwm_frequency_do1(self, value):
        """
        Writes a value to the PwmFrequencyDO1 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PwmFrequencyDO1 register.
        """
        address = 61
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PwmFrequencyDO1 register: {reply.error_message}")

    def read_pwm_frequency_do2(self):
        """
        Reads the contents of the PwmFrequencyDO2 register.

        Returns
        -------
        ushort
            Value read from the PwmFrequencyDO2 register.
        """
        address = 62
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PwmFrequencyDO2 register: {reply.error_message}")

        return reply.payload

    def write_pwm_frequency_do2(self, value):
        """
        Writes a value to the PwmFrequencyDO2 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PwmFrequencyDO2 register.
        """
        address = 62
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PwmFrequencyDO2 register: {reply.error_message}")

    def read_pwm_frequency_do3(self):
        """
        Reads the contents of the PwmFrequencyDO3 register.

        Returns
        -------
        ushort
            Value read from the PwmFrequencyDO3 register.
        """
        address = 63
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading PwmFrequencyDO3 register: {reply.error_message}")

        return reply.payload

    def write_pwm_frequency_do3(self, value):
        """
        Writes a value to the PwmFrequencyDO3 register.

        Parameters
        ----------
        value : ushort
            Value to write to the PwmFrequencyDO3 register.
        """
        address = 63
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing PwmFrequencyDO3 register: {reply.error_message}")

    def read_pwm_duty_cycle_do0(self):
        """
        Reads the contents of the PwmDutyCycleDO0 register.

        Returns
        -------
        byte
            Value read from the PwmDutyCycleDO0 register.
        """
        address = 64
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading PwmDutyCycleDO0 register: {reply.error_message}")

        return reply.payload

    def write_pwm_duty_cycle_do0(self, value):
        """
        Writes a value to the PwmDutyCycleDO0 register.

        Parameters
        ----------
        value : byte
            Value to write to the PwmDutyCycleDO0 register.
        """
        address = 64
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing PwmDutyCycleDO0 register: {reply.error_message}")

    def read_pwm_duty_cycle_do1(self):
        """
        Reads the contents of the PwmDutyCycleDO1 register.

        Returns
        -------
        byte
            Value read from the PwmDutyCycleDO1 register.
        """
        address = 65
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading PwmDutyCycleDO1 register: {reply.error_message}")

        return reply.payload

    def write_pwm_duty_cycle_do1(self, value):
        """
        Writes a value to the PwmDutyCycleDO1 register.

        Parameters
        ----------
        value : byte
            Value to write to the PwmDutyCycleDO1 register.
        """
        address = 65
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing PwmDutyCycleDO1 register: {reply.error_message}")

    def read_pwm_duty_cycle_do2(self):
        """
        Reads the contents of the PwmDutyCycleDO2 register.

        Returns
        -------
        byte
            Value read from the PwmDutyCycleDO2 register.
        """
        address = 66
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading PwmDutyCycleDO2 register: {reply.error_message}")

        return reply.payload

    def write_pwm_duty_cycle_do2(self, value):
        """
        Writes a value to the PwmDutyCycleDO2 register.

        Parameters
        ----------
        value : byte
            Value to write to the PwmDutyCycleDO2 register.
        """
        address = 66
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing PwmDutyCycleDO2 register: {reply.error_message}")

    def read_pwm_duty_cycle_do3(self):
        """
        Reads the contents of the PwmDutyCycleDO3 register.

        Returns
        -------
        byte
            Value read from the PwmDutyCycleDO3 register.
        """
        address = 67
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading PwmDutyCycleDO3 register: {reply.error_message}")

        return reply.payload

    def write_pwm_duty_cycle_do3(self, value):
        """
        Writes a value to the PwmDutyCycleDO3 register.

        Parameters
        ----------
        value : byte
            Value to write to the PwmDutyCycleDO3 register.
        """
        address = 67
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing PwmDutyCycleDO3 register: {reply.error_message}")

    def read_pwm_start(self):
        """
        Reads the contents of the PwmStart register.

        Returns
        -------
        byte
            Value read from the PwmStart register.
        """
        address = 68
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading PwmStart register: {reply.error_message}")

        return reply.payload

    def write_pwm_start(self, value):
        """
        Writes a value to the PwmStart register.

        Parameters
        ----------
        value : byte
            Value to write to the PwmStart register.
        """
        address = 68
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing PwmStart register: {reply.error_message}")

    def read_pwm_stop(self):
        """
        Reads the contents of the PwmStop register.

        Returns
        -------
        byte
            Value read from the PwmStop register.
        """
        address = 69
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading PwmStop register: {reply.error_message}")

        return reply.payload

    def write_pwm_stop(self, value):
        """
        Writes a value to the PwmStop register.

        Parameters
        ----------
        value : byte
            Value to write to the PwmStop register.
        """
        address = 69
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing PwmStop register: {reply.error_message}")

    def read_rgb_all(self):
        """
        Reads the contents of the RgbAll register.

        Returns
        -------
        byte[]
            Value read from the RgbAll register.
        """
        address = 70
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading RgbAll register: {reply.error_message}")

        return reply.payload

    def write_rgb_all(self, value):
        """
        Writes a value to the RgbAll register.

        Parameters
        ----------
        value : byte[]
            Value to write to the RgbAll register.
        """
        address = 70
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing RgbAll register: {reply.error_message}")

    def read_rgb0(self):
        """
        Reads the contents of the Rgb0 register.

        Returns
        -------
        byte[]
            Value read from the Rgb0 register.
        """
        address = 71
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading Rgb0 register: {reply.error_message}")

        return reply.payload

    def write_rgb0(self, value):
        """
        Writes a value to the Rgb0 register.

        Parameters
        ----------
        value : byte[]
            Value to write to the Rgb0 register.
        """
        address = 71
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing Rgb0 register: {reply.error_message}")

    def read_rgb1(self):
        """
        Reads the contents of the Rgb1 register.

        Returns
        -------
        byte[]
            Value read from the Rgb1 register.
        """
        address = 72
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading Rgb1 register: {reply.error_message}")

        return reply.payload

    def write_rgb1(self, value):
        """
        Writes a value to the Rgb1 register.

        Parameters
        ----------
        value : byte[]
            Value to write to the Rgb1 register.
        """
        address = 72
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing Rgb1 register: {reply.error_message}")

    def read_led0_current(self):
        """
        Reads the contents of the Led0Current register.

        Returns
        -------
        byte
            Value read from the Led0Current register.
        """
        address = 73
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading Led0Current register: {reply.error_message}")

        return reply.payload

    def write_led0_current(self, value):
        """
        Writes a value to the Led0Current register.

        Parameters
        ----------
        value : byte
            Value to write to the Led0Current register.
        """
        address = 73
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing Led0Current register: {reply.error_message}")

    def read_led1_current(self):
        """
        Reads the contents of the Led1Current register.

        Returns
        -------
        byte
            Value read from the Led1Current register.
        """
        address = 74
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading Led1Current register: {reply.error_message}")

        return reply.payload

    def write_led1_current(self, value):
        """
        Writes a value to the Led1Current register.

        Parameters
        ----------
        value : byte
            Value to write to the Led1Current register.
        """
        address = 74
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing Led1Current register: {reply.error_message}")

    def read_led0_max_current(self):
        """
        Reads the contents of the Led0MaxCurrent register.

        Returns
        -------
        byte
            Value read from the Led0MaxCurrent register.
        """
        address = 75
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading Led0MaxCurrent register: {reply.error_message}")

        return reply.payload

    def write_led0_max_current(self, value):
        """
        Writes a value to the Led0MaxCurrent register.

        Parameters
        ----------
        value : byte
            Value to write to the Led0MaxCurrent register.
        """
        address = 75
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing Led0MaxCurrent register: {reply.error_message}")

    def read_led1_max_current(self):
        """
        Reads the contents of the Led1MaxCurrent register.

        Returns
        -------
        byte
            Value read from the Led1MaxCurrent register.
        """
        address = 76
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading Led1MaxCurrent register: {reply.error_message}")

        return reply.payload

    def write_led1_max_current(self, value):
        """
        Writes a value to the Led1MaxCurrent register.

        Parameters
        ----------
        value : byte
            Value to write to the Led1MaxCurrent register.
        """
        address = 76
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing Led1MaxCurrent register: {reply.error_message}")

    def read_event_enable(self):
        """
        Reads the contents of the EventEnable register.

        Returns
        -------
        byte
            Value read from the EventEnable register.
        """
        address = 77
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading EventEnable register: {reply.error_message}")

        return reply.payload

    def write_event_enable(self, value):
        """
        Writes a value to the EventEnable register.

        Parameters
        ----------
        value : byte
            Value to write to the EventEnable register.
        """
        address = 77
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing EventEnable register: {reply.error_message}")

    def read_start_cameras(self):
        """
        Reads the contents of the StartCameras register.

        Returns
        -------
        byte
            Value read from the StartCameras register.
        """
        address = 78
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading StartCameras register: {reply.error_message}")

        return reply.payload

    def write_start_cameras(self, value):
        """
        Writes a value to the StartCameras register.

        Parameters
        ----------
        value : byte
            Value to write to the StartCameras register.
        """
        address = 78
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing StartCameras register: {reply.error_message}")

    def read_stop_cameras(self):
        """
        Reads the contents of the StopCameras register.

        Returns
        -------
        byte
            Value read from the StopCameras register.
        """
        address = 79
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading StopCameras register: {reply.error_message}")

        return reply.payload

    def write_stop_cameras(self, value):
        """
        Writes a value to the StopCameras register.

        Parameters
        ----------
        value : byte
            Value to write to the StopCameras register.
        """
        address = 79
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing StopCameras register: {reply.error_message}")

    def read_enable_servos(self):
        """
        Reads the contents of the EnableServos register.

        Returns
        -------
        byte
            Value read from the EnableServos register.
        """
        address = 80
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading EnableServos register: {reply.error_message}")

        return reply.payload

    def write_enable_servos(self, value):
        """
        Writes a value to the EnableServos register.

        Parameters
        ----------
        value : byte
            Value to write to the EnableServos register.
        """
        address = 80
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing EnableServos register: {reply.error_message}")

    def read_disable_servos(self):
        """
        Reads the contents of the DisableServos register.

        Returns
        -------
        byte
            Value read from the DisableServos register.
        """
        address = 81
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DisableServos register: {reply.error_message}")

        return reply.payload

    def write_disable_servos(self, value):
        """
        Writes a value to the DisableServos register.

        Parameters
        ----------
        value : byte
            Value to write to the DisableServos register.
        """
        address = 81
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DisableServos register: {reply.error_message}")

    def read_enable_encoders(self):
        """
        Reads the contents of the EnableEncoders register.

        Returns
        -------
        byte
            Value read from the EnableEncoders register.
        """
        address = 82
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading EnableEncoders register: {reply.error_message}")

        return reply.payload

    def write_enable_encoders(self, value):
        """
        Writes a value to the EnableEncoders register.

        Parameters
        ----------
        value : byte
            Value to write to the EnableEncoders register.
        """
        address = 82
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing EnableEncoders register: {reply.error_message}")

    def read_encoder_mode(self):
        """
        Reads the contents of the EncoderMode register.

        Returns
        -------
        byte
            Value read from the EncoderMode register.
        """
        address = 83
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading EncoderMode register: {reply.error_message}")

        return reply.payload

    def write_encoder_mode(self, value):
        """
        Writes a value to the EncoderMode register.

        Parameters
        ----------
        value : byte
            Value to write to the EncoderMode register.
        """
        address = 83
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing EncoderMode register: {reply.error_message}")

    def read_camera0_frame(self):
        """
        Reads the contents of the Camera0Frame register.

        Returns
        -------
        byte
            Value read from the Camera0Frame register.
        """
        address = 92
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading Camera0Frame register: {reply.error_message}")

        return reply.payload

    def read_camera0_frequency(self):
        """
        Reads the contents of the Camera0Frequency register.

        Returns
        -------
        ushort
            Value read from the Camera0Frequency register.
        """
        address = 93
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading Camera0Frequency register: {reply.error_message}")

        return reply.payload

    def write_camera0_frequency(self, value):
        """
        Writes a value to the Camera0Frequency register.

        Parameters
        ----------
        value : ushort
            Value to write to the Camera0Frequency register.
        """
        address = 93
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing Camera0Frequency register: {reply.error_message}")

    def read_camera1_frame(self):
        """
        Reads the contents of the Camera1Frame register.

        Returns
        -------
        byte
            Value read from the Camera1Frame register.
        """
        address = 94
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading Camera1Frame register: {reply.error_message}")

        return reply.payload

    def read_camera1_frequency(self):
        """
        Reads the contents of the Camera1Frequency register.

        Returns
        -------
        ushort
            Value read from the Camera1Frequency register.
        """
        address = 95
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading Camera1Frequency register: {reply.error_message}")

        return reply.payload

    def write_camera1_frequency(self, value):
        """
        Writes a value to the Camera1Frequency register.

        Parameters
        ----------
        value : ushort
            Value to write to the Camera1Frequency register.
        """
        address = 95
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing Camera1Frequency register: {reply.error_message}")

    def read_servo_motor2_period(self):
        """
        Reads the contents of the ServoMotor2Period register.

        Returns
        -------
        ushort
            Value read from the ServoMotor2Period register.
        """
        address = 100
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading ServoMotor2Period register: {reply.error_message}")

        return reply.payload

    def write_servo_motor2_period(self, value):
        """
        Writes a value to the ServoMotor2Period register.

        Parameters
        ----------
        value : ushort
            Value to write to the ServoMotor2Period register.
        """
        address = 100
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing ServoMotor2Period register: {reply.error_message}")

    def read_servo_motor2_pulse(self):
        """
        Reads the contents of the ServoMotor2Pulse register.

        Returns
        -------
        ushort
            Value read from the ServoMotor2Pulse register.
        """
        address = 101
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading ServoMotor2Pulse register: {reply.error_message}")

        return reply.payload

    def write_servo_motor2_pulse(self, value):
        """
        Writes a value to the ServoMotor2Pulse register.

        Parameters
        ----------
        value : ushort
            Value to write to the ServoMotor2Pulse register.
        """
        address = 101
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing ServoMotor2Pulse register: {reply.error_message}")

    def read_servo_motor3_period(self):
        """
        Reads the contents of the ServoMotor3Period register.

        Returns
        -------
        ushort
            Value read from the ServoMotor3Period register.
        """
        address = 102
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading ServoMotor3Period register: {reply.error_message}")

        return reply.payload

    def write_servo_motor3_period(self, value):
        """
        Writes a value to the ServoMotor3Period register.

        Parameters
        ----------
        value : ushort
            Value to write to the ServoMotor3Period register.
        """
        address = 102
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing ServoMotor3Period register: {reply.error_message}")

    def read_servo_motor3_pulse(self):
        """
        Reads the contents of the ServoMotor3Pulse register.

        Returns
        -------
        ushort
            Value read from the ServoMotor3Pulse register.
        """
        address = 103
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading ServoMotor3Pulse register: {reply.error_message}")

        return reply.payload

    def write_servo_motor3_pulse(self, value):
        """
        Writes a value to the ServoMotor3Pulse register.

        Parameters
        ----------
        value : ushort
            Value to write to the ServoMotor3Pulse register.
        """
        address = 103
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing ServoMotor3Pulse register: {reply.error_message}")

    def read_encoder_reset(self):
        """
        Reads the contents of the EncoderReset register.

        Returns
        -------
        byte
            Value read from the EncoderReset register.
        """
        address = 108
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading EncoderReset register: {reply.error_message}")

        return reply.payload

    def write_encoder_reset(self, value):
        """
        Writes a value to the EncoderReset register.

        Parameters
        ----------
        value : byte
            Value to write to the EncoderReset register.
        """
        address = 108
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing EncoderReset register: {reply.error_message}")

    def read_enable_serial_timestamp(self):
        """
        Reads the contents of the EnableSerialTimestamp register.

        Returns
        -------
        byte
            Value read from the EnableSerialTimestamp register.
        """
        address = 110
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading EnableSerialTimestamp register: {reply.error_message}")

        return reply.payload

    def write_enable_serial_timestamp(self, value):
        """
        Writes a value to the EnableSerialTimestamp register.

        Parameters
        ----------
        value : byte
            Value to write to the EnableSerialTimestamp register.
        """
        address = 110
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing EnableSerialTimestamp register: {reply.error_message}")

    def read_mimic_port0_ir(self):
        """
        Reads the contents of the MimicPort0IR register.

        Returns
        -------
        byte
            Value read from the MimicPort0IR register.
        """
        address = 111
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading MimicPort0IR register: {reply.error_message}")

        return reply.payload

    def write_mimic_port0_ir(self, value):
        """
        Writes a value to the MimicPort0IR register.

        Parameters
        ----------
        value : byte
            Value to write to the MimicPort0IR register.
        """
        address = 111
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing MimicPort0IR register: {reply.error_message}")

    def read_mimic_port1_ir(self):
        """
        Reads the contents of the MimicPort1IR register.

        Returns
        -------
        byte
            Value read from the MimicPort1IR register.
        """
        address = 112
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading MimicPort1IR register: {reply.error_message}")

        return reply.payload

    def write_mimic_port1_ir(self, value):
        """
        Writes a value to the MimicPort1IR register.

        Parameters
        ----------
        value : byte
            Value to write to the MimicPort1IR register.
        """
        address = 112
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing MimicPort1IR register: {reply.error_message}")

    def read_mimic_port2_ir(self):
        """
        Reads the contents of the MimicPort2IR register.

        Returns
        -------
        byte
            Value read from the MimicPort2IR register.
        """
        address = 113
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading MimicPort2IR register: {reply.error_message}")

        return reply.payload

    def write_mimic_port2_ir(self, value):
        """
        Writes a value to the MimicPort2IR register.

        Parameters
        ----------
        value : byte
            Value to write to the MimicPort2IR register.
        """
        address = 113
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing MimicPort2IR register: {reply.error_message}")

    def read_mimic_port0_valve(self):
        """
        Reads the contents of the MimicPort0Valve register.

        Returns
        -------
        byte
            Value read from the MimicPort0Valve register.
        """
        address = 117
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading MimicPort0Valve register: {reply.error_message}")

        return reply.payload

    def write_mimic_port0_valve(self, value):
        """
        Writes a value to the MimicPort0Valve register.

        Parameters
        ----------
        value : byte
            Value to write to the MimicPort0Valve register.
        """
        address = 117
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing MimicPort0Valve register: {reply.error_message}")

    def read_mimic_port1_valve(self):
        """
        Reads the contents of the MimicPort1Valve register.

        Returns
        -------
        byte
            Value read from the MimicPort1Valve register.
        """
        address = 118
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading MimicPort1Valve register: {reply.error_message}")

        return reply.payload

    def write_mimic_port1_valve(self, value):
        """
        Writes a value to the MimicPort1Valve register.

        Parameters
        ----------
        value : byte
            Value to write to the MimicPort1Valve register.
        """
        address = 118
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing MimicPort1Valve register: {reply.error_message}")

    def read_mimic_port2_valve(self):
        """
        Reads the contents of the MimicPort2Valve register.

        Returns
        -------
        byte
            Value read from the MimicPort2Valve register.
        """
        address = 119
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading MimicPort2Valve register: {reply.error_message}")

        return reply.payload

    def write_mimic_port2_valve(self, value):
        """
        Writes a value to the MimicPort2Valve register.

        Parameters
        ----------
        value : byte
            Value to write to the MimicPort2Valve register.
        """
        address = 119
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing MimicPort2Valve register: {reply.error_message}")

    def read_poke_input_filter(self):
        """
        Reads the contents of the PokeInputFilter register.

        Returns
        -------
        byte
            Value read from the PokeInputFilter register.
        """
        address = 122
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading PokeInputFilter register: {reply.error_message}")

        return reply.payload

    def write_poke_input_filter(self, value):
        """
        Writes a value to the PokeInputFilter register.

        Parameters
        ----------
        value : byte
            Value to write to the PokeInputFilter register.
        """
        address = 122
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing PokeInputFilter register: {reply.error_message}")

