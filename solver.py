from pathlib import Path
from copy import deepcopy
from typing import List
from os import cpu_count

from scipy.stats import entropy

from tqdm.contrib.concurrent import process_map
from multiprocessing import Pool

WORD_LEN = 5


class WordleHelper:
    def __init__(self, word_list: List[str]):
        self.all_words = word_list
        self.valid_words = deepcopy(word_list)

    def _match(self, word: str, guess: str):
        """Compute the match result of the two words.

        Returns
        -------
        match_result: str
            A string with the format '`green`-`yellow`-`grey`', where
            `green`, `yellow`, `grey` represents the sorted green, yellow,
            and grey characters, respectively.
        """
        grn, yllw, gry = set(), set(), set()
        for i in range(WORD_LEN):
            if guess[i] == word[i]:
                grn.add(guess[i])
            elif guess[i] in word:
                yllw.add(guess[i])
            else:
                gry.add(guess[i])
        return "-".join("".join(sorted(chars)) for chars in [grn, yllw, gry])

    def _eval_guess(self, guess: str):
        """Evaluate a guess and return the resulting metric."""
        match_dist = {}
        for word in self.valid_words:
            match_result = self._match(word, guess)
            match_dist.setdefault(match_result, 0)
            match_dist[match_result] += 1
        return -entropy(list(match_dist.values()))

    def get_best_guess(self, top_k: int = 5, progress_bar: bool = True):
        """Get the top `top_k` guesses.

        If there are less than `top_k` valid words, return all."""
        # candidates
        is_close = (len(self.valid_words) < 30) and not (
            len(self.valid_words) > 3 and self.n_green >= WORD_LEN - 2
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

    def update_valid_words(self, guess: str, g_chars: str, y_chars: str):
        """Update the list of valid words based on the guess and its results.

        Parameters
        ----------
        guess: str
            The word you guessed.
        g_chars: str
            A string containing green characters.
        y_chars: str
            A string containing yellow characters.
        """
        guess = guess.lower()
        g_chars, y_chars = g_chars.lower(), y_chars.lower()
        absent_chars = set(guess).difference(set(g_chars + y_chars))

        new_valid_words = []
        for word in self.valid_words:
            try:
                for g_c in g_chars:
                    assert word.index(g_c) == guess.index(g_c)
                for y_c in y_chars:
                    assert word.index(y_c) != guess.index(y_c)
                for abs_c in absent_chars:
                    assert abs_c not in word
                new_valid_words.append(word)
            except Exception:
                pass
        self.valid_words = new_valid_words


def get_valid_words(word_list):
    """Filter words and return those containing `WORD_LEN` unique characters"""
    return [
        word
        for word in word_list
        if len(word) == WORD_LEN and len(set(word)) == WORD_LEN
    ]


if __name__ == "__main__":

    # construct word list
    word_list_path = Path("data") / "words_alpha.txt"
    with open(word_list_path, "r") as fp:
        word_list = get_valid_words([word.rstrip() for word in fp])

    # start wordle-solver
    solver = WordleHelper(word_list)
    while True:
        # guess a word
        best_guesses = solver.get_best_guess()
        print(
            f"\nThe suggested words are {best_guesses} "
            f"(over {len(solver.valid_words)})."
        )

        # enter the guessing result
        guess = input("Enter the word you guessed: ")
        g_chars = input("Enter the green character(s): ")
        y_chars = input("Enter the yellow character(s): ")
        solver.update_valid_words(guess, g_chars, y_chars)

        # hit
        if len(g_chars) == 5:
            print("Congratulations!!")
            break
