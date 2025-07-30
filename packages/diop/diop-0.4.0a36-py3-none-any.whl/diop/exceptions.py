"""Diop exception classes."""

import logging

log = logging.getLogger(__name__)


class UpdateTaskError(Exception):
    def __init__(self, message, details, okay, fail):
        self.message = message
        self.details = details
        self.okay = okay
        self.fail = fail

    def __str__(self):
        details = "\n".join(str(self.details))
        return (
            f"{self.message}\n"
            f"OKAY={self.okay}\n"
            f"FAIL={self.fail}\n"
            f"FAILED DETAILS:\n{details}"
        )


class UpdateMachinesError(UpdateTaskError):
    pass


class UpdateSessionsError(UpdateTaskError):
    pass
