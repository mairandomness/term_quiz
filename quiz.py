#!/usr/bin/env python3

""" This is a quiz program that uses multiple choice questions """

import json
import random
from blessed import Terminal


class Game:
    """ Class that holds the game state """

    def __init__(self):
        self.term = Terminal()
        self.score = 0
        self.answer_pos = (0, 0)
        self.data = []
        self.curr_question = 0
        self.questions = []

    def set_data(self, filepath):
        """ Opens a JSON file and creates a list of dictionaries with keys being
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
            self.print_alert(
                "The source file didn't give me any good questions ;-; sorry and good bye")

        elif len(self.data) < 10:
            print(self.term.home + self.term.clear +
                  self.term.move_y(self.term.height // 2))
            self.print_alert(
                "The source file didn't give me enough questions for a full round of questions :(")
            self.print_alert(
                "The game will continue but will only have {} questions".format(len(self.data)))

    def set_questions(self):
        """ Creates a list of 10 (or less in case not enough questions are available)
        random unique questions """
        self.questions = random.sample(
            self.data, k=min(10, len(self.data)))

    def get_shuffled_answers(self):
        """ Creates a random ordering to display the answer options """
        answers = self.questions[self.curr_question]['incorrect'] + \
            [self.questions[self.curr_question]['correct']]
        random.shuffle(answers)
        return answers

    def get_any_key(self):
        """ Wait for any key input """
        with self.term.cbreak(), self.term.hidden_cursor():
            self.term.inkey()

    def print_alert(self, message, bold=False, blink=False):
        """ Prints message in the alert styling, bold and blink optional """
        if bold and blink:
            print(
                self.term.black_on_darkkhaki(self.term.bold(
                    self.term.blink(self.term.center(message)))))
        elif bold:
            print(
                self.term.black_on_darkkhaki(self.term.bold(self.term.center(message))))
        elif blink:
            print(
                self.term.black_on_darkkhaki(self.term.blink(self.term.center(message))))
        else:
            print(self.term.black_on_darkkhaki(self.term.center(message)))

    def print_welcome(self):
        """ Prints the welcome screen """
        print(self.term.home + self.term.clear +
              self.term.move_y(self.term.height // 2))
        self.print_alert('Hello! Welcome to this trivia game :D')
        self.print_alert('We are doing {} questions!'.format(
            len(self.questions)))
        self.print_alert('press any key to continue', blink=True)
        self.get_any_key()

    def print_question(self):
        """ Prints a question to the terminal """
        # Print the terminal screen
        print(self.term.home + self.term.clear)
        self.print_alert("YOUR CURRENT SCORE {}".format(self.score), bold=True)
        print(self.term.down(5))
        print(self.term.bold(" Question {}".format(self.curr_question + 1)))
        print(self.term.down(2))

        # Print the actual question
        print(" " + self.questions[self.curr_question]['question'])
        print(self.term.down(2))

        # Save the cursor position
        self.answer_pos = self.term.get_location()

    def print_alternatives(self, answers, selection):
        """ Prints the alternatives to the terminal, with the selected line
        being highlighted """

        y, x = self.answer_pos

        # Prints the alternatives according to the selection
        for j, answer in enumerate(answers):
            if j == selection:
                print(self.term.move_xy(x, y + j) + self.term.bold(self.term.reverse(
                    " > {}".format(answer))))
            else:
                print(self.term.move_xy(x, y + j) +
                      "   {}".format(answer))

    def get_input(self, answers):
        """ Gets the user input """

        # A loop to get the user input
        selection = 0
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                # Update alternative display
                self.print_alternatives(answers, selection)
                key = self.term.inkey()
                if key.name in ('KEY_TAB', 'KEY_DOWN'):
                    selection += 1
                elif key.name == 'KEY_UP':
                    selection -= 1
                elif key.name == 'KEY_ENTER':
                    break
                # Since there are only 4 options for the selection, let's make sure
                # it's in the correct range
                selection = selection % 4

        return answers[selection]

    def check_answer(self, answer):
        """ Compares user answer and responds accordingly """

        print(self.term.down(2))

        # Compare the user input
        if answer == self.questions[self.curr_question]['correct']:
            self.score += 1

            self.print_alert("Nice job! You got it right!")
        else:
            self.print_alert("You got it wrong, the correct answer was: ")
            self.print_alert(
                self.questions[self.curr_question]['correct'], bold=True)

        self.get_any_key()

    def print_new_score(self):
        """ Prints messages after each question is answered """
        # End game messages
        if self.curr_question == len(self.questions) - 1:
            self.print_alert("END OF GAME!", bold=True)
            self.print_alert("Your total score is {}/{} point(s)!!".format(
                self.score, len(self.questions)), bold=True)

            if self.score == len(self.questions):
                self.print_perfect()

        # Or just update the player on their score
        else:
            self.print_alert(
                "Your score is {} point(s) now.".format(self.score))

        print(self.term.move_xy(0, 1) + self.term.black_on_darkkhaki(
            self.term.center(self.term.bold("YOUR CURRENT SCORE {}".format(self.score)))))

        self.get_any_key()

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

    def run_game(self):
        """ Run the game!!! """
        with self.term.fullscreen():
            self.set_questions()
            self.print_welcome()

            while self.curr_question < len(self.questions):
                self.print_question()
                answers = self.get_shuffled_answers()
                inp = self.get_input(answers)
                self.check_answer(inp)
                self.print_new_score()
                self.curr_question += 1


if __name__ == '__main__':
    quiz = Game()
    quiz.set_data('Apprentice_TandemFor400_Data.json')
    quiz.run_game()
