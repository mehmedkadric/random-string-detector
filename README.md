# random_string_detector

This package helps you identify random strings within text data by analyzing the frequency of bigrams (two-letter combinations). It leverages the fact that certain bigrams are more common in natural language than others. By comparing the bigram frequencies in your text data to those in a reference language corpus, you can spot strings of characters that deviate from typical language patterns.

See [**Explanation**](#explanation) for more information.

## Features

- Detect random strings of English and other languages.
- Specify thresholds to control the sensitivity of the detection.
- **Supported Languages:** English and Portuguese.

> Do you want to add support for another language? Open an issue or a pull request.
> 
> See [**contributing section**](#contributing) for more information.

## Installation

You can install the package using pip:

```bash
pip install random-string-detector
```

## Usage

```python
from random_string_detector import RandomStringDetector

detector = RandomStringDetector()
detector("Hello World") # False
detector("aowkaoskaos") # True
detector("aoekaoekaoe") # True
```

## Explanation

Using the fact that the expected number of 2-letter combinations in English is 676, and this includes combinations with identical letters and combinations with distinct letters, it is possible to use low-frequency bigrams in order to detect random strings of English letters.

As per [**Peter Norvig analysis**](http://norvig.com/mayzner.html), the most frequent bigram in English language is "th". On the other side, "zx" is not so common. By comparing the frequency of different bigrams in your text data to those in the English language corpus, you can identify strings of characters that do not fit typical language patterns.

This package contains a class named `RandomStringDetector()` and language-specific bigram frequency dictionaries that can be combined to detect random strings in English and other languages. The threshold value (between 0 and 100) can be used to control the sensitivity of the detection. Higher values represent more frequent bigrams (like "th") and lower values represent less frequent bigrams (like "zx").

Only words with length greater than 4 are considered.

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
