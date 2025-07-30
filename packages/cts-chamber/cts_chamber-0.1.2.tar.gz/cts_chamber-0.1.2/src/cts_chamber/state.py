from dataclasses import dataclass
from enum import Enum


class CTSStateError(Enum):
    ERR_NO_ERROR = 0x00
    "No error."

    ERR_ADD_WATER = 0x01
    "Add water to the chamber."

    ERR_UPPER_TEMP_TOLERANNCE_BAND = 0x02
    "Upper temperature tolerance band exceeded."

    ERR_LOWER_TEMP_TOLERANNCE_BAND = 0x03
    "Lower temperature tolerance band exceeded."

    ERR_UPPER_HUMIDITY_TOLERANNCE_BAND = 0x04
    "Upper humidity tolerance band exceeded."

    ERR_LOWER_HUMIDITY_TOLERANNCE_BAND = 0x05

    ERR_DE_SLUDGE = 0x06
    "De-sludge the water bath."

    ERR_TEMP_LIMIT_MIN_08B1 = 0x31
    "Min. temperature limit 08-B1"

    ERR_TEMP_LIMIT_MAX_08B1 = 0x32
    "Max. temperature limit 08-B1"

    ERR_TEMP_LIMITER_TEST_SPACE_01F11 = 0x33
    "Temp. limiter 1 test space 01-F1.1"

    ERR_THERMAL_CONTACT_TEST_SPACE_FAN_02F21 = 0x34
    "Thermal contact test space fan 02-F2.1"

    ERR_MAX_TEST_SPECIMEN_PROTECTION_09A1 = 0x35
    "Max test specimen protection 09-A1"

    ERR_PRECOOLING_OVERPRESSURE_03B50 = 0x36
    "Pre-cooling overpressure 03-B50"

    ERR_COOLING_OVERPRESSURE_03B40 = 0x37
    "Cooling overpressure 03-B40"

    ERR_MIN_HUMIDITY_08B2 = 0x38
    "Min. humidity 08-B2"

    ERR_MAX_HUMIDITY_08B2 = 0x39
    "Max. humidity 08-B2"

    ERR_HUMIDITY_SENSOR_08B2 = 0x3a
    "Humidity sensor 08-B2"

    ERR_LACK_OF_WATER_HUMIDITY_07B80 = 0x3b
    "Lack of water humidity 07-B80"

    ERR_THERMAL_CONTACT_CONDENSER_FAN_03F51 = 0x3c
    "Therm. cont. condenser fan 03-F5.1"

    ERR_BOILING_PRESSURE_SENSOR_03B60 = 0x3d
    "Boiling pressure sensor 03-B60"

    ERR_CONDENSER_PRESSURE_SENSOR_C_03B41 = 0x3e
    "Condenser pressure sensor C 03-B41"

    ERR_PT100_EXHAUST_AIR_08B11 = 0x3f
    "Pt100 exhaust air 08-B1.1"

    ERR_PT100_SUPPLY_AIR_08B12 = 0x40
    "Pt100 supply air 08-B1.2"

    ERR_PT100_WATER_BATH_07B4 = 0x41
    "Pt100 water bath 07-B4"

    ERR_FLOAT_WATER_SUPPLY_07B81 = 0x42
    "Float water supply 07-B81"

    ERR_PT100_MOVEABLE_08B15 = 0x43
    "Pt100 moveable 08-B15"

    ERR_PT100_SUCTION_GAS_PC_03B19 = 0x46
    "Pt100 suction gas PC 03-B19"

    ERR_PT100_SUCTION_GAS_C_03B13 = 0x47
    "Pt100 suction gas C 03-B13"

    ERR_PT100_COMPRESSED_GAS_C_03B10 = 0x48
    "Pt100 compressed gas C 03-B10"

    ERR_SUCTION_GAS_TEMP_PC_03B19 = 0x4a
    "Suction gas temperature PC 03-B19"

    ERR_SUCTION_GAS_TEMP_C_03B13 = 0x4b
    "Suction gas temperature C 03-B13"

    ERR_COMPRESSED_GAS_TEMP_C_03B10 = 0x4c
    "Compr.gas temperature C 03-B10"

    ERR_PRECOOLING_NEG_PRESSURE_03B53 = 0x4e
    "Pre-cooling negative pressure 03-B53"

    ERR_COOLING_NEG_PRESSURE_03B43 = 0x4f
    "Cooling negative pressure 03-B43"

    ERR_SUCTION_PRECOOL_REFR_CYCLE_03B53 = 0x52
    "SuctPre-coolRefrCycle 03-B53"

    ERR_SUCTION_COOL_REFR_CYCLE_03B43 = 0x53
    "Suct.cool.refrig.cycle 03-B43"

    ERR_FLOAT_WATER_BATH_07B80 = 0x5b
    "Float water bath 07-B80"

    ERR_PT100_SUCTION_STEAM_C_03B12 = 0x5c
    "Pt100 suction steam C 03-B12"

    ERR_PT100_SUCTION_STEAM_PC_03B18 = 0x5d
    "Pt100 suction steam PC 03-B18"

    ERR_BOILING_PRESSURE_SENSOR_C_03B43 = 0x5e
    "Boiling pressure sensor C 03-B43"

    ERR_BOILING_PRESSURE_SENSOR_PC_03B53 = 0x5f
    "Boiling pressure sensor PC 03-B53"

    ERR_CIRCUIT_BREAKER_POWER_SUPPLY_00Q1 = 0x62
    "Circuit breaker power supply 00-Q1"

    ERR_PRECOOLING_CIRCUIT = 0x63
    "Pre-cooling circuit"

    @classmethod
    def from_value(cls, value: int) -> 'CTSStateError':
        """
        Returns the CTSStateError corresponding to the given value.
        """
        for error in cls:
            if error.value == value:
                return error
        raise ValueError(f"Invalid CTSStateError value: {value}")

@dataclass
class CTSState:
    """
    Represents the state of the CTS Environmental Chamber.
    """
    running: bool
    "Whether the chamber is currently running."

    error: bool
    "Whether there is an error in the chamber."

    paused: bool
    "Whether the chamber is currently paused."

    humidity_on: bool
    "Whether the humidity control is currently on."

    dew_point_above_seven: bool
    "Whether the dew point is above 7°C."

    dew_point_below_seven: bool
    "Whether the dew point is below 7°C."

    deep_dehumidity_on: bool
    "Whether the deep dehumidification is currently on."

    reg_suply_air: bool
    "Whether the supply air regulation is currently on."

    error_number: CTSStateError
    "The error number if there is an error, otherwise None."
