#!/usr/bin/env python3
"""
Baseline performance test for random-string-detector
"""

from random_string_detector import RandomStringDetector

def run_baseline_test():
    detector = RandomStringDetector(uncommon_bigrams_threshold=0.01)
    detector_with_numbers = RandomStringDetector(allow_numbers=True)
    
    # Positive cases (should be detected as random)
    positive_cases = [
        "aowkaoskaos",      # Random typing
        "gasdgz",           # Random typing 
        "dgagfdag",         # Random typing 
        "jglngm",           # Random typing
        "gdkgag",           # Random typing
        "adgpoagda",        # Random typing
        "gdaskoga",         # Random typing
        "iqweutp",          # Random typing
        "mvcamp",           # Random typing
        "qwertyuiop",       # Keyboard pattern
        "asdfghjkl",        # Keyboard pattern
        "zxcvbnm",          # Keyboard pattern
        "qwerty",           # Keyboard pattern
        "asdfgh",           # Keyboard pattern
        "zxcvbn",           # Keyboard pattern
        "abcdef",           # Sequential letters
        "fedcba",           # Reverse sequential
        "aaaaa",            # Repeated character
        "ththththth",       # Repeated bigram
        "hehehehehe",       # Repeated bigram
        "ininininin",       # Repeated bigram
        "aowkaoskaosaowkaoskaosaowkaoskaos",  # Very long random
    ]
    
    # Negative cases (should NOT be detected as random)
    negative_cases = [
        "hello",            # Valid English word
        "world",            # Valid English word
        "computer",         # Valid English word
        "programming",      # Valid English word
        "algorithm",        # Valid English word
        "the",              # Common word
        "and",              # Common word
        "for",              # Common word
        "you",              # Common word
        "with",             # Common word
        "john",             # Common name
        "mary",             # Common name
        "david",            # Common name
        "sarah",            # Common name
        "michael",          # Common name
        "api",              # Technical term
        "url",              # Technical term
        "sql",              # Technical term
        "xml",              # Technical term
        "hi",               # Short valid word
        "ok",               # Short valid word
        "no",               # Short valid word
        "yes",              # Short valid word
        "supercalifragilisticexpialidocious",  # Very long valid word
        "Hello",            # Capitalized word
        "WORLD",            # All caps
        "hElLo",            # Mixed case
        "password",         # Common password
        "admin",            # Common admin
        "root",             # Common root
        "user",             # Common user
        "guest",            # Common guest
        "test",             # Common test
        "demo",             # Common demo
        "sample",           # Common sample
    ]
    
    print("BASELINE PERFORMANCE TEST")
    print("=" * 50)
    
    # Test positive cases
    print("\nPOSITIVE CASES (should be detected as random):")
    print("-" * 50)
    positive_correct = 0
    positive_total = len(positive_cases)
    
    for text in positive_cases:
        result = detector(text)
        status = "✓" if result else "✗"
        print(f"{status} '{text}' -> {result}")
        if result:
            positive_correct += 1
    
    # Test negative cases
    print("\nNEGATIVE CASES (should NOT be detected as random):")
    print("-" * 50)
    negative_correct = 0
    negative_total = len(negative_cases)
    
    for text in negative_cases:
        result = detector(text)
        status = "✓" if not result else "✗"
        print(f"{status} '{text}' -> {result}")
        if not result:
            negative_correct += 1
    
    # Test with numbers
    print("\nWITH NUMBERS ALLOWED:")
    print("-" * 50)
    number_cases = [
        # Valid usernames with numbers (should be False - not random)
        ("chicagofan23", False),      # Updated to match README documentation
        ("basketballfan99", False),   # Sports fan username
        ("musiclover2024", False),    # Music lover with year
        ("johnsmith1985", False),     # Name with birth year
        ("techgeek2023", False),      # Tech enthusiast username
        ("guitarplayer42", False),    # Hobby-based username
        ("codingwizard123", False),   # Programming username
        
        # Generic/short usernames (should be True - random)
        ("user123", True),            # Generic username
        ("test456", True),            # Test account
        ("admin999", True),           # Admin account
        ("guest789", True),           # Guest account
        ("temp123", True),            # Temporary account
        
        # Edge cases testing 8-character threshold
        ("username1", False),         # 9 chars - meaningful word
        ("abc1234", True),            # 7 chars - high digit ratio
        ("dev2024", True),            # Short abbreviated form
        
        # Random patterns (should be True)
        ("aowkaoskaos", True),        # Random typing
        ("qwerty", True),             # Keyboard pattern
        ("abc123def", True),          # Mixed alphanumeric
        ("a1b2c3d4e5f6", True),       # Hex hash pattern
    ]
    
    number_correct = 0
    number_total = len(number_cases)
    
    for text, expected in number_cases:
        result = detector_with_numbers(text)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{text}' -> {result} (expected {expected})")
        if result == expected:
            number_correct += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("BASELINE RESULTS:")
    print(f"Positive cases: {positive_correct}/{positive_total} ({positive_correct/positive_total*100:.1f}%)")
    print(f"Negative cases: {negative_correct}/{negative_total} ({negative_correct/negative_total*100:.1f}%)")
    print(f"With numbers: {number_correct}/{number_total} ({number_correct/number_total*100:.1f}%)")
    
    total_correct = positive_correct + negative_correct + number_correct
    total_tests = positive_total + negative_total + number_total
    print(f"Overall accuracy: {total_correct}/{total_tests} ({total_correct/total_tests*100:.1f}%)")
    
    return {
        'positive_accuracy': positive_correct/positive_total,
        'negative_accuracy': negative_correct/negative_total,
        'number_accuracy': number_correct/number_total,
        'overall_accuracy': total_correct/total_tests
    }

if __name__ == "__main__":
    run_baseline_test() 