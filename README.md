# random-string-detector

This package helps you identify random strings within text data by analyzing the frequency of bigrams (two-letter combinations), keyboard patterns, and mixed alphanumeric patterns. It leverages the fact that certain bigrams are more common in natural language than others, and that random or structured patterns (like UUIDs, hashes, or keyboard walks) deviate from typical language patterns.

See [**Explanation**](#explanation) for more information.

## Features

- Detect random strings, keyboard patterns, UUIDs, hashes, license keys, and mixed alphanumeric strings.
- Specify thresholds to control the sensitivity of the detection.
- **Supported Languages:** English, Portuguese and French.
- Handles both single words and sentences.
- Detects random typing, keyboard walks, and random-looking identifiers.

> Do you want to add support for another language? Open an issue or a pull request.
> 
> See [**contributing section**](#contributing) for more information.

## Installation

You can install the package using pip:

```bash
pip install random-string-detector
```

## Usage
### Example 1: Single Word
```python
from random_string_detector import RandomStringDetector

detector = RandomStringDetector()
print(detector("Hello"))  # False
print(detector("aowkaoskaos"))  # True
print(detector("qwerty"))  # True
```

### Example 2: Sentence
```python
from random_string_detector import RandomStringDetector

detector = RandomStringDetector()
print(detector("the quick brown fox"))  # False
print(detector("the qwerty brown fox", threshold=0.25))  # True (because 'qwerty' is random)
```

### Example 3: Word + Number, UUID, Hash, License Key
```python
from random_string_detector import RandomStringDetector

detector = RandomStringDetector(allow_numbers=True)
print(detector("user123"))  # True (mixed alphanumeric, flagged as random)
print(detector("123e4567-e89b-12d3-a456-426614174000"))  # True (UUID)
print(detector("a1b2c3d4e5f6"))  # True (hex hash)
print(detector("AB12-CD34-EF56"))  # True (license key)
print(detector("abc123def"))  # True (mixed alphanumeric)
print(detector("chicagofan23"))  # False (valid username with numbers)
```

## Explanation

Using the fact that the expected number of 2-letter combinations in English is 676, and this includes combinations with identical letters and combinations with distinct letters, it is possible to use low-frequency bigrams in order to detect random strings of English letters.

The detector also checks for:
- **Keyboard patterns** (e.g. 'qwerty', 'asdfgh', 'zxcvbn')
- **UUIDs, hashes, license keys, and mixed alphanumeric strings** (e.g. '123e4567-e89b-12d3-a456-426614174000', 'a1b2c3d4e5f6', 'AB12-CD34-EF56', 'abc123def')
- **Pure numbers** (e.g. '123456') are always flagged as random

As per [**Peter Norvig analysis**](http://norvig.com/mayzner.html), the most frequent bigram in English language is "th". On the other side, "zx" is not so common. By comparing the frequency of different bigrams in your text data to those in the English language corpus, you can identify strings of characters that do not fit typical language patterns.

This package contains a class named `RandomStringDetector()` and language-specific bigram frequency dictionaries that can be combined to detect random strings in English and other languages. The threshold value (between 0 and 100) can be used to control the sensitivity of the detection. Higher values represent more frequent bigrams (like "th") and lower values represent less frequent bigrams (like "zx").

Only words with length greater than 3 are considered. Pure numbers are always flagged as random. Mixed alphanumeric strings (e.g. UUIDs, hashes, license keys) are flagged as random when `allow_numbers=True`.

The boolean `allow_numbers` argument (default `False`) will allow detection of random strings that include numbers (such as UUIDs, hashes, and license keys). This is useful if you are validating whether or not a string is random, as many random identifiers include both letters and numbers.

## CI/CD

This project uses GitHub Actions for continuous integration and testing:

- **Tests**: Runs on every push and pull request to main/master branches
- **Coverage**: Runs weekly and on code changes to track test coverage
- **Python Versions**: Tests against Python 3.9, 3.10, 3.11, and 3.12

### Running Tests Locally

```bash
# Install in development mode
pip install -e .

# Run baseline tests
python baseline_test.py

# Run comprehensive tests
python -m unittest test -v

# Run with coverage
pip install coverage
coverage run --source=random_string_detector test.py
coverage run --source=random_string_detector baseline_test.py
coverage report
```

## Contributing

We happily accept any contributions and feedback. 😊

### Adding support for a new language

To add support for a new language, you need to follow these steps:

- Find a large text corpus in the language you want to add support for.
- Compute the bigram frequencies for the corpus (see [**/notebooks/portuguese.ipynb**](/notebooks/portuguese.ipynb) for an example).
- Add the bigram frequencies to [**/random_string_detector/bigrams/<language>.py**](/random_string_detector/bigrams).
- Import the bigram frequencies in [**/random_string_detector/bigrams/__init__.py**](/random_string_detector/bigrams/__init__.py).

> **Note:** The bigram frequencies should be a dictionary with the bigram as the key and the normalized frequency as the value. The bigram should be a string with the two letters concatenated. The normalized frequency should be a float between 0 and 100.

If you have any questions, issues, or suggestions, please feel free to contact us.

## License

This package is distributed under the MIT license.

See [**LICENSE**](LICENSE) for more information.
