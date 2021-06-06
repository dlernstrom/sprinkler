"""Exceptions for the Sprinkler project"""


class NumatoError(Exception):
    """Base class for all Numato thrown errors"""


class LoginError(NumatoError):
    """Thrown when we cannot log into device"""
