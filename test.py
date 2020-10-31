#!/usr/bin/env python3

import unittest

from quiz import Game

class TestQuiz(unittest.TestCase):
    def test_set_data(self):
        quiz = Game()
        quiz.set_data("test_files/no_valid.json")
        self.assertEqual(len(quiz.data), 0)

        quiz = Game()
        quiz.set_data("test_files/two_questions.json")
        self.assertEqual(len(quiz.data), 2)

        quiz = Game()
        quiz.set_data("test_files/twenty_questions.json")
        self.assertEqual(len(quiz.data), 20)



    def test_set_question_order(self):
        quiz = Game()
        quiz.set_question_order()
        self.assertEqual(quiz.question_order, [])

        quiz = Game()
        quiz.set_data("test_files/two_questions.json")
        quiz.set_question_order()
        self.assertEqual(len(quiz.question_order), 2)

        quiz = Game()
        quiz.set_data("test_files/twenty_questions.json")
        quiz.set_question_order()
        self.assertEqual(len(quiz.question_order), 10)

if __name__ == '__main__':
    unittest.main()
