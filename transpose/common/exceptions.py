class InstanceConnectionError(Exception):
    """Raised when there is an error connecting to a dedicated instance."""


class InvalidSyncTableError(Exception):
    """Raised when the given table does not fall into any of the three sync categories."""


class InvalidSyncStateError(Exception):
    """Raised when an invalid sync state is attempted"""
