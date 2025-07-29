"""Custom exceptions for XDBC Client"""


class XDBCException(Exception):
    """Base exception for XDBC Client"""
    pass


class AuthenticationError(XDBCException):
    """Raised when authentication fails"""
    pass


class APIError(XDBCException):
    """Raised when API request fails"""
    pass