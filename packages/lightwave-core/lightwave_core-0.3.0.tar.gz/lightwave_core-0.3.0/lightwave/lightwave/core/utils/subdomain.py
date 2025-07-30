"""Subdomain utilities for the Lightwave ecosystem."""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urlparse


def extract_subdomain(url_or_domain: str) -> Optional[str]:
    """Extract subdomain from a URL or domain.
    
    Args:
        url_or_domain: Full URL or domain name
        
    Returns:
        Subdomain if found, None otherwise
        
    Examples:
        >>> extract_subdomain("https://api.example.com/path")
        'api'
        >>> extract_subdomain("blog.company.co.uk")
        'blog'
        >>> extract_subdomain("example.com")
        None
    """
    # Handle URLs vs domain names
    if url_or_domain.startswith(('http://', 'https://')):
        parsed = urlparse(url_or_domain)
        domain = parsed.netloc
    else:
        domain = url_or_domain
    
    # Remove port if present
    domain = domain.split(':')[0]
    
    # Split domain parts
    parts = domain.split('.')
    
    # Need at least 3 parts for subdomain (subdomain.domain.tld)
    if len(parts) < 3:
        return None
    
    # Handle common TLD patterns
    if len(parts) >= 4 and parts[-2] in ['co', 'com', 'org', 'net', 'gov']:
        # Handle cases like example.co.uk, example.com.au
        return '.'.join(parts[:-3]) if len(parts) > 3 else None
    else:
        # Standard case: subdomain.domain.tld
        return '.'.join(parts[:-2]) if len(parts) > 2 else None


def validate_subdomain(subdomain: str) -> bool:
    """Validate if a string is a valid subdomain.
    
    Args:
        subdomain: Subdomain to validate
        
    Returns:
        True if valid subdomain, False otherwise
        
    Examples:
        >>> validate_subdomain("api")
        True
        >>> validate_subdomain("my-app")
        True
        >>> validate_subdomain("_invalid")
        False
    """
    if not subdomain:
        return False
    
    # Check length (1-63 characters per RFC)
    if len(subdomain) > 63:
        return False
    
    # Subdomain pattern: letters, numbers, hyphens (not at start/end)
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$'
    
    # Single character subdomains are valid
    if len(subdomain) == 1:
        return subdomain.isalnum()
    
    return bool(re.match(pattern, subdomain))


def parse_domain_parts(domain: str) -> Tuple[Optional[str], str, str]:
    """Parse domain into subdomain, domain, and TLD parts.
    
    Args:
        domain: Domain to parse
        
    Returns:
        Tuple of (subdomain, domain, tld)
        
    Examples:
        >>> parse_domain_parts("api.example.com")
        ('api', 'example', 'com')
        >>> parse_domain_parts("example.co.uk")
        (None, 'example', 'co.uk')
    """
    parts = domain.split('.')
    
    if len(parts) < 2:
        raise ValueError("Invalid domain format")
    
    # Handle complex TLDs like co.uk, com.au
    known_compound_tlds = [
        'co.uk', 'co.jp', 'co.za', 'com.au', 'com.br', 'com.mx',
        'org.uk', 'net.uk', 'gov.uk', 'ac.uk'
    ]
    
    # Check if last two parts form a compound TLD
    potential_tld = '.'.join(parts[-2:])
    if potential_tld in known_compound_tlds:
        tld = potential_tld
        if len(parts) == 2:
            # example.co.uk -> (None, 'example', 'co.uk')
            return None, parts[0], tld
        elif len(parts) == 3:
            # subdomain.example.co.uk -> ('subdomain', 'example', 'co.uk')
            return parts[0], parts[1], tld
        else:
            # multi.level.subdomain.example.co.uk
            subdomain = '.'.join(parts[:-3])
            return subdomain, parts[-3], tld
    else:
        # Standard TLD
        tld = parts[-1]
        if len(parts) == 2:
            # example.com -> (None, 'example', 'com')
            return None, parts[0], tld
        else:
            # subdomain.example.com -> ('subdomain', 'example', 'com')
            subdomain = '.'.join(parts[:-2])
            return subdomain, parts[-2], tld


def is_valid_domain(domain: str) -> bool:
    """Check if a domain is valid.
    
    Args:
        domain: Domain to validate
        
    Returns:
        True if valid domain, False otherwise
    """
    if not domain:
        return False
    
    # Basic checks
    if len(domain) > 253:  # RFC limit
        return False
    
    if domain.startswith('.') or domain.endswith('.'):
        return False
    
    if '..' in domain:
        return False
    
    try:
        subdomain, domain_part, tld = parse_domain_parts(domain)
        
        # Validate each part
        if subdomain and not validate_subdomain(subdomain):
            return False
        
        if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', domain_part):
            return False
        
        if not re.match(r'^[a-zA-Z0-9.]([a-zA-Z0-9.-]*[a-zA-Z0-9])?$', tld):
            return False
        
        return True
    
    except ValueError:
        return False


def normalize_domain(domain: str) -> str:
    """Normalize domain to lowercase and remove trailing dots.
    
    Args:
        domain: Domain to normalize
        
    Returns:
        Normalized domain
    """
    return domain.lower().rstrip('.')


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load configuration from YAML file.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        config_path = "config.yaml"
    
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def get_application_name() -> str:
    """Get the current application name.
    
    Returns:
        Application name
    """
    return os.environ.get('APPLICATION_NAME', 'lightwave')


def get_host_url(subdomain: Optional[str] = None) -> str:
    """Get the host URL for a subdomain.
    
    Args:
        subdomain: Subdomain name
        
    Returns:
        Full host URL
    """
    base_domain = os.environ.get('BASE_DOMAIN', 'localhost')
    scheme = os.environ.get('SCHEME', 'http')
    
    if subdomain:
        return f"{scheme}://{subdomain}.{base_domain}"
    else:
        return f"{scheme}://{base_domain}"


def get_subdomain_list() -> List[str]:
    """Get list of available subdomains.
    
    Returns:
        List of subdomain names
    """
    config = load_config()
    return config.get('subdomains', [])


def is_subdomain_enabled(subdomain: str) -> bool:
    """Check if a subdomain is enabled.
    
    Args:
        subdomain: Subdomain to check
        
    Returns:
        True if subdomain is enabled
    """
    return subdomain in get_subdomain_list()


def get_parent_domain() -> str:
    """Get the parent domain.
    
    Returns:
        Parent domain name
    """
    return os.environ.get('PARENT_DOMAIN', 'localhost')


def get_full_domain(subdomain: Optional[str] = None) -> str:
    """Get the full domain including subdomain.
    
    Args:
        subdomain: Subdomain name
        
    Returns:
        Full domain name
    """
    parent = get_parent_domain()
    if subdomain:
        return f"{subdomain}.{parent}"
    else:
        return parent


def get_current_subdomain() -> Optional[str]:
    """Get the current subdomain from environment.
    
    Returns:
        Current subdomain or None
    """
    return os.environ.get('CURRENT_SUBDOMAIN')