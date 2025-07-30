"""
Constants for the CTS environmental chamber.
"""

from enum import Enum

__author__ = "Leandro Lanzieri"
__copyright__ = "Deutsches Elektronen-Synchrotron, DESY"
__license__ = "LGPL-3.0"


class CTSChamberModel(Enum):
    """
    Enum for the model of the CTS environmental chamber.
    """

    C_40 = "C-40"
    """CTS C-40/... environmental chamber."""

    C_65 = "C-65"
    """CTS C-65/... environmental chamber."""

    C_70 = "C-70"
    """CTS C-70/... environmental chamber."""
