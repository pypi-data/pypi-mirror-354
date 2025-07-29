"""
Utility functions for HashKit
"""

import hashlib
import hmac
import base64
import binascii
import math
from typing import Callable, Any, Dict, Optional
from collections import Counter

from .models import HashType
from .exceptions import HashKitError


def get_hasher(hash_type: HashType) -> Callable[[str], str]:
    """
    Get the appropriate hasher function for a hash type
    
    Args:
        hash_type: Hash type enum
        
    Returns:
        Hasher function that takes a string and returns hex hash
    """
    hashers = {
        HashType.MD5: lambda x: hashlib.md5(x.encode('utf-8')).hexdigest(),
        HashType.SHA1: lambda x: hashlib.sha1(x.encode('utf-8')).hexdigest(),
        HashType.SHA224: lambda x: hashlib.sha224(x.encode('utf-8')).hexdigest(),
        HashType.SHA256: lambda x: hashlib.sha256(x.encode('utf-8')).hexdigest(),
        HashType.SHA384: lambda x: hashlib.sha384(x.encode('utf-8')).hexdigest(),
        HashType.SHA512: lambda x: hashlib.sha512(x.encode('utf-8')).hexdigest(),
        HashType.SHA3_224: lambda x: hashlib.sha3_224(x.encode('utf-8')).hexdigest(),
        HashType.SHA3_256: lambda x: hashlib.sha3_256(x.encode('utf-8')).hexdigest(),
        HashType.SHA3_384: lambda x: hashlib.sha3_384(x.encode('utf-8')).hexdigest(),
        HashType.SHA3_512: lambda x: hashlib.sha3_512(x.encode('utf-8')).hexdigest(),
        HashType.BLAKE2B: lambda x: hashlib.blake2b(x.encode('utf-8')).hexdigest(),
        HashType.BLAKE2S: lambda x: hashlib.blake2s(x.encode('utf-8')).hexdigest(),
        HashType.NTLM: lambda x: hashlib.new('md4', x.encode('utf-16le')).hexdigest(),
    }
    
    if hash_type not in hashers:
        raise HashKitError(f"Unsupported hash type: {hash_type}")
    
    return hashers[hash_type]


def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy of text"""
    if not text:
        return 0.0
    
    # Count character frequencies
    char_counts = Counter(text)
    text_length = len(text)
    
    # Calculate entropy
    entropy = 0.0
    for count in char_counts.values():
        probability = count / text_length
        if probability > 0:
            entropy -= probability * math.log2(probability)
    
    return entropy


def format_size(size_bytes: int) -> str:
    """Format byte size as human readable string"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"


def format_number(number: int) -> str:
    """Format large numbers with commas"""
    return f"{number:,}"


def validate_hash_format(hash_value: str, hash_type: HashType) -> bool:
    """Validate if a hash matches the expected format for its type"""
    if not hash_value:
        return False
    
    format_specs = {
        HashType.MD5: (32, r'^[a-fA-F0-9]{32}$'),
        HashType.SHA1: (40, r'^[a-fA-F0-9]{40}$'),
        HashType.SHA224: (56, r'^[a-fA-F0-9]{56}$'),
        HashType.SHA256: (64, r'^[a-fA-F0-9]{64}$'),
        HashType.SHA384: (96, r'^[a-fA-F0-9]{96}$'),
        HashType.SHA512: (128, r'^[a-fA-F0-9]{128}$'),
        HashType.NTLM: (32, r'^[a-fA-F0-9]{32}$'),
    }
    
    if hash_type not in format_specs:
        return True  # Can't validate unknown formats
    
    expected_length, pattern = format_specs[hash_type]
    
    return len(hash_value) == expected_length and bool(re.match(pattern, hash_value))


def generate_test_hash(plaintext: str, hash_type: HashType) -> str:
    """Generate a test hash for verification"""
    hasher = get_hasher(hash_type)
    return hasher(plaintext)


def benchmark_hasher(hash_type: HashType, iterations: int = 10000) -> Dict[str, float]:
    """Benchmark hash function performance"""
    import time
    
    hasher = get_hasher(hash_type)
    test_string = "benchmark_test_string_123"
    
    # Warm up
    for _ in range(100):
        hasher(test_string)
    
    # Benchmark
    start_time = time.time()
    for _ in range(iterations):
        hasher(test_string)
    end_time = time.time()
    
    total_time = end_time - start_time
    hashes_per_second = iterations / total_time
    
    return {
        'total_time': total_time,
        'iterations': iterations,
        'hashes_per_second': hashes_per_second,
        'avg_time_per_hash': total_time / iterations
    }
