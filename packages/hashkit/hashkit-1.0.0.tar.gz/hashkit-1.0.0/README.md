# HashKit - Hash Analysis and Cracking Tool

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security: Ethical Use Only](https://img.shields.io/badge/Security-Ethical%20Use%20Only-red.svg)](#legal-disclaimer)

## ⚠️ LEGAL DISCLAIMER ⚠️

**FOR AUTHORIZED SECURITY TESTING ONLY**

This tool is designed exclusively for:
- **Authorized penetration testing** with written permission
- **Digital forensics** and incident response
- **Educational purposes** in controlled environments  
- **Security research** with proper authorization
- **Password policy compliance** testing
- **Bug bounty programs** with proper scope

**UNAUTHORIZED PASSWORD CRACKING IS ILLEGAL AND UNETHICAL.**

Users are responsible for complying with all applicable laws and regulations. The authors assume no responsibility for misuse of this tool.

## Features

### 🔍 Hash Identification
- **Advanced identification engine** with confidence scoring
- **20+ hash types** including MD5, SHA family, NTLM, bcrypt, scrypt, Argon2
- **Entropy analysis** and pattern recognition
- **Batch processing** for multiple hashes
- **Format validation** and charset analysis

### ⚔️ Multiple Attack Modes
- **Dictionary attacks** with threading support
- **Rule-based attacks** with custom rule sets
- **Brute force attacks** with configurable charset
- **Mask attacks** with pattern support (?l?u?d?s)
- **Hybrid attacks** combining multiple methods
- **Combinator attacks** for wordlist combinations

### 📊 Advanced Analytics
- **Statistical analysis** of hash collections
- **Entropy calculations** and randomness testing
- **Pattern detection** in hash sets
- **Crack difficulty estimation** with time predictions
- **Performance benchmarking** of hash functions

### 📋 Wordlist Management
- **Automatic downloads** of popular wordlists (rockyou, SecLists, etc.)
- **Local storage** in project wordlists/ folder
- **Auto-detection** of available wordlists for cracking
- **Wordlist validation** and statistics
- **Custom wordlist generation** with rules
- **Wordlist merging** and deduplication
- **Clear command** for easy cleanup

### 🖥️ Professional CLI
- **Intuitive command structure** with subcommands
- **Colored output** for better readability
- **Progress tracking** with real-time statistics
- **Detailed reporting** with JSON export
- **Configurable threading** for performance tuning

## Installation

### From PyPI (Recommended)
```bash
pip install hashkit
```

### From Source
```bash
git clone https://github.com/abderrahimghazali/hashkit.git
cd hashkit
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/abderrahimghazali/hashkit.git
cd hashkit
pip install -e ".[dev]"
```

## Quick Start

### Hash Identification
```bash
# Identify a single hash
hashkit identify 5d41402abc4b2a76b9719d911017c592

# Verbose identification with details
hashkit identify -v aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
```

### Hash Cracking
```bash
# Auto-detect wordlist from local wordlists/ folder
hashkit crack 5d41402abc4b2a76b9719d911017c592

# Dictionary attack with specific wordlist
hashkit crack 5d41402abc4b2a76b9719d911017c592 -w rockyou.txt

# Specify hash type and attack mode
hashkit crack -t md5 -m dictionary -w wordlist.txt -threads 8 hash_value

# Rule-based attack
hashkit crack hash_value -w wordlist.txt -m rule_based

# Brute force attack (short hashes only)
hashkit crack hash_value -m bruteforce --max-length 4

# Mask attack
hashkit crack hash_value -m mask --mask "?l?l?l?d?d"
```

### Hash Analysis
```bash
# Analyze hash file
hashkit analyze hashes.txt

# Generate detailed report
hashkit analyze hashes.txt -o analysis_report.json

# Estimate crack difficulty
hashkit difficulty 5d41402abc4b2a76b9719d911017c592
```

### Wordlist Management
```bash
# List cached wordlists (stored in local wordlists/ folder)
hashkit wordlist list

# Download popular wordlists to local wordlists/ folder
hashkit wordlist download rockyou
hashkit wordlist download common-passwords
hashkit wordlist download john
hashkit wordlist download darkweb2017

# Clear all cached wordlists
hashkit wordlist clear

# Validate wordlist
hashkit wordlist validate /path/to/wordlist.txt
```

## Supported Hash Types

| Hash Type | Length | Security | Use Cases |
|-----------|--------|----------|-----------|
| MD5 | 32 | ❌ Broken | Legacy systems, checksums |
| SHA1 | 40 | ⚠️ Deprecated | Git (legacy), old systems |
| SHA224 | 56 | ✅ Secure | General purpose |
| SHA256 | 64 | ✅ Secure | Cryptocurrency, modern apps |
| SHA384 | 96 | ✅ Secure | High security applications |
| SHA512 | 128 | ✅ Secure | Password hashing, security |
| SHA3-* | Variable | ✅ Secure | Next-gen applications |
| BLAKE2b/s | Variable | ✅ Secure | High performance hashing |
| NTLM | 32 | ❌ Weak | Windows authentication |
| bcrypt | Variable | ✅ Very Secure | Password storage |
| scrypt | Variable | ✅ Very Secure | Password storage |
| Argon2 | Variable | ✅ Very Secure | Modern password storage |
| PBKDF2 | Variable | ✅ Secure | Key derivation |

## Attack Modes

### Dictionary Attack
Uses wordlists to test common passwords:
```bash
# Auto-detect wordlist from wordlists/ folder
hashkit crack hash_value

# Use specific wordlist
hashkit crack hash_value -w rockyou.txt -m dictionary
```

### Rule-Based Attack
Applies transformation rules to wordlist entries:
```bash
hashkit crack hash_value -w wordlist.txt -m rule_based
```

Common rules:
- `:` - No change
- `l` - Lowercase
- `u` - Uppercase  
- `c` - Capitalize
- `r` - Reverse
- `$1` - Append "1"
- `^@` - Prepend "@"

### Brute Force Attack
Tests all possible combinations up to specified length:
```bash
hashkit crack hash_value -m bruteforce --max-length 6
```

### Mask Attack
Uses patterns to generate candidates:
```bash
hashkit crack hash_value -m mask --mask "?u?l?l?l?d?d"
```

Mask characters:
- `?l` - Lowercase letter (a-z)
- `?u` - Uppercase letter (A-Z)
- `?d` - Digit (0-9)
- `?s` - Symbol (!@#$%...)

### Hybrid Attack
Combines multiple attack methods automatically:
```bash
hashkit crack hash_value -w wordlist.txt -m hybrid
```

## Wordlist Storage

HashKit stores wordlists locally in the project directory:

### Local Storage Structure
```
hashkit/
├── wordlists/           # Auto-created wordlist storage
│   ├── rockyou.txt     # Downloaded wordlists
│   ├── john.txt
│   └── custom.txt      # Your personal wordlists
├── hashkit/            # Source code
└── README.md
```

### Auto-Detection Priority
When no `-w` option is specified, HashKit automatically searches the `wordlists/` folder:

1. **rockyou** (preferred - 14M+ passwords)
2. **common-passwords** (1M most common)
3. **john** (John the Ripper default)
4. **darkweb2017** (10K from breaches)
5. **Largest available** (if none of above found)

### Benefits
- ✅ **Project-local**: Wordlists travel with your project
- ✅ **Version control**: Add to .gitignore to avoid committing large files  
- ✅ **Auto-detection**: No need to specify `-w` for common use cases
- ✅ **Easy cleanup**: `hashkit wordlist clear` removes all cached wordlists

## Configuration

HashKit supports configuration through:
- Command-line arguments
- Environment variables
- Configuration files

### Environment Variables
```bash
export HASHKIT_CACHE_DIR="/custom/cache/path"
export HASHKIT_DEFAULT_THREADS=8
export HASHKIT_MAX_WORDLIST_SIZE=1000000000
```

## Performance Tuning

### Threading
Adjust thread count based on your system:
```bash
# Use all CPU cores
hashkit crack hash_value -w wordlist.txt --threads $(nproc)

# Conservative threading
hashkit crack hash_value -w wordlist.txt --threads 4
```

### Memory Management
For large wordlists, HashKit uses chunked processing to manage memory efficiently.

### GPU Acceleration (Optional)
Install GPU acceleration support:
```bash
pip install "hashkit[gpu]"
```

## Security Considerations

### Responsible Use
- ✅ Only use on systems you own or have explicit permission to test
- ✅ Follow responsible disclosure for vulnerabilities
- ✅ Respect rate limits and system resources
- ✅ Document authorization and scope
- ❌ Never use for unauthorized access
- ❌ Never crack passwords without permission
- ❌ Never use for malicious purposes

### Operational Security
- Use dedicated testing environments
- Secure storage of wordlists and results
- Regular updates of hash databases
- Proper logging and audit trails

## Development

### Contributing
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality  
4. Ensure all tests pass
5. Submit a pull request

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=hashkit

# Run specific test categories
pytest tests/test_identifier.py
pytest tests/test_cracker.py
```

### Code Style
```bash
# Format code
black hashkit/

# Sort imports
isort hashkit/

# Lint code
flake8 hashkit/

# Type checking
mypy hashkit/
```

## Troubleshooting

### Common Issues

**"Wordlist not found" or "No wordlists available"**
```bash
# Download popular wordlists to local wordlists/ folder
hashkit wordlist download rockyou
hashkit wordlist download john
hashkit wordlist download common-passwords

# List available wordlists
hashkit wordlist list
```

**"Hash type not identified"**
```bash
# Use verbose mode for details
hashkit identify -v your_hash_here
```

**"Low performance"**
```bash
# Increase thread count
hashkit crack hash_value -w wordlist.txt --threads 8

# Use smaller wordlists for testing
```

**"Memory issues with large wordlists"**
HashKit automatically chunks large wordlists. If issues persist, use smaller wordlists or increase available RAM.

### Debug Mode
```bash
# Enable debug logging
export HASHKIT_DEBUG=1
hashkit crack hash_value -w wordlist.txt
```

## Credits

- **SecLists** - Comprehensive security wordlists
- **John the Ripper** - Password cracking inspiration  
- **Hashcat** - Advanced cracking techniques
- **OWASP** - Security best practices

## Support

- 📖 **Documentation**: [docs/](docs/)
- 🐛 **Issues**: [GitHub Issues](https://github.com/abderrahimghazali/hashkit/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/abderrahimghazali/hashkit/discussions)

---

**Remember: With great power comes great responsibility. Use HashKit ethically and legally.**
