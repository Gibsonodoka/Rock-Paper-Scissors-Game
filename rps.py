#!/usr/bin/env python3

#-----------------------------------------------------------------------------
# This project plays a game of Rock, Paper, Scissors between two Players,
# and reports both Players scores each round.
#-----------------------------------------------------------------------------

import random
import time
import string
import enum
import sys


moves = ['rock', 'paper', 'scissors']   

# The Player class is the parent class for all of the Players in this game



# Color utilities for the game
class Color(enum.Enum):
    red = '\033[91m'
    purple = '\033[95m'
    blue = '\033[94m'
    cyan = '\033[96m'
    green = '\033[92m'
    black = '\033[0m'

    def get_color(color_type):
        if(color_type == "error"):
            return Color.red.value
        elif(color_type == "info"):
            return Color.cyan.value
        elif(color_type == "success"):
            return Color.green.value

        return Color.purple.value


def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


def typewriter_simulator(message, color):
    for char in message:
        print(color + char, end='', flush=True)
        if char in string.punctuation:
            time.sleep(.2)
        time.sleep(.03)


def print_wait(prompt, wait_time=0, color_type=""):
    typewriter_simulator(prompt, Color.get_color(color_type))
    print('')
    time.sleep(wait_time)

#  Function for validation of input

def valid_string_input(prompt, options=[]):
    while True:
        response = input(prompt).lower()
        if len(options) < 1 or response in options:
            return response
        print_wait(f"{response} is invalid, try again.", color_type="error")


class Player:
    def __init__(self, name=""):
        self.name = name

    def move(self):
        return 'rock'

    def learn(self, my_move, their_move):
        pass

# Randomplayer picks moves at random
class RandomPlayer(Player):
    

    def move(self):
        return random.choice(moves)

# Human player
class HumanPlayer(Player):

    def move(self):
        return valid_string_input("Rock, paper, scissors > ",
                                  ["rock", "paper", "scissors"])

# This player remembers the last move of the opponent and plays it this time
class ReflectivePlayer(Player):

    def __init__(self, name=""):
        super().__init__(name)
        self.next_move = random.choice(moves)

    def move(self):
        return self.next_move

    def learn(self, my_move, their_move):
        self.next_move = their_move


class CyclePlayer(Player):

    def __init__(self, name=""):
        super().__init__(name)
        self.next_move = random.choice(moves)

    def move(self):
        return self.next_move

    def learn(self, my_move, their_move):
        i = 0
        while i < 3:
            if(my_move == moves[i]):
                i = (i+1) % 3
                self.next_move = moves[i]
                break
            i += 1


class Game:
    def __init__(self, p1=HumanPlayer("Player 1"),
                 p2=Player("Player 2")):
        self.score = {1: 0, 2: 0}
        self.p1 = p1  # The human player
        self.p2 = p2  # The computer player

    def player_introduction(self):
        print_wait("Welcome to Rock, paper and scissors game.\n\n")
        my_name = valid_string_input(
            "Introduce yourself by telling us your name: ")
        self.p1.name = my_name[0].upper()+my_name[1:]
        print_wait(f"Hello {self.p1.name},", 1)
        print_wait("Choose who you would like to play with ", 1)
        name = valid_string_input(
            "Jack, Miles or Star: ", ["jack", "miles", "star"])
        if name == "jack":
            self.p2 = RandomPlayer(name[0].upper()+name[1:])
        elif name == "miles":
            self.p2 = ReflectivePlayer(name[0].upper()+name[1:])
        elif name == "star":
            self.p2 = CyclePlayer(name[0].upper()+name[1:])
        print_wait(
            f"\n\n{self.p1.name}, Your opponent is {self.p2.name}!", 1)

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        if(move1 != move2):
            self.score[1] += beats(move1, move2)
            self.score[2] += beats(move2, move1)
        print_wait(
            f"Move: {self.p1.name} - {move1},  {self.p2.name} - {move2}",
            1, color_type="info")
        print_wait(
            f"Score: {self.p1.name} {self.score[1]}, "
            f"{self.p2.name} {self.score[2]}\n\n", color_type="info")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    def play_game(self):
        play_again = 'y'
        while play_again == 'y':
            self.score = {1: 0, 2: 0}
            print_wait("\n\nYou have 3 rounds.")
            print_wait("Game start in...")
            print_wait("1", 1)
            print_wait("2", 1)
            print_wait("3\n\n", 1)
            for round in range(3):
                print_wait(f"Round {round}:", 1)
                self.play_round()

            if (self.score[1] > self.score[2]):
                print_wait(f"*** {self.p1.name}, you won!! ***", 1, "success")
            elif (self.score[1] < self.score[2]):
                print_wait(
                    f"**** {self.p1.name}, you have been defeated by "
                    f"{self.p2.name}. Your oponent!! ***", 1, "error")
            else:
                print_wait(f"Its a tie!!! There is no winner or loser.", 1)

            print_wait(
                f"Score: {self.p1.name} {self.score[1]}, "
                f"{self.p2.name} {self.score[2]}\n\n", 1, "info")
            play_again = valid_string_input("Play again? Y or N: ", "y,n")

        print_wait("Game over!", 1)


if __name__ == '__main__':
    try:
        game = Game()
        game.player_introduction()
        game.play_game()
    except TypeError as e:
        print(e)
        sys.exit(1)
    except NameError as e:
        print(e)
        sys.exit(1)
    except IndexError as e:
        print(e)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nProgram interrupted.")
        sys.exit(1)