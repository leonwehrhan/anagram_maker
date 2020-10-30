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
    # count letters of word and return dictionary with counts for every letter
    abc = 'abcdefghijklmnopqrstuvwxyz'
    abc_counts = {}
    for l in abc:
        count = 0
        for ll in word:
            if ll == l:
                count += 1
        abc_counts[l] = count
    return abc_counts


def get_len_indices(wordlist):
    # get indices of last word with length i
    di = {}
    l = 1
    for i, w in enumerate(wordlist):
        ll = len(w)
        if ll > l:
            l = ll
            di[ll - 1] = i
        elif ll < l:
            raise ValueError('Word list not sorted.')
    for key in range(1, l):
        if key not in di:
            di[key] = di[key - 1]
    for key in range(l, l + 11):
        di[key] = di[l - 1]
    di[0] = di[l - 1]
    print(di)
    return di


def find_anagrams(words, word1):

    # list for 1-word and 2-word
    w1_anagrams = []

    words_for_w2 = []
    w2_anagrams = []

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
    for a in w2_anagrams:
        print(a[0], a[1])


if __name__ == '__main__':
    words = read_words('words_alpha.txt')
    # get_len_indices(words)
    anagram = 'italienholtlot'

    reduced_words = reduce_words(words, anagram)
    find_anagrams(reduced_words, anagram)
