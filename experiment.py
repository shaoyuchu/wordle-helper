from pathlib import Path
import json
from statistics import mean
from collections import Counter
import argparse

from tqdm import tqdm

from solver import GameMode, WordleHelper, match, WORD_LEN

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--hard", action="store_true")
    args = parser.parse_args()
    mode = GameMode.Hard if args.hard else GameMode.Easy

    # construct word list
    word_list_path = Path("data") / "wordle_words.json"
    with open(word_list_path, "r") as fp:
        word_dict = json.load(fp)
        valid_words = word_dict["La"] + word_dict["Ta"]
        candidates = word_dict["La"]

    # iterate all words
    result = {}
    for word in tqdm(candidates):
        wh = WordleHelper(valid_words, candidates, mode)
        history = []
        n_valid = []
        n_trial = 1
        while True:
            if n_trial == 1:
                guess = "soare"
            else:
                guess = wh.get_best_guess(top_k=1, progress_bar=False)[0]
            history.append(guess)
            n_valid.append(len(wh.candidates))

            # get compare results
            guess_result = match(word, guess)
            if guess_result.count("g") == WORD_LEN:
                break
            wh.update_valid_words(guess, guess_result)
            n_trial += 1

        result[word] = {
            "count": n_trial,
            "history": "-".join(history),
            "n_valid": "-".join([str(num) for num in n_valid]),
        }

    # write result
    with open(Path("data") / "experiment_result.json", "w") as fp:
        json.dump(result, fp, indent=4)

    # statistics
    all_counts = [stat["count"] for stat in list(result.values())]
    print(f"mean = {'{:.3f}'.format(mean(all_counts))}")
    counter = Counter(stat["count"] for stat in list(result.values()))
    for key in sorted(list(counter.keys())):
        print(f"{key} trials: {counter[key]}")
