#!/usr/bin/env python3

""" This is a Python program that uses the blessed library to launch a quiz that uses
multiple choice questions on the terminal"""

import json
import random
import interface


class Quiz:
    """ Class that holds the game state and the io object,
    which has the capabilities to print things to terminal and recover user key presses"""

    def __init__(self):
        self.io = interface.InputOutput()
        self.score = 0
        self.data = []

    def is_valid_question(self, question):
        """ Returns true if question is a valid question or false otherwise """
        # The number of alternatives that each question is expected to have
        # We have 4 hardcoded only here, in case that changes
        alternative_number = 4

        # We expect a valid answer to not be a duplicate of another valid question
        if question in self.data:
            return False

        # We expect a question to have the fields 'question', 'incorrect', 'correct'
        # It's ok if it has more information, but we use only what we need
        elif 'question' not in question.keys():
            return False
        elif 'correct' not in question.keys():
            return False
        elif 'incorrect' not in question.keys():
            return False

        # We expect question['incorrect'] to:
        # - be a list
        elif not isinstance(question['incorrect'], list):
            return False
        # - have (alternative_number - 1) elements
        elif len(question['incorrect']) != alternative_number - 1:
            return False
        # - for the alternatives to be distinct
        elif len(set(question['incorrect'])) != len(question['incorrect']):
            return False

        # We expect question['question'] and question['correct'] to be strings
        elif not isinstance(question['question'], str):
            return False
        elif not isinstance(question['correct'], str):
            return False

        # We expect the correct answer to not be in the incorrect alternatives
        elif question['correct'] in question['incorrect']:
            return False

        # We expect the type of each alternative in question['incorrect'] to be a string
        for alternative in question['incorrect']:
            if not isinstance(alternative, str):
                return False

        return True

    def load_data(self, filepath):
        """ Opens a JSON file, reads it and creates a list of dictionaries with keys being
        'question', 'incorrect' and 'correct' """

        # First, let's open and parse the JSON file
        with open(filepath) as f:
            original_data = json.load(f)

        # We'll clean the questions that don't suit our needs
        self.data = []
        for question in original_data:
            if self.is_valid_question(question):
                self.data.append(question)

        # Make sure we have enough questions
        if len(self.data) == 0:
            self.io.print_alert(
                "The source file didn't give me any good questions", vcenter=True)

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
        """ Compares user answer with the correct option and responds accordingly """

        # Compare the user input
        if answer == question['correct']:
            self.score += 1

            self.io.print_alert("Nice job! You got it right!")
        else:
            self.io.print_alert("You got it wrong, the correct answer was: ")
            self.io.print_alert(question['correct'], bold=True)

    def run_game(self):
        """ Run the game!!! """
        self.score = 0

        if not self.data:
            self.io.print_alert(
                "No questions were loaded ;-; sorry and good bye", vcenter=True)

        questions = self.get_questions()
        self.io.print_welcome(len(questions))

        for question_index, question in enumerate(questions):
            self.io.print_clean_term()
            self.io.print_header(self.score)
            self.io.print_question(question_index, question['question'])
            answers = self.get_shuffled_answers(question)
            selected = self.io.get_input(answers)
            self.check_answer(selected, question)
            self.io.print_new_score(
                self.score, question_index, len(questions))

        self.io.print_end(self.score, len(questions))


if __name__ == '__main__':
    quiz = Quiz()
    with quiz.io.fullscreen():
        quiz.load_data('Apprentice_TandemFor400_Data.json')
        quiz.run_game()
