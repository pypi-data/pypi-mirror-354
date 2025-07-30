# This file is auto-generated. Do not edit manually.
from dataclasses import dataclass
from enum import Enum, IntFlag

from pyharp.communication import Device
from pyharp.protocol import MessageType, PayloadType
from pyharp.protocol.messages import HarpMessage




@dataclass
class FlowmeterPayload:
    # 
    channel0: int
    # 
    channel1: int
    # 
    channel2: int
    # 
    channel3: int
    # 
    channel4: int


@dataclass
class ChannelsTargetFlowPayload:
    # 
    channel0: float
    # 
    channel1: float
    # 
    channel2: float
    # 
    channel3: float
    # 
    channel4: float


class DigitalOutputs(IntFlag):
    """
    Specifies the states of the digital outputs.
    """
    NONE = 0x0
    do0 = 0x1
    do1 = 0x2


class Valves(IntFlag):
    """
    Specifies the states of the valves.
    """
    NONE = 0x0
    valve0 = 0x1
    valve1 = 0x2
    valve2 = 0x4
    valve3 = 0x8
    end_valve0 = 0x10
    end_valve1 = 0x20
    valve_dummy = 0x40


class OdorValves(IntFlag):
    """
    Specifies the states of the odor valves.
    """
    NONE = 0x0
    valve0 = 0x1
    valve1 = 0x2
    valve2 = 0x4
    valve3 = 0x8


class EndValves(IntFlag):
    """
    Specifies the states of the end valves.
    """
    NONE = 0x0
    end_valve0 = 0x10
    end_valve1 = 0x20
    valve_dummy = 0x40


class OlfactometerEvents(IntFlag):
    """
    The events that can be enabled/disabled.
    """
    NONE = 0x0
    flowmeter = 0x1
    di0_trigger = 0x2
    channel_actual_flow = 0x4


class DigitalState(Enum):
    """
    The state of a digital pin.
    """
    low = 0
    high = 1


class DO0SyncConfig(Enum):
    """
    Available configurations when using DO0 pin to report firmware events.
    """
    none = 0
    mimic_enable_flow = 1


class DO1SyncConfig(Enum):
    """
    Available configurations when using DO1 pin to report firmware events.
    """
    none = 0
    mimic_enable_flow = 1


class DI0TriggerConfig(Enum):
    """
    Specifies the configuration of the digital input 0 (DIN0).
    """
    sync = 0
    enable_flow_while_high = 1
    valve_toggle = 2


class MimicOutputs(Enum):
    """
    Specifies the target IO on which to mimic the specified register.
    """
    none = 0
    do0 = 1
    do1 = 2


class Channel3RangeConfig(Enum):
    """
    Available flow ranges for channel 3 (ml/min).
    """
    flow_rate100 = 0
    flow_rate1000 = 1


