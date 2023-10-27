from collections import defaultdict
import unidecode
import random
from dataclasses import dataclass, field
from enum import Enum


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


class WordType(Enum):
    WORD = "WORD"
    NAME = "NAME"


class AllowedLanguages(Enum):
    EN = "EN"
    FR = "FR"
    DE = "DE"
    FI = "FI"
    IT = "IT"
    PT = "PT"
    SE = "SE"


def get_supported_languages():
    return [l.value for l in AllowedLanguages]


def get_supported_word_types():
    return [w.value for w in WordType]


@dataclass
class MarkovWordGenerator():

    """
    Class to scan dictionary files,
    generate character-frequency dict mapping table
    and generate a random word from this mapping table using the last N digit apparition frequency (Markov chain of lenth N)
    """
    markov_length: int
    language: AllowedLanguages | None = None
    word_type: WordType | None = None
    dictionary_filename: str | None = None
    ignore_accents: bool = False
    mapping_chars: dict = field(init=False)

    def __post_init__(self):
        self.mapping_chars = defaultdict(int)
        # Check language/word_type and dictionary_filename are mutually exclusive
        if ((self.language or self.word_type) and self.dictionary_filename):
            print("Error: Either language and word_type parameters must be set, or use a custom dictionary_filename. dictionary_filename parameter cannot be set if either language or word_type is set")
            return
        # Check language/word_type or dictionary_filename are set
        if (not (self.language or self.word_type) and not self.dictionary_filename):
            print("Error: Either language and word_type parameters must be set, or use a custom dictionary_filename. dictionary_filename parameter cannot be set if either language or word_type is set")
            return
        if self.dictionary_filename is None:
            # Check word_type is correctly set
            if not isinstance(self.word_type, WordType):
                print(f"word_type can only be one of the allowed word types: {get_supported_word_types()}")
                return
            # Check language is correctly set
            if isinstance(self.language, str):
                if self.language.upper() not in [l.value for l in AllowedLanguages]:
                    print(f"language {self.language} is not supported yet. language can only either be: {get_supported_languages()}")
                    return
            elif (not isinstance(self.language, AllowedLanguages)):
                print(f"language {self.language} is not supported yet. language can only either be: {get_supported_languages()}")
                return
            else:
                self.language = self.language.value
        if (self.dictionary_filename is None):
            self.dictionary_filename = f"dictionaries/{self.language.upper()}-{self.word_type.value.lower()}s.dic"
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
        """
        Function to generate a word based on the MarkovWordGenerator object
        Will stop when end delimitor is the next generated character
        Can be customized with a given seed that sets the first characters to start the word with
        """
        c = self.select_next_chars(previous_chars='^' + seed)
        if c == DELIMITER_END:
            return seed
        word = seed + c
        c = self.select_next_chars(previous_chars=word[-self.markov_length:])
        while c != DELIMITER_END:
            word += c
            c = self.select_next_chars(previous_chars=word[-self.markov_length:])
        if word[-1] == DELIMITER_END:
            word = word[:-1]
        return word
