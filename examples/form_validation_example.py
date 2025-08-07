from random_string_detector import RandomStringDetector

# Initialize detector (allow numbers in valid strings)
detector = RandomStringDetector(allow_numbers=True)

def is_valid_input(text: str) -> bool:
    """Return False if the input looks like random garbage."""
    return not detector(text.strip())

examples = [
    "asdjf2398rj",                            # random typing
    "qwerty",                                 # keyboard pattern
    "123e4567-e89b-12d3-a456-426614174000",   # UUID
    "Chicago",                                # valid city
    "hello world"                             # valid text
]

for text in examples:
    status = "Valid" if is_valid_input(text) else "Suspicious entry detected"
    print(f"{status} — '{text}'")

# Suspicious entry detected — 'asdjf2398rj'
# Suspicious entry detected — 'qwerty'
# Suspicious entry detected — '123e4567-e89b-12d3-a456-426614174000'
# Valid — 'Chicago'
# Valid — 'hello world'