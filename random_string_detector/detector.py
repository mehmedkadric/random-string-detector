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

    def _is_likely_random_alphanumeric_bigram(self, bigram: str, full_word: str) -> bool:
        """Check if an alphanumeric bigram is likely random or part of a structured pattern.
        
        Args:
        - bigram: the two-character bigram to check
        - full_word: the full word context
        
        Returns:
        - True if the bigram appears to be random, False if it's likely legitimate
        """
        # Check for patterns that suggest randomness first
        if self._has_alternating_pattern(full_word) or self._looks_like_hex(full_word):
            return True
        
        # For shorter words (< 10 chars), be more strict about numbers
        # This handles cases like "user123", "admin999" which should be flagged as random
        if len(full_word) < 10:
            # Count how many characters are letters vs digits
            letter_count = sum(1 for c in full_word if c.isalpha())
            digit_count = sum(1 for c in full_word if c.isdigit())
            
            # If less than 6 letters, or if digits make up >30% of the word, treat as random
            if letter_count < 6 or digit_count / len(full_word) > 0.3:
                return True
            else:
                # Short word that doesn't meet random criteria - legitimate
                return False
        
        # For longer words (>= 10 chars), be more lenient but still detect mixed patterns
        # This handles cases like "chicagofan23" which should not be flagged
        else:
            # Check for mixed alphanumeric patterns that suggest randomness
            # Count digit clusters vs letter clusters
            clusters = []
            current_cluster_type = None
            
            for char in full_word:
                char_type = 'digit' if char.isdigit() else 'letter'
                if char_type != current_cluster_type:
                    clusters.append(char_type)
                    current_cluster_type = char_type
            
            # If there are 3 or more alternating clusters, it's likely random
            # e.g., "test123user" -> ['letter', 'digit', 'letter'] = 3 clusters (random)
            # e.g., "chicagofan23" -> ['letter', 'digit'] = 2 clusters (legitimate)
            if len(clusters) >= 3:
                return True
                
            # If both characters are digits at the end, likely a legitimate number suffix
            if bigram.isdigit():
                bigram_pos = full_word.rfind(bigram)
                if bigram_pos >= len(full_word) - 4:  # Within last 4 characters
                    return False
            
            # Mixed letter-digit bigrams are often legitimate in longer words
            if any(c.isdigit() for c in bigram) and any(c.isalpha() for c in bigram):
                bigram_pos = full_word.rfind(bigram)
                # More lenient for longer words - allow digit bigrams in the last part
                if bigram_pos >= len(full_word) - 6:  # Within last 6 characters
                    return False
            
            # For longer words, be very lenient - only flag if it really looks random
            # This allows most legitimate usernames with numbers to pass
            return False
        
        # Default for shorter words: digit-containing bigrams are treated as random
        return True
    
    def _has_alternating_pattern(self, word: str) -> bool:
        """Check if word has alternating letter-digit pattern suggesting randomness."""
        if len(word) < 6:
            return False
        
        alternations = 0
        for i in range(len(word) - 1):
            if word[i].isalpha() != word[i+1].isalpha():
                alternations += 1
        
        # If more than half the transitions are alternating, it's likely random
        return alternations / (len(word) - 1) > 0.6
    
    def _looks_like_hex(self, word: str) -> bool:
        """Check if word looks like a hexadecimal string."""
        if len(word) < 8:
            return False
        
        hex_chars = set('0123456789abcdef')
        hex_count = sum(1 for c in word.lower() if c in hex_chars)
        
        # If most characters are valid hex and it's long enough, likely a hash
        return hex_count / len(word) > 0.8 and len(word) >= 8

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

        # Count bigrams, being more nuanced about alphanumeric patterns
        num_common_bigrams = 0
        num_uncommon_bigrams = 0
        num_duplicated_bigrams = len(bigrams) - len(set(bigrams))
        
        for bigram in bigrams:
            if self.allow_numbers and any(c.isdigit() for c in bigram):
                # For bigrams containing digits, be more selective
                # Only treat as uncommon if it looks like a random pattern
                if self._is_likely_random_alphanumeric_bigram(bigram, word):
                    num_uncommon_bigrams += 1
                else:
                    # Treat legitimate digit bigrams as common to avoid skewing the ratio
                    # This allows usernames like "chicagofan23" to not be flagged
                    num_common_bigrams += 1
            elif self.bigrams.get(bigram, 0) > self.common_bigrams_threshold:
                num_common_bigrams += 1
            else:
                num_uncommon_bigrams += 1

        # Adjust thresholds based on word length for more nuanced detection
        # Longer words are more likely to contain some uncommon bigrams naturally
        if len(word) >= 12:
            # Very long words: be very lenient (allow up to 20% uncommon bigrams)
            adjusted_uncommon_threshold = 0.2
        elif len(word) >= 10:
            # Long words: be more lenient (allow up to 15% uncommon bigrams)
            adjusted_uncommon_threshold = 0.15
        else:
            # Short words: use the original strict threshold
            adjusted_uncommon_threshold = self.uncommon_bigrams_threshold

        # Higher number wins
        # if uncommon_bigrams is more than n of the bigrams, return True
        if len(bigrams) > 0 and num_uncommon_bigrams / len(bigrams) > adjusted_uncommon_threshold:
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
