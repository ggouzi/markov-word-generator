
# markov-word-generator
[![PyPI version](https://badge.fury.io/py/markov-word-generator.svg)](https://badge.fury.io/py/markov-word-generator) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)`

A small Python library to generate random credible words based on a  list of words by estimating the probability of the next character from the frequency of the previous ones.
This uses [Markov chain](https://en.wikipedia.org/wiki/Markov_chain)


# Installation
```bash
pip install markov-word-generator
```

# Principle

The generator will parse an input text file containing one word per line (dictionary), count each character occurrence based on the occurrence of the N previous ones  create a mapping table for each character-combination and its associated frequency in the corpus.

[enter link description here](https://raw.githubusercontent.com/ggouzi/markov-word-generator/main/images/diagram.png)


![enter image description here](https://raw.githubusercontent.com/ggouzi/markov-word-generator/main/images/heatmap_EN-words.png)![enter image description here](https://raw.githubusercontent.com/ggouzi/markov-word-generator/main/images/heatmap_FR-words.png)
# Usage
```python
from markov_word_generator import MarkovWordGenerator

generator = MarkovWordGenerator(
	markov_length=4,
	dictionary_filename='dictionaries/EN-words.dic',
	ignore_accents=True
)
print(generator.generate_word())
```
output:
```
rebutaneously
```




## Parameters

 - `markov_length`: int. Number of previous characters the generator will take into account to compute probability of apparition of each the next character.
 - `dictionary_filename`: str. Corpus the generator will parse to analyze character apparition frequency
 - `ignore_accents`: Optional boolean. If set to True, accents will not be considered  while parsing `dictionary_filename`. Default to False


## Impact of the markov_length parameter

### Length 1
```python
from markov_word_generator import MarkovWordGenerator

generator = MarkovWordGenerator(markov_length=1, dictionary_filename='dictionaries/EN-words.dic', ignore_accents=True)

for i in range(0, 10):
    print(generator.generate_word())

```
output:
```
eroun
unteticakreatintes
sucle
erarums
eablatirlac
e
ghils
rllig
beseleforuat
de
```

Initialize the generator with a `markov_length` of 3.
This means the generator will create words by generating characters based on their probability to appear in the given dictionary according to the occurrence of the 3 previous characters.
P("aaaa") = X
P("aaab") = X
P("aaac") = X
...

### Length 3
```python
from markov_word_generator import MarkovWordGenerator

generator = MarkovWordGenerator(
	markov_length=3,
	dictionary_filename='dictionaries/EN-words.dic',
	ignore_accents=True
)

for i in range(0, 10):
    print(generator.generate_word())
```
output:
```
blungalinther
super
solder
degreetricked
mittlessly
out
hearf
fracertory
gyny
locious
```

### Length 4
```python
from markov_word_generator import MarkovWordGenerator

generator = MarkovWordGenerator(
	markov_length=4,
	dictionary_filename='dictionaries/EN-words.dic',
	ignore_accents=True
)

for i in range(0, 10):
    print(generator.generate_word())
```
output:
```
authering
negligented
manoeistical
bleat
lover
confusions
dest
hand
display
entwinkle
```

# More examples

## Words
| EN | FR | ES | DE | IT |
|--|--|--|--|--|
|  |  |  |  |  |

## Names

| EN | FR | ES | DE | IT |
|--|--|--|--|--|
|  |  |  |  |  |

Example with seed
