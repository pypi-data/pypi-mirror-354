import pytest
from cts_chamber import CTSChamber
from cts_chamber_mocker import CTSChamberMocker
from pyvisa import ResourceManager
from pyvisa_mock.base.register import register_resource

MOCK_RESOURCE_PATH = "MOCK0::mock1::INSTR"
"VISA resource path for the mock CTS chamber."

def pytest_addoption(parser):
    parser.addoption(
        "--hil", action="store_true", help="Run tests on hardware-in-the-loop"
    )
    parser.addoption("--hil_serial_device", help="Serial device to run the tests on")


@pytest.fixture(scope="module")
def mock_cts_chamber():
    mock_cts_chamber = CTSChamberMocker()
    register_resource(MOCK_RESOURCE_PATH, mock_cts_chamber)
    return mock_cts_chamber


@pytest.fixture(scope="session")
def hil(request):
    return request.config.option.hil is not None and request.config.option.hil


@pytest.fixture(scope="session")
def hil_serial_device(request):
    if request.config.option.hil_serial_device is not None:
        return request.config.option.hil_serial_device
    else:
        return "/dev/ttyUSB0"


@pytest.fixture(scope="module")
def cts_chamber(mock_cts_chamber, hil, hil_serial_device):
    if hil:
        clock_generator = CTSChamber(
            serial_device=hil_serial_device,
        )
    else:
        resource_manager = ResourceManager(visa_library="@mock")
        clock_generator = CTSChamber(
            resource_path=MOCK_RESOURCE_PATH,
            resource_manager=resource_manager,
        )
    return clock_generator
