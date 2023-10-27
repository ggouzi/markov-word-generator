from setuptools import setup, find_packages

setup(
    name='markov_word_generator',
    version='0.4',
    description='A small Python librairy to generate random credible words based on a list of words by esimating the probability of the next character from the frequency of the previous ones',
    long_description='A small Python librairy to generate random credible words based on a list of words by esimating the probability of the next character from the frequency of the previous ones',
    author='Gaetan GOUZI',
    author_email='gouzi.gaetan@gmail.com',
    url='https://github.com/ggouzi/markov-word-generator',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        'Unidecode',
    ]
)
