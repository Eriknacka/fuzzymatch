# fuzzymatch

A Python library for fuzzy matching Swedish addresses using RapidFuzz.

## Overview

This project provides tools for matching, normalizing, and scoring Swedish addresses. It's designed to help with deduplication, data matching, and address standardization tasks common in Swedish business operations.

## Features

- **Swedish Character Normalization**: Handles å, ä, ö characters
- **Street Type Normalization**: Standardizes gata/väg variations
- **Fuzzy Matching**: Uses RapidFuzz for flexible address matching
- **Scoring Rules**: Customizable scoring and quality classification
- **Evaluation Metrics**: Tools to assess matching performance
- **Sample Data**: Synthetic Swedish address datasets included

## Project Structure

```
fuzzymatch/
├── normalization/       # Address normalization functions
│   └── __init__.py     # Swedish-specific normalization (åäö, gata/väg)
├── matching/           # Fuzzy matching logic
│   └── __init__.py     # RapidFuzz-based matching functions
├── scoring/            # Scoring and ranking
│   └── __init__.py     # Match quality scoring rules
├── evaluation/         # Performance evaluation
│   └── __init__.py     # Metrics and evaluation functions
├── data/              # Sample datasets
│   ├── customers.csv  # Sample customer addresses
│   └── leads.csv      # Sample lead addresses
├── notebooks/         # Jupyter notebooks
│   └── demo.ipynb     # Interactive demo and examples
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Eriknacka/fuzzymatch.git
cd fuzzymatch
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from normalization import normalize_address
from matching import fuzzy_match_address, find_best_match
from scoring import classify_match_quality

# Normalize a Swedish address
address = "Drottninggatan 123, Stockholm"
normalized = normalize_address(address)
print(normalized)  # Output: "drottninggatan 123, stockholm"

# Match addresses
query = "Drottningsgatan 123"
candidates = [
    "Drottninggatan 123",
    "Kungsgatan 45",
    "Götgatan 78"
]

# Find all matches above threshold
matches = fuzzy_match_address(query, candidates, score_cutoff=60.0)
for address, score in matches:
    quality = classify_match_quality(score)
    print(f"{address}: {score:.1f} ({quality})")

# Find best match only
best_match = find_best_match(query, candidates)
if best_match:
    address, score = best_match
    print(f"Best match: {address} (score: {score:.1f})")
```

### Address Normalization

```python
from normalization import (
    normalize_address,
    normalize_swedish_chars,
    extract_street_number,
    extract_postal_code
)

# Normalize Swedish characters
text = "Götgatan 45, Malmö"
normalized = normalize_swedish_chars(text)
print(normalized)  # "Gotgatan 45, Malmo"

# Extract components
address = "Drottninggatan 123, 111 21 Stockholm"
street_number = extract_street_number(address)  # "123"
postal_code = extract_postal_code(address)      # "111 21"
```

### Fuzzy Matching

```python
from matching import similarity_score, batch_match_addresses

# Calculate similarity between two addresses
score = similarity_score("Götgatan 45", "Götatan 45")
print(f"Similarity: {score:.1f}")  # High score despite typo

# Batch matching
queries = ["Drottningsgatan 123", "Kungsvägen 45"]
candidates = ["Drottninggatan 123", "Kungsgatan 45"]
results = batch_match_addresses(queries, candidates)

for query, match in results.items():
    if match:
        address, score = match
        print(f"{query} -> {address} ({score:.1f})")
```

### Scoring and Ranking

```python
from scoring import rank_matches, apply_business_rules

# Rank matches with quality classification
matches = [
    ("Drottninggatan 123", 95.0),
    ("Kungsgatan 45", 70.0),
    ("Götgatan 78", 55.0)
]

ranked = rank_matches(matches, min_score=60.0)
for match in ranked:
    print(f"Rank {match['rank']}: {match['address']} - "
          f"{match['score']:.1f} ({match['quality']})")

# Apply business rules
rules = {'min_quality': 'good', 'max_results': 3}
filtered = apply_business_rules(ranked, rules)
```

