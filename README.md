# Terminal quiz

This is an application that launches a quiz with multiple choice questions on the terminal, using Python and the blessed library

## Requirements for running it

1. Have Python 3 installed

2. Install the blessed library. If you use pip as a package installer, you can do this by running the following in your terminal:
```
pip install blessed
```

## How to use it

1. Download the contents of this repository. If you use git, you can run the following in your terminal:
```
git clone https://github.com/mairandomness/term_quiz.git
```

2. Enter the folder from the terminal.
```
cd term_quiz
```

3. To run the quiz you can type
```
python3 quiz.py
```

or

```
./quiz.py
```

## Tests

To run the tests:

1. Enter the folder from the terminal.
```
cd term_quiz
```

2. To run the test results you can type
```
python3 test.py
```

or

```
./test.py
```

## Additional information

The quiz works by reading a JSON file with questions, each question having the fields: question, correct, incorrect. A valid question is considered one that has 4 distinct alternatives in total.
You can see examples of valid and invalid question formats in the test files or you can see the considerations made in the `is_valid_question` function in the `quiz.py` file.

In case you want to change the questions in the quiz, you can edit the `Apprentice_TandemFor400_Data.json` file or add your own JSON file and edit the main function in `quiz.py` and change the argument that goes in the `load_data` function.


#### Assumptions on the original project proposal
* A round of trivia has 10 questions
* All questions are multiple-choice questions
* Your score does not need to update in real time
* Results can update on form submit, button click, or any interaction you choose
* We will provide you with the trivia data such as the questions, correct and incorrect answers via a
JSON file.

#### Acceptance criteria on the original project proposal
* A user can view questions.
* Questions with their multiple choice options must be displayed one at a time.
* Questions should not repeat in a round.
* A user can select only 1 answer out of the 4 possible answers.
* The correct answer must be revealed after a user has submitted their answer
* A user can see the score they received at the end of the round
