"""Random String Detector."""
from types import MappingProxyType
from typing import Dict, Union
from random_string_detector.bigrams import ENGLISH

# Common keyboard patterns
KEYBOARD_PATTERNS = [
    # QWERTY row patterns
    "qwerty", "qwertyuiop", "asdfghjkl", "zxcvbnm",
    "qwertyuiopasdfghjklzxcvbnm",
    
    # Partial QWERTY patterns
    "qwer", "wert", "erty", "rtyu", "tyui", "yuio", "uiop",
    "asdf", "sdfg", "dfgh", "fghj", "ghjk", "hjkl",
    "zxcv", "xcvb", "cvbn", "vbnm",
    
    # Reverse patterns
    "poiuytrewq", "lkjhgfdsa", "mnbvcxz",
    
    # Number patterns
    "1234567890", "123456", "654321", "0987654321",
    
    # Letter sequences
    "abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba",
    "abcdef", "fedcba",
]

def is_keyboard_pattern(text):
    """Check if text matches common keyboard patterns"""
    text_lower = text.lower()
    
    # Check exact matches
    if text_lower in KEYBOARD_PATTERNS:
        return True
    
    # Check if it's a substring of a longer pattern
    for pattern in KEYBOARD_PATTERNS:
        if len(text_lower) >= 4 and text_lower in pattern:
            return True
    
    # Check for sequential characters (easy to type)
    if len(text_lower) >= 4:
        # Check for sequential letters
        for i in range(len(text_lower) - 3):
            if (ord(text_lower[i+1]) - ord(text_lower[i]) == 1 and
                ord(text_lower[i+2]) - ord(text_lower[i+1]) == 1 and
                ord(text_lower[i+3]) - ord(text_lower[i+2]) == 1):
                return True
        
        # Check for sequential numbers
        if text_lower.isdigit():
            for i in range(len(text_lower) - 3):
                if (int(text_lower[i+1]) - int(text_lower[i]) == 1 and
                    int(text_lower[i+2]) - int(text_lower[i+1]) == 1 and
                    int(text_lower[i+3]) - int(text_lower[i+2]) == 1):
                    return True
    
    return False


class RandomStringDetector(object):
    """Class to detect random typing in a given text."""

    def __init__(
            self,
            bigrams_probs: Union[MappingProxyType[str,
                                                  float], Dict[str, float]] = ENGLISH,
            common_bigrams_threshold: float = 0.1,
            uncommon_bigrams_threshold: float = 0.005,
            duplicated_bigrams_threshold: float = 0.33,
            allow_numbers: bool = False):
        """Initialize a RandomStringDetector object.

        Attributes:
        - bigrams_probs (dict): dictionary with bigrams and their probabilities.
        - common_bigrams_threshold (float): threshold to determine if a bigram is common or not.
        - uncommon_bigrams_threshold (float): threshold to determine if a word is random typing or not.
        - duplicated_bigrams_threshold (float): threshold to determine if a word is random typing or not.
        - allow_numbers (bool): whether to allow numbers in the string
        """
        self.bigrams = bigrams_probs
        self.common_bigrams_threshold = common_bigrams_threshold
        self.uncommon_bigrams_threshold = uncommon_bigrams_threshold
        self.duplicated_bigrams_threshold = duplicated_bigrams_threshold
        self.allow_numbers = allow_numbers

    def is_random_word(self, word: str):
        """Check if a word is random typing or not.

        Args:
        - word: word to check.

        Returns:
        - True if the word is random typing, False otherwise
        """
        # Allow only words longer than 3 characters
        if self.allow_numbers:
            # Allow letters and numbers
            if len(word) < 4:
                return False
        else:
            # Allow only letters
            if len(word) < 4 or not word.isalpha():
                return False

        # Return True if the word contains only digits (pure numbers are always random)
        if word.isdigit():
            return True
        
        # Return True if the word is a single character repeated multiple times
        if len(set(word)) == 1:
            return True

        # Check for keyboard patterns (only for alphabetic words)
        if word.isalpha() and is_keyboard_pattern(word):
            return True

        word = word.lower()

        # Get list of bigrams from the word
        bigrams = [word[i:i + 2] for i in range(len(word) - 1)]

        # For allow_numbers: treat any bigram with a digit or '-' as uncommon
        num_common_bigrams = 0
        num_uncommon_bigrams = 0
        num_duplicated_bigrams = len(bigrams) - len(set(bigrams))
        for bigram in bigrams:
            if self.allow_numbers and (any(c.isdigit() or c == '-' for c in bigram)):
                num_uncommon_bigrams += 1
            elif self.bigrams.get(bigram, 0) > self.common_bigrams_threshold:
                num_common_bigrams += 1
            else:
                num_uncommon_bigrams += 1

        # Higher number wins
        # if uncommon_bigrams is more than n of the bigrams, return True
        if len(bigrams) > 0 and num_uncommon_bigrams / len(bigrams) > self.uncommon_bigrams_threshold:
            return True
        # if more than n of the bigrams are duplicated, return True
        elif len(bigrams) > 0 and num_duplicated_bigrams / len(bigrams) > self.duplicated_bigrams_threshold:
            return True
        else:
            return False

    def __call__(self, text: str, threshold: float = 0.5):
        """Check if the input text of a given user is random typing using pt_bigrams_dict.

        Args:
        - text: input text of a given user.
        - threshold: threshold to determine if a word is random typing or not.

        Returns:
        - True if the input text is random typing, False otherwise
        """
        words = text.lower().split()
        if not words:  # Handle empty string case
            return False
            
        counter = 0
        for word in words:
            if self.is_random_word(word):
                counter += 1

        if counter / len(words) >= threshold:
            return True
        return False
