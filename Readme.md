
# Levenshtein Distance #

Source: [CodeEval](https://www.codeeval.com/open_challenges/58/)  
Link: <https://www.codeeval.com/open_challenges/58/>

## Challenge Description ##

[Levenshtein distance]: http://en.wikipedia.org/wiki/Levenshtein_distance

Two words are friends if they have a Levenshtein distance of 1 (For details see [Levenshtein distance]). That is, you can add, remove, or substitute exactly one letter in word X to create word Y. A word’s social network consists of all of its friends, plus all of their friends, and all of their friends’ friends, and so on. Write a program to tell us how big the social network for the given word is, using our word list.

**Note: The network also includes the word itself.**

### Input sample: ###

The first argument will be a path to a filename, containing words, and the word list to search in. The first N lines of the file will contain test cases, they will be terminated by string 'END OF INPUT'. After that there will be a list of words one per line.

**Example:**

| line	| text			|  
| ------	| ------			|  
| 0		| recursiveness	|  
| 1		| elastic			|  
| 2		| macrographies	|  
| 3		| END OF INPUT		|  
| 4		| aa				|  
| 5		| aahed			|  
| 6		| aahs			|  
| 7		| aalii			|  
| ...	| ...			|  
| ...	| ...			|  
| 11555	| zymoses			|  
| 11556	| zymosimeters		|  

### Output sample ###

For each test case print out how big the social network for the word is. In the sample input above, the social network for the word 'elastic' is 3 and for the word 'recursiveness' is 1.

**Example:**

    $ ./levenshtein tests/input1
    1
    3
    1

### Constraints ###

- The number of test cases, N, will be in the range 15 to 30, inclusive.
- The word list will always be the same, and it's length will be around 10000 words.
- All words are composed solely of lowercase ASCII letters with no punctuation.

### Notes ###

- CodeEval's original description doesn't include the word itself in the network, but their test cases do.
- Use any Levenshtein distance algorithm, code, or library you can find.
- In order to get a good score with CodeEval, you'll want to optimize for computing if two words differ by only one character or less.
- You can use multi-processing and multi-threading with CodeEval, but threading seems to be faster on their site.
