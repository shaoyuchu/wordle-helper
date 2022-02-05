from pathlib import Path
from statistics import mean
from typing import List
from os import cpu_count, get_terminal_size
import json

from tqdm.contrib.concurrent import process_map
from multiprocessing import Pool

WORD_LEN = 5
SUGGEST_S = "The suggested words are {words} ({v_len} candidates left)."
INPUT_GUESS_S = "Enter the word you guessed: "
INVALID_GUESS_S = (
    "Invalid guess. The guessed word should contain "
    f"exactly {WORD_LEN} alphabetic characters."
)
INPUT_GUESS_RES_S = "Enter the guessing result, e.g. y-yg-: "
INVALID_GUESS_RES_S = (
    "Invalid result. The result should contain exactly "
    f"{WORD_LEN} characters from ['g', 'y', '-']."
)
GAME_END_S = "Congratulations!!"


def match(word: str, guess: str):
    """Compute the match result of the two words.

    Returns
    -------
    match_result: str
        A string representing the guess results,
        where `g`, `y`, `-` stands for the green, yellow,
        and grey characters, respectively.
    """
    word_l, guess_l = list(word), list(guess)
    match_result = ["-" for i in range(WORD_LEN)]

    # green
    for i in range(WORD_LEN):
        if guess_l[i] == word_l[i]:
            match_result[i] = "g"
            word_l[i] = guess_l[i] = "."

    # yellow
    for i in range(WORD_LEN):
        if guess_l[i] != "." and guess_l[i] in word_l:
            match_result[i] = "y"
            word_l[word_l.index(guess_l[i])] = "."
    return "".join(match_result)


class WordleHelper:
    def __init__(self, word_list: List[str], candidates: List[str]):
        """Init WordleHelper.

        Parameters
        ----------
        word_list: str
            A list of all valid words.
        candidates: str
            A list of candidate words.
        """
        self.all_words = word_list
        self.valid_words = candidates
        self.n_green = 0

    def _eval_guess(self, guess: str):
        """Evaluate a guess and return the resulting metric."""
        match_dist = {}
        for word in self.valid_words:
            match_result = match(word, guess)
            match_dist.setdefault(match_result, 0)
            match_dist[match_result] += 1

        # expected group size
        group_sizes = list(match_dist.values())
        total = sum(group_sizes)
        return mean((size ** 2) / total for size in group_sizes)

    def get_best_guess(self, top_k: int = 5, progress_bar: bool = True):
        """Get the top `top_k` guesses.

        If there are less than `top_k` valid words, return all."""
        # candidates
        is_close = (len(self.valid_words) < 30) and not (
            len(self.valid_words) > 2 and self.n_green >= WORD_LEN - 2
        )
        if is_close:
            cand = self.valid_words
        else:
            cand = self.all_words

        # compute metrics
        if progress_bar:
            metrics = process_map(
                self._eval_guess,
                cand,
                max_workers=cpu_count(),
                chunksize=cpu_count(),
            )
        else:
            with Pool(processes=cpu_count()) as pool:
                metrics = pool.map(self._eval_guess, cand)

        # sort by metrics
        all_gue_met = sorted(list(zip(cand, metrics)), key=lambda x: x[1])
        n_best = min(top_k, len(all_gue_met))
        return [gue_met[0] for gue_met in all_gue_met[:n_best]]

    def update_valid_words(self, guess: str, guess_result: str):
        """Update the list of valid words based on the guess and its results.

        Parameters
        ----------
        guess: str
            The word you guessed.
        guess_result: str
            A string representing the guess results,
            where `g`, `y`, `-` stands for the green, yellow,
            and grey characters, respectively.
        """
        guess = guess.lower()
        self.n_green = max(self.n_green, guess_result.count("g"))
        self.valid_words = [
            word
            for word in self.valid_words
            if match(word, guess) == guess_result
        ]


if __name__ == "__main__":
    # construct word list
    word_list_path = Path("data") / "wordle_words.json"
    with open(word_list_path, "r") as fp:
        word_dict = json.load(fp)
        word_list = word_dict["La"] + word_dict["Ta"]
        candidates = word_dict["La"]

    # start wordle-helper
    wh = WordleHelper(word_list, candidates)
    while True:
        # guess a word
        best_guesses = wh.get_best_guess()
        print(SUGGEST_S.format(words=best_guesses, v_len=len(wh.valid_words)))

        # enter the guessing result
        guess = input(INPUT_GUESS_S)
        while len(guess) != WORD_LEN and not guess.isalpha():
            print(INVALID_GUESS_S)

        guess_res = input(INPUT_GUESS_RES_S)
        while len(guess_res) != WORD_LEN or not set(guess_res) <= set("gy-"):
            print(INVALID_GUESS_RES_S)
            guess_res = input(INPUT_GUESS_RES_S)
        print("-" * get_terminal_size(0)[0])

        # update valid words
        wh.update_valid_words(guess, guess_res)

        # hit
        if guess_res == "ggggg":
            print(GAME_END_S)
            break
