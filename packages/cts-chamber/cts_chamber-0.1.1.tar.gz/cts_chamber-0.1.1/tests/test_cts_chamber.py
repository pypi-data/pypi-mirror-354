import time

import pytest
from cts_chamber import (
    CTSChamber,
)


def test_temperature_setpoint(cts_chamber: CTSChamber):
    SETPOINT = 25.0

    cts_chamber.set_temperature(SETPOINT)

    _, setpoint = cts_chamber.get_temperature()

    assert isinstance(setpoint, float)
    assert setpoint == SETPOINT

@pytest.mark.skipif(
    "config.getvalue('hil')", reason="Not valid for hardware-in-the-loop"
)
def test_temperature(cts_chamber: CTSChamber, mock_cts_chamber):
    SETPOINT = 25.0
    CURRENT = 20.0

    cts_chamber.set_temperature(SETPOINT)
    mock_cts_chamber.set_current_temperature(CURRENT)

    current, setpoint = cts_chamber.get_temperature()

    assert isinstance(current, float)
    assert isinstance(setpoint, float)
    assert current == CURRENT
    assert setpoint == SETPOINT

def test_start_stop(cts_chamber: CTSChamber):
    cts_chamber.start()
    state = cts_chamber.get_state()
    assert state.running

    time.sleep(2)

    cts_chamber.stop()
    state = cts_chamber.get_state()
    assert not state.running

def test_humidity_setpoint(cts_chamber: CTSChamber):
    SETPOINT = 55.0

    cts_chamber.set_humidity(SETPOINT)

    _, setpoint = cts_chamber.get_humidity()

    assert isinstance(setpoint, float)
    assert setpoint == SETPOINT

@pytest.mark.skipif(
    "config.getvalue('hil')", reason="Not valid for hardware-in-the-loop"
)
def test_humidity(cts_chamber: CTSChamber, mock_cts_chamber):
    SETPOINT = 60.0
    CURRENT = 45.0

    cts_chamber.set_humidity(SETPOINT)
    mock_cts_chamber.set_current_humidity(CURRENT)

    current, setpoint = cts_chamber.get_humidity()

    assert isinstance(current, float)
    assert isinstance(setpoint, float)
    assert current == CURRENT
    assert setpoint == SETPOINT

def test_temperature_ramp_up(cts_chamber: CTSChamber, mock_cts_chamber):
    CURRENT = 20.0
    SETPOINT = 40.0
    RAMP_UP = 2.0
    RAMP_DOWN = 1.0

    # Set initial temperature below setpoint
    mock_cts_chamber.set_current_temperature(CURRENT)

    cts_chamber.set_temperature(SETPOINT)
    cts_chamber.ramp_to_temperature(SETPOINT, ramp_up_rate=RAMP_UP, ramp_down_rate=RAMP_DOWN)

    ramp_info = cts_chamber.get_temperature_ramp_information()

    assert ramp_info.ramp_active
    assert ramp_info.ramp_running
    assert ramp_info.ramp_rate_up == RAMP_UP
    assert ramp_info.ramp_rate_down == RAMP_DOWN
    assert ramp_info.ramp_target == SETPOINT

def test_temperature_ramp_down(cts_chamber: CTSChamber, mock_cts_chamber):
    CURRENT = 30.0
    SETPOINT = 10.0
    RAMP_UP = 2.0
    RAMP_DOWN = 1.5

    # Set initial temperature above setpoint
    mock_cts_chamber.set_current_temperature(CURRENT)

    cts_chamber.set_temperature(SETPOINT)
    cts_chamber.ramp_to_temperature(SETPOINT, ramp_up_rate=RAMP_UP, ramp_down_rate=RAMP_DOWN)

    ramp_info = cts_chamber.get_temperature_ramp_information()

    assert ramp_info.ramp_active
    assert ramp_info.ramp_running
    assert ramp_info.ramp_rate_up == RAMP_UP
    assert ramp_info.ramp_rate_down == RAMP_DOWN
    assert ramp_info.ramp_target == SETPOINT

def test_humidity_ramp_up(cts_chamber: CTSChamber, mock_cts_chamber):
    CURRENT = 40.0
    SETPOINT = 60.0
    RAMP_UP = 3.0
    RAMP_DOWN = 1.0

    # Set initial humidity below setpoint
    mock_cts_chamber.set_current_humidity(CURRENT)

    cts_chamber.set_humidity(SETPOINT)
    cts_chamber.ramp_to_humidity(SETPOINT, ramp_up_rate=RAMP_UP, ramp_down_rate=RAMP_DOWN)

    ramp_info = cts_chamber.get_humidity_ramp_information()

    assert ramp_info.ramp_active
    assert ramp_info.ramp_running
    assert ramp_info.ramp_rate_up == RAMP_UP
    assert ramp_info.ramp_rate_down == RAMP_DOWN
    assert ramp_info.ramp_target == SETPOINT

def test_humidity_ramp_down(cts_chamber: CTSChamber, mock_cts_chamber):
    CURRENT = 70.0
    SETPOINT = 50.0
    RAMP_UP = 2.0
    RAMP_DOWN = 1.5

    # Set initial humidity above setpoint
    mock_cts_chamber.set_current_humidity(CURRENT)

    cts_chamber.set_humidity(SETPOINT)
    cts_chamber.ramp_to_humidity(SETPOINT, ramp_up_rate=RAMP_UP, ramp_down_rate=RAMP_DOWN)

    ramp_info = cts_chamber.get_humidity_ramp_information()

    assert ramp_info.ramp_active
    assert ramp_info.ramp_running
    assert ramp_info.ramp_rate_up == RAMP_UP
    assert ramp_info.ramp_rate_down == RAMP_DOWN
    assert ramp_info.ramp_target == SETPOINT
