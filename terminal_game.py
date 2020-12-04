# Python Implementation of Mastermind

# RULES:
# Computer selects 4 colored pegs or balls and arranges them
# Player has eight guesses to find the correct sequence/color of hidden pegs
# Player makes a guess by arranging 4 pegs
# Computer responds with feedback in form of black or white peg
# A white peg means that a correct color was used but is in the wrong position
# A black peg means that both the color and the position are correct

import pprint
import numpy as np
import random
import pygame
import sys


class Game:
    """Mastermind game class"""
    def __init__(self, players, duplicates):
        self.board = [(['' for x in range(4)], []) for y in range(8)]

        # Colors: R = red, B = blue, Y = yellow, G = green, W = white, O = orange
        self.colors = ['R', 'B', 'Y', 'G', 'W', 'O']
        self.solution = []
        self.guess_counter = 7
        self.players = players
        self.duplicates = duplicates
        self.colors_seen = []
        self.colors_in_sol = []
        self.game_over = False
        self.player_win = False
        self.comp_p2_win = False

    def get_board(self):
        """returns game board"""
        return self.board

    def create_solution(self):
        """creates valid solution based on criteria specified from user"""
        if self.duplicates:
            self.solution = [random.choice(self.colors) for _ in range(4)]
        else:
            self.solution = random.sample(self.colors, 4)

    def get_solution(self):
        """returns correct solution"""
        return self.solution

    def guess_row(self, color1, color2, color3, color4):
        """valid game move"""
        if self.game_over:
            return False

        guess = [color1, color2, color3, color4]
        result = self.feedback(guess)
        row = (guess, result)

        self.board[self.guess_counter] = row

        self.guess_counter -= 1

        if self.verification(guess, result):
            self.game_over = True
            self.player_win = True

        if self.guess_counter < 0:
            self.game_over = True
            self.comp_p2_win = True

        return True

    def feedback(self, guess):
        """feedback to user based on guesses made"""
        result = []
        row = guess
        tracker = {x: [] for x in row}

        for i in range(len(self.solution)):
            sol = self.solution[i]
            guess = row[i]

            if sol == guess:
                tracker[sol] = ['B']

            elif sol in row:
                tracker[sol] += ['W']

        for i in tracker:
            self.colors_seen.append(i)
            for j in tracker[i]:
                if self.duplicates:
                    result += [j]
                    self.colors_in_sol.append(j)
                else:
                    result += [j[0]]
                    self.colors_in_sol.append(j[0])

        random.shuffle(result)

        return result

    def verification(self, guess, result):
        if guess == self.solution and result == ['B', 'B', 'B', 'B']:
            return True
        else:
            return False

    def solver(self):
        pass


if __name__ == '__main__':
    print('Welcome to MasterMind!')
    num_players = int(input('Would you like to play 1 Player or 2 Player? (Enter a 1 or 2)'))
    allow_duplicates = input('Allow duplicate colors in solution? (y/n)')

    if allow_duplicates == 'n':
        allow_duplicates = False
    else:
        allow_duplicates = True

    if num_players == 2:
        game = Game(2, allow_duplicates)
        print("Mastermind, have other player look away and create your solution using the following colors "
              "R, B, G, Y, O, W (Enter 1 at a time)\n")
        solution = []
        valid_picks = 4
        while valid_picks > 0:
            to_add = input()
            valid_choices = game.colors

            if to_add in valid_choices:
                if not game.duplicates and to_add in solution:
                    print('Cannot add color, already in solution')

                else:
                    solution.append(to_add)
                    valid_picks -= 1

            else:
                print('Please choose a valid option')

        game.solution = solution

    else:
        game = Game(1, allow_duplicates)
        game.create_solution()

    game.solution = ['Y', 'O', 'B', 'R']
    pprint.pprint(game.get_board())
    print(game.guess_row('Y', 'Y', 'Y', 'Y'))
    print(game.guess_row('Y', 'W', 'O', 'O'))
    print(game.guess_row('Y', 'W', 'O', 'O'))
    print(game.guess_row('Y', 'O', 'B', 'R'))
    print(game.guess_row('Y', 'W', 'O', 'O'))
    print(game.guess_row('Y', 'W', 'O', 'O'))
    print(game.guess_row('Y', 'W', 'O', 'O'))
    print(game.guess_row('Y', 'O', 'O', 'O'))
    pprint.pprint(game.get_board())

    print(f'Guess Counter: {game.guess_counter}')
    print(f'Game Over? {game.game_over}')
    print(f'Player Win? {game.player_win}')
    print(f'Computer Win? {game.comp_p2_win}')
