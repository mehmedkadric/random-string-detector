from bigrams import en_bigrams_dict

def is_random_string(word, threshold):
    # Allow only words longer than 3 characters which contains only English alphabetic characters
    if len(word) < 4 or not word.isalpha():
        return False

    # Repeating characters
    if len(set(word)) == 1:
        return True

    # Turn word into lowercase
    word = word.lower()

    # Get list of bigrams from the word
    bigrams = [word[i:i + 2] for i in range(len(word) - 1)]

    # Get number of common and uncommon bigrams
    num_common_bigrams = sum(1 for bigram in bigrams if en_bigrams_dict.get(bigram, 0) > threshold)
    num_uncommon_bigrams = len(bigrams) - num_common_bigrams

    # Higher number wins
    if num_common_bigrams > num_uncommon_bigrams:
        return False
    else:
        return True

if __name__ == '__main__':
    print(is_random_string("Jdjfjfk", 0.1))