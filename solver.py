# from os import cpu_count
from pathlib import Path

from scipy.stats import entropy

# from tqdm.contrib.concurrent import process_map
from tqdm import tqdm

WORD_LEN = 5
MATCHES = []
for a in range(WORD_LEN + 1):
    for b in range(WORD_LEN + 1 - a):
        MATCHES.append(f"{a}a{b}b")


def get_valid_words(valid_words):
    """Filter words and return those containing 5 unique characters"""
    return [
        word
        for word in valid_words
        if len(word) == WORD_LEN and len(set(word)) == WORD_LEN
    ]


def match(word, guess):
    """?a?b

    "a" is the number of matched characters in the correct position,
    "b" is the number of matched characters in a wrong position
    """
    a, b = 0, 0
    matched_char = set()
    for i in range(WORD_LEN):
        if word[i] == guess[i]:
            a += 1
            matched_char.add(word[i])
    b = len(set(word).intersection(set(guess)).difference(matched_char))
    return f"{a}a{b}b"


def update_word_list(valid_words, guess, a_chars, b_chars):
    result = []
    for word in valid_words:
        try:
            for a_c in a_chars:
                assert word.index(a_c) == guess.index(a_c)
            for b_c in b_chars:
                assert word.index(b_c) != guess.index(b_c)
            result.append(word)
        except Exception:
            pass
    return result


def eval_guess(guess, valid_words):
    match_dist = {mat: 0 for mat in MATCHES}

    # compare to the word list
    for word in valid_words:
        match_dist[match(word, guess)] += 1

    # compute entropy
    total = sum(list(match_dist.values()))
    probs = [val / total for val in match_dist.values()]
    return entropy(probs)


def get_best_guess(valid_words, all_words):
    # TODO: multiprocessing
    max_entropy = 0
    best_guess = ""
    for guess in tqdm(all_words):
        ent = eval_guess(guess, valid_words)
        if ent > max_entropy:
            max_entropy = ent
            best_guess = guess
    return best_guess


if __name__ == "__main__":
    # construct word list
    word_list_path = Path("data") / "words_alpha.txt"
    with open(word_list_path, "r") as fp:
        valid_words = get_valid_words([word.rstrip() for word in fp])
    all_words = [word for word in valid_words]

    n_trials = 0
    while True:
        # guess a word
        best_guess = (
            get_best_guess(valid_words, all_words)
            if WORD_LEN != 5 or n_trials != 0
            else "tares"
        )
        print(
            f"\nThe best guess is '{best_guess}' (over {len(valid_words)}/{len(all_words)})."
        )

        # enter the guessing result
        guess = input("The actual guess: ")
        a_chars = input("The green characters: ")
        b_chars = input("The yellow characters: ")
        valid_words = update_word_list(valid_words, guess, a_chars, b_chars)
        print(valid_words)
        if len(a_chars) == 5:
            break

        n_trials += 1
