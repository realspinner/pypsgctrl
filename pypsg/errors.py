## @file
# @brief Driver exceptions.
from __future__ import annotations

## @brief Base driver exception.
class PSGError(Exception):
    """Base driver error."""


## @brief Malformed response, rejected write, or incomplete write.
class ProtocolError(PSGError):
    """Malformed, unexpected, or rejected device response."""


## @brief Response timeout expired; reopen the connection.
class PSGTimeoutError(PSGError, TimeoutError):
    """No complete response arrived within the transport timeout."""
