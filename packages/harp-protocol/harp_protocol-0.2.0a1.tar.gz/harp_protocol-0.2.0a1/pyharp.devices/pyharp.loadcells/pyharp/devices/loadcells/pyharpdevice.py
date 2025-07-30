# This file is auto-generated. Do not edit manually.
from dataclasses import dataclass
from enum import Enum, IntFlag

from pyharp.communication import Device
from pyharp.protocol import MessageType, PayloadType
from pyharp.protocol.messages import HarpMessage




@dataclass
class LoadCellDataPayload:
    # 
    Channel0: int
    # 
    Channel1: int
    # 
    Channel2: int
    # 
    Channel3: int
    # 
    Channel4: int
    # 
    Channel5: int
    # 
    Channel6: int
    # 
    Channel7: int


class DigitalInputs(IntFlag):
    """
    Available digital input lines.
    """
    NONE = 0x0
    DI0 = 0x1


class SyncOutputs(IntFlag):
    """
    Specifies the state output synchronization lines.
    """
    NONE = 0x0
    DO0 = 0x1


class DigitalOutputs(IntFlag):
    """
    Specifies the state of port digital output lines.
    """
    NONE = 0x0
    DO1 = 0x1
    DO2 = 0x2
    DO3 = 0x4
    DO4 = 0x8
    DO5 = 0x10
    DO6 = 0x20
    DO7 = 0x40
    DO8 = 0x80


class LoadCellEvents(IntFlag):
    """
    The events that can be enabled/disabled.
    """
    NONE = 0x0
    LOAD_CELL_DATA = 0x1
    DIGITAL_INPUT = 0x2
    SYNC_OUTPUT = 0x4
    THRESHOLDS = 0x8


class TriggerConfig(Enum):
    """
    Available configurations when using a digital input as an acquisition trigger.
    """
    NONE = 0
    RISING_EDGE = 1
    FALLING_EDGE = 2


class SyncConfig(Enum):
    """
    Available configurations when using a digital output pin to report firmware events.
    """
    NONE = 0
    HEARTBEAT = 1
    PULSE = 2


class LoadCellChannel(Enum):
    """
    Available target load cells to be targeted on threshold events.
    """
    CHANNEL0 = 0
    CHANNEL1 = 1
    CHANNEL2 = 2
    CHANNEL3 = 3
    CHANNEL4 = 4
    CHANNEL5 = 5
    CHANNEL6 = 6
    CHANNEL7 = 7
    NONE = 8


