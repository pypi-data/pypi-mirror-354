"""
Custom exceptions for the alumath_peergroup_6 library.
"""

class AlumathError(Exception):
    """Base exception class for alumath_peergroup_6."""
    pass

class DimensionError(AlumathError):
    """Raised when matrix dimensions are incompatible for the requested operation."""
    pass

class InvalidMatrixError(AlumathError):
    """Raised when the input is not a valid matrix."""
    pass
