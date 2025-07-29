"""
Hash cracking engine with multiple attack modes
"""

import hashlib
import hmac
import time
import threading
from typing import Optional, List, Dict, Iterator, Callable, Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import os
import signal

from .models import HashType, HashInfo, CrackResult, AttackMode, CrackStatus, CrackingSession
from .identifier import HashIdentifier
from .wordlists import WordlistManager
from .exceptions import CrackingError
from .utils import get_hasher, calculate_entropy


class HashCracker:
    """
    Professional hash cracking engine supporting multiple attack modes
    """
    
    def __init__(self, threads: int = 4, chunk_size: int = 1000):
        self.identifier = HashIdentifier()
        self.wordlist_manager = WordlistManager()
        self.threads = threads
        self.chunk_size = chunk_size
        self.running = False
        self.session = None
        self._stop_event = threading.Event()
        
        # Statistics
        self.total_attempts = 0
        self.start_time = None
        self.results = []
        
    def crack_hash(self, 
                   hash_value: str,
                   attack_mode: AttackMode = AttackMode.DICTIONARY,
                   wordlist_path: Optional[str] = None,
                   hash_type: Optional[HashType] = None,
                   rules: Optional[List[str]] = None,
                   mask: Optional[str] = None,
                   max_length: int = 8,
                   callback: Optional[Callable] = None) -> CrackResult:
        """
        Crack a single hash using specified attack mode
        
        Args:
            hash_value: Hash to crack
            attack_mode: Attack mode to use
            wordlist_path: Path to wordlist file
            hash_type: Hash type (auto-detect if None)
            rules: Rule set for rule-based attacks
            mask: Mask for mask attacks (?l?u?d?s)
            max_length: Maximum length for brute force
            callback: Progress callback function
            
        Returns:
            CrackResult object
        """
        if not hash_value:
            raise CrackingError("Hash value cannot be empty")
        
        # Identify hash type if not provided
        if not hash_type:
            hash_info = self.identifier.identify(hash_value)
            if hash_info.hash_type == HashType.UNKNOWN:
                raise CrackingError(f"Could not identify hash type: {hash_value}")
            hash_type = hash_info.hash_type
        
        # Initialize result
        result = CrackResult(
            hash_value=hash_value,
            plaintext=None,
            attack_mode=attack_mode,
            status=CrackStatus.RUNNING,
            attempts=0,
            duration=0.0,
            cracked_at=None,
            wordlist_used=wordlist_path,
            rule_used=None
        )
        
        self.start_time = time.time()
        self.running = True
        self._stop_event.clear()
        
        try:
            # Get hasher function
            hasher = get_hasher(hash_type)
            
            # Execute attack based on mode
            if attack_mode == AttackMode.DICTIONARY:
                plaintext = self._dictionary_attack(hash_value, hasher, wordlist_path, callback)
            elif attack_mode == AttackMode.BRUTEFORCE:
                plaintext = self._bruteforce_attack(hash_value, hasher, max_length, callback)
            elif attack_mode == AttackMode.RULE_BASED:
                plaintext = self._rule_based_attack(hash_value, hasher, wordlist_path, rules, callback)
            elif attack_mode == AttackMode.MASK:
                plaintext = self._mask_attack(hash_value, hasher, mask, callback)
            elif attack_mode == AttackMode.HYBRID:
                plaintext = self._hybrid_attack(hash_value, hasher, wordlist_path, callback)
            else:
                raise CrackingError(f"Unsupported attack mode: {attack_mode}")
            
            # Update result
            result.plaintext = plaintext
            result.status = CrackStatus.CRACKED if plaintext else CrackStatus.EXHAUSTED
            result.attempts = self.total_attempts
            result.duration = time.time() - self.start_time
            result.cracked_at = datetime.now() if plaintext else None
            
        except KeyboardInterrupt:
            result.status = CrackStatus.STOPPED
        except Exception as e:
            result.status = CrackStatus.ERROR
            raise CrackingError(f"Cracking failed: {e}")
        finally:
            self.running = False
        
        return result
    
    def _dictionary_attack(self, 
                          hash_value: str, 
                          hasher: Callable,
                          wordlist_path: str,
                          callback: Optional[Callable] = None) -> Optional[str]:
        """Dictionary attack implementation"""
        if not wordlist_path or not os.path.exists(wordlist_path):
            raise CrackingError(f"Wordlist not found: {wordlist_path}")
        
        # Use ThreadPoolExecutor for parallel processing
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            # Read wordlist in chunks
            for chunk in self._read_wordlist_chunks(wordlist_path):
                if self._stop_event.is_set():
                    break
                
                # Submit chunk to thread pool
                futures = []
                for word_batch in self._split_chunk(chunk, self.threads):
                    future = executor.submit(self._test_words, hash_value, hasher, word_batch)
                    futures.append(future)
                
                # Check results
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        return result
                    
                    # Update progress
                    if callback:
                        callback(self.total_attempts)
        
        return None
    
    def _bruteforce_attack(self,
                          hash_value: str,
                          hasher: Callable,
                          max_length: int,
                          callback: Optional[Callable] = None) -> Optional[str]:
        """Brute force attack implementation"""
        charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        for length in range(1, max_length + 1):
            if self._stop_event.is_set():
                break
                
            for candidate in self._generate_candidates(charset, length):
                if self._stop_event.is_set():
                    break
                
                self.total_attempts += 1
                
                if hasher(candidate) == hash_value.lower():
                    return candidate
                
                if callback and self.total_attempts % 1000 == 0:
                    callback(self.total_attempts)
        
        return None
    
    def _rule_based_attack(self,
                          hash_value: str,
                          hasher: Callable,
                          wordlist_path: str,
                          rules: List[str],
                          callback: Optional[Callable] = None) -> Optional[str]:
        """Rule-based attack implementation"""
        if not rules:
            rules = self._get_default_rules()
        
        for chunk in self._read_wordlist_chunks(wordlist_path):
            if self._stop_event.is_set():
                break
            
            for word in chunk:
                if self._stop_event.is_set():
                    break
                
                # Apply rules to generate candidates
                for rule in rules:
                    candidates = self._apply_rule(word.strip(), rule)
                    
                    for candidate in candidates:
                        self.total_attempts += 1
                        
                        if hasher(candidate) == hash_value.lower():
                            return candidate
                        
                        if callback and self.total_attempts % 1000 == 0:
                            callback(self.total_attempts)
        
        return None
    
    def _mask_attack(self,
                    hash_value: str,
                    hasher: Callable,
                    mask: str,
                    callback: Optional[Callable] = None) -> Optional[str]:
        """Mask attack implementation (?l=lowercase, ?u=uppercase, ?d=digit, ?s=symbol)"""
        if not mask:
            raise CrackingError("Mask cannot be empty")
        
        # Parse mask
        charset_map = {
            '?l': 'abcdefghijklmnopqrstuvwxyz',
            '?u': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            '?d': '0123456789',
            '?s': '!@#$%^&*()_+-=[]{}|;:,.<>?'
        }
        
        # Generate candidates based on mask
        for candidate in self._generate_mask_candidates(mask, charset_map):
            if self._stop_event.is_set():
                break
            
            self.total_attempts += 1
            
            if hasher(candidate) == hash_value.lower():
                return candidate
            
            if callback and self.total_attempts % 1000 == 0:
                callback(self.total_attempts)
        
        return None
    
    def _hybrid_attack(self,
                      hash_value: str,
                      hasher: Callable,
                      wordlist_path: str,
                      callback: Optional[Callable] = None) -> Optional[str]:
        """Hybrid attack combining dictionary + rules + common modifications"""
        # Try dictionary first
        result = self._dictionary_attack(hash_value, hasher, wordlist_path, callback)
        if result:
            return result
        
        # Try rule-based
        common_rules = [':', 'l', 'u', 'c', 'r', '$1', '$2', '$3', '^1', '^2']
        result = self._rule_based_attack(hash_value, hasher, wordlist_path, common_rules, callback)
        if result:
            return result
        
        # Try common masks for short passwords
        common_masks = ['?l?l?l?l?d?d', '?u?l?l?l?d?d', '?l?l?l?l?l?d']
        for mask in common_masks:
            if self._stop_event.is_set():
                break
            result = self._mask_attack(hash_value, hasher, mask, callback)
            if result:
                return result
        
        return None
    
    def _read_wordlist_chunks(self, wordlist_path: str) -> Generator[List[str], None, None]:
        """Read wordlist in chunks for memory efficiency"""
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                chunk = []
                for line in f:
                    word = line.strip()
                    if word:
                        chunk.append(word)
                        if len(chunk) >= self.chunk_size:
                            yield chunk
                            chunk = []
                
                if chunk:  # Yield remaining words
                    yield chunk
        except Exception as e:
            raise CrackingError(f"Error reading wordlist: {e}")
    
    def _split_chunk(self, chunk: List[str], num_splits: int) -> List[List[str]]:
        """Split chunk into smaller batches for threading"""
        chunk_size = len(chunk) // num_splits + 1
        return [chunk[i:i + chunk_size] for i in range(0, len(chunk), chunk_size)]
    
    def _test_words(self, hash_value: str, hasher: Callable, words: List[str]) -> Optional[str]:
        """Test a batch of words"""
        for word in words:
            if self._stop_event.is_set():
                break
            
            self.total_attempts += 1
            
            if hasher(word) == hash_value.lower():
                return word
        
        return None
    
    def _generate_candidates(self, charset: str, length: int) -> Generator[str, None, None]:
        """Generate brute force candidates"""
        if length == 1:
            for char in charset:
                yield char
        else:
            for char in charset:
                for rest in self._generate_candidates(charset, length - 1):
                    yield char + rest
    
    def _generate_mask_candidates(self, mask: str, charset_map: Dict[str, str]) -> Generator[str, None, None]:
        """Generate candidates based on mask pattern"""
        # Parse mask into positions
        positions = []
        i = 0
        while i < len(mask):
            if i < len(mask) - 1 and mask[i:i+2] in charset_map:
                positions.append(charset_map[mask[i:i+2]])
                i += 2
            else:
                positions.append(mask[i])  # Literal character
                i += 1
        
        # Generate all combinations
        def generate_recursive(pos: int, current: str):
            if pos >= len(positions):
                yield current
            else:
                charset = positions[pos]
                if len(charset) == 1:  # Literal character
                    yield from generate_recursive(pos + 1, current + charset)
                else:  # Character set
                    for char in charset:
                        yield from generate_recursive(pos + 1, current + char)
        
        yield from generate_recursive(0, "")
    
    def _get_default_rules(self) -> List[str]:
        """Get default rule set for rule-based attacks"""
        return [
            ':',      # No change
            'l',      # Lowercase
            'u',      # Uppercase  
            'c',      # Capitalize
            'r',      # Reverse
            '$1',     # Append 1
            '$2',     # Append 2
            '$3',     # Append 3
            '$!',     # Append !
            '^1',     # Prepend 1
            '^2',     # Prepend 2
            'l$1',    # Lowercase + append 1
            'c$1',    # Capitalize + append 1
            'l$!',    # Lowercase + append !
            'r$1',    # Reverse + append 1
        ]
    
    def _apply_rule(self, word: str, rule: str) -> List[str]:
        """Apply a single rule to a word"""
        candidates = []
        
        if rule == ':':
            candidates.append(word)
        elif rule == 'l':
            candidates.append(word.lower())
        elif rule == 'u':
            candidates.append(word.upper())
        elif rule == 'c':
            candidates.append(word.capitalize())
        elif rule == 'r':
            candidates.append(word[::-1])
        elif rule.startswith('$'):
            candidates.append(word + rule[1:])
        elif rule.startswith('^'):
            candidates.append(rule[1:] + word)
        elif 'l$' in rule:
            suffix = rule.split('$')[1]
            candidates.append(word.lower() + suffix)
        elif 'c$' in rule:
            suffix = rule.split('$')[1]
            candidates.append(word.capitalize() + suffix)
        elif 'r$' in rule:
            suffix = rule.split('$')[1]
            candidates.append(word[::-1] + suffix)
        
        return candidates
    
    def stop(self):
        """Stop the cracking process"""
        self._stop_event.set()
        self.running = False