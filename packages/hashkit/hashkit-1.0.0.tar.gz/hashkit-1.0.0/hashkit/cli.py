"""
Command-line interface for HashKit
"""

import click
import os
import sys
from typing import Optional, List
from tabulate import tabulate
from colorama import Fore, Style, init

from . import __version__, LEGAL_DISCLAIMER
from .models import HashType, AttackMode
from .identifier import HashIdentifier
from .cracker import HashCracker
from .analyzer import HashAnalyzer
from .wordlists import WordlistManager
from .exceptions import HashKitError

# Initialize colorama
init(autoreset=True)


def print_banner():
    """Print HashKit banner"""
    banner = f"{Fore.MAGENTA}HashKit v{__version__}{Style.RESET_ALL}"
    print(banner)


def print_error(message: str):
    """Print error message"""
    click.echo(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}", err=True)


def print_success(message: str):
    """Print success message"""
    click.echo(f"{Fore.GREEN}[SUCCESS] {message}{Style.RESET_ALL}")


def print_warning(message: str):
    """Print warning message"""
    click.echo(f"{Fore.YELLOW}[WARNING] {message}{Style.RESET_ALL}")


def print_info(message: str):
    """Print info message"""
    click.echo(f"{Fore.BLUE}[INFO] {message}{Style.RESET_ALL}")


class HashKitGroup(click.Group):
    """Custom group class to show banner on help"""
    
    def get_help(self, ctx):
        """Override to show banner before help"""
        if not ctx.params.get('quiet', False):
            print_banner()
        return super().get_help(ctx)


@click.group(cls=HashKitGroup, invoke_without_command=True)
@click.version_option(version=__version__)
@click.option('--quiet', '-q', is_flag=True, help='Quiet mode')
@click.pass_context
def cli(ctx, quiet):
    """HashKit - Professional Hash Analysis and Cracking Tool"""
    if ctx.invoked_subcommand is None:
        # Show help when no command is provided (banner will be shown by get_help)
        print(ctx.get_help())


@cli.command()
@click.argument('hash_value')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def identify(hash_value, verbose):
    """Identify hash type"""
    try:
        identifier = HashIdentifier()
        hash_info = identifier.identify(hash_value)
        
        if verbose:
            print_info(f"Hash: {hash_info.hash_value}")
            print_info(f"Length: {hash_info.length}")
            print_info(f"Charset: {hash_info.charset}")
            print_info(f"Confidence: {hash_info.confidence:.1%}")
            
            if hash_info.possible_types:
                print_info("Possible types:")
                for ht in hash_info.possible_types:
                    print(f"  - {ht.value.upper()}")
        
        if hash_info.hash_type != HashType.UNKNOWN:
            print_success(f"Identified as: {hash_info.hash_type.value.upper()}")
        else:
            print_warning("Could not identify hash type")
            
    except Exception as e:
        print_error(f"Identification failed: {e}")
        sys.exit(1)


@cli.command()
@click.argument('hash_value')
@click.option('--wordlist', '-w', help='Wordlist file path (auto-detects from wordlists/ if not specified)')
@click.option('--type', '-t', 'hash_type', type=click.Choice([t.value for t in HashType]), 
              help='Hash type (auto-detect if not specified)')
@click.option('--mode', '-m', type=click.Choice([m.value for m in AttackMode]), 
              default='dictionary', help='Attack mode')
