import unittest
import traligner as ta

class TestAlignment(unittest.TestCase):
    def test_basic_alignment(self):
        suspect_tokens = ["בראשית", "ברא", "אלהים", "ח", "השמים", "ואת", "הארץ"]
        source_tokens = ["בראשית", "ברא", "אלוהים", "שמונה", "השמים", "ואתהארץ" ]
        
        methods = {"ortography": ["י", "ו"],
           "extra_seperators": [""],
           "missing_seperators": [""],
           "abbreviation": ["'"],
           #"embeding": [(embeding_model, 0.75)],
           #"morphology-embeding": [(embeding_model, 0.702)],
           #"edit_distance": 0.75,
           "morphology": True
          }
        
        alignment_sequences, df_alignment, suspect_matrix, source_matrix = ta.alignment(
            suspect_tokens,
            source_tokens,
            match_score=3,
            mismatch_score=1,
            methods=methods
        )
        
        # Check that we got some alignment
        self.assertTrue(len(alignment_sequences) > 0)
        
    def test_is_abbreviation(self):
        # Test abbreviation detection
        self.assertTrue(ta.is_abbreviation("ר'"))
        self.assertFalse(ta.is_abbreviation("שלום"))
        
        # Test with get_spliter
        is_abbr, tokens = ta.is_abbreviation("ר'", get_spliter=True)
        self.assertTrue(is_abbr)
        self.assertTrue(len(tokens) > 0)

if __name__ == "__main__":
    unittest.main()