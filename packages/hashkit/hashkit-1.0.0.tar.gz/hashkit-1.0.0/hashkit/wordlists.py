"""
Wordlist management and generation
"""

import os
import gzip
import requests
from typing import List, Dict, Optional, Iterator
from pathlib import Path
import tempfile
import shutil
from urllib.parse import urlparse

from .exceptions import WordlistError


class WordlistManager:
    """
    Wordlist management system with download and caching capabilities
    """
    
    def __init__(self, cache_dir: Optional[str] = None):
        self.cache_dir = cache_dir or os.path.join(os.getcwd(), 'wordlists')
        self.ensure_cache_dir()
        
        # Popular wordlist URLs
        self.popular_wordlists = {
            'rockyou': 'https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt',
            'common-passwords': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt',
            'john': 'https://raw.githubusercontent.com/openwall/john/bleeding-jumbo/run/password.lst',
            'darkweb2017': 'https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Leaked-Databases/darkweb2017-top10000.txt',
        }
    
    def ensure_cache_dir(self):
        """Ensure cache directory exists"""
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def download_wordlist(self, name: str, force: bool = False) -> str:
        """
        Download a popular wordlist
        
        Args:
            name: Wordlist name (rockyou, common-passwords, etc.)
            force: Force re-download even if cached
            
        Returns:
            Path to downloaded wordlist
        """
        if name not in self.popular_wordlists:
            raise WordlistError(f"Unknown wordlist: {name}")
        
        url = self.popular_wordlists[name]
        filename = f"{name}.txt"
        local_path = os.path.join(self.cache_dir, filename)
        
        # Check if already cached
        if os.path.exists(local_path) and not force:
            return local_path
        
        print(f"Downloading {name} wordlist...")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Handle compressed files
            if url.endswith('.gz'):
                # Download to temp file first
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    for chunk in response.iter_content(chunk_size=8192):
                        temp_file.write(chunk)
                    temp_path = temp_file.name
                
                # Decompress
                with gzip.open(temp_path, 'rt', encoding='utf-8', errors='ignore') as gz_file:
                    with open(local_path, 'w', encoding='utf-8') as out_file:
                        shutil.copyfileobj(gz_file, out_file)
                
                os.unlink(temp_path)
            else:
                # Direct download
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            print(f"Downloaded to: {local_path}")
            return local_path
            
        except Exception as e:
            raise WordlistError(f"Failed to download {name}: {e}")
    
    def list_cached_wordlists(self) -> List[Dict[str, str]]:
        """List cached wordlists"""
        wordlists = []
        
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.txt'):
                path = os.path.join(self.cache_dir, filename)
                size = os.path.getsize(path)
                lines = self.count_lines(path)
                
                wordlists.append({
                    'name': filename[:-4],  # Remove .txt
                    'path': path,
                    'size': size,
                    'lines': lines
                })
        
        return wordlists
    
    def count_lines(self, filepath: str) -> int:
        """Count lines in a file efficiently"""
        try:
            with open(filepath, 'rb') as f:
                count = sum(1 for _ in f)
            return count
        except Exception:
            return 0
    
    def validate_wordlist(self, filepath: str) -> Dict[str, any]:
        """Validate and analyze a wordlist"""
        if not os.path.exists(filepath):
            raise WordlistError(f"Wordlist not found: {filepath}")
        
        stats = {
            'path': filepath,
            'exists': True,
            'readable': False,
            'lines': 0,
            'size': 0,
            'min_length': float('inf'),
            'max_length': 0,
            'avg_length': 0,
            'charset': set(),
            'sample_words': []
        }
        
        try:
            # Basic file info
            stats['size'] = os.path.getsize(filepath)
            
            # Analyze content
            total_length = 0
            sample_count = 0
            
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    word = line.strip()
                    if not word:
                        continue
                    
                    stats['lines'] += 1
                    word_len = len(word)
                    total_length += word_len
                    
                    stats['min_length'] = min(stats['min_length'], word_len)
                    stats['max_length'] = max(stats['max_length'], word_len)
                    stats['charset'].update(word)
                    
                    # Sample first 10 words
                    if sample_count < 10:
                        stats['sample_words'].append(word)
                        sample_count += 1
            
            stats['readable'] = True
            stats['avg_length'] = total_length / stats['lines'] if stats['lines'] > 0 else 0
            stats['charset'] = ''.join(sorted(stats['charset']))
            
            # Fix min_length if no words found
            if stats['min_length'] == float('inf'):
                stats['min_length'] = 0
                
        except Exception as e:
            stats['error'] = str(e)
        
        return stats
    
    def generate_custom_wordlist(self, 
                                base_words: List[str],
                                rules: Optional[List[str]] = None,
                                output_path: Optional[str] = None) -> str:
        """Generate custom wordlist from base words and rules"""
        if not base_words:
            raise WordlistError("Base words cannot be empty")
        
        if not rules:
            rules = [':', 'l', 'u', 'c', '$1', '$2', '$3', '$!']  # Default rules
        
        if not output_path:
            output_path = os.path.join(self.cache_dir, 'custom_wordlist.txt')
        
        generated_words = set()
        
        # Apply rules to base words
        for word in base_words:
            for rule in rules:
                modified_words = self._apply_rule(word, rule)
                generated_words.update(modified_words)
        
        # Write to file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for word in sorted(generated_words):
                    f.write(f"{word}\n")
            
            return output_path
        except Exception as e:
            raise WordlistError(f"Failed to generate wordlist: {e}")
    
    def _apply_rule(self, word: str, rule: str) -> List[str]:
        """Apply transformation rule to word"""
        results = []
        
        if rule == ':':
            results.append(word)
        elif rule == 'l':
            results.append(word.lower())
        elif rule == 'u':
            results.append(word.upper())
        elif rule == 'c':
            results.append(word.capitalize())
        elif rule == 'r':
            results.append(word[::-1])
        elif rule.startswith('$'):
            results.append(word + rule[1:])
        elif rule.startswith('^'):
            results.append(rule[1:] + word)
        
        return results
    
    def merge_wordlists(self, paths: List[str], output_path: str, remove_duplicates: bool = True):
        """Merge multiple wordlists"""
        if not paths:
            raise WordlistError("No wordlists to merge")
        
        words = set() if remove_duplicates else []
        
        for path in paths:
            if not os.path.exists(path):
                raise WordlistError(f"Wordlist not found: {path}")
            
            try:
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        word = line.strip()
                        if word:
                            if remove_duplicates:
                                words.add(word)
                            else:
                                words.append(word)
            except Exception as e:
                raise WordlistError(f"Error reading {path}: {e}")
        
        # Write merged wordlist
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                if remove_duplicates:
                    for word in sorted(words):
                        f.write(f"{word}\n")
                else:
                    for word in words:
                        f.write(f"{word}\n")
        except Exception as e:
            raise WordlistError(f"Error writing merged wordlist: {e}")
    
    def clear_cache(self) -> Dict[str, any]:
        """Clear all cached wordlists"""
        if not os.path.exists(self.cache_dir):
            return {
                'deleted_files': 0,
                'freed_space': 0,
                'message': 'Wordlists directory does not exist'
            }
        
        deleted_files = 0
        freed_space = 0
        
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.txt'):
                    file_path = os.path.join(self.cache_dir, filename)
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    deleted_files += 1
                    freed_space += file_size
            
            # Remove directory if empty
            if not os.listdir(self.cache_dir):
                os.rmdir(self.cache_dir)
            
            return {
                'deleted_files': deleted_files,
                'freed_space': freed_space,
                'message': f'Cleared {deleted_files} wordlists, freed {freed_space:,} bytes'
            }
            
        except Exception as e:
            raise WordlistError(f"Failed to clear cache: {e}")