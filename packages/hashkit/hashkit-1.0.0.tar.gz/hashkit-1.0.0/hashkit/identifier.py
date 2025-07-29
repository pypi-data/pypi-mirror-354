"""
Hash identification engine
"""

import hashlib
import re
import binascii
from typing import List, Dict, Optional, Tuple, Any
from .models import HashType, HashInfo
from .exceptions import IdentificationError


class HashIdentifier:
    """
    Professional hash identification engine
    
    Identifies hash types based on length, format, and entropy analysis
    """
    
    def __init__(self):
        self.hash_patterns = self._load_hash_patterns()
        self.hash_lengths = self._load_hash_lengths()
        self.format_patterns = self._load_format_patterns()
    
    def _load_hash_patterns(self) -> Dict[HashType, List[str]]:
        """Load regex patterns for hash identification"""
        return {
            HashType.MD5: [r'^[a-f0-9]{32}$'],
            HashType.SHA1: [r'^[a-f0-9]{40}$'],
            HashType.SHA224: [r'^[a-f0-9]{56}$'],
            HashType.SHA256: [r'^[a-f0-9]{64}$'],
            HashType.SHA384: [r'^[a-f0-9]{96}$'],
            HashType.SHA512: [r'^[a-f0-9]{128}$'],
            HashType.NTLM: [r'^[a-f0-9]{32}$'],  # Same as MD5 but different context
            HashType.LM: [r'^[a-f0-9]{32}$'],
            HashType.MYSQL: [
                r'^\*[A-F0-9]{40}$',  # MySQL 4.1+
                r'^[a-f0-9]{16}$'     # MySQL < 4.1
            ],
            HashType.POSTGRESQL: [r'^md5[a-f0-9]{32}$'],
            HashType.BCRYPT: [r'^\$2[aby]?\$[0-9]{2}\$[A-Za-z0-9./]{53}$'],
            HashType.SCRYPT: [r'^\$scrypt\$'],
            HashType.ARGON2: [r'^\$argon2[id]?\$'],
            HashType.PBKDF2: [r'^\$pbkdf2'],
            HashType.CRC32: [r'^[a-f0-9]{8}$'],
            HashType.BLAKE2B: [r'^[a-f0-9]{128}$'],  # Default 512-bit
            HashType.BLAKE2S: [r'^[a-f0-9]{64}$'],   # Default 256-bit
        }
    
    def _load_hash_lengths(self) -> Dict[int, List[HashType]]:
        """Map hash lengths to possible types"""
        return {
            8: [HashType.CRC32, HashType.ADLER32],
            16: [HashType.MYSQL],  # Old MySQL
            32: [HashType.MD5, HashType.NTLM, HashType.LM],
            40: [HashType.SHA1],
            41: [HashType.MYSQL],  # MySQL 4.1+ with *
            56: [HashType.SHA224],
            64: [HashType.SHA256, HashType.BLAKE2S],
            96: [HashType.SHA384],
            128: [HashType.SHA512, HashType.BLAKE2B],
        }
    
    def _load_format_patterns(self) -> Dict[str, HashType]:
        """Load format-specific patterns"""
        return {
            r'^\*[A-F0-9]{40}$': HashType.MYSQL,
            r'^md5[a-f0-9]{32}$': HashType.POSTGRESQL,
            r'^\$2[aby]?\$': HashType.BCRYPT,
            r'^\$scrypt\$': HashType.SCRYPT,
            r'^\$argon2': HashType.ARGON2,
            r'^\$pbkdf2': HashType.PBKDF2,
        }
    
    def identify(self, hash_value: str) -> HashInfo:
        """
        Identify hash type with confidence scoring
        
        Args:
            hash_value: Hash string to identify
            
        Returns:
            HashInfo object with identification results
        """
        if not hash_value:
            raise IdentificationError("Empty hash provided")
        
        # Clean hash (remove whitespace)
        clean_hash = hash_value.strip()
        
        # Check format patterns first (highest confidence)
        format_match = self._check_format_patterns(clean_hash)
        if format_match:
            return HashInfo(
                hash_value=clean_hash,
                hash_type=format_match,
                confidence=0.95,
                length=len(clean_hash),
                charset=self._analyze_charset(clean_hash),
                possible_types=[format_match]
            )
        
        # Check by length and pattern
        possible_types = self._identify_by_length_and_pattern(clean_hash)
        
        if not possible_types:
            return HashInfo(
                hash_value=clean_hash,
                hash_type=HashType.UNKNOWN,
                confidence=0.0,
                length=len(clean_hash),
                charset=self._analyze_charset(clean_hash),
                possible_types=[]
            )
        
        # If only one possibility, high confidence
        if len(possible_types) == 1:
            return HashInfo(
                hash_value=clean_hash,
                hash_type=possible_types[0],
                confidence=0.9,
                length=len(clean_hash),
                charset=self._analyze_charset(clean_hash),
                possible_types=possible_types
            )
        
        # Multiple possibilities - use heuristics
        best_type, confidence = self._apply_heuristics(clean_hash, possible_types)
        
        return HashInfo(
            hash_value=clean_hash,
            hash_type=best_type,
            confidence=confidence,
            length=len(clean_hash),
            charset=self._analyze_charset(clean_hash),
            possible_types=possible_types
        )
    
    def _check_format_patterns(self, hash_value: str) -> Optional[HashType]:
        """Check format-specific patterns"""
        for pattern, hash_type in self.format_patterns.items():
            if re.match(pattern, hash_value):
                return hash_type
        return None
    
    def _identify_by_length_and_pattern(self, hash_value: str) -> List[HashType]:
        """Identify possible types by length and basic patterns"""
        length = len(hash_value)
        possible_types = []
        
        # Get types by length
        length_matches = self.hash_lengths.get(length, [])
        
        # Check patterns for each possible type
        for hash_type in length_matches:
            patterns = self.hash_patterns.get(hash_type, [])
            for pattern in patterns:
                if re.match(pattern, hash_value, re.IGNORECASE):
                    possible_types.append(hash_type)
                    break
        
        return list(set(possible_types))  # Remove duplicates
    
    def _apply_heuristics(self, hash_value: str, possible_types: List[HashType]) -> Tuple[HashType, float]:
        """Apply heuristics to determine most likely type"""
        scores = {}
        
        for hash_type in possible_types:
            score = 0.5  # Base score
            
            # Charset analysis
            if hash_type in [HashType.MD5, HashType.SHA1, HashType.SHA256, HashType.SHA512]:
                if self._is_hex_lowercase(hash_value):
                    score += 0.2
                elif self._is_hex_uppercase(hash_value):
                    score += 0.1
            
            # Common hash type preferences
            if hash_type == HashType.MD5 and len(hash_value) == 32:
                score += 0.1  # MD5 is common
            elif hash_type == HashType.SHA1 and len(hash_value) == 40:
                score += 0.1  # SHA1 is common
            elif hash_type == HashType.SHA256 and len(hash_value) == 64:
                score += 0.15  # SHA256 is very common nowadays
            
            # NTLM vs MD5 disambiguation (both 32 chars)
            if hash_type == HashType.NTLM and len(hash_value) == 32:
                if self._looks_like_ntlm(hash_value):
                    score += 0.2
            
            scores[hash_type] = score
        
        # Return type with highest score
        best_type = max(scores, key=scores.get)
        confidence = min(scores[best_type], 0.95)  # Cap at 95%
        
        return best_type, confidence
    
    def _analyze_charset(self, hash_value: str) -> str:
        """Analyze character set used in hash"""
        if re.match(r'^[0-9a-f]+$', hash_value):
            return "hex_lower"
        elif re.match(r'^[0-9A-F]+$', hash_value):
            return "hex_upper"
        elif re.match(r'^[0-9a-fA-F]+$', hash_value):
            return "hex_mixed"
        elif re.match(r'^[A-Za-z0-9+/]+={0,2}$', hash_value):
            return "base64"
        elif re.match(r'^[A-Za-z0-9./]+$', hash_value):
            return "base64_bcrypt"
        else:
            return "mixed"
    
    def _is_hex_lowercase(self, value: str) -> bool:
        return re.match(r'^[0-9a-f]+$', value) is not None
    
    def _is_hex_uppercase(self, value: str) -> bool:
        return re.match(r'^[0-9A-F]+$', value) is not None
    
    def _looks_like_ntlm(self, hash_value: str) -> bool:
        """Heuristic to detect NTLM vs MD5"""
        # NTLM hashes often have different entropy patterns
        # This is a simplified heuristic
        uppercase_count = sum(1 for c in hash_value if c.isupper())
        return uppercase_count > len(hash_value) * 0.3  # More than 30% uppercase
    
    def identify_multiple(self, hashes: List[str]) -> List[HashInfo]:
        """Identify multiple hashes"""
        results = []
        for hash_value in hashes:
            try:
                info = self.identify(hash_value)
                results.append(info)
            except IdentificationError as e:
                # Create error result
                results.append(HashInfo(
                    hash_value=hash_value,
                    hash_type=HashType.UNKNOWN,
                    confidence=0.0,
                    length=len(hash_value),
                    charset="unknown",
                    possible_types=[]
                ))
        return results
    
    def get_hash_info(self, hash_type: HashType) -> Dict[str, Any]:
        """Get detailed information about a hash type"""
        info_map = {
            HashType.MD5: {
                "name": "MD5",
                "full_name": "Message Digest Algorithm 5",
                "output_size": 128,
                "security": "Broken (collision attacks)",
                "use_cases": ["Legacy systems", "Checksums (non-security)"],
                "year": 1991
            },
            HashType.SHA1: {
                "name": "SHA-1", 
                "full_name": "Secure Hash Algorithm 1",
                "output_size": 160,
                "security": "Deprecated (collision attacks)",
                "use_cases": ["Legacy systems", "Git (being phased out)"],
                "year": 1995
            },
            HashType.SHA256: {
                "name": "SHA-256",
                "full_name": "Secure Hash Algorithm 256-bit",
                "output_size": 256,
                "security": "Secure",
                "use_cases": ["Cryptocurrency", "TLS", "Modern applications"],
                "year": 2001
            },
            HashType.SHA512: {
                "name": "SHA-512",
                "full_name": "Secure Hash Algorithm 512-bit", 
                "output_size": 512,
                "security": "Secure",
                "use_cases": ["High security applications", "Password hashing"],
                "year": 2001
            },
            HashType.BCRYPT: {
                "name": "bcrypt",
                "full_name": "bcrypt adaptive hash function",
                "output_size": "Variable",
                "security": "Very Secure (adaptive)",
                "use_cases": ["Password storage", "Authentication systems"],
                "year": 1999
            },
            HashType.NTLM: {
                "name": "NTLM",
                "full_name": "NT Lan Manager Hash",
                "output_size": 128,
                "security": "Weak (no salt, MD4-based)",
                "use_cases": ["Windows authentication (legacy)"],
                "year": 1993
            }
        }
        
        return info_map.get(hash_type, {
            "name": hash_type.value,
            "full_name": "Unknown hash type",
            "output_size": "Unknown",
            "security": "Unknown",
            "use_cases": [],
            "year": "Unknown"
        })


# Quick identification functions
def identify_hash(hash_value: str) -> HashInfo:
    """Quick hash identification"""
    identifier = HashIdentifier()
    return identifier.identify(hash_value)

def identify_hashes(hashes: List[str]) -> List[HashInfo]:
    """Quick multiple hash identification"""
    identifier = HashIdentifier()
    return identifier.identify_multiple(hashes)