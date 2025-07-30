"""
Exceptions for a CTS environmental chamber.
"""

__author__ = "Leandro Lanzieri"
__copyright__ = "Deutsches Elektronen-Synchrotron, DESY"
__license__ = "LGPL-3.0"


class CTSChamberOperationTimeoutError(Exception):
    """Raised when a command to the CTS chamber times out."""

    pass


class CTSChamberCommunicationError(Exception):
    """Raised when there is a communication error with the CTS chamber."""

    pass


class CTSChamberCommandError(Exception):
    """Raised when there is an error in a command to the CTS chamber."""

    pass
