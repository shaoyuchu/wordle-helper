from pathlib import Path
import json
from statistics import mean
from random import sample
from collections import Counter

from tqdm import tqdm

from solver import WordleHelper, get_valid_words, WORD_LEN

SAMPLE_SIZE = 500


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
    word_list_path = Path("data") / "wordle_words.json"
    with open(word_list_path, "r") as fp:
        word_dict = json.load(fp)
        word_list = word_dict["La"] + word_dict["Ta"]

    # iterate all words
    result = {}
    for word in tqdm(sample(word_list, SAMPLE_SIZE)):
        solver = WordleHelper(word_list)
        history = []
        n_valid = []
        n_trial = 1
        while True:
            if n_trial == 1:
                guess = "tares"
            else:
                guess = solver.get_best_guess(top_k=1, progress_bar=False)[0]
            history.append(guess)
            n_valid.append(len(solver.valid_words))

            # get compare results
            res = compare(word, guess)
            if len(res[0]) == WORD_LEN:
                break
            solver.update_valid_words(guess, res[0], res[1])
            n_trial += 1

        result[word] = {
            "count": n_trial,
            "history": "-".join(history),
            "n_valid": "-".join([str(num) for num in n_valid]),
        }

    # write result
    with open(Path("data") / "experiment_result_sample.json", "w") as fp:
        json.dump(result, fp, indent=4)

    # statistics
    all_counts = [stat["count"] for stat in list(result.values())]
    print(f"min = {min(all_counts)}")
    print(f"max = {max(all_counts)}")
    print(f"mean = {mean(all_counts)}")
    counter = Counter(stat["count"] for stat in list(result.values()))
    for key in sorted(list(counter.keys())):
        print(f"{key} trials: {counter[key]}")
