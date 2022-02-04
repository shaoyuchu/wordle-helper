from pathlib import Path
import json
from statistics import mean

from tqdm import tqdm

from solver import WordleHelper, get_valid_words, WORD_LEN


def compare(word, guess):
    g_chars = ""
    y_chars = ""
    for i in range(WORD_LEN):
        if guess[i] == word[i]:
            g_chars += guess[i]
        elif guess[i] in word:
            y_chars += guess[i]
    return (g_chars, y_chars)


if __name__ == "__main__":

    # construct word list
    word_list_path = Path("data") / "words_alpha.txt"
    with open(word_list_path, "r") as fp:
        word_list = get_valid_words([word.rstrip() for word in fp])

    # iterate all words
    result = {}
    for word in tqdm(word_list):
        solver = WordleHelper(word_list)
        history = []
        n_trial = 1
        while True:
            if n_trial == 1:
                guess = "tares"
            else:
                guess = solver.get_best_guess(top_k=1, progress_bar=False)[0]
            history.append(guess)

            # get compare results
            res = compare(word, guess)
            if len(res[0]) == WORD_LEN:
                break
            else:
                solver.update_valid_words(guess, res[0], res[1])
                n_trial += 1

        result[word] = {"count": n_trial, "history": "-".join(history)}

    # write result
    with open(Path("data") / "experiment_result.json", "w") as fp:
        json.dump(result, fp, indent=4)

    # statistics
    all_counts = [stat["count"] for stat in list(result.values())]
    print(f"min = {min(all_counts)}")
    print(f"max = {max(all_counts)}")
    print(f"mean = {mean(all_counts)}")
