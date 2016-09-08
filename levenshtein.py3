#!/usr/bin/env python3

import re
import sys
import functools
import itertools
import string
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import ThreadPoolExecutor

def lower_and_only_alpha(s):
    """ Convert to lowercase and strip out non-letters"""
    return s.strip()
    #return re.sub(r'[^a-z]', r'', s.strip().lower())
    #return re.sub(r'[\']', r'', s.strip().lower())

#
# LevenshteinDistance implementations from Wikipedia
# https://en.wikipedia.org/wiki/Levenshtein_distance#Computing_Levenshtein_distance
#

# len_s and len_t are the number of characters in string s and t respectively
def LevenshteinDistance_SlowAsHell(s, t, max = None):
  # base case: empty strings
  if not s:
      return len(t)
  if not t:
      return len(s)
  if max and abs(len(s) - len(t)) > max:
      return 99
  # test if last characters of the strings match
  cost = 0 if s[-1] == t[-1] else 1
  # return minimum of delete char from s, delete char from t, and delete char from both
  return min(LevenshteinDistance(s[:-1], t) + 1,
             LevenshteinDistance(s     , t[:-1]) + 1,
             LevenshteinDistance(s[:-1], t[:-1]) + cost)

def LevenshteinDistance(s, t, max = None):
    # degenerate cases
    if s == t:
        return 0
    if not s:
        return len(t)
    if not t:
        return len(s)

    # create two work vectors of integer distances
    # initialize v0 (the previous row of distances)
    # this row is A[0][i]: edit distance for an empty s
    # the distance is just the number of characters to delete from t
    v0 = list(range(len(t) + 1))
    v1 = [ 0 ] * (len(t) + 1)

    for i in range(len(s)):
        # calculate v1 (current row distances) from the previous row v0

        # first element of v1 is A[i+1][0]
        #   edit distance is delete (i+1) chars from s to match empty t
        v1[0] = i + 1

        # use formula to fill in the rest of the row
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)

        # copy v1 (current row) to v0 (previous row) for next iteration
        for j in range(len(v0)):
            v0[j] = v1[j]

        # print(s[:i+1], t, v0)
        if max and min(v0) > max:
            return max + 1
        
    return v1[len(t)]

def read_wordlist(f):
    return [ lower_and_only_alpha(s) for s in f.readlines() ]

# from itertools recipes
def flatten(listOfLists):
    "Flatten one level of nesting"
    return itertools.chain.from_iterable(listOfLists)

# from itertools recipes
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

def pool_list_of_friends(word, words, nprocs):
    # Let the executor divide the work among processes by using 'map'.
    with ProcessPoolExecutor(max_workers=nprocs) as executor:
    #with ThreadPoolExecutor(max_workers=nprocs) as executor:
        list_of_friends_for_word = functools.partial(real_list_of_friends, word)
        chunksize = len(words) // nprocs
        lists_of_words = grouper(words, chunksize)
        results = executor.map(list_of_friends_for_word, lists_of_words)
        return list(flatten(results))

def pool_list_of_friends2(word, words, nprocs):
    # Let the executor divide the work among processes by using 'map'.
    #with ProcessPoolExecutor(max_workers=nprocs) as executor:
    with ThreadPoolExecutor(max_workers=nprocs) as executor:
        list_of_friends_for_word = functools.partial(real_list_of_friends2, words)
        permutations = set(list_of_distance1_permutations(word))
        chunksize = max(1, len(permutations) // nprocs)
        lists_of_permutations = grouper(permutations, chunksize)
        results = executor.map(list_of_friends_for_word, lists_of_permutations)
        return list(flatten(results))

def list_of_distance1_permutations(word):
    # abc
    # What are all of the distance = 1 variations?
    # for each position in string including -1 and +1: [ '', 'a', 'b', 'c', '']
    # replace current with one from this set: [ '', '[a-z]' ]
    wordarray = [ '' ] + list(word) + [ '' ]
    chars = [ '' ] + list(string.ascii_lowercase)
    results = []
    for i in range(len(wordarray)):
        pre = word[:i]
        post1 = word[i+1:]
        post2 = word[i:]
        for c in chars:
            yield pre + c + post1
            yield pre + c + post2

def real_list_of_friends(word, words):
    return [ w for w in words if LevenshteinDistance(word, w, max=1) == 1 ]

def real_list_of_friends2(words, permutations):
    return { w for w in permutations if w in words }

def list_of_friends(word, words):
    #return real_list_of_friends(word, words)
    #return pool_list_of_friends(word, words, 16)
    #return real_list_of_friends2(words, list_of_distance1_permutations(word))
    return pool_list_of_friends2(word, words, 16)

def find_friend_tree(word, wordlist):
    tree = {}
    words = [ word ]
    while True:
        count = 0
        new_words = []
        for w in words:
            if w not in tree:
                tree[w] = list_of_friends(w, wordlist)
                new_words.extend(tree[w])
                count = count + len(tree[w])
        words = new_words
        if not count:
            break
    return tree

def read_input_words(f):
    words = []
    while True:
        word = f.readline().strip()
        #print(word)
        if word == 'END OF INPUT':
            break
        words.append(word)
    return words

def read_input(f):
    words = read_input_words(f)
    wordlist = set(read_wordlist(f))
    for word in words:
        tree = find_friend_tree(word, wordlist)
        print(len(tree.keys()))

if len(sys.argv) < 2 or sys.argv[1] == '-':
    read_input(sys.stdin)
else:
    with open(sys.argv[1], 'r') as f:
        read_input(f)
