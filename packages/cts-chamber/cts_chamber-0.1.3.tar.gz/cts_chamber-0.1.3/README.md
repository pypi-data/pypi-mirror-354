# CTS Environmental Chamber Interface

Interface with a CTS Environmental Chamber.

## Installation

```bash
$ pip install cts-chamber
```

## Supported Features

- Temperature control
- Humidity control
- R232 communication

## Usage

```python
from cts_chamber import CTSChamber

chamber = CTSChamber(
        serial_device='/dev/ttyUSB0',
)

chamber.set_temperature(30.0)

current, set_point = chamber.get_temperature()
print(f"Current temperture is {current} °C")
print(f"Setpoint is {set_point} °C")

chamber.start()

```

## Running tests on hardware

During normal development and for the CI the unit test suite is executed on a mock
device using pyvisa-mock. It is also possible to run tests on real hardware connected
to your system. Just set the `hil` flag when running `poe`

```bash
$ uv run poe test_hil
```

By default it will try to connect to `/dev/ttyUSB0`, but you can specify a different
device using the `--hil_serial_device` option:

```bash
$ uv run poe test_hil --hil_serial_device /dev/ttyUSB1
```

## Status

Currently only the RS232 communication has been tested on the device.

## Documentation

Check out the API documentation of the module [here](https://cts-chamber-8923d6.pages.desy.de/).

## Feeling like contributing?

Great! Check the [Contributing Guide](CONTRIBUTING.md) to get started.
