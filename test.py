#!/usr/bin/env python3

import unittest

from quiz import Game

class TestQuiz(unittest.TestCase):
    def test_set_data(self):
        quiz = Game()
        # the fullscreen is in the tests to make the output cleaner
        with quiz.term.fullscreen():
            quiz.set_data("test_files/no_valid.json")
            self.assertEqual(len(quiz.data), 0)

        quiz = Game()
        with quiz.term.fullscreen():
            quiz.set_data("test_files/two_questions.json")
            self.assertEqual(len(quiz.data), 2)

        quiz = Game()
        with quiz.term.fullscreen():
            quiz.set_data("test_files/twenty_questions.json")
            self.assertEqual(len(quiz.data), 20)



    def test_set_questions(self):
        quiz = Game()
        with quiz.term.fullscreen():
            quiz.set_questions()
            self.assertEqual(quiz.questions, [])

        quiz = Game()
        with quiz.term.fullscreen():
            quiz.set_data("test_files/two_questions.json")
            quiz.set_questions()
            self.assertEqual(len(quiz.questions), 2)

        quiz = Game()
        with quiz.term.fullscreen():
            quiz.set_data("test_files/twenty_questions.json")
            quiz.set_questions()
            self.assertEqual(len(quiz.questions), 10)

    def test_get_shuffled_answers(self):
        quiz = Game()
        with quiz.term.fullscreen():
            quiz.set_questions()
            self.assert_Equal(len(quiz.get_shuffled_answers(), 4))
            self.assertIsInstance(quiz.get_shuffled_answers[0], str)

        quiz = Game()
        with quiz.term.fullscreen():
            quiz.set_data("test_files/two_questions.json")
            quiz.set_questions()
            self.assert_Equal(len(quiz.get_shuffled_answers(), 4))
            self.assertIsInstance(quiz.get_shuffled_answers[0], str)

        quiz = Game()
        with quiz.term.fullscreen():
            quiz.set_data("test_files/twenty_questions.json")
            quiz.set_questions()
            self.assert_Equal(len(quiz.get_shuffled_answers(), 4))
            self.assertIsInstance(quiz.get_shuffled_answers[0], str)

if __name__ == '__main__':
    unittest.main()
