#!/usr/bin/env python3
"""
Simple test script to verify all modules import correctly.
"""

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        print("  - Testing normalization module...")
        from normalization import (
            normalize_address,
            normalize_swedish_chars,
            normalize_street_types,
            extract_street_number,
            extract_postal_code
        )
        print("    ✓ normalization module imported successfully")
        
        print("  - Testing matching module...")
        from matching import (
            fuzzy_match_address,
            find_best_match,
            similarity_score,
            batch_match_addresses
        )
        print("    ✓ matching module imported successfully")
        
        print("  - Testing scoring module...")
        from scoring import (
            calculate_match_confidence,
            classify_match_quality,
            rank_matches,
            apply_business_rules
        )
        print("    ✓ scoring module imported successfully")
        
        print("  - Testing evaluation module...")
        from evaluation import (
            calculate_precision_recall,
            calculate_accuracy,
            evaluate_score_distribution,
            calculate_match_rate
        )
        print("    ✓ evaluation module imported successfully")
        
        print("\n✓ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n✗ Import failed: {e}")
        return False


def test_basic_functionality():
    """Test basic functionality of each module."""
    print("\nTesting basic functionality...")
    
    from normalization import normalize_address
    from matching import similarity_score
    from scoring import classify_match_quality
    
    # Test normalization
    print("\n  - Testing normalization...")
    test_addr = "Götgatan 45, Stockholm"
    normalized = normalize_address(test_addr)
    print(f"    Input:      '{test_addr}'")
    print(f"    Normalized: '{normalized}'")
    assert normalized == "gotgatan 45, stockholm", "Normalization failed"
    print("    ✓ Normalization works")
    
    # Test similarity scoring
    print("\n  - Testing similarity scoring...")
    addr1 = "Drottninggatan 123"
    addr2 = "Drottningsgatan 123"
    score = similarity_score(addr1, addr2)
    print(f"    Address 1: '{addr1}'")
    print(f"    Address 2: '{addr2}'")
    print(f"    Score:     {score:.1f}")
    assert score > 90, "Similarity score should be high"
    print("    ✓ Similarity scoring works")
    
    # Test quality classification
    print("\n  - Testing quality classification...")
    quality = classify_match_quality(score)
    print(f"    Score:   {score:.1f}")
    print(f"    Quality: {quality}")
    assert quality in ["excellent", "good", "fair", "poor", "no_match"], "Invalid quality"
    print("    ✓ Quality classification works")
    
    print("\n✓ All basic functionality tests passed!")
    return True


def test_sample_data():
    """Test loading sample CSV files."""
    print("\nTesting sample data loading...")
    
    try:
        import pandas as pd
        
        # Load customer data
        print("  - Loading customers.csv...")
        customers = pd.read_csv('data/customers.csv')
        print(f"    ✓ Loaded {len(customers)} customers")
        
        # Load lead data
        print("  - Loading leads.csv...")
        leads = pd.read_csv('data/leads.csv')
        print(f"    ✓ Loaded {len(leads)} leads")
        
        print("\n✓ Sample data loaded successfully!")
        return True
        
    except Exception as e:
        print(f"\n✗ Failed to load sample data: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("Swedish Address Fuzzy Matching - Module Test")
    print("=" * 70)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test functionality
    if not test_basic_functionality():
        all_passed = False
    
    # Test sample data
    if not test_sample_data():
        all_passed = False
    
    # Final result
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 70)
    
    return all_passed


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
