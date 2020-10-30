import sys
import random
from enum import Enum
from functools import reduce

class Guess_Result(Enum):
	SUCCESS = 1
	FAILURE = 2
	DUPLICATE = 3
	GAME_OVER = 4


guesses = []
chosen_word = "" 
part_word = ""
words = []
word_len = 0
guesses_allowed = 15
guesses_left = -1


def _load_words():
	words_file = open("C:\\\\USers\\timregan\\source\\pythonlessons\\Hangman-Game\\common.txt")
	for line in words_file:
		word = line.strip()
		words.append(word) 


def _choose_word(word_length=-1):
	global chosen_word
	words_to_chose_from = words
	minimum_length = reduce(lambda x, y: min(x, len(y)), words, sys.maxsize)
	if word_length < minimum_length and word_length > -1:
		raise ValueError(f'Minimum length of words available: {minimum_length}, requested word length: {word_length}')
	elif word_length >= minimum_length:
		words_to_chose_from = [word for word in words if len(word) == word_length]
	chosen_word = random.choice(words_to_chose_from)
	global word_len 
	word_len = len(chosen_word)
def _create_part_word():
	global part_word 
	part_word = ""
	for letter in list(chosen_word):
		if letter in guesses:
			part_word = part_word+letter
		else:
			part_word = part_word+"_"
	return part_word


def process_guess(guess):
	global guesses_left, chosen_word
	guess = guess.strip()
	guess = guess.lower()
	guess = guess[0]
	if guesses_left <= 0:
		return Guess_Result.GAME_OVER, chosen_word
	if guess in guesses:
		return Guess_Result.DUPLICATE, _create_part_word()
	guesses.append(guess)
	if guess in chosen_word:
		return Guess_Result.SUCCESS, _create_part_word()
	guesses_left = guesses_left - 1
	return Guess_Result.FAILURE, _create_part_word()


def num_wrong_guesses():
	wrong_guesses = 0
	for guess in guesses:
		if guess not in chosen_word:
			wrong_guesses += 1
	return wrong_guesses

def start_game(word_length=-1):
	if len(words) == 0:
		_load_words()
	_choose_word(word_length)
	global guesses 
	guesses = []
	global guesses_left 
	guesses_left = guesses_allowed
	return _create_part_word()
