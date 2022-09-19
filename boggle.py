"""Utilities related to Boggle game."""

from numpy.random import choice
import string


class Boggle():

    def __init__(self):

        self.words = self.read_dict("words.txt")
        self.size = 5

        # Letters matched with their recurence in the english language
        self.letter_probs = {
            "A": 0.084966,
            "B": 0.020720,
            "C": 0.045388,
            "D": 0.033844,
            "E": 0.0111607,
            "F": 0.018121,
            "G": 0.024705,
            "H": 0.030034,
            "I": 0.075448,
            "J": 0.001965,
            "K": 0.011016,
            "L": 0.054893,
            "M": 0.030129,
            "N": 0.066544,
            "O": 0.071635,
            "P": 0.031671,
            "Q": 0.001962,
            "R": 0.075809,
            "S": 0.057351,
            "T": 0.069509,
            "U": 0.036308,
            "V": 0.010074,
            "W": 0.012899,
            "X": 0.002902,
            "Y": 0.017779,
            "Z": 0.002722
        }

    def read_dict(self, dict_path):
        """Read and return all words in dictionary."""

        dict_file = open(dict_path)
        words = [w.strip() for w in dict_file]
        dict_file.close()
        return words

    def make_board(self, size=5):
        """Make and return a random boggle board."""

        self.size = size
        board = []

        letters = list(self.letter_probs.keys())
        probs = list(self.letter_probs.values())

        # probs must sum to 1
        adjusted_probs = [prob + ((1-sum(probs)) / len(letters))
                          for prob in probs]

        for y in range(self.size):
            row = [choice(letters, p=adjusted_probs) for i in range(self.size)]
            board.append(row)

        return board

    def check_valid_word(self, board, word):
        """Check if a word is a valid word in the dictionary and/or the boggle board"""

        word_exists = word in self.words
        valid_word = self.find(board, word.upper())

        if word_exists and valid_word:
            result = "ok"
        elif word_exists and not valid_word:
            result = "not-on-board"
        else:
            result = "not-word"

        return result

    def find_from(self, board, word, y, x, seen):
        """Can we find a word on board, starting at x, y?"""

        if x >= self.size or y >= self.size:
            return

        # This is called recursively to find smaller and smaller words
        # until all tries are exhausted or until success.

        # Base case: this isn't the letter we're looking for.

        if board[y][x] != word[0]:
            return False

        # Base case: we've used this letter before in this current path

        if (y, x) in seen:
            return False

        # Base case: we are down to the last letter --- so we win!

        if len(word) == 1:
            return True

        # Otherwise, this letter is good, so note that we've seen it,
        # and try of all of its neighbors for the first letter of the
        # rest of the word
        # This next line is a bit tricky: we want to note that we've seen the
        # letter at this location. However, we only want the child calls of this
        # to get that, and if we used `seen.add(...)` to add it to our set,
        # *all* calls would get that, since the set is passed around. That would
        # mean that once we try a letter in one call, it could never be tried again,
        # even in a totally different path. Therefore, we want to create a *new*
        # seen set that is equal to this set plus the new letter. Being a new
        # object, rather than a mutated shared object, calls that don't descend
        # from us won't have this `y,x` point in their seen.
        #
        # To do this, we use the | (set-union) operator, read this line as
        # "rebind seen to the union of the current seen and the set of point(y,x))."
        #
        # (this could be written with an augmented operator as "seen |= {(y, x)}",
        # in the same way "x = x + 2" can be written as "x += 2", but that would seem
        # harder to understand).

        seen = seen | {(y, x)}

        # adding diagonals

        if y > 0:
            if self.find_from(board, word[1:], y - 1, x, seen):
                return True

        if y < self.size - 1:
            if self.find_from(board, word[1:], y + 1, x, seen):
                return True

        if x > 0:
            if self.find_from(board, word[1:], y, x - 1, seen):
                return True

        if x < self.size - 1:
            if self.find_from(board, word[1:], y, x + 1, seen):
                return True

        # diagonals
        if y > 0 and x > 0:
            if self.find_from(board, word[1:], y - 1, x - 1, seen):
                return True

        if y < self.size - 1 and x < self.size - 1:
            if self.find_from(board, word[1:], y + 1, x + 1, seen):
                return True

        if x > 0 and y < self.size - 1:
            if self.find_from(board, word[1:], y + 1, x - 1, seen):
                return True

        if x < self.size - 1 and y > 0:
            if self.find_from(board, word[1:], y - 1, x + 1, seen):
                return True
        # Couldn't find the next letter, so this path is dead

        return False

    def find(self, board, word):
        """Can word be found in board?"""

        # Find starting letter --- try every spot on board and,
        # win fast, should we find the word at that place.

        for y in range(0, self.size):
            for x in range(0, self.size):
                if self.find_from(board, word, y, x, seen=set()):
                    return True

        # We've tried every path from every starting square w/o luck.
        # Sad panda.

        return False
