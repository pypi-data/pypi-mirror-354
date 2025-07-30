"""
Module for the control of the CTS environmental chamber.
"""

import logging
import re
from typing import Optional, Tuple

import pyvisa
import pyvisa.constants

from ._constants import CTSChamberModel
from ._exceptions import (
    CTSChamberCommandError,
    CTSChamberCommunicationError,
)
from ._ramp_parameters import CTSChamberRampParameters
from ._state import CTSState, CTSStateError

__author__ = "Leandro Lanzieri"
__copyright__ = "Deutsches Elektronen-Synchrotron, DESY"
__license__ = "LGPL-3.0"

_LOGGER = logging.getLogger(__name__)


class CTSChamber:
    """
    Implements the control of a CTS environmental chamber.

    Args:
        serial_device (Optional[str]): The serial device to use for communication, in case RS-232
            or USB (via an adapter) is used. Cannot be used together with resource_path. Default is
            None.
        resource_path (Optional[str]): The resource path to use for communication. Cannot be used
            together with serial_device. Default is None.
        resource_manager (pyvisa.Optional[ResourceManager]): The resource manager to use for
            communication. If None, a new resource manager will be created. Default is None.
        ascii_protocol_address (Optional[int]): The ASCII protocol address to use for communication.
            Default is 0x81. Must be between 0x81 and 0xA0.
        communication_timeout (Optional[int]): The communication timeout in milliseconds. Default
            is 1000.
        chamber_model (Optional[CTSChamberModel]): The model of the CTS environmental chamber. If
            None, the default model (CTSChamberModel.C_40) will be used. Default is None.

    Raises:
        CTSChamberCommunicationError: If the connection to the device cannot be established.
    """

    DEFAULT_ASCII_PROTOCOL_ADDRESS = 0x81
    """Default ASCII protocol address for the device."""

    DEFAULT_COMMUNICATION_TIMEOUT = 1000
    """Default communication timeout in milliseconds."""

    _RS232_BAUDRATE = 19200
    """Baud rate for the RS232 communication."""

    _RS323_BITS = 8
    """Number of bits for the RS232 communication."""

    _RS232_STOP_BITS = pyvisa.constants.StopBits.one
    """Number of stop bits for the RS232 communication."""

    _RS232_PARITY = pyvisa.constants.Parity.odd
    """Parity for the RS232 communication."""

    _RS232_FLOW_CONTROL = pyvisa.constants.ControlFlow.none
    """Flow control for the RS232 communication."""

    DEFAULT_CHAMBER_MODEL = CTSChamberModel.C_40
    """Default model of the CTS environmental chamber."""

    _ANALOG_CHANNEL_TEMPERATURE = 0
    """Analog channel for temperature."""

    _ANALOG_CHANNEL_HUMIDITY = 1
    """Analog channel for humidity."""

    _RAMP_CHANNEL_TEMPERATURE = 1
    """Ramp channel for temperature."""

    _RAMP_CHANNEL_HUMIDITY = 2
    """Ramp channel for humidity."""

    def __init__(
        self,
        serial_device: Optional[str] = None,
        ascii_protocol_address: Optional[int] = None,
        resource_path: Optional[str] = None,
        resource_manager: Optional[pyvisa.ResourceManager] = None,
        communication_timeout: Optional[int] = None,
        chamber_model: Optional[CTSChamberModel] = None,
    ):

        self._communication_timeout = communication_timeout or self.DEFAULT_COMMUNICATION_TIMEOUT
        self._chamber_model = chamber_model or self.DEFAULT_CHAMBER_MODEL
        self._resource_manager = resource_manager or pyvisa.ResourceManager("@py")

        assert serial_device is not None or resource_path is not None, (
            "Either serial_device or resource_path must be provided, but not both."
        )
        assert not (serial_device is not None and resource_path is not None), (
            "Cannot use both serial_device and resource_path at the same time."
        )

        if resource_path is None:
            resource_path = f"ASRL{serial_device}::INSTR"

        self._resource_path = resource_path

        if ascii_protocol_address is None:
            ascii_protocol_address = self.DEFAULT_ASCII_PROTOCOL_ADDRESS

        self._ascii_protocol_address = ascii_protocol_address
        assert 0x81 <= self._ascii_protocol_address <= 0xA0, (
            "ASCII protocol address must be between 0x81 and 0xFF"
        )

        try:
            self._resource: pyvisa.resources.SerialInstrument = (
                self._resource_manager.open_resource(self._resource_path)
            )
        except pyvisa.VisaIOError as e:
            _LOGGER.exception(f"Failed to open resource {self._resource_path}: {e}")
            raise CTSChamberCommunicationError(
                f"Could not open resource {self._resource_path}. "
                "Please check the connection and the resource path."
            )

        self._resource.timeout = self._communication_timeout
        self._resource.baud_rate = self._RS232_BAUDRATE
        self._resource.data_bits = self._RS323_BITS
        self._resource.stop_bits = self._RS232_STOP_BITS
        self._resource.parity = self._RS232_PARITY
        self._resource.flow_control = self._RS232_FLOW_CONTROL
        self._resource.read_termination = chr(0x03)  # ETX (End of Text)

    def _prepare_frame(self, data: str) -> bytes:
        """
        Prepares a frame to be sent to the device.

        Args:
            data: The ASCII string data to be sent to the device.

        Returns:
            The prepared frame.
        """
        data_bytes = data.encode("ascii")  # Convert string to bytes
        # convert to bytearray
        data_bytes = bytearray(data_bytes)

        # set MSB of all data
        for i in range(len(data_bytes)):
            data_bytes[i] |= 0x80

        # add the ASCII protocol address in the first byte
        data_bytes.insert(0, self._ascii_protocol_address)

        # calculate the checksum
        checksum = 0
        for byte in data_bytes:
            checksum ^= byte

        # set MSB of the checksum
        checksum |= 0x80

        # build the final frame
        frame = bytearray([0x02]) + data_bytes + bytearray([checksum, 0x03])
        return frame

    def _send_cmd(self, data: str) -> str:
        """
        Sends bytes to the device and waits for a response.

        Args:
            data: The ASCII string data to be sent to the device.

        Returns:
            The response from the device as a string.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        frame = self._prepare_frame(data)

        _LOGGER.debug(f"Sending frame: {frame.hex()}")
        self._resource.write_raw(frame)

        try:
            response = self._resource.read_raw()
        except Exception as e:
            _LOGGER.exception(f"Error reading from device: {e}")
            raise CTSChamberCommandError(
                f"Failed to read response from device: {self._resource_path}. "
                "Please check the connection and the command."
            )

        response = bytearray(response)
        _LOGGER.debug(f"Received frame: {response.hex()}")

        assert response[0] == 0x02, "Response does not start with STX (0x02)"
        assert response[-1] == 0x03, "Response does not end with ETX (0x03)"

        # Exclude MSB from all bytes
        for i in range(len(response)):
            response[i] &= 0x7F

        # verify checksum
        checksum = 0
        for byte in response[1:-2]:  # Exclude STX and ETX
            checksum ^= byte

        if checksum != response[-2]:  # Checksum is the second last byte
            _LOGGER.error("Checksum mismatch in response")
            raise CTSChamberCommandError(
                f"Checksum mismatch in response: {response.hex()}"
            )


        return response[2:-2].decode("ascii")  # Exclude STX and ETX, and checksum

    def _get_analog_channel(self, channel: int) -> Tuple[float, float]:
        """
        Gets the current value and the set value of an analog channel from the CTS chamber.

        Args:
            channel: The channel number to retrieve the values from [0-6].

        Returns:
            A tuple containing the current value and the set value.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        assert 0 <= channel <= 6, "Channel must be between 0 and 6"
        message = f"A{channel}"
        response = self._send_cmd(message)

        pattern = f"^A{channel}"
        pattern += r" (?:\d{3}|-\d{2})\.\d (?:\d{3}|-\d{2})\.\d$"
        if re.match(pattern, response):
            actual_temperature, set_temperature = response[3:].split()
            return float(actual_temperature), float(set_temperature)
        else:
            _LOGGER.error(f"Response does not match expected format: {response}")
            raise CTSChamberCommandError(
                f"Invalid response format: {response}. Expected: 'A{channel} xxx.xxx xxx.xxx'"
            )

    def _set_analog_channel(self, channel: int, value: float) -> None:
        """
        Sets the value of an analog channel on the CTS chamber.

        Args:
            channel: The channel number to set the value for [0-6].
            value: The value to set for the channel.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        assert 0 <= channel <= 6, "Channel must be between 0 and 6"
        value_str = f"{value:05.1f}"
        message = f"a{channel} {value_str}"

        response = self._send_cmd(message)

        if response != "a":
            _LOGGER.error(f"Response does not match expected format: {response}")
            raise CTSChamberCommandError(
                f"Invalid response format: {response}. Expected format: 'a'"
            )

    def _set_digital_channel(self, channel: int, value: bool) -> None:
        """
        Sets the value of a digital channel on the CTS chamber.

        Args:
            channel: The channel number to set the value for [1-11].
            value: The value to set for the channel (True for ON, False for OFF).

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        if not (1 <= channel <= 11):
            raise CTSChamberCommandError("Channel must be between 1 and 11")

        if channel == 10:
            channel_str = ":"
        elif channel == 11:
            channel_str = ";"
        else:
            channel_str = str(channel)

        value_str = "1" if value else "0"
        message = f"s{channel_str} {value_str}"

        response = self._send_cmd(message)

        if not response.startswith("s") or int(response[-1]) != channel:
            _LOGGER.error(f"Response does not match expected format: {response}")
            raise CTSChamberCommandError(
                f"Invalid response format: {response}. Expected format: 's{channel}'"
            )

    def get_temperature(self) -> Tuple[float, float]:
        """
        Gets the current temperature and set temperature from the CTS chamber.

        Returns:
            A tuple containing the current temperature and the set temperature.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        return self._get_analog_channel(self._ANALOG_CHANNEL_TEMPERATURE)

    def get_humidity(self) -> Tuple[float, float]:
        """
        Gets the current humidity and set humidity from the CTS chamber.

        Returns:
            A tuple containing the current humidity and the set humidity.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        return self._get_analog_channel(self._ANALOG_CHANNEL_HUMIDITY)

    def set_temperature(self, value: float) -> None:
        """
        Sets the temperature on the CTS chamber.

        Args:
            value: The temperature value to set.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        if self._chamber_model == CTSChamberModel.C_40:
            minimum_temperature = -40.0
        elif self._chamber_model == CTSChamberModel.C_65:
            minimum_temperature = -65.0
        elif self._chamber_model == CTSChamberModel.C_70:
            minimum_temperature = -70.0
        else:
            minimum_temperature = -40.0

        if value < minimum_temperature:
            raise CTSChamberCommandError(
                f"Temperature must be greater than or equal to {minimum_temperature}"
            )

        if value > 180.0:
            raise CTSChamberCommandError("Temperature must be less than or equal to 180.0")

        self._set_analog_channel(self._ANALOG_CHANNEL_TEMPERATURE, value)

    def set_humidity(self, value: float) -> None:
        """
        Sets the humidity on the CTS chamber.

        Args:
            value: The humidity value to set.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        if value < 0.0 or value > 98.0:
            raise CTSChamberCommandError("Humidity must be between 0.0 and 98.0")

        self._set_analog_channel(self._ANALOG_CHANNEL_HUMIDITY, value)

    def _set_ramp(self, channel: int, up: bool, rate: Optional[float] = None) -> None:
        """
        Sets the ramp rate for a specific channel (temperature or humidity).

        Args:
            channel: The channel number to set the ramp rate for.
                Either _RAMP_CHANNEL_TEMPERATURE or _RAMP_CHANNEL_HUMIDITY.
            up: True if setting the ramp rate for increasing values, False for decreasing values.
            rate: The ramp rate in K/min. If None, the maximum ramp rate will be used.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        if channel not in (self._RAMP_CHANNEL_TEMPERATURE, self._RAMP_CHANNEL_HUMIDITY):
            raise CTSChamberCommandError("Invalid channel for ramp setting.")

        if rate is None:
            rate = 999.9

        message = "u" if up else "d"
        message += f"{channel} "
        message += f"{rate:05.1f}"

        response = self._send_cmd(message)
        pattern = r"u" if up else r"d"

        if not re.match(pattern, response):
            raise CTSChamberCommandError(f"Invalid response format: {response}.")

    def ramp_to_temperature(
        self,
        target: float,
        ramp_up_rate: Optional[float] = None,
        ramp_down_rate: Optional[float] = None
    ) -> None:
        """
        Ramps up or down to a target temperature on the CTS chamber using the specified ramp rates
        If a rate is None, the chamber will use the maximum ramp rate.

        Args:
            target: The target temperature to ramp to in degrees Celsius.
            ramp_up_rate: The rate (K/min) for ramping up (target > current).
            ramp_down_rate: The rate (K/min) for ramping down (target < current).

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        # first, set the ramp rates
        self._set_ramp(channel=self._RAMP_CHANNEL_TEMPERATURE, up=True, rate=ramp_up_rate)
        self._set_ramp(channel=self._RAMP_CHANNEL_TEMPERATURE, up=False, rate=ramp_down_rate)

        # then, set the target temperature
        self._set_analog_channel(self._ANALOG_CHANNEL_TEMPERATURE, target)

    def ramp_to_humidity(
        self,
        target: float,
        ramp_up_rate: Optional[float] = None,
        ramp_down_rate: Optional[float] = None
    ) -> None:
        # first, set the ramp rates
        self._set_ramp(channel=self._RAMP_CHANNEL_HUMIDITY, up=True, rate=ramp_up_rate)
        self._set_ramp(channel=self._RAMP_CHANNEL_HUMIDITY, up=False, rate=ramp_down_rate)

        # then, set the target humidity
        self._set_analog_channel(self._ANALOG_CHANNEL_HUMIDITY, target)

    def _get_ramp_information(self, channel: int) -> CTSChamberRampParameters:
        """
        Gets the ramp information for the specified channel.

        Args:
            channel: The channel number to retrieve the ramp information. Either
                _RAMP_CHANNEL_TEMPERATURE or _RAMP_CHANNEL_HUMIDITY.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        if channel not in (self._RAMP_CHANNEL_TEMPERATURE, self._RAMP_CHANNEL_HUMIDITY):
            raise CTSChamberCommandError("Invalid channel for ramp information.")

        message = f"R{channel}"
        response = self._send_cmd(message)
        pattern = (
            rf"^R{channel} "
            r"(?P<ramp_active>[01])"
            r"(?P<ramp_running>[01]) "
            r"(?P<ramp_rate_up>(?:\d{4}|-\d{2})\.\d{2}) "
            r"(?P<ramp_rate_down>(?:\d{4}|-\d{2})\.\d{2}) "
            r"(?P<ramp_target>(?:\d{4}|-\d{2})\.\d{2})$"
        )
        if match := re.match(pattern, response):
            return CTSChamberRampParameters(
                ramp_active=bool(int(match.group("ramp_active"))),
                ramp_running=bool(int(match.group("ramp_running"))),
                ramp_rate_up=float(match.group("ramp_rate_up")),
                ramp_rate_down=float(match.group("ramp_rate_down")),
                ramp_target=float(match.group("ramp_target"))
            )

        raise CTSChamberCommandError(f"Invalid response format: {response}.")

    def get_temperature_ramp_information(self) -> CTSChamberRampParameters:
        """
        Gets information about the ongoing temperature ramp operation.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        return self._get_ramp_information(self._RAMP_CHANNEL_TEMPERATURE)

    def get_humidity_ramp_information(self) -> CTSChamberRampParameters:
        """
        Gets information about the ongoing humidity ramp operation.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        return self._get_ramp_information(self._RAMP_CHANNEL_HUMIDITY)

    def get_state(self) -> CTSState:
        """
        Gets the current state of the CTS chamber.

        Returns:
            An instance of CTSState containing the current state of the chamber.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        message = "S"
        response = self._send_cmd(message)

        pattern = (
            r"^S"
            r"(?P<running>[01])"
            r"(?P<error>[01])"
            r"(?P<not_paused>[01])"
            r"(?P<humidity_on>[01])"
            r"(?P<dew_gt_7>[01])"
            r"(?P<dew_lt_7>[01])"
            r"(?P<deep_humidity>[01])"
            r"(?P<reg_supply_air>[01])"
            r"(?P<error_number>.)"
        )
        if match := re.match(pattern, response):
            try:
                error_number = match.group("error_number")
                error_number = CTSStateError.from_value(int(error_number))
            except ValueError:
                _LOGGER.error(f"Invalid error number in response: {response}")
                raise CTSChamberCommandError(
                    f"Invalid error number in response: {response}."
                )

            state = CTSState(
                running=bool(int(match.group("running"))),
                error=bool(int(match.group("error"))),
                paused=not bool(int(match.group("not_paused"))),
                humidity_on=bool(int(match.group("humidity_on"))),
                dew_point_above_seven=bool(int(match.group("dew_gt_7"))),
                dew_point_below_seven=bool(int(match.group("dew_lt_7"))),
                deep_dehumidity_on=bool(int(match.group("deep_humidity"))),
                reg_suply_air=bool(int(match.group("reg_supply_air"))),
                error_number=error_number
            )
            return state
        else:
            _LOGGER.error(f"Response does not match expected format: {response}")
            raise CTSChamberCommandError(
                f"Invalid response format: {response}."
            )

    def start(self) -> None:
        """
        Starts the CTS chamber.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        self._set_digital_channel(1, True)  # Start the chamber

    def stop(self) -> None:
        """
        Stops the CTS chamber.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        self._set_digital_channel(1, False)

    def pause(self) -> None:
        """
        Pauses the CTS chamber.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        self._set_digital_channel(3, False)  # Pause the chamber

    def resume(self) -> None:
        """
        Resumes the CTS chamber from a paused state.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        self._set_digital_channel(3, True)

    def collect_errors(self) -> None:
        """
        Collects errors from the CTS chamber. Errors are available in the state
        after calling this method.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        self._set_digital_channel(2, True)

    def close(self):
        """
        Closes the connection to the device.
        """
        try:
            self._resource.close()
        except Exception as e:
            _LOGGER.exception(f"Error closing resource: {e}")

    def send_command(self, command: str) -> str:
        """
        Sends a command to the CTS chamber and returns the response. The command should be an ASCII
        string, which will be encoded to bytes before sending.

        Args:
            command: The command to send to the chamber.

        Returns:
            The response from the chamber.

        Raises:
            CTSChamberCommandError: If the command fails or the response is invalid.
            CTSChamberCommunicationError: If there is an error in communication with the device.
        """
        return self._send_cmd(command)

    def __del__(self):
        self.close()
