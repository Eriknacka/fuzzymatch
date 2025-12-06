#!/usr/bin/env python3
"""
Example script demonstrating the Swedish address fuzzy matching library.
"""

import pandas as pd
from normalization import normalize_address, extract_postal_code
from matching import fuzzy_match_address, find_best_match
from scoring import rank_matches, classify_match_quality
from evaluation import calculate_match_rate, evaluate_score_distribution


def main():
    print("=" * 70)
    print("Swedish Address Fuzzy Matching - Example Usage")
    print("=" * 70)
    
    # Load sample data
    print("\n1. Loading sample data...")
    customers = pd.read_csv('data/customers.csv')
    leads = pd.read_csv('data/leads.csv')
    print(f"   Loaded {len(customers)} customers and {len(leads)} leads")
    
    # Example 1: Normalize addresses
    print("\n2. Address Normalization Example")
    print("-" * 70)
    example_addresses = [
        "Drottninggatan 45, 111 21 Stockholm",
        "Götgatan 78",
        "Östra Hamngatan 12"
    ]
    
    for addr in example_addresses:
        normalized = normalize_address(addr)
        postal = extract_postal_code(addr)
        print(f"Original:     {addr}")
        print(f"Normalized:   {normalized}")
        print(f"Postal Code:  {postal if postal else 'N/A'}")
        print()
    
    # Example 2: Find matches for a single address
    print("\n3. Single Address Matching Example")
    print("-" * 70)
    query = "Drottningsgatan 45"  # Note the typo
    customer_addresses = customers['address'].tolist()
    
    print(f"Query: '{query}'")
    print("\nTop 3 matches:")
    matches = fuzzy_match_address(query, customer_addresses, limit=3)
    
    for i, (addr, score) in enumerate(matches, 1):
        quality = classify_match_quality(score)
        print(f"  {i}. {addr:40} | Score: {score:5.1f} | {quality}")
    
    # Example 3: Batch matching leads to customers
    print("\n4. Batch Matching Example")
    print("-" * 70)
    
    results = []
    for _, lead in leads.head(10).iterrows():
        lead_addr = lead['contact_address']
        match = find_best_match(lead_addr, customer_addresses, score_cutoff=60.0)
        
        if match:
            customer_addr, score = match
            results.append({
                'lead_company': lead['company'],
                'lead_address': lead_addr,
                'matched_customer_address': customer_addr,
                'score': score,
                'quality': classify_match_quality(score)
            })
    
    results_df = pd.DataFrame(results)
    print(results_df.to_string(index=False))
    
    # Example 4: Quality distribution
    print("\n5. Match Quality Distribution")
    print("-" * 70)
    
    all_scores = []
    all_matches = []
    
    for _, lead in leads.iterrows():
        match = find_best_match(lead['contact_address'], customer_addresses, score_cutoff=60.0)
        if match:
            _, score = match
            all_scores.append(score)
            all_matches.append({'score': score, 'quality': classify_match_quality(score)})
    
    # Count by quality
    quality_counts = {}
    for match in all_matches:
        quality = match['quality']
        quality_counts[quality] = quality_counts.get(quality, 0) + 1
    
    for quality, count in sorted(quality_counts.items(), reverse=True):
        percentage = (count / len(all_matches)) * 100
        print(f"{quality:12}: {count:3} ({percentage:5.1f}%)")
    
    # Example 5: Statistics
    print("\n6. Match Statistics")
    print("-" * 70)
    
    stats = evaluate_score_distribution(all_scores)
    print(f"Mean Score:   {stats['mean']:.2f}")
    print(f"Median Score: {stats['median']:.2f}")
    print(f"Std Dev:      {stats['std_dev']:.2f}")
    print(f"Min Score:    {stats['min']:.2f}")
    print(f"Max Score:    {stats['max']:.2f}")
    print(f"Total Matches: {stats['count']}")
    
    match_rate_stats = calculate_match_rate(len(leads), len(all_matches), threshold=60.0)
    print(f"\nMatch Rate:   {match_rate_stats['match_rate']:.1%}")
    print(f"No Match:     {match_rate_stats['no_match_rate']:.1%}")
    
    print("\n" + "=" * 70)
    print("Example completed successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
