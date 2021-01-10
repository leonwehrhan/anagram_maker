import argparse
import numpy as np
import string
import os


def _word_to_vector(word):
    '''
    '''
    v = np.zeros(26, dtype=int)

    for i, c in enumerate(string.ascii_lowercase):
        v[i] = word.count(c)

    if not v.sum() == len(word):
        raise ValueError('Only lowercase alphabetical characters allowed.')

    return v


def encode_words_alpha(file='words_alpha.txt', save=True):
    '''
    Encode word database as vectors.
    '''
    words = read_words(file)
    encoded = np.zeros((len(words), 26), dtype=int)

    for i, word in enumerate(words):
        v = _word_to_vector(word)
        encoded[i] = v

    if save:
        filename, file_extension = os.path.splitext(file)
        np.save(filename + '.npy', encoded)

    return encoded


def read_words(file):
    '''
    Read words from textfile and return as list.

    Parameters
    ----------
    file : str
        Path to textfile with all words that will be considered for anagrams.

    Returns
    -------
    words : list
        List of words from textfile.
    '''
    with open(file, 'r') as f:
        words = f.read().split('\n')
    words = sorted(words, key=len)
    return words


if __name__ == '__main__':
    encode_words_alpha()
