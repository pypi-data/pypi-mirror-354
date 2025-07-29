"""
Custom exceptions for HashKit
"""

class HashKitError(Exception):
    """Base exception for HashKit"""
    pass

class IdentificationError(HashKitError):
    """Raised when hash identification fails"""
    pass

class CrackingError(HashKitError):
    """Raised when hash cracking encounters an error"""
    pass

class WordlistError(HashKitError):
    """Raised when wordlist operations fail"""
    pass

class ConfigurationError(HashKitError):
    """Raised when configuration is invalid"""
    pass