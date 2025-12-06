"""
Scoring rules module for address matching.

This module provides functions to score and rank address matches based on
various business rules and criteria.
"""

from typing import Dict, List, Tuple, Optional


def calculate_match_confidence(similarity_score: float,
                               has_street_number_match: bool = False,
                               has_postal_code_match: bool = False,
                               has_city_match: bool = False) -> float:
    """
    Calculate overall confidence score for an address match.
    
    Combines similarity score with additional matching criteria to provide
    a confidence score for the match.
    
    Args:
        similarity_score: Fuzzy match similarity score (0-100)
        has_street_number_match: Whether street numbers match
        has_postal_code_match: Whether postal codes match
        has_city_match: Whether cities match
        
    Returns:
        Confidence score (0-100)
        
    Example:
        >>> calculate_match_confidence(85.0, True, True, True)
        95.0
        >>> calculate_match_confidence(85.0, False, False, False)
        85.0
    """
    confidence = similarity_score
    
    # Boost confidence if additional criteria match
    if has_street_number_match:
        confidence = min(100, confidence + 5.0)
    
    if has_postal_code_match:
        confidence = min(100, confidence + 5.0)
    
    if has_city_match:
        confidence = min(100, confidence + 5.0)
    
    return confidence


def classify_match_quality(score: float) -> str:
    """
    Classify match quality based on similarity score.
    
    Args:
        score: Similarity score (0-100)
        
    Returns:
        Quality classification: "excellent", "good", "fair", "poor", or "no_match"
        
    Example:
        >>> classify_match_quality(95.0)
        'excellent'
        >>> classify_match_quality(75.0)
        'good'
        >>> classify_match_quality(50.0)
        'poor'
    """
    if score >= 90:
        return "excellent"
    elif score >= 75:
        return "good"
    elif score >= 60:
        return "fair"
    elif score >= 40:
        return "poor"
    else:
        return "no_match"


def rank_matches(matches: List[Tuple[str, float]],
                min_score: float = 60.0) -> List[Dict]:
    """
    Rank and annotate a list of matches with quality classifications.
    
    Args:
        matches: List of (address, score) tuples
        min_score: Minimum score to include in results
        
    Returns:
        List of dictionaries with match details, ranked by score
        
    Example:
        >>> matches = [("Drottninggatan 123", 95.0), ("Kungsgatan 45", 70.0)]
        >>> rank_matches(matches)
        [{'address': 'Drottninggatan 123', 'score': 95.0, 'quality': 'excellent', 'rank': 1}, ...]
    """
    # Filter by minimum score
    filtered_matches = [(addr, score) for addr, score in matches if score >= min_score]
    
    # Sort by score descending (should already be sorted, but ensure)
    sorted_matches = sorted(filtered_matches, key=lambda x: x[1], reverse=True)
    
    # Create ranked result with annotations
    results = []
    for rank, (address, score) in enumerate(sorted_matches, 1):
        results.append({
            'address': address,
            'score': score,
            'quality': classify_match_quality(score),
            'rank': rank
        })
    
    return results


def apply_business_rules(matches: List[Dict],
                        rules: Optional[Dict] = None) -> List[Dict]:
    """
    Apply business-specific rules to filter or adjust matches.
    
    This is a stub for implementing custom business logic.
    
    Args:
        matches: List of match dictionaries from rank_matches
        rules: Dictionary of business rules to apply
        
    Returns:
        Filtered/adjusted list of matches
        
    Example:
        >>> matches = [{'address': 'Drottninggatan 123', 'score': 95.0, 'quality': 'excellent'}]
        >>> rules = {'min_quality': 'good', 'max_results': 3}
        >>> apply_business_rules(matches, rules)
        [{'address': 'Drottninggatan 123', 'score': 95.0, 'quality': 'excellent'}]
    """
    if not rules:
        return matches
    
    results = matches.copy()
    
    # Apply minimum quality filter
    if 'min_quality' in rules:
        quality_order = ['no_match', 'poor', 'fair', 'good', 'excellent']
        min_idx = quality_order.index(rules['min_quality'])
        results = [m for m in results if quality_order.index(m['quality']) >= min_idx]
    
    # Apply maximum results limit
    if 'max_results' in rules:
        results = results[:rules['max_results']]
    
    # Apply minimum score filter
    if 'min_score' in rules:
        results = [m for m in results if m['score'] >= rules['min_score']]
    
    return results


def calculate_weighted_score(base_score: float,
                            weights: Optional[Dict[str, float]] = None,
                            features: Optional[Dict[str, bool]] = None) -> float:
    """
    Calculate weighted score based on additional features.
    
    Args:
        base_score: Base similarity score
        weights: Dictionary of feature weights
        features: Dictionary of boolean features
        
    Returns:
        Weighted score
        
    Example:
        >>> weights = {'exact_number': 10, 'same_city': 5}
        >>> features = {'exact_number': True, 'same_city': True}
        >>> calculate_weighted_score(80.0, weights, features)
        95.0
    """
    if not weights or not features:
        return base_score
    
    score = base_score
    
    for feature_name, weight in weights.items():
        if features.get(feature_name, False):
            score += weight
    
    # Cap at 100
    return min(100.0, score)


def score_batch(query_addresses: List[str],
               match_results: Dict[str, List[Dict]]) -> Dict[str, Dict]:
    """
    Score a batch of address matches with summary statistics.
    
    Args:
        query_addresses: List of query addresses
        match_results: Dictionary mapping queries to their match results
        
    Returns:
        Dictionary with scoring summary for each query
        
    Example:
        >>> queries = ["Drottninggatan 123"]
        >>> results = {"Drottninggatan 123": [{'score': 95.0, 'quality': 'excellent'}]}
        >>> score_batch(queries, results)
        {'Drottninggatan 123': {'best_score': 95.0, 'best_quality': 'excellent', ...}}
    """
    summary = {}
    
    for query in query_addresses:
        matches = match_results.get(query, [])
        
        if matches:
            best_match = matches[0]
            summary[query] = {
                'best_score': best_match['score'],
                'best_quality': best_match['quality'],
                'num_matches': len(matches),
                'has_excellent_match': any(m['quality'] == 'excellent' for m in matches),
                'has_good_match': any(m['quality'] in ['excellent', 'good'] for m in matches)
            }
        else:
            summary[query] = {
                'best_score': 0.0,
                'best_quality': 'no_match',
                'num_matches': 0,
                'has_excellent_match': False,
                'has_good_match': False
            }
    
    return summary
