# TRAligner

A Python package for text alignment with specialized support for Hebrew text processing.

## Installation

```bash
pip install traligner
```

## Features

- Text alignment using Smith-Waterman algorithm
- Support for Hebrew text with specialized matching methods
- Handling of abbreviations, gematria, and other Hebrew-specific text features
- Sequence scoring and merging capabilities
- Word embedding support for semantic similarity

## Quick Start

```python
import traligner as ta

# Align two texts
suspect_tokens = ["בראשית", "ברא", "אלהים", ]
source_tokens = ["בראשית", "ברא", "אלוהים",  ]

alignment_sequences, df_alignment, suspect_matrix, source_matrix = ta.alignment(
    suspect_tokens,
    source_tokens,
    match_score=3,
    mismatch_score=1,
    methods={}
)

# Score the alignment
score, sequences = ta.alignmentScore(alignment_sequences)
print(f"Alignment score: {score}")
```

### The Results

The alignment_sequences will look like this:
[[(0, 0, 1, 'exact_match'),
  (1, 1, 1, 'exact_match'),
  (2, 2, 1, 'exact_match')]]

The alignment_sequences variable is a list of lists, where each inner list represents a local alignment between the two texts. Each local alignment is a list of tuples.
Each tuple contains four elements:
a. The sequence of aligned tokens from the first input list
b. The sequence of aligned tokens from the second input list
c. The alignment score assigned to these tokens
d. The reason for the alignment



## Advanced Usage

### Using Word Embeddings and Lexicons

```python
# Initialize embedding model
import fasttext
embeding_model = fasttext.load_model("path/to/fasttext/model.bin")

# Initialize Lexicons
import trelasticext as ee # If you would like to use synonyms in Elasticsearch, you may load them from a file.
synonyms = ee.load_synonyms("path/to/elasticsearch/analysis/your_lexicon')


# In the following alignment example, the two texts exhibit word boundary errors,
# typographical mistakes, orthographic variations, differences in Gematria, 
# and the use of synonyms. However they are exactly similar. 

suspect_tokens = ["בראשית", "כרא", "ה'", "ח", "השמים", "ואת", "הארץ"]
source_tokens = ["בראשית", "ברא", "אלוהים", "שמונה", "השמיים", "ואתהארץ" ]


methods = {"ortography": ["י", "ו"],
...            "extra_seperators": [""],
...            "missing_seperators": [""],
...            "abbreviation": ["'"],
...            "morphology-embeding": [(embeding_model, 0.702)],
...           }

alignment_sequences, df_alignment, suspect_matrix, source_matrix = ta.alignment(
    suspect_tokens,
    source_tokens,
    methods=methods
)
```

### Results
[[(0, 0, 1, 'exact_match'),
  (1, 1, 0.8, 'ocr_replacables'),
  (2, 2, 1.0, 'synonym_simple_match'),
  (3, 3, 0.75, 'single_gematria_match'),
  (4, 4, 0.8280513747171923, 'morphology_embeding_match'),
  (5, 5, 0.8, 'missing_spaces_match'),
  (6, 5, 0.8, 'missing_spaces_match')]]

## License

MIT