class Olfactometer(Device):
    """
    Olfactometer class for controlling the device.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read_enable_flow(self):
        """
        Reads the contents of the EnableFlow register.

        Returns
        -------
        byte
            Value read from the EnableFlow register.
        """
        address = 32
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading EnableFlow register: {reply.error_message}")

        return reply.payload

    def write_enable_flow(self, value):
        """
        Writes a value to the EnableFlow register.

        Parameters
        ----------
        value : byte
            Value to write to the EnableFlow register.
        """
        address = 32
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing EnableFlow register: {reply.error_message}")

    def read_flowmeter(self):
        """
        Reads the contents of the Flowmeter register.

        Returns
        -------
        short[]
            Value read from the Flowmeter register.
        """
        address = 33
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading Flowmeter register: {reply.error_message}")

        return reply.payload

    def read_di0_state(self):
        """
        Reads the contents of the DI0State register.

        Returns
        -------
        byte
            Value read from the DI0State register.
        """
        address = 34
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DI0State register: {reply.error_message}")

        return reply.payload

    def read_channel0_user_calibration(self):
        """
        Reads the contents of the Channel0UserCalibration register.

        Returns
        -------
        ushort[]
            Value read from the Channel0UserCalibration register.
        """
        address = 35
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading Channel0UserCalibration register: {reply.error_message}")

        return reply.payload

    def write_channel0_user_calibration(self, value):
        """
        Writes a value to the Channel0UserCalibration register.

        Parameters
        ----------
        value : ushort[]
            Value to write to the Channel0UserCalibration register.
        """
        address = 35
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel0UserCalibration register: {reply.error_message}")

    def read_channel1_user_calibration(self):
        """
        Reads the contents of the Channel1UserCalibration register.

        Returns
        -------
        ushort[]
            Value read from the Channel1UserCalibration register.
        """
        address = 36
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading Channel1UserCalibration register: {reply.error_message}")

        return reply.payload

    def write_channel1_user_calibration(self, value):
        """
        Writes a value to the Channel1UserCalibration register.

        Parameters
        ----------
        value : ushort[]
            Value to write to the Channel1UserCalibration register.
        """
        address = 36
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel1UserCalibration register: {reply.error_message}")

    def read_channel2_user_calibration(self):
        """
        Reads the contents of the Channel2UserCalibration register.

        Returns
        -------
        ushort[]
            Value read from the Channel2UserCalibration register.
        """
        address = 37
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading Channel2UserCalibration register: {reply.error_message}")

        return reply.payload

    def write_channel2_user_calibration(self, value):
        """
        Writes a value to the Channel2UserCalibration register.

        Parameters
        ----------
        value : ushort[]
            Value to write to the Channel2UserCalibration register.
        """
        address = 37
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel2UserCalibration register: {reply.error_message}")

    def read_channel3_user_calibration(self):
        """
        Reads the contents of the Channel3UserCalibration register.

        Returns
        -------
        ushort[]
            Value read from the Channel3UserCalibration register.
        """
        address = 38
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading Channel3UserCalibration register: {reply.error_message}")

        return reply.payload

    def write_channel3_user_calibration(self, value):
        """
        Writes a value to the Channel3UserCalibration register.

        Parameters
        ----------
        value : ushort[]
            Value to write to the Channel3UserCalibration register.
        """
        address = 38
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel3UserCalibration register: {reply.error_message}")

    def read_channel4_user_calibration(self):
        """
        Reads the contents of the Channel4UserCalibration register.

        Returns
        -------
        ushort[]
            Value read from the Channel4UserCalibration register.
        """
        address = 39
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading Channel4UserCalibration register: {reply.error_message}")

        return reply.payload

    def write_channel4_user_calibration(self, value):
        """
        Writes a value to the Channel4UserCalibration register.

        Parameters
        ----------
        value : ushort[]
            Value to write to the Channel4UserCalibration register.
        """
        address = 39
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel4UserCalibration register: {reply.error_message}")

    def read_channel3_user_calibration_aux(self):
        """
        Reads the contents of the Channel3UserCalibrationAux register.

        Returns
        -------
        ushort[]
            Value read from the Channel3UserCalibrationAux register.
        """
        address = 40
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading Channel3UserCalibrationAux register: {reply.error_message}")

        return reply.payload

    def write_channel3_user_calibration_aux(self, value):
        """
        Writes a value to the Channel3UserCalibrationAux register.

        Parameters
        ----------
        value : ushort[]
            Value to write to the Channel3UserCalibrationAux register.
        """
        address = 40
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel3UserCalibrationAux register: {reply.error_message}")

    def read_user_calibration_enable(self):
        """
        Reads the contents of the UserCalibrationEnable register.

        Returns
        -------
        byte
            Value read from the UserCalibrationEnable register.
        """
        address = 41
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading UserCalibrationEnable register: {reply.error_message}")

        return reply.payload

    def write_user_calibration_enable(self, value):
        """
        Writes a value to the UserCalibrationEnable register.

        Parameters
        ----------
        value : byte
            Value to write to the UserCalibrationEnable register.
        """
        address = 41
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing UserCalibrationEnable register: {reply.error_message}")

    def read_channel0_target_flow(self):
        """
        Reads the contents of the Channel0TargetFlow register.

        Returns
        -------
        float
            Value read from the Channel0TargetFlow register.
        """
        address = 42
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel0TargetFlow register: {reply.error_message}")

        return reply.payload

    def write_channel0_target_flow(self, value):
        """
        Writes a value to the Channel0TargetFlow register.

        Parameters
        ----------
        value : float
            Value to write to the Channel0TargetFlow register.
        """
        address = 42
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.Float, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel0TargetFlow register: {reply.error_message}")

    def read_channel1_target_flow(self):
        """
        Reads the contents of the Channel1TargetFlow register.

        Returns
        -------
        float
            Value read from the Channel1TargetFlow register.
        """
        address = 43
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel1TargetFlow register: {reply.error_message}")

        return reply.payload

    def write_channel1_target_flow(self, value):
        """
        Writes a value to the Channel1TargetFlow register.

        Parameters
        ----------
        value : float
            Value to write to the Channel1TargetFlow register.
        """
        address = 43
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.Float, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel1TargetFlow register: {reply.error_message}")

    def read_channel2_target_flow(self):
        """
        Reads the contents of the Channel2TargetFlow register.

        Returns
        -------
        float
            Value read from the Channel2TargetFlow register.
        """
        address = 44
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel2TargetFlow register: {reply.error_message}")

        return reply.payload

    def write_channel2_target_flow(self, value):
        """
        Writes a value to the Channel2TargetFlow register.

        Parameters
        ----------
        value : float
            Value to write to the Channel2TargetFlow register.
        """
        address = 44
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.Float, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel2TargetFlow register: {reply.error_message}")

    def read_channel3_target_flow(self):
        """
        Reads the contents of the Channel3TargetFlow register.

        Returns
        -------
        float
            Value read from the Channel3TargetFlow register.
        """
        address = 45
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel3TargetFlow register: {reply.error_message}")

        return reply.payload

    def write_channel3_target_flow(self, value):
        """
        Writes a value to the Channel3TargetFlow register.

        Parameters
        ----------
        value : float
            Value to write to the Channel3TargetFlow register.
        """
        address = 45
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.Float, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel3TargetFlow register: {reply.error_message}")

    def read_channel4_target_flow(self):
        """
        Reads the contents of the Channel4TargetFlow register.

        Returns
        -------
        float
            Value read from the Channel4TargetFlow register.
        """
        address = 46
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel4TargetFlow register: {reply.error_message}")

        return reply.payload

    def write_channel4_target_flow(self, value):
        """
        Writes a value to the Channel4TargetFlow register.

        Parameters
        ----------
        value : float
            Value to write to the Channel4TargetFlow register.
        """
        address = 46
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.Float, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel4TargetFlow register: {reply.error_message}")

    def read_channels_target_flow(self):
        """
        Reads the contents of the ChannelsTargetFlow register.

        Returns
        -------
        float[]
            Value read from the ChannelsTargetFlow register.
        """
        address = 47
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading ChannelsTargetFlow register: {reply.error_message}")

        return reply.payload

    def write_channels_target_flow(self, value):
        """
        Writes a value to the ChannelsTargetFlow register.

        Parameters
        ----------
        value : float[]
            Value to write to the ChannelsTargetFlow register.
        """
        address = 47
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.Float, value))
        if reply.is_error:
            raise Exception(f"Error writing ChannelsTargetFlow register: {reply.error_message}")

    def read_channel0_actual_flow(self):
        """
        Reads the contents of the Channel0ActualFlow register.

        Returns
        -------
        float
            Value read from the Channel0ActualFlow register.
        """
        address = 48
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel0ActualFlow register: {reply.error_message}")

        return reply.payload

    def read_channel1_actual_flow(self):
        """
        Reads the contents of the Channel1ActualFlow register.

        Returns
        -------
        float
            Value read from the Channel1ActualFlow register.
        """
        address = 49
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel1ActualFlow register: {reply.error_message}")

        return reply.payload

    def read_channel2_actual_flow(self):
        """
        Reads the contents of the Channel2ActualFlow register.

        Returns
        -------
        float
            Value read from the Channel2ActualFlow register.
        """
        address = 50
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel2ActualFlow register: {reply.error_message}")

        return reply.payload

    def read_channel3_actual_flow(self):
        """
        Reads the contents of the Channel3ActualFlow register.

        Returns
        -------
        float
            Value read from the Channel3ActualFlow register.
        """
        address = 51
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel3ActualFlow register: {reply.error_message}")

        return reply.payload

    def read_channel4_actual_flow(self):
        """
        Reads the contents of the Channel4ActualFlow register.

        Returns
        -------
        float
            Value read from the Channel4ActualFlow register.
        """
        address = 52
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel4ActualFlow register: {reply.error_message}")

        return reply.payload

    def read_channel0_duty_cycle(self):
        """
        Reads the contents of the Channel0DutyCycle register.

        Returns
        -------
        float
            Value read from the Channel0DutyCycle register.
        """
        address = 58
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel0DutyCycle register: {reply.error_message}")

        return reply.payload

    def write_channel0_duty_cycle(self, value):
        """
        Writes a value to the Channel0DutyCycle register.

        Parameters
        ----------
        value : float
            Value to write to the Channel0DutyCycle register.
        """
        address = 58
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.Float, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel0DutyCycle register: {reply.error_message}")

    def read_channel1_duty_cycle(self):
        """
        Reads the contents of the Channel1DutyCycle register.

        Returns
        -------
        float
            Value read from the Channel1DutyCycle register.
        """
        address = 59
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel1DutyCycle register: {reply.error_message}")

        return reply.payload

    def write_channel1_duty_cycle(self, value):
        """
        Writes a value to the Channel1DutyCycle register.

        Parameters
        ----------
        value : float
            Value to write to the Channel1DutyCycle register.
        """
        address = 59
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.Float, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel1DutyCycle register: {reply.error_message}")

    def read_channel2_duty_cycle(self):
        """
        Reads the contents of the Channel2DutyCycle register.

        Returns
        -------
        float
            Value read from the Channel2DutyCycle register.
        """
        address = 60
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel2DutyCycle register: {reply.error_message}")

        return reply.payload

    def write_channel2_duty_cycle(self, value):
        """
        Writes a value to the Channel2DutyCycle register.

        Parameters
        ----------
        value : float
            Value to write to the Channel2DutyCycle register.
        """
        address = 60
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.Float, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel2DutyCycle register: {reply.error_message}")

    def read_channel3_duty_cycle(self):
        """
        Reads the contents of the Channel3DutyCycle register.

        Returns
        -------
        float
            Value read from the Channel3DutyCycle register.
        """
        address = 61
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel3DutyCycle register: {reply.error_message}")

        return reply.payload

    def write_channel3_duty_cycle(self, value):
        """
        Writes a value to the Channel3DutyCycle register.

        Parameters
        ----------
        value : float
            Value to write to the Channel3DutyCycle register.
        """
        address = 61
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.Float, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel3DutyCycle register: {reply.error_message}")

    def read_channel4_duty_cycle(self):
        """
        Reads the contents of the Channel4DutyCycle register.

        Returns
        -------
        float
            Value read from the Channel4DutyCycle register.
        """
        address = 62
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.Float))
        if reply.is_error:
            raise Exception(f"Error reading Channel4DutyCycle register: {reply.error_message}")

        return reply.payload

    def write_channel4_duty_cycle(self, value):
        """
        Writes a value to the Channel4DutyCycle register.

        Parameters
        ----------
        value : float
            Value to write to the Channel4DutyCycle register.
        """
        address = 62
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.Float, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel4DutyCycle register: {reply.error_message}")

    def read_digital_output_set(self):
        """
        Reads the contents of the DigitalOutputSet register.

        Returns
        -------
        byte
            Value read from the DigitalOutputSet register.
        """
        address = 63
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DigitalOutputSet register: {reply.error_message}")

        return reply.payload

    def write_digital_output_set(self, value):
        """
        Writes a value to the DigitalOutputSet register.

        Parameters
        ----------
        value : byte
            Value to write to the DigitalOutputSet register.
        """
        address = 63
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DigitalOutputSet register: {reply.error_message}")

    def read_digital_output_clear(self):
        """
        Reads the contents of the DigitalOutputClear register.

        Returns
        -------
        byte
            Value read from the DigitalOutputClear register.
        """
        address = 64
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DigitalOutputClear register: {reply.error_message}")

        return reply.payload

    def write_digital_output_clear(self, value):
        """
        Writes a value to the DigitalOutputClear register.

        Parameters
        ----------
        value : byte
            Value to write to the DigitalOutputClear register.
        """
        address = 64
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DigitalOutputClear register: {reply.error_message}")

    def read_digital_output_toggle(self):
        """
        Reads the contents of the DigitalOutputToggle register.

        Returns
        -------
        byte
            Value read from the DigitalOutputToggle register.
        """
        address = 65
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DigitalOutputToggle register: {reply.error_message}")

        return reply.payload

    def write_digital_output_toggle(self, value):
        """
        Writes a value to the DigitalOutputToggle register.

        Parameters
        ----------
        value : byte
            Value to write to the DigitalOutputToggle register.
        """
        address = 65
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DigitalOutputToggle register: {reply.error_message}")

    def read_digital_output_state(self):
        """
        Reads the contents of the DigitalOutputState register.

        Returns
        -------
        byte
            Value read from the DigitalOutputState register.
        """
        address = 66
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DigitalOutputState register: {reply.error_message}")

        return reply.payload

    def write_digital_output_state(self, value):
        """
        Writes a value to the DigitalOutputState register.

        Parameters
        ----------
        value : byte
            Value to write to the DigitalOutputState register.
        """
        address = 66
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DigitalOutputState register: {reply.error_message}")

    def read_enable_valve_pulse(self):
        """
        Reads the contents of the EnableValvePulse register.

        Returns
        -------
        byte
            Value read from the EnableValvePulse register.
        """
        address = 67
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading EnableValvePulse register: {reply.error_message}")

        return reply.payload

    def write_enable_valve_pulse(self, value):
        """
        Writes a value to the EnableValvePulse register.

        Parameters
        ----------
        value : byte
            Value to write to the EnableValvePulse register.
        """
        address = 67
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing EnableValvePulse register: {reply.error_message}")

    def read_valve_set(self):
        """
        Reads the contents of the ValveSet register.

        Returns
        -------
        byte
            Value read from the ValveSet register.
        """
        address = 68
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading ValveSet register: {reply.error_message}")

        return reply.payload

    def write_valve_set(self, value):
        """
        Writes a value to the ValveSet register.

        Parameters
        ----------
        value : byte
            Value to write to the ValveSet register.
        """
        address = 68
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing ValveSet register: {reply.error_message}")

    def read_valve_clear(self):
        """
        Reads the contents of the ValveClear register.

        Returns
        -------
        byte
            Value read from the ValveClear register.
        """
        address = 69
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading ValveClear register: {reply.error_message}")

        return reply.payload

    def write_valve_clear(self, value):
        """
        Writes a value to the ValveClear register.

        Parameters
        ----------
        value : byte
            Value to write to the ValveClear register.
        """
        address = 69
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing ValveClear register: {reply.error_message}")

    def read_valve_toggle(self):
        """
        Reads the contents of the ValveToggle register.

        Returns
        -------
        byte
            Value read from the ValveToggle register.
        """
        address = 70
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading ValveToggle register: {reply.error_message}")

        return reply.payload

    def write_valve_toggle(self, value):
        """
        Writes a value to the ValveToggle register.

        Parameters
        ----------
        value : byte
            Value to write to the ValveToggle register.
        """
        address = 70
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing ValveToggle register: {reply.error_message}")

    def read_o_dor_valve_state(self):
        """
        Reads the contents of the OdorValveState register.

        Returns
        -------
        byte
            Value read from the OdorValveState register.
        """
        address = 71
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading OdorValveState register: {reply.error_message}")

        return reply.payload

    def write_o_dor_valve_state(self, value):
        """
        Writes a value to the OdorValveState register.

        Parameters
        ----------
        value : byte
            Value to write to the OdorValveState register.
        """
        address = 71
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing OdorValveState register: {reply.error_message}")

    def read_end_valve_state(self):
        """
        Reads the contents of the EndValveState register.

        Returns
        -------
        byte
            Value read from the EndValveState register.
        """
        address = 72
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading EndValveState register: {reply.error_message}")

        return reply.payload

    def write_end_valve_state(self, value):
        """
        Writes a value to the EndValveState register.

        Parameters
        ----------
        value : byte
            Value to write to the EndValveState register.
        """
        address = 72
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing EndValveState register: {reply.error_message}")

    def read_valve0_pulse_duration(self):
        """
        Reads the contents of the Valve0PulseDuration register.

        Returns
        -------
        ushort
            Value read from the Valve0PulseDuration register.
        """
        address = 73
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading Valve0PulseDuration register: {reply.error_message}")

        return reply.payload

    def write_valve0_pulse_duration(self, value):
        """
        Writes a value to the Valve0PulseDuration register.

        Parameters
        ----------
        value : ushort
            Value to write to the Valve0PulseDuration register.
        """
        address = 73
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing Valve0PulseDuration register: {reply.error_message}")

    def read_valve1_pulse_duration(self):
        """
        Reads the contents of the Valve1PulseDuration register.

        Returns
        -------
        ushort
            Value read from the Valve1PulseDuration register.
        """
        address = 74
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading Valve1PulseDuration register: {reply.error_message}")

        return reply.payload

    def write_valve1_pulse_duration(self, value):
        """
        Writes a value to the Valve1PulseDuration register.

        Parameters
        ----------
        value : ushort
            Value to write to the Valve1PulseDuration register.
        """
        address = 74
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing Valve1PulseDuration register: {reply.error_message}")

    def read_valve2_pulse_duration(self):
        """
        Reads the contents of the Valve2PulseDuration register.

        Returns
        -------
        ushort
            Value read from the Valve2PulseDuration register.
        """
        address = 75
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading Valve2PulseDuration register: {reply.error_message}")

        return reply.payload

    def write_valve2_pulse_duration(self, value):
        """
        Writes a value to the Valve2PulseDuration register.

        Parameters
        ----------
        value : ushort
            Value to write to the Valve2PulseDuration register.
        """
        address = 75
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing Valve2PulseDuration register: {reply.error_message}")

    def read_valve3_pulse_duration(self):
        """
        Reads the contents of the Valve3PulseDuration register.

        Returns
        -------
        ushort
            Value read from the Valve3PulseDuration register.
        """
        address = 76
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading Valve3PulseDuration register: {reply.error_message}")

        return reply.payload

    def write_valve3_pulse_duration(self, value):
        """
        Writes a value to the Valve3PulseDuration register.

        Parameters
        ----------
        value : ushort
            Value to write to the Valve3PulseDuration register.
        """
        address = 76
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing Valve3PulseDuration register: {reply.error_message}")

    def read_end_valve0_pulse_duration(self):
        """
        Reads the contents of the EndValve0PulseDuration register.

        Returns
        -------
        ushort
            Value read from the EndValve0PulseDuration register.
        """
        address = 77
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading EndValve0PulseDuration register: {reply.error_message}")

        return reply.payload

    def write_end_valve0_pulse_duration(self, value):
        """
        Writes a value to the EndValve0PulseDuration register.

        Parameters
        ----------
        value : ushort
            Value to write to the EndValve0PulseDuration register.
        """
        address = 77
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing EndValve0PulseDuration register: {reply.error_message}")

    def read_end_valve1_pulse_duration(self):
        """
        Reads the contents of the EndValve1PulseDuration register.

        Returns
        -------
        ushort
            Value read from the EndValve1PulseDuration register.
        """
        address = 78
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading EndValve1PulseDuration register: {reply.error_message}")

        return reply.payload

    def write_end_valve1_pulse_duration(self, value):
        """
        Writes a value to the EndValve1PulseDuration register.

        Parameters
        ----------
        value : ushort
            Value to write to the EndValve1PulseDuration register.
        """
        address = 78
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing EndValve1PulseDuration register: {reply.error_message}")

    def read_do0_sync(self):
        """
        Reads the contents of the DO0Sync register.

        Returns
        -------
        byte
            Value read from the DO0Sync register.
        """
        address = 80
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DO0Sync register: {reply.error_message}")

        return reply.payload

    def write_do0_sync(self, value):
        """
        Writes a value to the DO0Sync register.

        Parameters
        ----------
        value : byte
            Value to write to the DO0Sync register.
        """
        address = 80
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DO0Sync register: {reply.error_message}")

    def read_do1_sync(self):
        """
        Reads the contents of the DO1Sync register.

        Returns
        -------
        byte
            Value read from the DO1Sync register.
        """
        address = 81
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DO1Sync register: {reply.error_message}")

        return reply.payload

    def write_do1_sync(self, value):
        """
        Writes a value to the DO1Sync register.

        Parameters
        ----------
        value : byte
            Value to write to the DO1Sync register.
        """
        address = 81
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DO1Sync register: {reply.error_message}")

    def read_di0_trigger(self):
        """
        Reads the contents of the DI0Trigger register.

        Returns
        -------
        byte
            Value read from the DI0Trigger register.
        """
        address = 82
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DI0Trigger register: {reply.error_message}")

        return reply.payload

    def write_di0_trigger(self, value):
        """
        Writes a value to the DI0Trigger register.

        Parameters
        ----------
        value : byte
            Value to write to the DI0Trigger register.
        """
        address = 82
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DI0Trigger register: {reply.error_message}")

    def read_mimic_valve0(self):
        """
        Reads the contents of the MimicValve0 register.

        Returns
        -------
        byte
            Value read from the MimicValve0 register.
        """
        address = 83
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading MimicValve0 register: {reply.error_message}")

        return reply.payload

    def write_mimic_valve0(self, value):
        """
        Writes a value to the MimicValve0 register.

        Parameters
        ----------
        value : byte
            Value to write to the MimicValve0 register.
        """
        address = 83
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing MimicValve0 register: {reply.error_message}")

    def read_mimic_valve1(self):
        """
        Reads the contents of the MimicValve1 register.

        Returns
        -------
        byte
            Value read from the MimicValve1 register.
        """
        address = 84
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading MimicValve1 register: {reply.error_message}")

        return reply.payload

    def write_mimic_valve1(self, value):
        """
        Writes a value to the MimicValve1 register.

        Parameters
        ----------
        value : byte
            Value to write to the MimicValve1 register.
        """
        address = 84
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing MimicValve1 register: {reply.error_message}")

    def read_mimic_valve2(self):
        """
        Reads the contents of the MimicValve2 register.

        Returns
        -------
        byte
            Value read from the MimicValve2 register.
        """
        address = 85
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading MimicValve2 register: {reply.error_message}")

        return reply.payload

    def write_mimic_valve2(self, value):
        """
        Writes a value to the MimicValve2 register.

        Parameters
        ----------
        value : byte
            Value to write to the MimicValve2 register.
        """
        address = 85
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing MimicValve2 register: {reply.error_message}")

    def read_mimic_valve3(self):
        """
        Reads the contents of the MimicValve3 register.

        Returns
        -------
        byte
            Value read from the MimicValve3 register.
        """
        address = 86
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading MimicValve3 register: {reply.error_message}")

        return reply.payload

    def write_mimic_valve3(self, value):
        """
        Writes a value to the MimicValve3 register.

        Parameters
        ----------
        value : byte
            Value to write to the MimicValve3 register.
        """
        address = 86
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing MimicValve3 register: {reply.error_message}")

    def read_mimic_end_valve0(self):
        """
        Reads the contents of the MimicEndValve0 register.

        Returns
        -------
        byte
            Value read from the MimicEndValve0 register.
        """
        address = 87
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading MimicEndValve0 register: {reply.error_message}")

        return reply.payload

    def write_mimic_end_valve0(self, value):
        """
        Writes a value to the MimicEndValve0 register.

        Parameters
        ----------
        value : byte
            Value to write to the MimicEndValve0 register.
        """
        address = 87
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing MimicEndValve0 register: {reply.error_message}")

    def read_mimic_end_valve1(self):
        """
        Reads the contents of the MimicEndValve1 register.

        Returns
        -------
        byte
            Value read from the MimicEndValve1 register.
        """
        address = 88
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading MimicEndValve1 register: {reply.error_message}")

        return reply.payload

    def write_mimic_end_valve1(self, value):
        """
        Writes a value to the MimicEndValve1 register.

        Parameters
        ----------
        value : byte
            Value to write to the MimicEndValve1 register.
        """
        address = 88
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing MimicEndValve1 register: {reply.error_message}")

    def read_enable_valve_external_control(self):
        """
        Reads the contents of the EnableValveExternalControl register.

        Returns
        -------
        byte
            Value read from the EnableValveExternalControl register.
        """
        address = 90
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading EnableValveExternalControl register: {reply.error_message}")

        return reply.payload

    def write_enable_valve_external_control(self, value):
        """
        Writes a value to the EnableValveExternalControl register.

        Parameters
        ----------
        value : byte
            Value to write to the EnableValveExternalControl register.
        """
        address = 90
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing EnableValveExternalControl register: {reply.error_message}")

    def read_channel3_range(self):
        """
        Reads the contents of the Channel3Range register.

        Returns
        -------
        byte
            Value read from the Channel3Range register.
        """
        address = 91
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading Channel3Range register: {reply.error_message}")

        return reply.payload

    def write_channel3_range(self, value):
        """
        Writes a value to the Channel3Range register.

        Parameters
        ----------
        value : byte
            Value to write to the Channel3Range register.
        """
        address = 91
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing Channel3Range register: {reply.error_message}")

    def read_temperature_value(self):
        """
        Reads the contents of the TemperatureValue register.

        Returns
        -------
        byte
            Value read from the TemperatureValue register.
        """
        address = 92
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading TemperatureValue register: {reply.error_message}")

        return reply.payload

    def read_enable_temperature_calibration(self):
        """
        Reads the contents of the EnableTemperatureCalibration register.

        Returns
        -------
        byte
            Value read from the EnableTemperatureCalibration register.
        """
        address = 93
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading EnableTemperatureCalibration register: {reply.error_message}")

        return reply.payload

    def write_enable_temperature_calibration(self, value):
        """
        Writes a value to the EnableTemperatureCalibration register.

        Parameters
        ----------
        value : byte
            Value to write to the EnableTemperatureCalibration register.
        """
        address = 93
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing EnableTemperatureCalibration register: {reply.error_message}")

    def read_temperature_calibration_value(self):
        """
        Reads the contents of the TemperatureCalibrationValue register.

        Returns
        -------
        byte
            Value read from the TemperatureCalibrationValue register.
        """
        address = 94
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading TemperatureCalibrationValue register: {reply.error_message}")

        return reply.payload

    def write_temperature_calibration_value(self, value):
        """
        Writes a value to the TemperatureCalibrationValue register.

        Parameters
        ----------
        value : byte
            Value to write to the TemperatureCalibrationValue register.
        """
        address = 94
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing TemperatureCalibrationValue register: {reply.error_message}")

    def read_enable_events(self):
        """
        Reads the contents of the EnableEvents register.

        Returns
        -------
        byte
            Value read from the EnableEvents register.
        """
        address = 95
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading EnableEvents register: {reply.error_message}")

        return reply.payload

    def write_enable_events(self, value):
        """
        Writes a value to the EnableEvents register.

        Parameters
        ----------
        value : byte
            Value to write to the EnableEvents register.
        """
        address = 95
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing EnableEvents register: {reply.error_message}")

