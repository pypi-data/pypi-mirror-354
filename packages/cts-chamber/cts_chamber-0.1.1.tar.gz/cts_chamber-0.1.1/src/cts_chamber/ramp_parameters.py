from dataclasses import dataclass


@dataclass
class CTSChamberRampParameters:
    """
    Parameters of a ramp operation in a CTS chamber.
    """
    ramp_active: bool
    "Ramp management is active"

    ramp_running: bool
    "Ramp management is currently running. Reasons not to run are pauses or errors."

    ramp_rate_up: float
    "Rate of increase in K/min"

    ramp_rate_down: float
    "Rate of decrease in K/min"

    ramp_target: float
    "Target temperature for the ramp in degrees Celsius for temperature and in % for humidity"
