#!/usr/bin/env python3

""" This is a quiz program that uses multiple choice questions """

import json
import random
import interface


class Game:
    """ Class that holds the game state """

    def __init__(self):
        self.io = interface.InputOutput()
        self.score = 0
        self.data = []

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
            self.io.print_alert(
                "The source file didn't give me any good questions ;-; sorry and good bye", vcenter=True)

        elif len(self.data) < 10:
            self.io.print_alert(
                "The source file didn't give me enough questions for a full round of questions :(", vcenter=True)
            self.io.print_alert(
                "The game will continue but will only have {} questions".format(len(self.data)))

    def get_questions(self):
        """ Creates a list of 10 (or less in case not enough questions are available)
        random unique questions """
        return random.sample(self.data, k=min(10, len(self.data)))

    def get_shuffled_answers(self, question):
        """ Creates a random ordering to display the answer options """
        answers = question['incorrect'] + [question['correct']]
        random.shuffle(answers)
        return answers

    def check_answer(self, answer, question):
        """ Compares user answer and responds accordingly """

        # Compare the user input
        if answer == question['correct']:
            self.score += 1

            self.io.print_alert("Nice job! You got it right!")
        else:
            self.io.print_alert("You got it wrong, the correct answer was: ")
            self.io.print_alert(question['correct'], bold=True)

        self.io.get_any_key()

    def run_game(self):
        """ Run the game!!! """
        with self.io.fullscreen():
            questions = self.get_questions()
            self.io.print_welcome(len(questions))

            for question_index, question in enumerate(questions):
                self.io.print_question(
                    self.score, question_index, question['question'])
                answers = self.get_shuffled_answers(question)
                inp = self.io.get_input(answers)
                self.check_answer(inp, question)
                self.io.print_new_score(
                    self.score, question_index, len(questions))


if __name__ == '__main__':
    quiz = Game()
    quiz.set_data('Apprentice_TandemFor400_Data.json')
    quiz.run_game()
