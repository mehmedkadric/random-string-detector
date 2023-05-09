# Random String Detector
## Instalation
```
pip install random-string-detector
```

## Example
```
from random_string_detector.random_string_detector import is_random_string

print(is_random_string("Home", 0.1)) # False
print(is_random_string("Jdjfjfk", 0.1)) # True
```

## Story behind
Using the fact that the expected number of 2-letter combinations in English is 676, 
and this includes combinations with identical letters and combinations with distinct letters, 
it is possible to use low-frequency bigrams in order to detect random strings of English letters.

As per [Peter Norvig analysis](http://norvig.com/mayzner.html), the most frequent bigram in English language is "th". 
On the other side, "zx" is not so common. 
By comparing the frequency of different bigrams in your text data to those in the English language corpus, 
you can identify strings of characters that do not fit typical language patterns.

Package contains a single method _is_random_string(word, threshold)_. 
The first argument represents a string/word 
and the second argument represents threshold value between 0 and 100. 
Higher values represent more frequent bigrams (like "th") and lower 
values represent less frequent bigrams (like "zx").

Only strings with length greater than 4 are considered as well as strings which contain only English characters.


We happily accept any contributions and feedback. 😊