@click.option('--threads', default=4, help='Number of threads')
@click.option('--max-length', default=8, help='Maximum length for brute force')
@click.option('--mask', help='Mask for mask attack (?l?u?d?s)')
def crack(hash_value, wordlist, hash_type, mode, threads, max_length, mask):
    """Crack a hash
    
    If no wordlist is specified with -w, automatically uses wordlists from the local wordlists/ folder.
    
    Examples:
    hashkit crack 5d41402abc4b2a76b9719d911017c592                    # Auto-detect wordlist
    hashkit crack 5d41402abc4b2a76b9719d911017c592 -w custom.txt      # Use specific wordlist
    """
    try:
        # Convert string enums
        attack_mode = AttackMode(mode)
        hash_type_enum = HashType(hash_type) if hash_type else None
        
        # Handle automatic wordlist detection
        if not wordlist:
            manager = WordlistManager()
            available_wordlists = manager.list_cached_wordlists()
            
            if not available_wordlists:
                print_error("No wordlists available")
                print_info("Download wordlists using:")
                print("  hashkit wordlist download rockyou")
                print("  hashkit wordlist download john")
                print("  hashkit wordlist download common-passwords")
                return
            
            # Prefer rockyou if available, otherwise use the largest wordlist
            preferred_names = ['rockyou', 'common-passwords', 'john', 'darkweb2017']
            chosen_wordlist = None
            
            # Try to find preferred wordlists in order
            for pref_name in preferred_names:
                for wl in available_wordlists:
                    if wl['name'] == pref_name:
                        chosen_wordlist = wl
                        break
                if chosen_wordlist:
                    break
            
            # If no preferred wordlist found, use the largest one
            if not chosen_wordlist:
                chosen_wordlist = max(available_wordlists, key=lambda x: x['lines'])
            
            wordlist = chosen_wordlist['path']
            print_info(f"Auto-selected wordlist: {chosen_wordlist['name']} ({chosen_wordlist['lines']:,} words)")
        
        # Initialize cracker
        cracker = HashCracker(threads=threads)
        
        # Progress callback
        def progress_callback(attempts):
            if attempts % 10000 == 0:
                print(f"\r{Fore.YELLOW}Attempts: {attempts:,}{Style.RESET_ALL}", end='')
        
        print_info(f"Starting {attack_mode.value} attack...")
        print_info(f"Target: {hash_value}")
        print_info(f"Wordlist: {wordlist}")
        print_info(f"Threads: {threads}")
        
        # Crack hash
        result = cracker.crack_hash(
            hash_value=hash_value,
            attack_mode=attack_mode,
            wordlist_path=wordlist,
            hash_type=hash_type_enum,
            max_length=max_length,
            mask=mask,
            callback=progress_callback
        )
        
        print()  # New line after progress
        
        # Display results
        if result.success:
            print_success(f"Hash cracked: {result.plaintext}")
        else:
            print_warning(f"Hash not cracked ({result.status.value})")
        
        print_info(f"Attempts: {result.attempts:,}")
        print_info(f"Duration: {result.duration:.2f} seconds")
        print_info(f"Rate: {result.rate:.0f} hashes/sec")
        
    except KeyboardInterrupt:
        print_warning("\nCracking interrupted by user")
    except Exception as e:
        print_error(f"Cracking failed: {e}")
        sys.exit(1)


@cli.command()
@click.argument('file_path')
@click.option('--output', '-o', help='Output file for analysis report')
def analyze(file_path, output):
    """Analyze hash file"""
    try:
        analyzer = HashAnalyzer()
        analysis = analyzer.analyze_hash_file(file_path)
        
        # Display summary
        print_info(f"Hash File Analysis: {file_path}")
        print(f"Total hashes: {analysis['total_hashes']:,}")
        print(f"Unique hashes: {analysis['unique_hashes']:,}")
        print(f"Duplicates: {len(analysis['duplicates'])}")
        print(f"Invalid hashes: {len(analysis['invalid_hashes'])}")
        
        # Hash types
        if analysis['hash_types']:
            print("\nHash Types:")
            table_data = []
            for hash_type, count in analysis['hash_types'].items():
                percentage = (count / analysis['total_hashes']) * 100
                table_data.append([hash_type.upper(), count, f"{percentage:.1f}%"])
            
            print(tabulate(table_data, headers=['Type', 'Count', 'Percentage'], tablefmt='grid'))
        
        # Length distribution
        if analysis['length_distribution']:
            print("\nLength Distribution:")
            table_data = []
            for length, count in sorted(analysis['length_distribution'].items()):
                percentage = (count / analysis['total_hashes']) * 100
                table_data.append([length, count, f"{percentage:.1f}%"])
            
            print(tabulate(table_data, headers=['Length', 'Count', 'Percentage'], tablefmt='grid'))
        
        # Entropy stats
        if analysis['entropy_stats']:
            print(f"\nEntropy Statistics:")
            stats = analysis['entropy_stats']
            print(f"  Min: {stats['min']:.2f}")
            print(f"  Max: {stats['max']:.2f}")
            print(f"  Mean: {stats['mean']:.2f}")
            print(f"  Median: {stats['median']:.2f}")
            print(f"  Std Dev: {stats['stdev']:.2f}")
        
        # Save detailed report if requested
        if output:
            import json
            with open(output, 'w') as f:
                # Convert defaultdict to dict for JSON serialization
                json_analysis = {}
                for key, value in analysis.items():
                    if hasattr(value, 'default_factory'):
                        json_analysis[key] = dict(value)
                    else:
                        json_analysis[key] = value
                json.dump(json_analysis, f, indent=2, default=str)
            print_success(f"Detailed report saved to: {output}")
        
    except Exception as e:
        print_error(f"Analysis failed: {e}")
        sys.exit(1)


@cli.group()
def wordlist():
    """Wordlist management commands"""
    pass


@wordlist.command('list')
def list_wordlists():
    """List available wordlists"""
    try:
        manager = WordlistManager()
        wordlists = manager.list_cached_wordlists()
        
        if not wordlists:
            print_warning("No wordlists found in cache")
            return
        
        table_data = []
        for wl in wordlists:
            size_str = f"{wl['size']:,} bytes"
            lines_str = f"{wl['lines']:,} words"
            table_data.append([wl['name'], size_str, lines_str, wl['path']])
        
        print(tabulate(table_data, headers=['Name', 'Size', 'Words', 'Path'], tablefmt='grid'))
        
    except Exception as e:
        print_error(f"Failed to list wordlists: {e}")


