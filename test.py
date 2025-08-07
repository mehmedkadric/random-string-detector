#!/usr/bin/env python3
"""
Comprehensive test suite for random-string-detector
positive test cases (should be detected as random)
negative test cases (should not be detected as random)
"""

import unittest
from random_string_detector import RandomStringDetector


class TestRandomStringDetector(unittest.TestCase):
    def setUp(self):
        self.detector = RandomStringDetector(uncommon_bigrams_threshold=0.01)
        self.detector_with_numbers = RandomStringDetector(allow_numbers=True)

    def test_positive_cases_should_be_detected_as_random(self):
        """Test cases that SHOULD be detected as random"""
        
        # Baseline positive cases (from baseline_test.py)
        self.assertTrue(self.detector("aowkaoskaos"), "Random typing")
        self.assertTrue(self.detector("gasdgz"), "Random typing")
        self.assertTrue(self.detector("dgagfdag"), "Random typing")
        self.assertTrue(self.detector("jglngm"), "Random typing")
        self.assertTrue(self.detector("gdkgag"), "Random typing")
        self.assertTrue(self.detector("adgpoagda"), "Random typing")
        self.assertTrue(self.detector("gdaskoga"), "Random typing")
        self.assertTrue(self.detector("iqweutp"), "Random typing")
        self.assertTrue(self.detector("mvcamp"), "Random typing")
        
        # Keyboard patterns (from baseline)
        self.assertTrue(self.detector("qwertyuiop"), "Keyboard pattern")
        self.assertTrue(self.detector("asdfghjkl"), "Keyboard pattern")
        self.assertTrue(self.detector("zxcvbnm"), "Keyboard pattern")
        self.assertTrue(self.detector("qwerty"), "Keyboard pattern")
        self.assertTrue(self.detector("asdfgh"), "Keyboard pattern")
        self.assertTrue(self.detector("zxcvbn"), "Keyboard pattern")
        
        # Sequential patterns (from baseline)
        self.assertTrue(self.detector("abcdef"), "Sequential letters")
        self.assertTrue(self.detector("fedcba"), "Reverse sequential")
        
        # Repeated patterns (from baseline)
        self.assertTrue(self.detector("aaaaa"), "Repeated character")
        self.assertTrue(self.detector("ththththth"), "Repeated bigram")
        self.assertTrue(self.detector("hehehehehe"), "Repeated bigram")
        self.assertTrue(self.detector("ininininin"), "Repeated bigram")
        
        # Very long random (from baseline)
        self.assertTrue(self.detector("aowkaoskaosaowkaoskaosaowkaoskaos"), "Very long random")
        
        # Additional comprehensive test cases
        self.assertTrue(self.detector("xqwerty"), "Random typing")
        self.assertTrue(self.detector("mnbvcxz"), "Random typing")
        self.assertTrue(self.detector("poiuyt"), "Random typing")
        self.assertTrue(self.detector("lkjhgf"), "Random typing")
        self.assertTrue(self.detector("qazwsx"), "Random typing")
        self.assertTrue(self.detector("edcrfv"), "Random typing")
        self.assertTrue(self.detector("tgbyhn"), "Random typing")
        self.assertTrue(self.detector("ujmikl"), "Random typing")
        self.assertTrue(self.detector("rfvbnm"), "Random typing")
        
        # Mixed content (should be detected due to random parts)
        self.assertTrue(self.detector("hello xqwerty"), "Mixed valid and random")
        self.assertTrue(self.detector("mnbvcxz world"), "Mixed random and valid")

    def test_negative_cases_should_not_be_detected_as_random(self):
        """test cases that should NOT be detected as random"""
        
        # Valid English words
        self.assertFalse(self.detector("hello"), "Valid English word")
        self.assertFalse(self.detector("world"), "Valid English word")
        self.assertFalse(self.detector("computer"), "Valid English word")
        self.assertFalse(self.detector("programming"), "Valid English word")
        self.assertFalse(self.detector("algorithm"), "Valid English word")
        
        # Common words
        self.assertFalse(self.detector("the"), "Common word")
        self.assertFalse(self.detector("and"), "Common word")
        self.assertFalse(self.detector("for"), "Common word")
        self.assertFalse(self.detector("you"), "Common word")
        self.assertFalse(self.detector("with"), "Common word")
        
        # Names
        self.assertFalse(self.detector("john"), "Common name")
        self.assertFalse(self.detector("mary"), "Common name")
        self.assertFalse(self.detector("david"), "Common name")
        self.assertFalse(self.detector("sarah"), "Common name")
        self.assertFalse(self.detector("michael"), "Common name")
        
        # Technical terms
        self.assertFalse(self.detector("api"), "Technical term")
        self.assertFalse(self.detector("url"), "Technical term")
        self.assertFalse(self.detector("sql"), "Technical term")
        self.assertFalse(self.detector("xml"), "Technical term")
        
        # Short valid words
        self.assertFalse(self.detector("hi"), "Short valid word")
        self.assertFalse(self.detector("ok"), "Short valid word")
        self.assertFalse(self.detector("no"), "Short valid word")
        self.assertFalse(self.detector("yes"), "Short valid word")
        
        # Very long valid word
        self.assertFalse(self.detector("supercalifragilisticexpialidocious"), "Very long valid word")
        
        # Mixed case
        self.assertFalse(self.detector("Hello"), "Capitalized word")
        self.assertFalse(self.detector("WORLD"), "All caps")
        self.assertFalse(self.detector("hElLo"), "Mixed case")
        
        # Common password/username patterns (these are valid words)
        self.assertFalse(self.detector("password"), "Common password")
        self.assertFalse(self.detector("admin"), "Common admin")
        self.assertFalse(self.detector("root"), "Common root")
        self.assertFalse(self.detector("user"), "Common user")
        self.assertFalse(self.detector("guest"), "Common guest")
        self.assertFalse(self.detector("test"), "Common test")
        self.assertFalse(self.detector("demo"), "Common demo")
        self.assertFalse(self.detector("sample"), "Common sample")

    def test_with_numbers_allowed(self):
        """Test cases with allow_numbers=True"""
        
        # Baseline number cases (updated to match README documentation)
        self.assertFalse(self.detector_with_numbers("chicagofan23"), "Username with numbers - valid username")
        self.assertTrue(self.detector_with_numbers("aowkaoskaos"), "Random typing")
        self.assertTrue(self.detector_with_numbers("qwerty"), "Keyboard pattern")
        
        # Additional number test cases
        self.assertTrue(self.detector_with_numbers("123456"), "Sequential numbers")
        self.assertTrue(self.detector_with_numbers("654321"), "Reverse sequential numbers")
        
        # Test with underscores (should be rejected as non-alphabetic)
        self.assertTrue(self.detector_with_numbers("john_doe"), "Username with underscores")

        # Valid usernames with numbers (should NOT be detected as random)
        # Long usernames with meaningful content + numbers
        self.assertFalse(self.detector_with_numbers("basketballfan99"), "Sports fan username")
        self.assertFalse(self.detector_with_numbers("musiclover2024"), "Music lover with year")
        self.assertFalse(self.detector_with_numbers("johnsmith1985"), "Name with birth year")
        self.assertFalse(self.detector_with_numbers("techgeek2023"), "Tech enthusiast username")
        self.assertFalse(self.detector_with_numbers("guitarplayer42"), "Hobby-based username")
        self.assertFalse(self.detector_with_numbers("bookworm1990"), "Interest-based username")
        self.assertFalse(self.detector_with_numbers("traveler2022"), "Traveler username")
        self.assertFalse(self.detector_with_numbers("photographer88"), "Professional username")
        self.assertFalse(self.detector_with_numbers("gamingmaster2024"), "Gaming username")
        self.assertFalse(self.detector_with_numbers("codingwizard123"), "Programming username")
        
        # Generic/short usernames with numbers (SHOULD be detected as random)
        # Short, generic patterns that are likely auto-generated or low-effort
        self.assertTrue(self.detector_with_numbers("user123"), "Generic username")
        self.assertTrue(self.detector_with_numbers("test456"), "Test account")
        self.assertTrue(self.detector_with_numbers("admin999"), "Admin account")
        self.assertTrue(self.detector_with_numbers("guest789"), "Guest account")
        self.assertTrue(self.detector_with_numbers("temp123"), "Temporary account")
        self.assertTrue(self.detector_with_numbers("demo567"), "Demo account")
        self.assertTrue(self.detector_with_numbers("new2024"), "Generic new user")
        self.assertTrue(self.detector_with_numbers("user999"), "Generic user pattern")
        self.assertTrue(self.detector_with_numbers("acc123"), "Account abbreviation")
        self.assertTrue(self.detector_with_numbers("id4567"), "ID pattern")

        # UUIDs, hashes, license keys, and mixed alphanumeric strings (should be detected as random)
        self.assertTrue(self.detector_with_numbers("123e4567-e89b-12d3-a456-426614174000"), "UUID")
        self.assertTrue(self.detector_with_numbers("a1b2c3d4e5f6"), "Hex hash")
        self.assertTrue(self.detector_with_numbers("AB12-CD34-EF56"), "License key")
        self.assertTrue(self.detector_with_numbers("550e8400-e29b-41d4-a716-446655440000"), "UUID v4")
        self.assertTrue(self.detector_with_numbers("f47ac10b-58cc-4372-a567-0e02b2c3d479"), "UUID v4")
        self.assertTrue(self.detector_with_numbers("abc123def"), "Mixed alphanumeric")
        self.assertTrue(self.detector_with_numbers("123abc456"), "Mixed alphanumeric")
        self.assertTrue(self.detector_with_numbers("test123user"), "Mixed alphanumeric")
        self.assertTrue(self.detector_with_numbers("user123test"), "Mixed alphanumeric")
        self.assertTrue(self.detector_with_numbers("a1b2c3"), "Mixed alphanumeric")
        self.assertTrue(self.detector_with_numbers("1a2b3c"), "Mixed alphanumeric")
        
        # Edge cases - borderline examples
        # These test the 8-character threshold and other edge conditions
        self.assertTrue(self.detector_with_numbers("abc1234"), "7 chars - high digit ratio")
        self.assertFalse(self.detector_with_numbers("username1"), "9 chars - meaningful word")
        self.assertTrue(self.detector_with_numbers("usr1234"), "7 chars - abbreviated generic")
        self.assertFalse(self.detector_with_numbers("developer2024"), "Long meaningful username")
        self.assertTrue(self.detector_with_numbers("dev2024"), "Short abbreviated form")

    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        
        # Too short
        self.assertFalse(self.detector(""), "Empty string")
        self.assertFalse(self.detector("a"), "Single character")
        self.assertFalse(self.detector("aa"), "Two characters")
        self.assertFalse(self.detector("aaa"), "Three characters")
        
        # Non-alphabetic (should be rejected)
        self.assertFalse(self.detector("hello!"), "Word with punctuation")
        self.assertFalse(self.detector("hello-world"), "Word with hyphen")
        self.assertFalse(self.detector("hello_world"), "Word with underscore")
        
        # With numbers (should be rejected without allow_numbers)
        self.assertFalse(self.detector("hello123"), "Word with numbers")
        self.assertFalse(self.detector("123hello"), "Numbers with word")
        self.assertFalse(self.detector("h3ll0"), "Leetspeak")

    def test_sentence_level(self):
        """Test sentence-level detection"""
        
        # Valid sentences
        self.assertFalse(self.detector("hello world"), "Valid sentence")
        self.assertFalse(self.detector("the quick brown fox"), "Valid sentence")
        self.assertFalse(self.detector("programming is fun"), "Valid sentence")
        
        # Sentences with random content
        self.assertTrue(self.detector("hello xqwerty"), "Sentence with random word")
        self.assertTrue(self.detector("mnbvcxz world"), "Sentence with random word")
        self.assertTrue(self.detector("the qwerty brown fox", threshold=0.25), "Sentence with keyboard pattern")

    def test_multi_language_support(self):
        """Test detection with different language bigram data"""
        
        # English (default)
        english_detector = RandomStringDetector()
        self.assertTrue(english_detector("xqwerty"), "English: Random typing")
        self.assertFalse(english_detector("hello"), "English: Valid word")
        
        # Portuguese
        from random_string_detector.bigrams import PORTUGUESE_WITHOUT_ACCENTS
        portuguese_detector = RandomStringDetector(bigrams_probs=PORTUGUESE_WITHOUT_ACCENTS)
        self.assertTrue(portuguese_detector("mnbvcxz"), "Portuguese: Random typing")
        self.assertFalse(portuguese_detector("olá"), "Portuguese: Valid word")
        
        # French
        from random_string_detector.bigrams import FRENCH_WITHOUT_ACCENTS
        french_detector = RandomStringDetector(bigrams_probs=FRENCH_WITHOUT_ACCENTS)
        self.assertTrue(french_detector("poiuyt"), "French: Random typing")
        self.assertFalse(french_detector("bonjour"), "French: Valid word")

    def test_cross_language_examples(self):
        """Test words that are not random in one language but random in the other two."""
        from random_string_detector.bigrams import ENGLISH, PORTUGUESE_WITHOUT_ACCENTS, FRENCH_WITHOUT_ACCENTS
        eng = RandomStringDetector(bigrams_probs=ENGLISH, uncommon_bigrams_threshold=0.005)
        por = RandomStringDetector(bigrams_probs=PORTUGUESE_WITHOUT_ACCENTS, uncommon_bigrams_threshold=0.005)
        fre = RandomStringDetector(bigrams_probs=FRENCH_WITHOUT_ACCENTS, uncommon_bigrams_threshold=0.005)

        # 'quartz': Not random in ENGLISH, random in other two
        self.assertFalse(eng("quartz"))
        self.assertTrue(por("quartz"))
        self.assertTrue(fre("quartz"))

        # 'exquisite': Not random in FRENCH, random in other two
        self.assertTrue(eng("exquisite"))
        self.assertTrue(por("exquisite"))
        self.assertFalse(fre("exquisite"))

        # 'fizz': Not random in PORTUGUESE, random in other two
        self.assertTrue(eng("fizz"))
        self.assertFalse(por("fizz"))
        self.assertTrue(fre("fizz"))


if __name__ == '__main__':
    unittest.main()