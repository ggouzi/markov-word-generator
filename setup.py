from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='markov_word_generator',
    version='0.5',
    description='A small Python librairy to generate random credible words based on a list of words by esimating the probability of the next character from the frequency of the previous ones',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Gaetan GOUZI',
    author_email='gouzi.gaetan@gmail.com',
    url='https://github.com/ggouzi/markov-word-generator',
    packages=find_packages(),
    install_requires=[
        'Unidecode',
    ]
)