@wordlist.command('download')
@click.argument('name')
@click.option('--force', is_flag=True, help='Force re-download')
def download_wordlist(name, force):
    """Download popular wordlists for password cracking
    
    Available wordlists:
    - rockyou: Famous RockYou wordlist (14M+ passwords)
    - common-passwords: Top 1M most common passwords  
    - john: John the Ripper default wordlist
    - darkweb2017: Top 10K passwords from dark web breaches
    
    Examples:
    hashkit wordlist download rockyou
    hashkit wordlist download common-passwords --force
    """
    try:
        manager = WordlistManager()
        
        if name not in manager.popular_wordlists:
            print_error(f"Unknown wordlist: {name}")
            print_info("Available wordlists:")
            for wl_name in manager.popular_wordlists.keys():
                print(f"  - {wl_name}")
            return
        
        path = manager.download_wordlist(name, force=force)
        print_success(f"Downloaded {name} to: {path}")
        
        # Validate downloaded wordlist
        stats = manager.validate_wordlist(path)
        print_info(f"Lines: {stats['lines']:,}")
        print_info(f"Size: {stats['size']:,} bytes")
        
    except Exception as e:
        print_error(f"Download failed: {e}")


@wordlist.command('validate')
@click.argument('file_path')
def validate_wordlist(file_path):
    """Validate a wordlist file"""
    try:
        manager = WordlistManager()
        stats = manager.validate_wordlist(file_path)
        
        if stats['readable']:
            print_success("Wordlist is valid and readable")
            print_info(f"Lines: {stats['lines']:,}")
            print_info(f"Size: {stats['size']:,} bytes")
            print_info(f"Min length: {stats['min_length']}")
            print_info(f"Max length: {stats['max_length']}")
            print_info(f"Avg length: {stats['avg_length']:.1f}")
            
            if stats['sample_words']:
                print_info("Sample words:")
                for word in stats['sample_words'][:5]:
                    print(f"  - {word}")
        else:
            print_error("Wordlist is not readable")
            if 'error' in stats:
                print_error(f"Error: {stats['error']}")
        
    except Exception as e:
        print_error(f"Validation failed: {e}")


@wordlist.command('clear')
@click.option('--confirm', is_flag=True, help='Skip confirmation prompt')
def clear_wordlists(confirm):
    """Clear all cached wordlists
    
    This will delete all downloaded wordlists from the local wordlists/ directory.
    Use with caution as this cannot be undone!
    
    Examples:
    hashkit wordlist clear
    hashkit wordlist clear --confirm
    """
    try:
        manager = WordlistManager()
        
        # Show what will be deleted
        wordlists = manager.list_cached_wordlists()
        if not wordlists:
            print_info("No wordlists found to clear")
            return
        
        total_size = sum(wl['size'] for wl in wordlists)
        print_info(f"Found {len(wordlists)} wordlists ({total_size:,} bytes)")
        
        for wl in wordlists:
            print(f"  - {wl['name']} ({wl['size']:,} bytes)")
        
        # Confirmation
        if not confirm:
            response = click.confirm("\nAre you sure you want to delete all wordlists?")
            if not response:
                print_info("Operation cancelled")
                return
        
        # Clear the cache
        result = manager.clear_cache()
        print_success(result['message'])
        
    except Exception as e:
        print_error(f"Failed to clear wordlists: {e}")


@cli.command()
def disclaimer():
    """Show legal disclaimer"""
    print(LEGAL_DISCLAIMER)


@cli.command()
@click.argument('hash_value')
def difficulty(hash_value):
    """Estimate crack difficulty for a hash"""
    try:
        identifier = HashIdentifier()
        analyzer = HashAnalyzer()
        
        hash_info = identifier.identify(hash_value)
        difficulty = analyzer.calculate_crack_difficulty(hash_info)
        
        print_info(f"Hash: {hash_value}")
        print_info(f"Type: {difficulty['hash_type'].upper()}")
        print_info(f"Difficulty Score: {difficulty['difficulty_score']:.1f}/10")
        
        print("\nEstimated Crack Times:")
        for hardware, time_str in difficulty['estimated_time'].items():
            print(f"  {hardware.replace('_', ' ').title()}: {time_str}")
        
        if difficulty['recommendations']:
            print("\nRecommendations:")
            for rec in difficulty['recommendations']:
                print(f"  • {rec}")
        
    except Exception as e:
        print_error(f"Difficulty analysis failed: {e}")


def main():
    """Main entry point"""
    try:
        cli()
    except KeyboardInterrupt:
        print_warning("\nOperation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()