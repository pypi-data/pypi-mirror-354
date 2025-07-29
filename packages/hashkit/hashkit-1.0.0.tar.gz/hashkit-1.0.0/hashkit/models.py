"""
Data models for HashKit
"""

import hashlib
import hmac
import base64
import binascii
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass


class HashType(str, Enum):
    """Supported hash types"""
    MD5 = "md5"
    SHA1 = "sha1"
    SHA224 = "sha224"
    SHA256 = "sha256"
    SHA384 = "sha384"
    SHA512 = "sha512"
    SHA3_224 = "sha3_224"
    SHA3_256 = "sha3_256"
    SHA3_384 = "sha3_384"
    SHA3_512 = "sha3_512"
    BLAKE2B = "blake2b"
    BLAKE2S = "blake2s"
    NTLM = "ntlm"
    LM = "lm"
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    BCRYPT = "bcrypt"
    SCRYPT = "scrypt"
    ARGON2 = "argon2"
    PBKDF2 = "pbkdf2"
    CRC32 = "crc32"
    ADLER32 = "adler32"
    UNKNOWN = "unknown"


class AttackMode(str, Enum):
    """Hash cracking attack modes"""
    DICTIONARY = "dictionary"
    BRUTEFORCE = "bruteforce"
    HYBRID = "hybrid"
    RULE_BASED = "rule_based"
    MASK = "mask"
    COMBINATOR = "combinator"


class CrackStatus(str, Enum):
    """Status of cracking attempt"""
    NOT_STARTED = "not_started"
    RUNNING = "running"
    CRACKED = "cracked"
    EXHAUSTED = "exhausted"
    STOPPED = "stopped"
    ERROR = "error"


@dataclass
class HashInfo:
    """Information about a hash"""
    hash_value: str
    hash_type: HashType
    confidence: float  # 0.0 to 1.0
    length: int
    charset: str
    possible_types: List[HashType]
    
    def __str__(self):
        return f"{self.hash_type.value.upper()} ({self.confidence:.1%} confidence)"


@dataclass
class CrackResult:
    """Result of a hash cracking attempt"""
    hash_value: str
    plaintext: Optional[str]
    attack_mode: AttackMode
    status: CrackStatus
    attempts: int
    duration: float
    cracked_at: Optional[datetime]
    wordlist_used: Optional[str]
    rule_used: Optional[str]
    
    @property
    def success(self) -> bool:
        return self.status == CrackStatus.CRACKED
    
    @property
    def rate(self) -> float:
        """Attempts per second"""
        if self.duration > 0:
            return self.attempts / self.duration
        return 0.0


@dataclass
class CrackingSession:
    """Information about a cracking session"""
    session_id: str
    target_hashes: List[str]
    attack_mode: AttackMode
    started_at: datetime
    status: CrackStatus
    progress: float  # 0.0 to 1.0
    results: List[CrackResult]
    
    @property
    def cracked_count(self) -> int:
        return sum(1 for result in self.results if result.success)
    
    @property
    def success_rate(self) -> float:
        if len(self.target_hashes) > 0:
            return self.cracked_count / len(self.target_hashes)
        return 0.0