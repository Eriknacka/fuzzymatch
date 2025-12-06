"""
Evaluation module for assessing address matching performance.

This module provides metrics and functions to evaluate the quality of
address matching algorithms and results.
"""

from typing import List, Dict, Tuple, Optional
import statistics


def calculate_precision_recall(true_matches: List[Tuple[str, str]],
                               predicted_matches: List[Tuple[str, str]]) -> Dict[str, float]:
    """
    Calculate precision and recall for address matching.
    
    Args:
        true_matches: List of (query, true_match) tuples (ground truth)
        predicted_matches: List of (query, predicted_match) tuples
        
    Returns:
        Dictionary with 'precision', 'recall', and 'f1_score'
        
    Example:
        >>> true = [("query1", "match1"), ("query2", "match2")]
        >>> pred = [("query1", "match1"), ("query2", "wrong")]
        >>> calculate_precision_recall(true, pred)
        {'precision': 0.5, 'recall': 0.5, 'f1_score': 0.5}
    """
    if not predicted_matches:
        return {'precision': 0.0, 'recall': 0.0, 'f1_score': 0.0}
    
    # Convert to sets for comparison
    true_set = set(true_matches)
    pred_set = set(predicted_matches)
    
    # Calculate true positives
    true_positives = len(true_set & pred_set)
    
    # Calculate precision and recall
    precision = true_positives / len(pred_set) if pred_set else 0.0
    recall = true_positives / len(true_set) if true_set else 0.0
    
    # Calculate F1 score
    if precision + recall > 0:
        f1_score = 2 * (precision * recall) / (precision + recall)
    else:
        f1_score = 0.0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'true_positives': true_positives,
        'total_predicted': len(pred_set),
        'total_true': len(true_set)
    }


def calculate_accuracy(true_matches: List[Tuple[str, str]],
                      predicted_matches: List[Tuple[str, str]]) -> float:
    """
    Calculate matching accuracy.
    
    Args:
        true_matches: Ground truth matches
        predicted_matches: Predicted matches
        
    Returns:
        Accuracy score (0.0 to 1.0)
        
    Example:
        >>> true = [("q1", "m1"), ("q2", "m2"), ("q3", "m3")]
        >>> pred = [("q1", "m1"), ("q2", "m2"), ("q3", "wrong")]
        >>> calculate_accuracy(true, pred)
        0.6666666666666666
    """
    if not true_matches or not predicted_matches:
        return 0.0
    
    # Ensure same length for fair comparison
    min_len = min(len(true_matches), len(predicted_matches))
    
    correct = sum(1 for i in range(min_len) if true_matches[i] == predicted_matches[i])
    
    return correct / min_len if min_len > 0 else 0.0


def evaluate_score_distribution(scores: List[float]) -> Dict[str, float]:
    """
    Analyze the distribution of similarity scores.
    
    Args:
        scores: List of similarity scores
        
    Returns:
        Dictionary with statistical measures
        
    Example:
        >>> scores = [95.0, 85.0, 75.0, 65.0, 55.0]
        >>> stats = evaluate_score_distribution(scores)
        >>> 'mean' in stats
        True
    """
    if not scores:
        return {
            'mean': 0.0,
            'median': 0.0,
            'std_dev': 0.0,
            'min': 0.0,
            'max': 0.0,
            'count': 0
        }
    
    return {
        'mean': statistics.mean(scores),
        'median': statistics.median(scores),
        'std_dev': statistics.stdev(scores) if len(scores) > 1 else 0.0,
        'min': min(scores),
        'max': max(scores),
        'count': len(scores)
    }


def calculate_match_rate(total_queries: int,
                        successful_matches: int,
                        threshold: float = 60.0) -> Dict[str, float]:
    """
    Calculate the rate of successful matches above a threshold.
    
    Args:
        total_queries: Total number of query addresses
        successful_matches: Number of matches above threshold
        threshold: Score threshold for successful match
        
    Returns:
        Dictionary with match rate statistics
        
    Example:
        >>> calculate_match_rate(100, 85, 60.0)
        {'match_rate': 0.85, 'no_match_rate': 0.15, 'threshold': 60.0}
    """
    if total_queries == 0:
        return {'match_rate': 0.0, 'no_match_rate': 0.0, 'threshold': threshold}
    
    match_rate = successful_matches / total_queries
    no_match_rate = 1.0 - match_rate
    
    return {
        'match_rate': match_rate,
        'no_match_rate': no_match_rate,
        'threshold': threshold,
        'total_queries': total_queries,
        'successful_matches': successful_matches
    }


def evaluate_quality_distribution(matches: List[Dict]) -> Dict[str, int]:
    """
    Count matches by quality classification.
    
    Args:
        matches: List of match dictionaries with 'quality' field
        
    Returns:
        Dictionary with counts per quality level
        
    Example:
        >>> matches = [
        ...     {'quality': 'excellent'},
        ...     {'quality': 'good'},
        ...     {'quality': 'excellent'}
        ... ]
        >>> evaluate_quality_distribution(matches)
        {'excellent': 2, 'good': 1, 'fair': 0, 'poor': 0, 'no_match': 0}
    """
    quality_counts = {
        'excellent': 0,
        'good': 0,
        'fair': 0,
        'poor': 0,
        'no_match': 0
    }
    
    for match in matches:
        quality = match.get('quality', 'no_match')
        if quality in quality_counts:
            quality_counts[quality] += 1
    
    return quality_counts


def generate_evaluation_report(true_matches: List[Tuple[str, str]],
                               predicted_matches: List[Tuple[str, str]],
                               scores: List[float],
                               matches: List[Dict]) -> Dict:
    """
    Generate a comprehensive evaluation report.
    
    Args:
        true_matches: Ground truth matches
        predicted_matches: Predicted matches
        scores: List of similarity scores
        matches: List of match dictionaries
        
    Returns:
        Comprehensive evaluation report dictionary
        
    Example:
        >>> report = generate_evaluation_report(true, pred, scores, matches)
        >>> 'precision_recall' in report
        True
    """
    report = {
        'precision_recall': calculate_precision_recall(true_matches, predicted_matches),
        'accuracy': calculate_accuracy(true_matches, predicted_matches),
        'score_distribution': evaluate_score_distribution(scores),
        'quality_distribution': evaluate_quality_distribution(matches),
        'match_rate': calculate_match_rate(
            len(predicted_matches),
            len([m for m in matches if m.get('score', 0) >= 60.0]),
            threshold=60.0
        )
    }
    
    return report


def compare_algorithms(algorithm_results: Dict[str, List[Tuple[str, str]]],
                      ground_truth: List[Tuple[str, str]]) -> Dict[str, Dict]:
    """
    Compare performance of different matching algorithms.
    
    Args:
        algorithm_results: Dictionary mapping algorithm name to predicted matches
        ground_truth: True matches for comparison
        
    Returns:
        Dictionary with evaluation metrics for each algorithm
        
    Example:
        >>> results = {
        ...     'algo1': [("q1", "m1"), ("q2", "m2")],
        ...     'algo2': [("q1", "m1"), ("q2", "wrong")]
        ... }
        >>> ground_truth = [("q1", "m1"), ("q2", "m2")]
        >>> compare_algorithms(results, ground_truth)
        {'algo1': {...}, 'algo2': {...}}
    """
    comparison = {}
    
    for algo_name, predictions in algorithm_results.items():
        comparison[algo_name] = calculate_precision_recall(ground_truth, predictions)
    
    return comparison
