#!/usr/bin/env python3

import json
import random
from blessed import Terminal

""" This is a quiz program that uses multiple choice questions """


class Game:
    """ Class that holds the game state """

    def __init__(self):
        self.term = Terminal()
        self.selection = 0
        self.selection_in_progress = True
        self.xy = (0, 0)
        self.score = 0
        self.data = []
        self.question_order = []
        self.curr_question = 0
        self.answers = []
        self.answer_order = []
        self.correct_selection = 0

    def set_data(self, filepath):
        """
        Opens a JSON file and creates a list of dictionaries with keys being
        'question', 'incorrect' (3 options) and 'correct'."""

        # First, let's open and parse the JSON file
        with open(filepath) as f:
            original_data = json.load(f)

        # We'll clean the questions that don't suit our needs
        self.data = []
        for line in original_data:
            if set(line.keys()) == set(['question', 'incorrect', 'correct']) and \
                    len(set(line['incorrect'])) == 3 and \
                    isinstance(line['incorrect'], list) and \
                    isinstance(line['question'], str) and \
                    isinstance(line['correct'], str) and \
                    isinstance(line['incorrect'][0], str) and \
                    isinstance(line['incorrect'][1], str) and \
                    isinstance(line['incorrect'][2], str) and \
                    line['correct'] not in line['incorrect'] and \
                    line not in self.data:
                self.data.append(line)

        # Make sure we have enough questions
        if len(self.data) == 0:
            print(self.term.home + self.term.clear +
                  self.term.move_y(self.term.height // 2))
            print(self.term.black_on_darkkhaki(self.term.center(
                "The source file didn't give me any good questions ;-; sorry and good bye")))

        elif len(self.data) < 10:
            print(self.term.home + self.term.clear +
                  self.term.move_y(self.term.height // 2))
            print(self.term.black_on_darkkhaki(self.term.center(
                "The source file didn't give me enough questions for a full round of questions :(")))
            print(self.term.black_on_darkkhaki(self.term.center(
                "The game will continue but will only have {} questions".format(len(self.data)))))

    def set_question_order(self):
        """ Creates 10 (or less in case not enough questions are available)
        random unique numbers as a selection of our questions """
        population = list(range(len(self.data)))
        self.question_order = random.sample(
            population, k=min(10, len(self.data)))

    def set_answer_order_and_correct_selection(self):
        """ Creates a random ordering to display the answer options """
        self.answer_order = [0, 1, 2, 3]
        random.shuffle(self.answer_order)

    def print_welcome(self):
        """ Prints the welcome screen """
        print(self.term.home + self.term.clear +
              self.term.move_y(self.term.height // 2))
        print(self.term.black_on_darkkhaki(self.term.center(
            'Hello! Welcome to this trivia game :D')))
        print(self.term.black_on_darkkhaki(
            self.term.center('We are doing {} questions!'.format(min(10, len(self.data))))))
        print(self.term.black_on_darkkhaki(
            self.term.center(self.term.blink('press any key to continue'))))

        with self.term.cbreak(), self.term.hidden_cursor():
            inp = self.term.inkey()

    def print_question(self):
        """ Prints a question to the terminal """
        # Randomize the answer choices ordering
        self.set_answer_order_and_correct_selection()

        # Print the terminal screen
        print(self.term.home + self.term.clear)
        print(self.term.black_on_darkkhaki(
            self.term.center(self.term.bold("YOUR CURRENT SCORE {}".format(self.score)))))
        print(self.term.down(5))
        print(self.term.bold(" Question {}".format(self.curr_question + 1)))
        print(self.term.down(2))

        question = self.data[self.question_order[self.curr_question]]
        # Note that answers[3] is the correct answer
        self.answers = question['incorrect'] + [question['correct']]
        self.correct_answer = question['correct']
        self.correct_selection = self.answer_order.index(3)

        # Print the actual question
        print(" {}".format(question['question']))
        print(self.term.down(2))

        # Save the cursor position
        self.xy = self.term.get_location()

        # Reset the selection
        self.selection = 0

    def print_alternatives(self):
        """ Prints the alternatives to the terminal, with the selected line
        being highlighted """

        y, x = self.xy

        # Prints the alternatives according to the selection
        for j, i in enumerate(self.answer_order):
            if j == self.selection:
                print(self.term.move_xy(x, y + j) + self.term.bold(self.term.darkkhaki(
                    " > {}".format(self.answers[i]))))
            else:
                print(self.term.move_xy(x, y + j) +
                      "   {}".format(self.answers[i]))

    def get_input(self):
        """ Gets the user input """

        # A loop to get the user input
        with self.term.cbreak(), self.term.hidden_cursor():
            while self.selection_in_progress:
                key = self.term.inkey()
                if key.name == 'KEY_TAB':
                    self.selection += 1
                if key.name == 'KEY_DOWN':
                    self.selection += 1
                if key.name == 'KEY_UP':
                    self.selection -= 1
                if key.name == 'KEY_ENTER':
                    self.selection_in_progress = False
                # Since there are only 4 options for the selection, let's make sure
                # it's in the correct range
                self.selection = self.selection % 4

                # Update screen
                self.print_alternatives()

        # Reset selection_in_progress
        self.selection_in_progress = True

    def check_answer(self):
        """ Compares user answer and responds accordingly """

        print(self.term.down(2))

        # Compare the user input
        if self.selection == self.correct_selection:
            self.score += 1

            print(self.term.black_on_darkkhaki(
                self.term.center("Nice job! You got it right!")))
        else:
            print(self.term.black_on_darkkhaki(self.term.center(
                "You got it wrong, the correct answer was: ")))
            print(self.term.black_on_darkkhaki(self.term.center(
                self.term.bold("{}".format(self.correct_answer)))))

        with self.term.cbreak(), self.term.hidden_cursor():
            inp = self.term.inkey()

        # End game messages
        if self.curr_question == len(self.question_order) - 1:
            print(self.term.black_on_darkkhaki(
                self.term.center(self.term.bold("END OF GAME!".format(self.score)))))
            print(self.term.black_on_darkkhaki(
                self.term.center(self.term.bold("Your total score is {}/{} point(s)!!"
                                                .format(self.score, len(self.question_order))))))
            if self.score == 10:
                self.print_perfect()
        else:
            print(self.term.black_on_darkkhaki(
                self.term.center("Your score is {} point(s) now.".format(self.score))))

        self.term.move_y(0)
        print(self.term.move_xy(0, 1) + self.term.black_on_darkkhaki(
            self.term.center(self.term.bold("YOUR CURRENT SCORE {}".format(self.score)))))

        with self.term.cbreak(), self.term.hidden_cursor():
            inp = self.term.inkey()

    def print_perfect(self):
        """ Prints a treat for a perfect game """

        print(self.term.down(3))
        print(self.term.center(
            "                  __          _                             "))
        print(self.term.center(
            "                 / _|        | |                            "))
        print(self.term.center(
            "  _ __   __ _ ___| |_ ___  ___| |_    __ _  __ _ _ __ ___   ___ "))
        print(self.term.center(
            "  | '_ \\ / _ \\ '__|  _/ _ \\/ __| __/  / _` |/ _` | '_ ` _ \\ / _ \\"))
        print(self.term.center(
            "  | |_) |  __/ |  | ||  __/ (__| |   | (_| | (_| | | | | | |  __/"))
        print(self.term.center(
            "  | .__/ \\___|_|  |_| \\___|\\___|\\__/  \\__, |\\__,_|_| |_| |_|\\___|"))
        print(self.term.center(
            "  | |                                  __/ |                     "))
        print(self.term.center(
            "  |_|                                 |___/                      "))


def run_game():
    quiz = Game()
    quiz.set_data('Apprentice_TandemFor400_Data.json')
    quiz.set_question_order()

    with quiz.term.fullscreen():
        quiz.print_welcome()

        while quiz.curr_question < min(10, len(quiz.data)):
            quiz.print_question()
            quiz.print_alternatives()
            quiz.get_input()
            quiz.check_answer()
            quiz.curr_question += 1


if __name__ == '__main__':
    run_game()
