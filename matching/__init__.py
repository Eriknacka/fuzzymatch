"""
Fuzzy matching module for Swedish addresses using RapidFuzz.

This module provides functions to perform fuzzy matching between addresses
using various similarity algorithms from the RapidFuzz library.
"""

from typing import List, Tuple, Optional, Dict
from rapidfuzz import fuzz, process
from normalization import normalize_address


def fuzzy_match_address(query: str, 
                       candidates: List[str],
                       score_cutoff: float = 60.0,
                       limit: Optional[int] = 5,
                       normalize: bool = True) -> List[Tuple[str, float]]:
    """
    Perform fuzzy matching of a query address against a list of candidate addresses.
    
    Uses RapidFuzz's WRatio (weighted ratio) for flexible matching.
    
    Args:
        query: The address to search for
        candidates: List of addresses to match against
        score_cutoff: Minimum similarity score (0-100) to include in results
        limit: Maximum number of results to return (None for all matches)
        normalize: Whether to normalize addresses before matching
        
    Returns:
        List of tuples (matched_address, similarity_score) sorted by score descending
        
    Example:
        >>> candidates = ["Drottninggatan 123", "Kungsgatan 45", "Götgatan 78"]
        >>> fuzzy_match_address("Drottningsgatan 123", candidates)
        [('Drottninggatan 123', 95.0), ...]
    """
    if normalize:
        normalized_query = normalize_address(query)
        normalized_candidates = [normalize_address(c) for c in candidates]
    else:
        normalized_query = query
        normalized_candidates = candidates
    
    # Use process.extract for efficient multiple matches
    results = process.extract(
        normalized_query,
        normalized_candidates,
        scorer=fuzz.WRatio,
        score_cutoff=score_cutoff,
        limit=limit
    )
    
    # Map back to original addresses
    matched_results = []
    for match, score, idx in results:
        matched_results.append((candidates[idx], score))
    
    return matched_results


def find_best_match(query: str,
                   candidates: List[str],
                   score_cutoff: float = 60.0,
                   normalize: bool = True) -> Optional[Tuple[str, float]]:
    """
    Find the single best matching address from candidates.
    
    Args:
        query: The address to search for
        candidates: List of addresses to match against
        score_cutoff: Minimum similarity score (0-100) to consider
        normalize: Whether to normalize addresses before matching
        
    Returns:
        Tuple of (best_match, score) or None if no match above cutoff
        
    Example:
        >>> candidates = ["Drottninggatan 123", "Kungsgatan 45"]
        >>> find_best_match("Drottningsgatan 123", candidates)
        ('Drottninggatan 123', 95.0)
    """
    matches = fuzzy_match_address(query, candidates, score_cutoff, limit=1, normalize=normalize)
    
    if matches:
        return matches[0]
    
    return None


def similarity_score(address1: str, 
                    address2: str,
                    normalize: bool = True,
                    method: str = "ratio") -> float:
    """
    Calculate similarity score between two addresses.
    
    Args:
        address1: First address
        address2: Second address
        normalize: Whether to normalize addresses before comparison
        method: Scoring method - "ratio", "partial_ratio", or "token_sort_ratio"
        
    Returns:
        Similarity score between 0 and 100
        
    Example:
        >>> similarity_score("Drottninggatan 123", "Drottningsgatan 123")
        95.0
    """
    if normalize:
        addr1 = normalize_address(address1)
        addr2 = normalize_address(address2)
    else:
        addr1 = address1
        addr2 = address2
    
    # Select scoring method
    if method == "ratio":
        score = fuzz.ratio(addr1, addr2)
    elif method == "partial_ratio":
        score = fuzz.partial_ratio(addr1, addr2)
    elif method == "token_sort_ratio":
        score = fuzz.token_sort_ratio(addr1, addr2)
    else:
        # Default to WRatio for best overall performance
        score = fuzz.WRatio(addr1, addr2)
    
    return score


def batch_match_addresses(queries: List[str],
                         candidates: List[str],
                         score_cutoff: float = 60.0,
                         normalize: bool = True) -> Dict[str, Optional[Tuple[str, float]]]:
    """
    Match multiple query addresses against candidates efficiently.
    
    Args:
        queries: List of addresses to match
        candidates: List of addresses to match against
        score_cutoff: Minimum similarity score to consider
        normalize: Whether to normalize addresses
        
    Returns:
        Dictionary mapping each query to its best match (or None)
        
    Example:
        >>> queries = ["Drottningsgatan 123", "Kungsvägen 45"]
        >>> candidates = ["Drottninggatan 123", "Kungsgatan 45"]
        >>> batch_match_addresses(queries, candidates)
        {'Drottningsgatan 123': ('Drottninggatan 123', 95.0), ...}
    """
    results = {}
    
    for query in queries:
        best_match = find_best_match(query, candidates, score_cutoff, normalize)
        results[query] = best_match
    
    return results


def match_with_context(query: str,
                      candidates: List[str],
                      query_context: Optional[Dict] = None,
                      candidate_contexts: Optional[List[Dict]] = None,
                      score_cutoff: float = 60.0) -> List[Tuple[str, float, Dict]]:
    """
    Match addresses with additional context (e.g., city, postal code).
    
    This is a stub for more advanced matching that considers context.
    
    Args:
        query: Address to search for
        candidates: List of addresses to match against
        query_context: Additional context for query (city, postal_code, etc.)
        candidate_contexts: List of context dicts for each candidate
        score_cutoff: Minimum similarity score
        
    Returns:
        List of tuples (address, score, context)
        
    Note:
        This is a placeholder for future implementation with context-aware matching.
    """
    # Basic implementation - match addresses only
    basic_matches = fuzzy_match_address(query, candidates, score_cutoff)
    
    # Add context if available
    results = []
    for addr, score in basic_matches:
        idx = candidates.index(addr)
        context = candidate_contexts[idx] if candidate_contexts else {}
        results.append((addr, score, context))
    
    return results
