from collections import defaultdict
import unidecode
import random
from dataclasses import dataclass, field


DELIMITER_END = '$'


def each_cons(xs, n):
    """
    Returns all combinations of arrays of size n from input string xs
    """
    return [xs[i:i + n] for i in range(len(xs) - n + 1)]


def normalize_hash(h):
    """
    Returns input dict with values normalized between 0 and 1 according to their occurrences among all of them
    """
    weights = {}
    total = sum(h.values())
    s = 0
    for c in sorted(h, key=h.get, reverse=True):
        s += h[c]
        weights[c] = float(s) / total
    return weights


@dataclass
class MarkovWordGenerator():

    """
    Class to scan dictionary files,
    generate character-frequency dict mapping table
    and generate a random word from this mapping table using the last N digit apparition frequency (Markov chain of lenth N)
    """
    markov_length: int
    dictionary_filename: str
    ignore_accents: bool = False
    mapping_chars: dict = field(init=False)

    def __post_init__(self):
        self.mapping_chars = defaultdict(int)
        with open(self.dictionary_filename) as list:
            for word in list:
                word = '^' + word.lower().replace('\n', DELIMITER_END).replace('.', '')
                if self.ignore_accents:
                    word = unidecode.unidecode(word)
                for combination in each_cons(word, self.markov_length + 1):
                    self.mapping_chars[combination] += 1

    def select_next_chars(self, previous_chars):
        remainings = self.markov_length + 1 - len(previous_chars)
        choices = {s: self.mapping_chars[s] for s in self.mapping_chars if s.startswith(previous_chars)}
        wp = normalize_hash(choices)
        u = random.uniform(0, 1)
        for s in wp:
            if wp[s] >= u:
                return s[-remainings:]
        return DELIMITER_END

    def word_exists(self, word):
        """
        Check if given word exists
        """
        with open(self.dictionary_filename) as file:
            for line in file:
                line = line.strip().lower()
                word = word.strip().lower()
                if self.ignore_accents:
                    unidecode.unidecode(word)
                    if unidecode.unidecode(line) == unidecode.unidecode(word):
                        return True
                else:
                    if line == word:
                        return True
        return False

    def generate_word(self, seed=''):
        c = self.select_next_chars(previous_chars='^' + seed)
        if c == DELIMITER_END:
            return seed
        word = seed + c
        c = self.select_next_chars(previous_chars=word[-self.markov_length:])
        while c != DELIMITER_END:
            word += c
            c = self.select_next_chars(previous_chars=word[-self.markov_length:])
        return word
