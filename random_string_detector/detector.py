"""Random String Detector."""
from types import MappingProxyType
from typing import Dict, Union
from random_string_detector.bigrams import ENGLISH


class RandomStringDetector(object):
    """Class to detect random typing in a given text."""

    def __init__(
            self,
            bigrams_probs: Union[MappingProxyType[str,
                                                  float], Dict[str, float]] = ENGLISH,
            common_bigrams_threshold: float = 0.1,
            uncommon_bigrams_threshold: float = 0.5,
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
        # Return True if the word is a single character repeated multiple times
        if len(set(word)) == 1:
            return True

        word = word.lower()

        # Get list of bigrams from the word
        bigrams = [word[i:i + 2] for i in range(len(word) - 1)]

        # Get number of common, uncommon and duplicated bigrams
        num_common_bigrams = sum(
            1 for bigram in bigrams if self.bigrams.get(bigram, 0) > self.common_bigrams_threshold
        )

        num_uncommon_bigrams = len(bigrams) - num_common_bigrams
        num_duplicated_bigrams = len(bigrams) - len(set(bigrams))

        # Higher number wins
        # if uncommon_bigrams is more than n of the bigrams, return True
        if num_uncommon_bigrams / len(bigrams) > self.uncommon_bigrams_threshold:
            return True
        # if more than n of the bigrams are duplicated, return True
        elif num_duplicated_bigrams / len(bigrams) > self.duplicated_bigrams_threshold:
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
        counter = 0
        for word in text.lower().split():
            if self.is_random_word(word):
                counter += 1

        if counter / len(text.split()) >= threshold:
            return True
        return False