class LoadCells(Device):
    """
    LoadCells class for controlling the device.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read_acquisition_state(self):
        """
        Reads the contents of the AcquisitionState register.

        Returns
        -------
        byte
            Value read from the AcquisitionState register.
        """
        address = 32
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading AcquisitionState register: {reply.error_message}")

        return reply.payload

    def write_acquisition_state(self, value):
        """
        Writes a value to the AcquisitionState register.

        Parameters
        ----------
        value : byte
            Value to write to the AcquisitionState register.
        """
        address = 32
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing AcquisitionState register: {reply.error_message}")

    def read_load_cell_data(self):
        """
        Reads the contents of the LoadCellData register.

        Returns
        -------
        short[]
            Value read from the LoadCellData register.
        """
        address = 33
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading LoadCellData register: {reply.error_message}")

        return reply.payload

    def read_digital_input_state(self):
        """
        Reads the contents of the DigitalInputState register.

        Returns
        -------
        byte
            Value read from the DigitalInputState register.
        """
        address = 34
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DigitalInputState register: {reply.error_message}")

        return reply.payload

    def read_sync_output_state(self):
        """
        Reads the contents of the SyncOutputState register.

        Returns
        -------
        byte
            Value read from the SyncOutputState register.
        """
        address = 35
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading SyncOutputState register: {reply.error_message}")

        return reply.payload

    def read_di0_trigger(self):
        """
        Reads the contents of the DI0Trigger register.

        Returns
        -------
        byte
            Value read from the DI0Trigger register.
        """
        address = 39
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
        address = 39
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DI0Trigger register: {reply.error_message}")

    def read_do0_sync(self):
        """
        Reads the contents of the DO0Sync register.

        Returns
        -------
        byte
            Value read from the DO0Sync register.
        """
        address = 40
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
        address = 40
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DO0Sync register: {reply.error_message}")

    def read_do0_pulse_width(self):
        """
        Reads the contents of the DO0PulseWidth register.

        Returns
        -------
        byte
            Value read from the DO0PulseWidth register.
        """
        address = 41
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DO0PulseWidth register: {reply.error_message}")

        return reply.payload

    def write_do0_pulse_width(self, value):
        """
        Writes a value to the DO0PulseWidth register.

        Parameters
        ----------
        value : byte
            Value to write to the DO0PulseWidth register.
        """
        address = 41
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DO0PulseWidth register: {reply.error_message}")

    def read_digital_output_set(self):
        """
        Reads the contents of the DigitalOutputSet register.

        Returns
        -------
        ushort
            Value read from the DigitalOutputSet register.
        """
        address = 42
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DigitalOutputSet register: {reply.error_message}")

        return reply.payload

    def write_digital_output_set(self, value):
        """
        Writes a value to the DigitalOutputSet register.

        Parameters
        ----------
        value : ushort
            Value to write to the DigitalOutputSet register.
        """
        address = 42
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DigitalOutputSet register: {reply.error_message}")

    def read_digital_output_clear(self):
        """
        Reads the contents of the DigitalOutputClear register.

        Returns
        -------
        ushort
            Value read from the DigitalOutputClear register.
        """
        address = 43
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DigitalOutputClear register: {reply.error_message}")

        return reply.payload

    def write_digital_output_clear(self, value):
        """
        Writes a value to the DigitalOutputClear register.

        Parameters
        ----------
        value : ushort
            Value to write to the DigitalOutputClear register.
        """
        address = 43
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DigitalOutputClear register: {reply.error_message}")

    def read_digital_output_toggle(self):
        """
        Reads the contents of the DigitalOutputToggle register.

        Returns
        -------
        ushort
            Value read from the DigitalOutputToggle register.
        """
        address = 44
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DigitalOutputToggle register: {reply.error_message}")

        return reply.payload

    def write_digital_output_toggle(self, value):
        """
        Writes a value to the DigitalOutputToggle register.

        Parameters
        ----------
        value : ushort
            Value to write to the DigitalOutputToggle register.
        """
        address = 44
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DigitalOutputToggle register: {reply.error_message}")

    def read_digital_output_state(self):
        """
        Reads the contents of the DigitalOutputState register.

        Returns
        -------
        ushort
            Value read from the DigitalOutputState register.
        """
        address = 45
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DigitalOutputState register: {reply.error_message}")

        return reply.payload

    def write_digital_output_state(self, value):
        """
        Writes a value to the DigitalOutputState register.

        Parameters
        ----------
        value : ushort
            Value to write to the DigitalOutputState register.
        """
        address = 45
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DigitalOutputState register: {reply.error_message}")

    def read_offset_load_cell0(self):
        """
        Reads the contents of the OffsetLoadCell0 register.

        Returns
        -------
        short
            Value read from the OffsetLoadCell0 register.
        """
        address = 48
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading OffsetLoadCell0 register: {reply.error_message}")

        return reply.payload

    def write_offset_load_cell0(self, value):
        """
        Writes a value to the OffsetLoadCell0 register.

        Parameters
        ----------
        value : short
            Value to write to the OffsetLoadCell0 register.
        """
        address = 48
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing OffsetLoadCell0 register: {reply.error_message}")

    def read_offset_load_cell1(self):
        """
        Reads the contents of the OffsetLoadCell1 register.

        Returns
        -------
        short
            Value read from the OffsetLoadCell1 register.
        """
        address = 49
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading OffsetLoadCell1 register: {reply.error_message}")

        return reply.payload

    def write_offset_load_cell1(self, value):
        """
        Writes a value to the OffsetLoadCell1 register.

        Parameters
        ----------
        value : short
            Value to write to the OffsetLoadCell1 register.
        """
        address = 49
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing OffsetLoadCell1 register: {reply.error_message}")

    def read_offset_load_cell2(self):
        """
        Reads the contents of the OffsetLoadCell2 register.

        Returns
        -------
        short
            Value read from the OffsetLoadCell2 register.
        """
        address = 50
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading OffsetLoadCell2 register: {reply.error_message}")

        return reply.payload

    def write_offset_load_cell2(self, value):
        """
        Writes a value to the OffsetLoadCell2 register.

        Parameters
        ----------
        value : short
            Value to write to the OffsetLoadCell2 register.
        """
        address = 50
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing OffsetLoadCell2 register: {reply.error_message}")

    def read_offset_load_cell3(self):
        """
        Reads the contents of the OffsetLoadCell3 register.

        Returns
        -------
        short
            Value read from the OffsetLoadCell3 register.
        """
        address = 51
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading OffsetLoadCell3 register: {reply.error_message}")

        return reply.payload

    def write_offset_load_cell3(self, value):
        """
        Writes a value to the OffsetLoadCell3 register.

        Parameters
        ----------
        value : short
            Value to write to the OffsetLoadCell3 register.
        """
        address = 51
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing OffsetLoadCell3 register: {reply.error_message}")

    def read_offset_load_cell4(self):
        """
        Reads the contents of the OffsetLoadCell4 register.

        Returns
        -------
        short
            Value read from the OffsetLoadCell4 register.
        """
        address = 52
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading OffsetLoadCell4 register: {reply.error_message}")

        return reply.payload

    def write_offset_load_cell4(self, value):
        """
        Writes a value to the OffsetLoadCell4 register.

        Parameters
        ----------
        value : short
            Value to write to the OffsetLoadCell4 register.
        """
        address = 52
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing OffsetLoadCell4 register: {reply.error_message}")

    def read_offset_load_cell5(self):
        """
        Reads the contents of the OffsetLoadCell5 register.

        Returns
        -------
        short
            Value read from the OffsetLoadCell5 register.
        """
        address = 53
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading OffsetLoadCell5 register: {reply.error_message}")

        return reply.payload

    def write_offset_load_cell5(self, value):
        """
        Writes a value to the OffsetLoadCell5 register.

        Parameters
        ----------
        value : short
            Value to write to the OffsetLoadCell5 register.
        """
        address = 53
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing OffsetLoadCell5 register: {reply.error_message}")

    def read_offset_load_cell6(self):
        """
        Reads the contents of the OffsetLoadCell6 register.

        Returns
        -------
        short
            Value read from the OffsetLoadCell6 register.
        """
        address = 54
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading OffsetLoadCell6 register: {reply.error_message}")

        return reply.payload

    def write_offset_load_cell6(self, value):
        """
        Writes a value to the OffsetLoadCell6 register.

        Parameters
        ----------
        value : short
            Value to write to the OffsetLoadCell6 register.
        """
        address = 54
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing OffsetLoadCell6 register: {reply.error_message}")

    def read_offset_load_cell7(self):
        """
        Reads the contents of the OffsetLoadCell7 register.

        Returns
        -------
        short
            Value read from the OffsetLoadCell7 register.
        """
        address = 55
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading OffsetLoadCell7 register: {reply.error_message}")

        return reply.payload

    def write_offset_load_cell7(self, value):
        """
        Writes a value to the OffsetLoadCell7 register.

        Parameters
        ----------
        value : short
            Value to write to the OffsetLoadCell7 register.
        """
        address = 55
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing OffsetLoadCell7 register: {reply.error_message}")

    def read_do1_target_load_cell(self):
        """
        Reads the contents of the DO1TargetLoadCell register.

        Returns
        -------
        byte
            Value read from the DO1TargetLoadCell register.
        """
        address = 58
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DO1TargetLoadCell register: {reply.error_message}")

        return reply.payload

    def write_do1_target_load_cell(self, value):
        """
        Writes a value to the DO1TargetLoadCell register.

        Parameters
        ----------
        value : byte
            Value to write to the DO1TargetLoadCell register.
        """
        address = 58
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DO1TargetLoadCell register: {reply.error_message}")

    def read_do2_target_load_cell(self):
        """
        Reads the contents of the DO2TargetLoadCell register.

        Returns
        -------
        byte
            Value read from the DO2TargetLoadCell register.
        """
        address = 59
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DO2TargetLoadCell register: {reply.error_message}")

        return reply.payload

    def write_do2_target_load_cell(self, value):
        """
        Writes a value to the DO2TargetLoadCell register.

        Parameters
        ----------
        value : byte
            Value to write to the DO2TargetLoadCell register.
        """
        address = 59
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DO2TargetLoadCell register: {reply.error_message}")

    def read_do3_target_load_cell(self):
        """
        Reads the contents of the DO3TargetLoadCell register.

        Returns
        -------
        byte
            Value read from the DO3TargetLoadCell register.
        """
        address = 60
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DO3TargetLoadCell register: {reply.error_message}")

        return reply.payload

    def write_do3_target_load_cell(self, value):
        """
        Writes a value to the DO3TargetLoadCell register.

        Parameters
        ----------
        value : byte
            Value to write to the DO3TargetLoadCell register.
        """
        address = 60
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DO3TargetLoadCell register: {reply.error_message}")

    def read_do4_target_load_cell(self):
        """
        Reads the contents of the DO4TargetLoadCell register.

        Returns
        -------
        byte
            Value read from the DO4TargetLoadCell register.
        """
        address = 61
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DO4TargetLoadCell register: {reply.error_message}")

        return reply.payload

    def write_do4_target_load_cell(self, value):
        """
        Writes a value to the DO4TargetLoadCell register.

        Parameters
        ----------
        value : byte
            Value to write to the DO4TargetLoadCell register.
        """
        address = 61
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DO4TargetLoadCell register: {reply.error_message}")

    def read_do5_target_load_cell(self):
        """
        Reads the contents of the DO5TargetLoadCell register.

        Returns
        -------
        byte
            Value read from the DO5TargetLoadCell register.
        """
        address = 62
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DO5TargetLoadCell register: {reply.error_message}")

        return reply.payload

    def write_do5_target_load_cell(self, value):
        """
        Writes a value to the DO5TargetLoadCell register.

        Parameters
        ----------
        value : byte
            Value to write to the DO5TargetLoadCell register.
        """
        address = 62
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DO5TargetLoadCell register: {reply.error_message}")

    def read_do6_target_load_cell(self):
        """
        Reads the contents of the DO6TargetLoadCell register.

        Returns
        -------
        byte
            Value read from the DO6TargetLoadCell register.
        """
        address = 63
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DO6TargetLoadCell register: {reply.error_message}")

        return reply.payload

    def write_do6_target_load_cell(self, value):
        """
        Writes a value to the DO6TargetLoadCell register.

        Parameters
        ----------
        value : byte
            Value to write to the DO6TargetLoadCell register.
        """
        address = 63
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DO6TargetLoadCell register: {reply.error_message}")

    def read_do7_target_load_cell(self):
        """
        Reads the contents of the DO7TargetLoadCell register.

        Returns
        -------
        byte
            Value read from the DO7TargetLoadCell register.
        """
        address = 64
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DO7TargetLoadCell register: {reply.error_message}")

        return reply.payload

    def write_do7_target_load_cell(self, value):
        """
        Writes a value to the DO7TargetLoadCell register.

        Parameters
        ----------
        value : byte
            Value to write to the DO7TargetLoadCell register.
        """
        address = 64
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DO7TargetLoadCell register: {reply.error_message}")

    def read_do8_target_load_cell(self):
        """
        Reads the contents of the DO8TargetLoadCell register.

        Returns
        -------
        byte
            Value read from the DO8TargetLoadCell register.
        """
        address = 65
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U8))
        if reply.is_error:
            raise Exception(f"Error reading DO8TargetLoadCell register: {reply.error_message}")

        return reply.payload

    def write_do8_target_load_cell(self, value):
        """
        Writes a value to the DO8TargetLoadCell register.

        Parameters
        ----------
        value : byte
            Value to write to the DO8TargetLoadCell register.
        """
        address = 65
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing DO8TargetLoadCell register: {reply.error_message}")

    def read_do1_threshold(self):
        """
        Reads the contents of the DO1Threshold register.

        Returns
        -------
        short
            Value read from the DO1Threshold register.
        """
        address = 66
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading DO1Threshold register: {reply.error_message}")

        return reply.payload

    def write_do1_threshold(self, value):
        """
        Writes a value to the DO1Threshold register.

        Parameters
        ----------
        value : short
            Value to write to the DO1Threshold register.
        """
        address = 66
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO1Threshold register: {reply.error_message}")

    def read_do2_threshold(self):
        """
        Reads the contents of the DO2Threshold register.

        Returns
        -------
        short
            Value read from the DO2Threshold register.
        """
        address = 67
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading DO2Threshold register: {reply.error_message}")

        return reply.payload

    def write_do2_threshold(self, value):
        """
        Writes a value to the DO2Threshold register.

        Parameters
        ----------
        value : short
            Value to write to the DO2Threshold register.
        """
        address = 67
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO2Threshold register: {reply.error_message}")

    def read_do3_threshold(self):
        """
        Reads the contents of the DO3Threshold register.

        Returns
        -------
        short
            Value read from the DO3Threshold register.
        """
        address = 68
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading DO3Threshold register: {reply.error_message}")

        return reply.payload

    def write_do3_threshold(self, value):
        """
        Writes a value to the DO3Threshold register.

        Parameters
        ----------
        value : short
            Value to write to the DO3Threshold register.
        """
        address = 68
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO3Threshold register: {reply.error_message}")

    def read_do4_threshold(self):
        """
        Reads the contents of the DO4Threshold register.

        Returns
        -------
        short
            Value read from the DO4Threshold register.
        """
        address = 69
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading DO4Threshold register: {reply.error_message}")

        return reply.payload

    def write_do4_threshold(self, value):
        """
        Writes a value to the DO4Threshold register.

        Parameters
        ----------
        value : short
            Value to write to the DO4Threshold register.
        """
        address = 69
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO4Threshold register: {reply.error_message}")

    def read_do5_threshold(self):
        """
        Reads the contents of the DO5Threshold register.

        Returns
        -------
        short
            Value read from the DO5Threshold register.
        """
        address = 70
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading DO5Threshold register: {reply.error_message}")

        return reply.payload

    def write_do5_threshold(self, value):
        """
        Writes a value to the DO5Threshold register.

        Parameters
        ----------
        value : short
            Value to write to the DO5Threshold register.
        """
        address = 70
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO5Threshold register: {reply.error_message}")

    def read_do6_threshold(self):
        """
        Reads the contents of the DO6Threshold register.

        Returns
        -------
        short
            Value read from the DO6Threshold register.
        """
        address = 71
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading DO6Threshold register: {reply.error_message}")

        return reply.payload

    def write_do6_threshold(self, value):
        """
        Writes a value to the DO6Threshold register.

        Parameters
        ----------
        value : short
            Value to write to the DO6Threshold register.
        """
        address = 71
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO6Threshold register: {reply.error_message}")

    def read_do7_threshold(self):
        """
        Reads the contents of the DO7Threshold register.

        Returns
        -------
        short
            Value read from the DO7Threshold register.
        """
        address = 72
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading DO7Threshold register: {reply.error_message}")

        return reply.payload

    def write_do7_threshold(self, value):
        """
        Writes a value to the DO7Threshold register.

        Parameters
        ----------
        value : short
            Value to write to the DO7Threshold register.
        """
        address = 72
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO7Threshold register: {reply.error_message}")

    def read_do8_threshold(self):
        """
        Reads the contents of the DO8Threshold register.

        Returns
        -------
        short
            Value read from the DO8Threshold register.
        """
        address = 73
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.S16))
        if reply.is_error:
            raise Exception(f"Error reading DO8Threshold register: {reply.error_message}")

        return reply.payload

    def write_do8_threshold(self, value):
        """
        Writes a value to the DO8Threshold register.

        Parameters
        ----------
        value : short
            Value to write to the DO8Threshold register.
        """
        address = 73
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.S16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO8Threshold register: {reply.error_message}")

    def read_do1_time_above_threshold(self):
        """
        Reads the contents of the DO1TimeAboveThreshold register.

        Returns
        -------
        ushort
            Value read from the DO1TimeAboveThreshold register.
        """
        address = 74
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO1TimeAboveThreshold register: {reply.error_message}")

        return reply.payload

    def write_do1_time_above_threshold(self, value):
        """
        Writes a value to the DO1TimeAboveThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO1TimeAboveThreshold register.
        """
        address = 74
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO1TimeAboveThreshold register: {reply.error_message}")

    def read_do2_time_above_threshold(self):
        """
        Reads the contents of the DO2TimeAboveThreshold register.

        Returns
        -------
        ushort
            Value read from the DO2TimeAboveThreshold register.
        """
        address = 75
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO2TimeAboveThreshold register: {reply.error_message}")

        return reply.payload

    def write_do2_time_above_threshold(self, value):
        """
        Writes a value to the DO2TimeAboveThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO2TimeAboveThreshold register.
        """
        address = 75
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO2TimeAboveThreshold register: {reply.error_message}")

    def read_do3_time_above_threshold(self):
        """
        Reads the contents of the DO3TimeAboveThreshold register.

        Returns
        -------
        ushort
            Value read from the DO3TimeAboveThreshold register.
        """
        address = 76
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO3TimeAboveThreshold register: {reply.error_message}")

        return reply.payload

    def write_do3_time_above_threshold(self, value):
        """
        Writes a value to the DO3TimeAboveThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO3TimeAboveThreshold register.
        """
        address = 76
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO3TimeAboveThreshold register: {reply.error_message}")

    def read_do4_time_above_threshold(self):
        """
        Reads the contents of the DO4TimeAboveThreshold register.

        Returns
        -------
        ushort
            Value read from the DO4TimeAboveThreshold register.
        """
        address = 77
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO4TimeAboveThreshold register: {reply.error_message}")

        return reply.payload

    def write_do4_time_above_threshold(self, value):
        """
        Writes a value to the DO4TimeAboveThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO4TimeAboveThreshold register.
        """
        address = 77
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO4TimeAboveThreshold register: {reply.error_message}")

    def read_do5_time_above_threshold(self):
        """
        Reads the contents of the DO5TimeAboveThreshold register.

        Returns
        -------
        ushort
            Value read from the DO5TimeAboveThreshold register.
        """
        address = 78
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO5TimeAboveThreshold register: {reply.error_message}")

        return reply.payload

    def write_do5_time_above_threshold(self, value):
        """
        Writes a value to the DO5TimeAboveThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO5TimeAboveThreshold register.
        """
        address = 78
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO5TimeAboveThreshold register: {reply.error_message}")

    def read_do6_time_above_threshold(self):
        """
        Reads the contents of the DO6TimeAboveThreshold register.

        Returns
        -------
        ushort
            Value read from the DO6TimeAboveThreshold register.
        """
        address = 79
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO6TimeAboveThreshold register: {reply.error_message}")

        return reply.payload

    def write_do6_time_above_threshold(self, value):
        """
        Writes a value to the DO6TimeAboveThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO6TimeAboveThreshold register.
        """
        address = 79
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO6TimeAboveThreshold register: {reply.error_message}")

    def read_do7_time_above_threshold(self):
        """
        Reads the contents of the DO7TimeAboveThreshold register.

        Returns
        -------
        ushort
            Value read from the DO7TimeAboveThreshold register.
        """
        address = 80
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO7TimeAboveThreshold register: {reply.error_message}")

        return reply.payload

    def write_do7_time_above_threshold(self, value):
        """
        Writes a value to the DO7TimeAboveThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO7TimeAboveThreshold register.
        """
        address = 80
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO7TimeAboveThreshold register: {reply.error_message}")

    def read_do8_time_above_threshold(self):
        """
        Reads the contents of the DO8TimeAboveThreshold register.

        Returns
        -------
        ushort
            Value read from the DO8TimeAboveThreshold register.
        """
        address = 81
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO8TimeAboveThreshold register: {reply.error_message}")

        return reply.payload

    def write_do8_time_above_threshold(self, value):
        """
        Writes a value to the DO8TimeAboveThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO8TimeAboveThreshold register.
        """
        address = 81
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO8TimeAboveThreshold register: {reply.error_message}")

    def read_do1_time_below_threshold(self):
        """
        Reads the contents of the DO1TimeBelowThreshold register.

        Returns
        -------
        ushort
            Value read from the DO1TimeBelowThreshold register.
        """
        address = 82
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO1TimeBelowThreshold register: {reply.error_message}")

        return reply.payload

    def write_do1_time_below_threshold(self, value):
        """
        Writes a value to the DO1TimeBelowThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO1TimeBelowThreshold register.
        """
        address = 82
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO1TimeBelowThreshold register: {reply.error_message}")

    def read_do2_time_below_threshold(self):
        """
        Reads the contents of the DO2TimeBelowThreshold register.

        Returns
        -------
        ushort
            Value read from the DO2TimeBelowThreshold register.
        """
        address = 83
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO2TimeBelowThreshold register: {reply.error_message}")

        return reply.payload

    def write_do2_time_below_threshold(self, value):
        """
        Writes a value to the DO2TimeBelowThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO2TimeBelowThreshold register.
        """
        address = 83
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO2TimeBelowThreshold register: {reply.error_message}")

    def read_do3_time_below_threshold(self):
        """
        Reads the contents of the DO3TimeBelowThreshold register.

        Returns
        -------
        ushort
            Value read from the DO3TimeBelowThreshold register.
        """
        address = 84
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO3TimeBelowThreshold register: {reply.error_message}")

        return reply.payload

    def write_do3_time_below_threshold(self, value):
        """
        Writes a value to the DO3TimeBelowThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO3TimeBelowThreshold register.
        """
        address = 84
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO3TimeBelowThreshold register: {reply.error_message}")

    def read_do4_time_below_threshold(self):
        """
        Reads the contents of the DO4TimeBelowThreshold register.

        Returns
        -------
        ushort
            Value read from the DO4TimeBelowThreshold register.
        """
        address = 85
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO4TimeBelowThreshold register: {reply.error_message}")

        return reply.payload

    def write_do4_time_below_threshold(self, value):
        """
        Writes a value to the DO4TimeBelowThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO4TimeBelowThreshold register.
        """
        address = 85
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO4TimeBelowThreshold register: {reply.error_message}")

    def read_do5_time_below_threshold(self):
        """
        Reads the contents of the DO5TimeBelowThreshold register.

        Returns
        -------
        ushort
            Value read from the DO5TimeBelowThreshold register.
        """
        address = 86
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO5TimeBelowThreshold register: {reply.error_message}")

        return reply.payload

    def write_do5_time_below_threshold(self, value):
        """
        Writes a value to the DO5TimeBelowThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO5TimeBelowThreshold register.
        """
        address = 86
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO5TimeBelowThreshold register: {reply.error_message}")

    def read_do6_time_below_threshold(self):
        """
        Reads the contents of the DO6TimeBelowThreshold register.

        Returns
        -------
        ushort
            Value read from the DO6TimeBelowThreshold register.
        """
        address = 87
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO6TimeBelowThreshold register: {reply.error_message}")

        return reply.payload

    def write_do6_time_below_threshold(self, value):
        """
        Writes a value to the DO6TimeBelowThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO6TimeBelowThreshold register.
        """
        address = 87
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO6TimeBelowThreshold register: {reply.error_message}")

    def read_do7_time_below_threshold(self):
        """
        Reads the contents of the DO7TimeBelowThreshold register.

        Returns
        -------
        ushort
            Value read from the DO7TimeBelowThreshold register.
        """
        address = 88
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO7TimeBelowThreshold register: {reply.error_message}")

        return reply.payload

    def write_do7_time_below_threshold(self, value):
        """
        Writes a value to the DO7TimeBelowThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO7TimeBelowThreshold register.
        """
        address = 88
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO7TimeBelowThreshold register: {reply.error_message}")

    def read_do8_time_below_threshold(self):
        """
        Reads the contents of the DO8TimeBelowThreshold register.

        Returns
        -------
        ushort
            Value read from the DO8TimeBelowThreshold register.
        """
        address = 89
        reply = self.send(HarpMessage.create(MessageType.READ, address, PayloadType.U16))
        if reply.is_error:
            raise Exception(f"Error reading DO8TimeBelowThreshold register: {reply.error_message}")

        return reply.payload

    def write_do8_time_below_threshold(self, value):
        """
        Writes a value to the DO8TimeBelowThreshold register.

        Parameters
        ----------
        value : ushort
            Value to write to the DO8TimeBelowThreshold register.
        """
        address = 89
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U16, value))
        if reply.is_error:
            raise Exception(f"Error writing DO8TimeBelowThreshold register: {reply.error_message}")

    def read_enable_events(self):
        """
        Reads the contents of the EnableEvents register.

        Returns
        -------
        byte
            Value read from the EnableEvents register.
        """
        address = 90
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
        address = 90
        reply = self.send(HarpMessage.create(MessageType.WRITE, address, PayloadType.U8, value))
        if reply.is_error:
            raise Exception(f"Error writing EnableEvents register: {reply.error_message}")

