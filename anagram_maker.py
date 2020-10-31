import argparse


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


def reduce_words(words, letters):
    '''
    Given the anagram search word, delete all words from list with more letters.

    Parameters
    ----------
    words : list
        List containing all possible words for anagram.
    letters : str
        Letters of the anagram.

    Returns
    -------
    reduced_words : list
        List not containing words with higher letter count than anagram.
    '''
    abc = 'abcdefghijklmnopqrstuvwxyz'
    abc_counts = count_letters(letters)

    reduced_words = []
    for word in words:
        if len(word) < len(letters):
            abc_counts_word = count_letters(word)
            if not any([abc_counts_word[key] > abc_counts[key] for key in abc]):
                reduced_words.append(word)
    return reduced_words


def count_letters(word):
    '''
    Count letters of word and return dictionary with counts for every letter.

    Parameters
    ----------
    word : str
        Word whose letters will be counted.

    Returns
    -------
    abc_counts : dict
        Dictionary with counts for every letter in word.
    '''
    abc = 'abcdefghijklmnopqrstuvwxyz'
    abc_counts = {}
    for letter_alpha in abc:
        count = 0
        for letter_word in word:
            if letter_word == letter_alpha:
                count += 1
        abc_counts[letter_alpha] = count
    return abc_counts


def get_len_indices(wordlist):
    '''
    Given a list of words with varying lengths, return a dictionary that maps
    word lengths to the index of the last word with that length in the list.

    Parameters
    ----------
    wordlist : list
        List of words. Has to be sorted by length.

    Returns
    -------
    di : dict
        Dictionary that maps word lengths as keys to the index of the last word
        in wordlist with that length as value.
    '''
    di = {}
    length = 1

    for i, w in enumerate(wordlist):
        length_word = len(w)

        # verify list is sorted
        if length_word > length:

            # set index of last word of previous length as value of that length
            length = length_word
            di[length_word - 1] = i

        # raise error if not sorted
        elif length_word < length:
            raise ValueError('Word list not sorted.')

    # fill missing keys in dictionary
    for key in range(1, length):
        if key not in di:

            # set value to that of previous length
            di[key] = di[key - 1]

    # fill up with keys for lengths within max. length from wordlist + 11
    for key in range(length, length + 11):

        # set value to that of maximum from wordlist
        di[key] = di[length - 1]

    # word with length 0
    di[0] = None

    return di


def find_anagrams(words, word1):
    '''
    Find anagrams of a search word from a list of words.

    Parameters
    ----------
    words : list
        List of words from which anagrams will be made.
    word1 : str
        Anagram search word.

    Returns
    -------
    anagrams : list
        Anagrams of the search word. The anagrams can be 1-word or 2-word
        combinations.
    '''
    # list for 1-word anagrams
    w1_anagrams = []

    # list for 2 word anagrams
    w2_anagrams = []

    # words that will be considered for 2-word combinations
    words_for_w2 = []

    # search wordlist for 1-word anagrams
    for word in words:
        if len(word1) == len(word):
            if count_letters(word1) == count_letters(word):
                w1_anagrams.append(word)

        # word from list only considered for 2-word anagrams if shorter
        elif len(word) < len(word1):
            words_for_w2.append(word)

        # list is sorted
        elif len(word) > len(word1):
            break

    lens_words_w2 = get_len_indices(words_for_w2)

    # search wordlist for 2-word anagrams
    for word in words_for_w2:
        # only considered if length of both is equal to word1
        for word2 in words_for_w2[lens_words_w2[len(word1) - len(word) - 1]:
                                  lens_words_w2[len(word1) - len(word)]]:
            comb = word + word2
            if len(comb) == len(word1):
                if count_letters(word1) == count_letters(comb):
                    w2_anagrams.append((word, word2))

    return w1_anagrams + w2_anagrams


if __name__ == '__main__':
    words = read_words('words_alpha.txt')

    parser = argparse.ArgumentParser()
    parser.add_argument('query')
    args = parser.parse_args()

    reduced_words = reduce_words(words, args.query)
    anagrams = find_anagrams(reduced_words, args.query)

    for a in anagrams:
        print(a)
