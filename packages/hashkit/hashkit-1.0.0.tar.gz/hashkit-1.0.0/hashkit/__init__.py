"""
HashKit - Professional Hash Analysis and Cracking Tool

⚠️  LEGAL DISCLAIMER ⚠️
This tool is designed for authorized security testing and forensic analysis only.
Use only on systems you own or have explicit permission to test.
Unauthorized password cracking is illegal and unethical.

The authors assume no responsibility for misuse of this tool.
"""

__version__ = "1.0.0"
__author__ = "AbderrahimGHAZALI"

# Legal disclaimer
LEGAL_DISCLAIMER = """
⚠️  LEGAL AND ETHICAL USE ONLY ⚠️

This tool is intended for:
- Authorized penetration testing with written permission
- Digital forensics and incident response
- Educational purposes in controlled environments
- Security research with proper authorization
- Password policy compliance testing

UNAUTHORIZED PASSWORD CRACKING IS ILLEGAL AND UNETHICAL.
The authors are not responsible for misuse of this tool.
"""

from .identifier import HashIdentifier
from .cracker import HashCracker
from .wordlists import WordlistManager
from .analyzer import HashAnalyzer
from .exceptions import HashKitError, IdentificationError, CrackingError

__all__ = [
    "HashIdentifier",
    "HashCracker", 
    "WordlistManager",
    "HashAnalyzer",
    "HashKitError",
    "IdentificationError",
    "CrackingError",
    "LEGAL_DISCLAIMER"
]

# Display disclaimer on import
import sys
if not any('pytest' in arg for arg in sys.argv):
    print(LEGAL_DISCLAIMER)