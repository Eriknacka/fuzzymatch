"""
Address normalization module for Swedish addresses.

This module provides functions to normalize Swedish addresses for fuzzy matching.
It handles Swedish-specific characters (å, ä, ö) and common street type abbreviations.
"""

import re
from typing import Optional


def normalize_swedish_chars(text: str) -> str:
    """
    Normalize Swedish characters (å, ä, ö) for comparison.
    
    Args:
        text: Input text containing Swedish characters
        
    Returns:
        Text with normalized Swedish characters
        
    Example:
        >>> normalize_swedish_chars("Götgatan 123")
        'Gotgatan 123'
    """
    if not text:
        return text
    
    # Normalize Swedish characters
    replacements = {
        'å': 'a', 'Å': 'A',
        'ä': 'a', 'Ä': 'A',
        'ö': 'o', 'Ö': 'O'
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text


def normalize_street_types(text: str) -> str:
    """
    Normalize Swedish street type abbreviations.
    
    Converts common variations of street types (gata, väg, etc.) to standard forms.
    
    Args:
        text: Address text with street type
        
    Returns:
        Text with normalized street types
        
    Example:
        >>> normalize_street_types("Storgatan 1")
        'Storgatan 1'
        >>> normalize_street_types("Storvägen 1")
        'Storvägen 1'
    """
    if not text:
        return text
    
    # Common Swedish street type variations
    # Format: (pattern, replacement)
    street_patterns = [
        (r'\bgata\b', 'gatan'),
        (r'\bväg\b', 'vägen'),
        (r'\btorg\b', 'torget'),
        (r'\bplan\b', 'platsen'),
        (r'\bvägen\b', 'vägen'),
        (r'\bgatan\b', 'gatan'),
    ]
    
    for pattern, replacement in street_patterns:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


def normalize_address(address: str, 
                     normalize_chars: bool = True,
                     normalize_streets: bool = True,
                     lowercase: bool = True,
                     remove_extra_spaces: bool = True) -> str:
    """
    Comprehensive address normalization for Swedish addresses.
    
    Args:
        address: The address string to normalize
        normalize_chars: Whether to normalize Swedish characters (å, ä, ö)
        normalize_streets: Whether to normalize street type variations
        lowercase: Whether to convert to lowercase
        remove_extra_spaces: Whether to remove extra whitespace
        
    Returns:
        Normalized address string
        
    Example:
        >>> normalize_address("  Drottninggatan  123  ")
        'drottninggatan 123'
        >>> normalize_address("Götgatan 45, Stockholm")
        'gotgatan 45, stockholm'
    """
    if not address:
        return ""
    
    result = address
    
    # Remove extra whitespace
    if remove_extra_spaces:
        result = re.sub(r'\s+', ' ', result).strip()
    
    # Normalize Swedish characters
    if normalize_chars:
        result = normalize_swedish_chars(result)
    
    # Convert to lowercase
    if lowercase:
        result = result.lower()
    
    # Normalize street types
    if normalize_streets:
        result = normalize_street_types(result)
    
    return result


def extract_street_number(address: str) -> Optional[str]:
    """
    Extract street number from Swedish address.
    
    Args:
        address: Address string
        
    Returns:
        Street number if found, None otherwise
        
    Example:
        >>> extract_street_number("Drottninggatan 123")
        '123'
        >>> extract_street_number("Kungsgatan 45B")
        '45B'
    """
    if not address:
        return None
    
    # Match common Swedish address patterns
    # Handles: "123", "123A", "123-125", etc.
    match = re.search(r'\b(\d+[A-Za-z]?(?:-\d+)?)\b', address)
    
    if match:
        return match.group(1)
    
    return None


def extract_postal_code(address: str) -> Optional[str]:
    """
    Extract Swedish postal code (5 digits, optionally with space after 3rd digit).
    
    Args:
        address: Address string
        
    Returns:
        Postal code if found, None otherwise
        
    Example:
        >>> extract_postal_code("Storgatan 1, 123 45 Stockholm")
        '123 45'
        >>> extract_postal_code("Vägen 5, 12345 Göteborg")
        '12345'
    """
    if not address:
        return None
    
    # Swedish postal codes: 5 digits, optionally with space after 3rd digit
    match = re.search(r'\b(\d{3}\s?\d{2})\b', address)
    
    if match:
        return match.group(1)
    
    return None
