#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Nick Giroux
@collaborators: 
"""

import random
import string
import re

# Here is some helper code. You don't need to understand or modify this helper code,
# but you will need to call the functions, so it's worth looking at the docstrings
# of the functions to see what they do

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    """
    wordlist = list()
    wordlist_filename = 'words.txt'
    print('Loading word list from file: {}'.format(wordlist_filename))
    with open(wordlist_filename, 'r') as f:
        for line in f.readlines():
            if 4 <= len(line.rstrip('\n')):  # don't read in words less than 4 chars long
                wordlist.append(line.rstrip('\n'))
    print('{} words loaded'.format(len(wordlist)))
    return wordlist

def choose_word(wordlist):
    return random.choice(wordlist)

# end of helper code

def is_word_guessed(secret_word, letters_guessed):
    """
    This function accepts the secret word, as well as a string of letters which the
    user has guessed, and returns False unless all letter in the secret word
    have been guessed.

    :param str secret_word: A string representation of the secret word
    :param str letters_guessed: A string containing all of the letters
      that the user has guessed (e.g. 'aei')
    :return: True if all letters have been guessed otherwise False
    :rtype: bool
    """
    
    # initialize a dictionary with letters as keys and 'false' as values
    secret_dict = dict()
    for secret_letter in secret_word:
        secret_dict[secret_letter] = 'false'
    
    # if a guessed letter is in the word, change the value to 'true'
    for letter in letters_guessed:
        is_a_member = letter.lower() in secret_word
        if is_a_member:
            secret_dict[letter.lower()] = 'true'
        
    bool_pass = True
    # if any of the letters in the secret word haven't been guessed, return false
    for key in secret_dict:
        if secret_dict[key] == 'false':
            bool_pass = False
    
    return bool_pass
    
    raise NotImplementedError

def print_secret_word_with_letters_guessed(secret_word, letters_guessed):
    """
    This function takes the secret word, as well as a string containing letters
    which the user has guessed, and prints the secret word showing the letters 
    guessed and underscores for unguessed letters.

    For example, if the secret word is apple and the user has guessed a and e, then
    the secret_word would be 'apple', letters_guessed would be 'ae', and this
    function would print: a _ _ _ e

    :param str secret_word: A string representation of the secret word
    :param str letters_guessed: A string containing the letters that the user 
      has guessed
    :return: Nothing
    :rtype: None
    """
    
    # initialize the underscore object to be the length of the secret word
    blank_SW = "_ " * len(secret_word)
    
    # for each letter guessed, check if the guess is in the secret word
    for guess in letters_guessed:
        guess_loc = [(m.start(0)*2, m.end(0)*2) for m in re.finditer(guess, secret_word)]
            
        # for each instance of the guess and build the new underscore object
        for loc in guess_loc:
            blank_SW = blank_SW[0:loc[0]] + guess + ' ' + blank_SW[loc[1]:]
    
    return blank_SW[0:-1]
    
    raise NotImplementedError

def get_available_letters(letters_guessed):
    """
    This function accepts a string containing the letters the user has guessed so far, and
    returns a string of letters the user hasn't guessed.

    Hint: use string.ascii_lowercase to get all the lowercase letters.

    :param str letters_guessed: A string containing the letters that the user has guessed
    :return: A string containing all of the letters the user hasn't guessed yet
    :rtype: str
    """
    
    # initialize the remaining letters to be all lowercase characters
    remaining_letters = string.ascii_lowercase
    
    # for each letter guessed, remove it from the remaining letters string
    for letter in letters_guessed:
        remaining_letters = remaining_letters.replace(letter, '')
        
    return remaining_letters
    
    raise NotImplementedError


def hangman(secret_word):
    """
    Starts an interactive game of hangman using `secret_word` as the word the user is
    trying to guess.

    At the start of the game, this function lets the user know how many letters
    secret_word contains.

    The user starts with a number of guesses equal to the number of letters in the word
    plus 4.

    Each round, the function tells the user how many guesses they have left, prints the
    possible letters the user can guess by calling `get_available_letters`,  and asks the user
    to guess a letter. The function checks that the user actually entered a letter (not
    another character, or nothing), and that the letter hasn't been guessed yet.
    Hint: you should convert entered characters to lowercase before handling them.

    Then the function then tells the user whether or not that letter was in the secret word,
    and prints the guessed letters in the secret word by calling
    `print_secret_word_with_letters_guessed`.

    The function then calls `is_word_guessed` to determine whether or not the word has been
    guessed. If the word was guessed, tell the user they have won! If the word has not been
    guessed, decrement the remaining guesses by 1, and continue play if guesses remain.

    :param str secret_word: The secret word to guess
    :return: Nothing
    :rtype: None
    """
    
    # print initial game information
    print('The secret word is', len(secret_word), 'letters long')
    print('You have', len(secret_word)+4, 'guesses to guess the secret word')
    
    # initialize the number of guesses and the string of guessed characters
    count_guess = 0
    letters_guessed = ''
    
    # while there are guesses remaining
    while count_guess < len(secret_word)+4:
        
        # stop guessing if the word has been guessed
        if is_word_guessed(secret_word, letters_guessed):
            break
        
        # print dashed line; print guess information
        print('-'*20)
        print('Available letters:', get_available_letters(letters_guessed))
        print(print_secret_word_with_letters_guessed(secret_word, letters_guessed))
        print('Guessed letters:', letters_guessed)
        
        # read in new guess
        new_guess =  str(input('Please guess a letter: '))
        
        # make sure the guess is a single letter that hasn't already been guessed
        while not(new_guess in string.ascii_letters) or new_guess.lower() in letters_guessed or not(len(new_guess) == 1):
            if new_guess.lower() in letters_guessed:
                print("You've already guessed", new_guess)
            if not(new_guess in string.ascii_letters) or not(len(new_guess) == 1):
                print("Please enter an uppercase or lowercase letter")
            new_guess =  str(input('Please guess a letter: '))
            
        # print whether the guess is in the word; decrease number of guesses if wrong
        if new_guess.lower() in secret_word:
            print('You got one!')
        else:
            print('Sorry, that letter is not in the secret word')
            count_guess += 1
            print('You have', len(secret_word)+4-count_guess, 'guesses remaining')
        
        # update the guessed string
        letters_guessed += new_guess.lower()
    
    # print message if the word has been guessed or not when out of guesses
    if is_word_guessed(secret_word, letters_guessed):
        print("Congratulations, you've won! The secret word was:", secret_word)
    elif not is_word_guessed(secret_word, letters_guessed):
        print("Sorry, you've lost. The secret word was:", secret_word)

if __name__ == '__main__':
    wordlist = load_words()
    secret_word = choose_word(wordlist)
    hangman(secret_word)
