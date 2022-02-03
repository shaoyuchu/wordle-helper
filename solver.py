from pathlib import Path

from scipy.stats import entropy

from tqdm import tqdm

WORD_LEN = 5
MATCHES = []
for a in range(WORD_LEN + 1):
    for b in range(WORD_LEN + 1 - a):
        MATCHES.append(f"{a}a{b}b")


def get_valid_words(word_list):
    """Filter words and return those containing 5 unique characters"""
    return [
        word
        for word in word_list
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


def update_word_list(word_list, guess, guess_result):
    return [word for word in word_list if match(word, guess) == guess_result]


def eval_guess(guess, word_list):
    match_dist = {mat: 0 for mat in MATCHES}

    # compare to the word list
    for word in word_list:
        match_dist[match(word, guess)] += 1

    # compute entropy
    total = sum(list(match_dist.values()))
    probs = [val / total for val in match_dist.values()]
    return entropy(probs)


def get_best_guess(word_list):
    max_entropy = 0
    best_guess = ""
    for guess in tqdm(word_list):
        ent = eval_guess(guess, word_list)
        if ent > max_entropy:
            max_entropy = ent
            best_guess = guess
    return best_guess


if __name__ == "__main__":
    # construct word list
    word_list_path = Path("data") / "words_alpha.txt"
    with open(word_list_path, "r") as fp:
        word_list = get_valid_words([word.rstrip() for word in fp])

    while True:
        # guess a word
        best_guess = get_best_guess(word_list)
        if best_guess == "":
            print("The word is not in the word list.")
            break
        print(f"The best guess is '{best_guess}'.")

        # enter the guessing result
        guess_result = input("Enter the guessing result (?a?b): ")
        assert guess_result in MATCHES
        word_list = update_word_list(word_list, best_guess, guess_result)
        if guess_result == f"{WORD_LEN}a0b":
            break
