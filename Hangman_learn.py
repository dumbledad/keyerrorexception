import random
import string
import json
import Hangman_engine as engine
from Hangman_engine import Guess_Result


iterations = 10_000_000
iteration_count = 0
num_letters = 4
learning_rate = 0.8
discount = 0.95
q_table = {} # Maps states (partial words) to actions (letter guessed) to score
states_with_scores = []

def init_q_table():
    alphabet_plus = ['_'] + list(string.ascii_uppercase)
    states = alphabet_plus
    for _ in range(num_letters - 1):
        states_old = states
        states = []
        for state in states_old:
            for letter in alphabet_plus:
                states.append(f'{state}{letter}')
    for state in states:
        q_table[state] = {letter: 0.04 for letter in list(string.ascii_uppercase)} # 1/26 = 0.04 so that no initial weight is zero
    print(f'Q-table initialised to zero for {len(states):,} states (rows) and 26 actions (columns)')


def print_interesting_entries():
    for state in states_with_scores:
        interesting_entries = {letter: score for letter, score in q_table[state] if score > 0}
        print(f'{state}: {interesting_entries}')


def play_and_learn():
    engine.guesses_allowed = 30
    letters = list(string.ascii_uppercase)
    current_state = '_' * num_letters
    part_word = engine.start_game(4)
    while '_' in part_word:
        weights = q_table[current_state]
        weights = [weights[letter] for letter in letters]
        guess = random.choices(letters, weights=weights, k=1)[0]
        letters.remove(guess)
        result, part_word = engine.process_guess(guess)
        print(f'({guess}, {result}, {part_word})')
        # Update q_table
        max_future_score = 0
        if '_' in part_word:
            max_future_score = max([score for letter, score in q_table[part_word]])
        score = 0
        if result == Guess_Result.SUCCESS:
            score = 1
            states_with_scores.append(current_state)
        # Bellman Equation from https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-0-q-learning-with-tables-and-neural-networks-d195264329d0
        # Q[s,a] = Q[s,a] + lr*(r + y*np.max(Q[s1,:]) - Q[s,a])
        q_s_a = q_table[current_state][guess]
        q_table[current_state][guess] = q_s_a + learning_rate * (score + (discount * max_future_score) - q_s_a)
        current_state = part_word


def main():
    init_q_table()
    while input('Next iteration? (y/n) ') == 'y':
        play_and_learn() 
        print_interesting_entries()


if __name__ == "__main__":
    main()