### Evaluation

```python
from evaluation import (
    calculate_precision_recall,
    evaluate_score_distribution,
    calculate_match_rate
)

# Evaluate matching performance
true_matches = [("query1", "match1"), ("query2", "match2")]
predicted = [("query1", "match1"), ("query2", "wrong")]

metrics = calculate_precision_recall(true_matches, predicted)
print(f"Precision: {metrics['precision']:.2f}")
print(f"Recall: {metrics['recall']:.2f}")
print(f"F1 Score: {metrics['f1_score']:.2f}")

# Analyze score distribution
scores = [95.0, 85.0, 75.0, 65.0, 55.0]
stats = evaluate_score_distribution(scores)
print(f"Mean: {stats['mean']:.1f}")
print(f"Median: {stats['median']:.1f}")
```

## Interactive Demo

Open the Jupyter notebook for an interactive demonstration:

```bash
jupyter notebook notebooks/demo.ipynb
```

The demo notebook includes:
- Address normalization examples
- Fuzzy matching with sample data
- Similarity score comparisons
- Batch matching and evaluation
- Quality distribution analysis

## Sample Data

The `data/` directory contains synthetic Swedish address datasets:

- **customers.csv**: 30 customer addresses across Swedish cities
- **leads.csv**: 30 lead addresses with intentional variations (typos, different spellings)

These datasets are useful for testing and demonstrating the matching capabilities.

## Modules

### normalization

Functions for normalizing Swedish addresses:
- `normalize_address()`: Comprehensive address normalization
- `normalize_swedish_chars()`: Convert å, ä, ö to a, o
- `normalize_street_types()`: Standardize gata/väg variations
- `extract_street_number()`: Extract house numbers
- `extract_postal_code()`: Extract Swedish postal codes

### matching

Fuzzy matching functions using RapidFuzz:
- `fuzzy_match_address()`: Match query against multiple candidates
- `find_best_match()`: Get single best match
- `similarity_score()`: Calculate similarity between two addresses
- `batch_match_addresses()`: Match multiple queries efficiently

### scoring

Scoring and quality assessment:
- `calculate_match_confidence()`: Calculate confidence scores
- `classify_match_quality()`: Classify as excellent/good/fair/poor
- `rank_matches()`: Rank and annotate matches
- `apply_business_rules()`: Apply custom filtering rules

### evaluation

Performance evaluation tools:
- `calculate_precision_recall()`: Calculate precision, recall, F1
- `calculate_accuracy()`: Calculate matching accuracy
- `evaluate_score_distribution()`: Analyze score statistics
- `calculate_match_rate()`: Calculate successful match rates

## Dependencies

- **rapidfuzz** (>=3.0.0): Fast fuzzy string matching
- **pandas** (>=2.0.0): Data manipulation
- **numpy** (>=1.24.0): Numerical operations
- **jupyter** (>=1.0.0): Interactive notebooks
- **notebook** (>=7.0.0): Jupyter notebook interface

## Use Cases

This library is designed for:
- **Customer deduplication**: Find duplicate customer records
- **Lead matching**: Match leads to existing customers
- **Address standardization**: Clean and normalize address data
- **Data integration**: Match addresses from different sources
- **Quality assessment**: Evaluate address data quality

## Swedish-Specific Features

- **Character normalization**: Handles å → a, ä → a, ö → o conversions
- **Street type variations**: Recognizes gata/gatan, väg/vägen patterns
- **Postal code extraction**: Supports "123 45" and "12345" formats
- **Common abbreviations**: Handles Swedish address conventions

## Development

This is a Python project used for internal purposes at Klara Färdiga Städ.

## License

For internal use at Klara Färdiga Städ.

## Contributing

This is an internal project. For questions or suggestions, contact the development team.

## Roadmap

Future enhancements:
- [ ] Add support for apartment numbers
- [ ] Implement geographic distance-based scoring
- [ ] Add machine learning-based matching
- [ ] Support for more Swedish address formats
- [ ] Integration with Swedish address APIs
- [ ] Performance optimization for large datasets
