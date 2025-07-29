"""
Hash analysis and statistics
"""

import hashlib
import statistics
from typing import List, Dict, Any, Optional
from collections import Counter, defaultdict
import string

from .models import HashType, HashInfo
from .identifier import HashIdentifier
from .exceptions import HashKitError


class HashAnalyzer:
    """
    Advanced hash analysis and statistics
    """
    
    def __init__(self):
        self.identifier = HashIdentifier()
    
    def analyze_hash_file(self, filepath: str) -> Dict[str, Any]:
        """
        Analyze a file containing multiple hashes
        
        Args:
            filepath: Path to hash file
            
        Returns:
            Analysis results
        """
        if not filepath:
            raise HashKitError("File path cannot be empty")
        
        analysis = {
            'total_hashes': 0,
            'unique_hashes': 0,
            'hash_types': defaultdict(int),
            'charset_analysis': {},
            'length_distribution': defaultdict(int),
            'entropy_stats': {},
            'duplicates': [],
            'invalid_hashes': [],
            'samples': {}
        }
        
        hashes = []
        hash_set = set()
        duplicate_tracker = defaultdict(list)
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    hash_value = line.strip()
                    if not hash_value:
                        continue
                    
                    analysis['total_hashes'] += 1
                    hashes.append(hash_value)
                    
                    # Track duplicates
                    duplicate_tracker[hash_value].append(line_num)
                    if hash_value not in hash_set:
                        hash_set.add(hash_value)
                        analysis['unique_hashes'] += 1
                    
                    # Length distribution
                    analysis['length_distribution'][len(hash_value)] += 1
                    
                    # Identify hash type
                    try:
                        hash_info = self.identifier.identify(hash_value)
                        analysis['hash_types'][hash_info.hash_type.value] += 1
                        
                        # Store samples
                        if hash_info.hash_type.value not in analysis['samples']:
                            analysis['samples'][hash_info.hash_type.value] = []
                        if len(analysis['samples'][hash_info.hash_type.value]) < 5:
                            analysis['samples'][hash_info.hash_type.value].append(hash_value)
                    except Exception:
                        analysis['invalid_hashes'].append({
                            'line': line_num,
                            'hash': hash_value,
                            'reason': 'Identification failed'
                        })
        
        except Exception as e:
            raise HashKitError(f"Error reading hash file: {e}")
        
        # Find duplicates
        for hash_value, line_numbers in duplicate_tracker.items():
            if len(line_numbers) > 1:
                analysis['duplicates'].append({
                    'hash': hash_value,
                    'occurrences': len(line_numbers),
                    'lines': line_numbers
                })
        
        # Charset analysis
        analysis['charset_analysis'] = self._analyze_charset(hashes)
        
        # Entropy statistics
        analysis['entropy_stats'] = self._calculate_entropy_stats(hashes)
        
        return analysis
    
    def compare_hashes(self, hash1: str, hash2: str) -> Dict[str, Any]:
        """Compare two hashes for similarity"""
        comparison = {
            'hash1': hash1,
            'hash2': hash2,
            'identical': hash1 == hash2,
            'length_diff': abs(len(hash1) - len(hash2)),
            'hamming_distance': self._hamming_distance(hash1, hash2),
            'common_chars': len(set(hash1) & set(hash2)),
            'type1': None,
            'type2': None,
            'same_type': False
        }
        
        # Identify types
        try:
            info1 = self.identifier.identify(hash1)
            info2 = self.identifier.identify(hash2)
            comparison['type1'] = info1.hash_type.value
            comparison['type2'] = info2.hash_type.value
            comparison['same_type'] = info1.hash_type == info2.hash_type
        except Exception:
            pass
        
        return comparison
    
    def find_hash_patterns(self, hashes: List[str]) -> Dict[str, Any]:
        """Find patterns in hash lists"""
        patterns = {
            'common_prefixes': defaultdict(int),
            'common_suffixes': defaultdict(int),
            'repeating_chars': defaultdict(int),
            'charset_patterns': defaultdict(int),
            'length_patterns': defaultdict(int)
        }
        
        for hash_value in hashes:
            # Length patterns
            patterns['length_patterns'][len(hash_value)] += 1
            
            # Prefix/suffix patterns (first/last 4 chars)
            if len(hash_value) >= 4:
                patterns['common_prefixes'][hash_value[:4]] += 1
                patterns['common_suffixes'][hash_value[-4:]] += 1
            
            # Repeating character patterns
            for i in range(len(hash_value) - 1):
                if hash_value[i] == hash_value[i + 1]:
                    patterns['repeating_chars'][hash_value[i]] += 1
            
            # Charset patterns
            charset = self._classify_charset(hash_value)
            patterns['charset_patterns'][charset] += 1
        
        # Convert to regular dicts and sort by frequency
        result = {}
        for key, value in patterns.items():
            sorted_items = sorted(value.items(), key=lambda x: x[1], reverse=True)
            result[key] = dict(sorted_items[:10])  # Top 10
        
        return result
    
    def calculate_crack_difficulty(self, hash_info: HashInfo) -> Dict[str, Any]:
        """Estimate crack difficulty for a hash"""
        difficulty = {
            'hash_type': hash_info.hash_type.value,
            'keyspace_size': 0,
            'estimated_time': {},
            'difficulty_score': 0,
            'recommendations': []
        }
        
        # Base difficulty by hash type
        type_difficulty = {
            HashType.MD5: 1,
            HashType.SHA1: 2,
            HashType.SHA256: 3,
            HashType.SHA512: 4,
            HashType.NTLM: 1,
            HashType.BCRYPT: 8,
            HashType.SCRYPT: 9,
            HashType.ARGON2: 10,
            HashType.PBKDF2: 7
        }
        
        base_score = type_difficulty.get(hash_info.hash_type, 5)
        
        # Analyze entropy
        entropy = self._calculate_hash_entropy(hash_info.hash_value)
        
        # Estimate keyspace based on length and charset
        if hash_info.charset == "hex_lower":
            charset_size = 16
        elif hash_info.charset == "hex_mixed":
            charset_size = 16
        elif hash_info.charset == "base64":
            charset_size = 64
        else:
            charset_size = 95  # Full ASCII
        
        # This is a rough approximation for the original password space
        estimated_password_length = hash_info.length // 8  # Very rough estimate
        keyspace = charset_size ** estimated_password_length
        
        difficulty['keyspace_size'] = keyspace
        difficulty['difficulty_score'] = base_score + (entropy / 10)
        
        # Time estimates (very rough, based on modern hardware)
        rates = {
            'cpu_single': 1e6,     # 1M hashes/sec
            'cpu_multi': 1e7,      # 10M hashes/sec
            'gpu_single': 1e9,     # 1B hashes/sec
            'gpu_cluster': 1e11    # 100B hashes/sec
        }
        
        for hardware, rate in rates.items():
            seconds = keyspace / rate
            difficulty['estimated_time'][hardware] = self._format_time(seconds)
        
        # Recommendations
        if base_score <= 2:
            difficulty['recommendations'].append("Weak hash - use dictionary attack first")
        if base_score <= 4:
            difficulty['recommendations'].append("Consider rule-based attacks")
        if entropy < 3.0:
            difficulty['recommendations'].append("Low entropy - may be simple password")
        if hash_info.hash_type in [HashType.BCRYPT, HashType.SCRYPT, HashType.ARGON2]:
            difficulty['recommendations'].append("Strong hash - focus on dictionary/rule attacks")
        
        return difficulty
    
    def _analyze_charset(self, hashes: List[str]) -> Dict[str, Any]:
        """Analyze character set usage in hashes"""
        charset_stats = {
            'hex_lower': 0,
            'hex_upper': 0,
            'hex_mixed': 0,
            'base64': 0,
            'mixed': 0,
            'char_frequency': defaultdict(int)
        }
        
        for hash_value in hashes:
            charset = self._classify_charset(hash_value)
            charset_stats[charset] += 1
            
            # Character frequency
            for char in hash_value:
                charset_stats['char_frequency'][char] += 1
        
        # Convert frequency dict to sorted list
        sorted_chars = sorted(charset_stats['char_frequency'].items(), 
                            key=lambda x: x[1], reverse=True)
        charset_stats['char_frequency'] = dict(sorted_chars[:20])  # Top 20
        
        return charset_stats
    
    def _classify_charset(self, hash_value: str) -> str:
        """Classify character set of a hash"""
        if all(c in '0123456789abcdef' for c in hash_value):
            return 'hex_lower'
        elif all(c in '0123456789ABCDEF' for c in hash_value):
            return 'hex_upper'
        elif all(c in '0123456789abcdefABCDEF' for c in hash_value):
            return 'hex_mixed'
        elif all(c in string.ascii_letters + string.digits + '+/=' for c in hash_value):
            return 'base64'
        else:
            return 'mixed'
    
    def _calculate_entropy_stats(self, hashes: List[str]) -> Dict[str, float]:
        """Calculate entropy statistics for hash list"""
        entropies = [self._calculate_hash_entropy(h) for h in hashes]
        
        if not entropies:
            return {}
        
        return {
            'min': min(entropies),
            'max': max(entropies),
            'mean': statistics.mean(entropies),
            'median': statistics.median(entropies),
            'stdev': statistics.stdev(entropies) if len(entropies) > 1 else 0
        }
    
    def _calculate_hash_entropy(self, hash_value: str) -> float:
        """Calculate Shannon entropy of a hash"""
        import math
        
        if not hash_value:
            return 0.0
        
        # Count character frequencies
        char_counts = Counter(hash_value)
        length = len(hash_value)
        
        # Calculate entropy using Shannon's formula
        entropy = 0.0
        for count in char_counts.values():
            probability = count / length
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def _hamming_distance(self, s1: str, s2: str) -> int:
        """Calculate Hamming distance between two strings"""
        if len(s1) != len(s2):
            return max(len(s1), len(s2))  # Maximum possible distance
        
        return sum(c1 != c2 for c1, c2 in zip(s1, s2))
    
    def _format_time(self, seconds: float) -> str:
        """Format time duration"""
        if seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.1f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.1f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.1f} days"
        else:
            return f"{seconds/31536000:.1f} years"