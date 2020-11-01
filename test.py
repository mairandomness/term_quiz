#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from quiz import Game


@patch("interface.InputOutput")
class TestQuiz(unittest.TestCase):

    def test_set_data(self, mock_io):
        io = mock_io()
        quiz = Game()
        quiz.set_data("test_files/no_valid.json")
        self.assertEqual(len(quiz.data), 0)
        self.assertEqual(io.print_alert.call_count, 1)
        self.assertIn("good bye", io.print_alert.call_args[0][0])

        io.reset_mock()
        quiz = Game()
        quiz.set_data("test_files/two_questions.json")
        self.assertEqual(len(quiz.data), 2)
        self.assertEqual(io.print_alert.call_count, 2)
        self.assertIn("will continue", io.print_alert.call_args[0][0])

        io.reset_mock()
        quiz = Game()
        quiz.set_data("test_files/twenty_questions.json")
        self.assertEqual(len(quiz.data), 20)
        io.print_alert.assert_not_called()

    def test_get_questions(self, mock_io):
        quiz = Game()
        self.assertEqual(quiz.get_questions(), [])

        quiz = Game()
        quiz.set_data("test_files/two_questions.json")
        self.assertEqual(len(quiz.get_questions()), 2)

        quiz = Game()
        quiz.set_data("test_files/twenty_questions.json")
        self.assertEqual(len(quiz.get_questions()), 10)

    def test_get_shuffled_answers(self, mock_io):
        quiz = Game()
        with self.assertRaises(KeyError):
            quiz.get_shuffled_answers({})

        with self.assertRaises(KeyError):
            quiz.get_shuffled_answers({'incorrect': ['a']})

        quiz = Game()
        quiz.set_data("test_files/two_questions.json")
        questions = quiz.get_questions()
        self.assertEqual(len(quiz.get_shuffled_answers(questions[0])), 4)

        quiz = Game()
        quiz.set_data("test_files/twenty_questions.json")
        questions = quiz.get_questions()
        self.assertEqual(len(quiz.get_shuffled_answers(questions[9])), 4)

    def test_check_answer(self, mock_io):
        quiz = Game()
        quiz.set_data("test_files/twenty_questions.json")
        questions = quiz.get_questions()

        for question in questions:
            self.assertEqual(quiz.score, 0)

            quiz.check_answer(question['incorrect'][0], question)
            self.assertEqual(quiz.score, 0)

            quiz.check_answer(question['correct'], question)
            self.assertEqual(quiz.score, 1)

            quiz.check_answer(question['correct'], question)
            self.assertEqual(quiz.score, 2)

            quiz.check_answer(question['incorrect'][1], question)
            self.assertEqual(quiz.score, 2)

            quiz.check_answer(question['incorrect'][2], question)
            self.assertEqual(quiz.score, 2)

            quiz.score = 0

    def test_run_game(self, mock_io):
        io = mock_io()

        io.reset_mock()
        quiz = Game()
        quiz.run_game()
        io.print_alert.assert_not_called()
        self.assertEqual(quiz.score, 0)

        io.reset_mock()
        quiz = Game()
        quiz.set_data("test_files/no_valid.json")
        quiz.run_game()
        self.assertEqual(io.print_alert.call_count, 1)
        io.print_question.assert_not_called()
        io.print_alternatives.assert_not_called()
        self.assertEqual(quiz.score, 0)

        io.reset_mock()
        quiz = Game()
        quiz.set_data("test_files/two_questions.json")
        quiz.run_game()
        self.assertEqual(io.print_question.call_count, 2)
        self.assertEqual(io.get_input.call_count, 2)
        self.assertEqual(quiz.score, 0)

        io.reset_mock()
        quiz = Game()
        quiz.set_data("test_files/twenty_questions.json")
        quiz.run_game()
        self.assertEqual(io.print_question.call_count, 10)
        self.assertEqual(io.get_input.call_count, 10)
        self.assertEqual(quiz.score, 0)

        io.reset_mock()
        io.get_input.return_value = "Devmynd"
        quiz = Game()
        quiz.set_data("test_files/two_questions.json")
        quiz.run_game()
        self.assertEqual(io.print_question.call_count, 2)
        self.assertEqual(io.get_input.call_count, 2)
        self.assertEqual(quiz.score, 1)




if __name__ == '__main__':
    unittest.main()
