import argparse
import numpy as np
import string
import os


def _word_to_vector(word):
    '''Encode word in vector that holds count of every alphabetical letter.'''
    v = np.zeros(26, dtype=int)

    for i, c in enumerate(string.ascii_lowercase):
        v[i] = word.count(c)

    if not v.sum() == len(word):
        raise ValueError('Only lowercase alphabetical characters allowed.')

    return v


def encode_words_alpha(file='words_alpha.txt', save=True):
    '''
    Encode word database as vectors using _word_to_vector.

    Parameters
    ----------
    file : str
        Path to word database file.
    save : bool
        Save encoded word database as numpy file.

    Returns
    -------
    encoded : np.ndarray
        2-D numpy array of shape (n_words, 26).
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


def find_anagrams(word_data, word_data_encoded, query_word):
    '''
    Find 1-word anagrams and 2-word combination anagrams of query.

    Parameters
    ----------
    word_data : str
        Path to word list file.
    word_data_encoded : str
        Path to numpy file holding word list as vectors.
    query_word : str
        String for which anagrams are searched.
    '''
    query_word = query_word.lower()
    for c in query_word:
        if c not in string.ascii_lowercase:
            query_word = query_word.replace(c, '')

    print(f'Query:\t{query_word}')
    print('')

    # load word database
    word_list = read_words(word_data)
    word_data = np.load(word_data_encoded)

    # encode query
    query_encoded = _word_to_vector(query_word)

    # 1-word anagrams
    anagrams_1 = []
    an = np.where((word_data == query_encoded).all(axis=1))[0]
    for x in an:
        anagrams_1.append(word_list[x])

    if query_word in anagrams_1:
        anagrams_1.remove(query_word)

    if len(anagrams_1) > 0:
        print('1-Word Anagrams')
        print('---------------')
        for w in anagrams_1:
            print(w)
    else:
        print('No 1-Word Anagrams')
    print('')

    # 2-word anagrams
    anagrams_2 = []

    for i_row, row in enumerate(word_data):
        diff = query_encoded - row

        if (diff < 0).any():
            continue
        elif (diff == 0).all():
            continue
        else:
            an = np.where((word_data == diff).all(axis=1))[0]
            for x in an:
                anagrams_2.append((word_list[i_row], word_list[x]))

    if len(anagrams_2) > 0:
        print('2-Word Anagrams')
        print('---------------')
        for w in anagrams_2:
            print(w[0], w[1])
    else:
        print('No 2-Word Anagrams')


if __name__ == '__main__':
    find_anagrams('words_alpha.txt', 'words_alpha.npy', 'helloworld')
