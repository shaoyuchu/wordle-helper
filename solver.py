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
        self.last_guess = None
        self.match_results = []
        for a in range(WORD_LEN + 1):
            for b in range(WORD_LEN + 1 - a):
                self.match_results.append(f"{a}a{b}b")
        self.match_results.remove(f"{WORD_LEN-1}a1b")

    def _match(self, word: str, guess: str):
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

    def _eval_guess(self, guess: str):
        """Evaluate a guess and return the resulting entropy."""
        match_dist = {mat: 0 for mat in self.match_results}
        # compare to the word list
        for word in self.valid_words:
            match_dist[self._match(word, guess)] += 1

        # compute entropy
        total = sum(list(match_dist.values()))
        probs = [val / total for val in match_dist.values()]
        return entropy(probs)

    def get_best_guess(self, top_k: int = 3, progress_bar: bool = True):
        """Get the top `top_k` guesses.

        If there are less than `top_k` valid words, return all."""
        # evaluate all guesses
        if len(self.valid_words) < len(self.all_words) * 0.01:
            search_list = self.valid_words
        else:
            search_list = self.all_words
        if progress_bar:
            entropies = process_map(
                self._eval_guess,
                search_list,
                max_workers=cpu_count(),
                chunksize=cpu_count(),
            )
        else:
            with Pool(processes=cpu_count()) as pool:
                entropies = pool.map(self._eval_guess, search_list)

        # sort based on entropy
        if top_k == 1:
            idx = entropies.index(max(entropies))
            return [search_list[idx]]
        all_gue_ent = sorted(
            list(zip(search_list, entropies)),
            key=lambda x: x[1],
            reverse=True,
        )
        n_best = min(top_k, len(all_gue_ent))
        return [gue_ent[0] for gue_ent in all_gue_ent[:n_best]]

    def update_valid_words(self, guess: str, a_chars: str, b_chars: str):
        """Update the list of valid words based on the guess and its results.

        Parameters
        ----------
        guess: str
            The word you guessed.
        a_chars: str
            A string containing characters that appears to be green.
        b_chars: str
            A string containing characters that appears to be yellow.
        """
        guess = guess.lower()
        a_chars, b_chars = a_chars.lower(), b_chars.lower()
        new_valid_words = []
        absent_chars = set(guess).difference(set(a_chars + b_chars))
        for word in self.valid_words:
            try:
                for a_c in a_chars:
                    assert word.index(a_c) == guess.index(a_c)
                for b_c in b_chars:
                    assert word.index(b_c) != guess.index(b_c)
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
        a_chars = input("Enter the green character(s): ")
        b_chars = input("Enter the yellow character(s): ")
        solver.update_valid_words(guess, a_chars, b_chars)

        # hit
        if len(a_chars) == 5:
            break
