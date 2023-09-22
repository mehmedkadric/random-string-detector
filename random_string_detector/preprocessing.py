"""This module contains the TextPreprocessing class."""
import re
import unicodedata
from typing import List
from string import punctuation
from collections import Counter
from unidecode import unidecode

class TextPreprocessing(object):
    """TextPreprocessing is a class that contains methods to process text."""
    def __init__(self, stopwords: List[str] = None):
        """Initialize TextPreprocessing object.

        Attributes:
        - stopwords: list of stopwords to remove from text
        """
        if stopwords and len(stopwords) > 0:
            self.stopwords = Counter(stopwords)
        else:
            self.stopwords = {}

    def remove_accents(self, text: str):
        """Remove accents from text.
        
        Args:
        - text: string to remove accents from
        
        Returns:
        - text without accents
        """
        return unidecode(text)

    def remove_stopwords(self, text: str, stopwords: List[str] = None):
        """Remove stopwords from text.

        Args:
        - text: string to remove stopwords from
        - stopwords: list of stopwords to remove from text

        Returns:
        - text without stopwords
        """
        if stopwords:
            stopwords = Counter(stopwords)
        else:
            stopwords = self.stopwords
        return ' '.join([w for w in text.split() if w not in stopwords])

    def remove_punctuation(self, text: str):
        """Remove punctuation from text.

        Args:
        - text: string to remove punctuation from

        Returns:
        - text without punctuation
        """
        return text.translate(str.maketrans('', '', punctuation))

    def non_ascii_to_ascii(self, text: str):
        """Remove characters such as emoji from strings.
        
        Args:
        - text: string to remove non-ascii characters from
        
        Returns:
        - text without non-ascii characters
        """
        return (
            unicodedata.normalize('NFKD', text)
            .encode('ascii', 'ignore')
            .decode('ascii')
        )

    def remove_numbers(self, text: str):
        """Remove numbers from text.
        
        Args:
        - text: string to remove numbers from
        
        Returns:
        - text without numbers
        """
        return re.sub(r'\d+', '', text)
    
    def __call__(self, text: str):
        """Process text.

        Args:
        - text: string to process

        Returns:
        - processed text
        """
        text = self.remove_accents(text)
        text = self.remove_punctuation(text)
        text = self.remove_stopwords(text)
        text = self.non_ascii_to_ascii(text)
        return text.strip()
