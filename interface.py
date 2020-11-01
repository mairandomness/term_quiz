from blessed import Terminal


class InputOutput:
    """ Class that takes care of inputs and outputs.
    It takes care of printing and updating all quiz screens to the terminal
    and receiving and interpreting user key presses"""

    def __init__(self):
        self.term = Terminal()
        # self.answer_pos is a tuple that holds the position that
        # the cursor should be moved to to print the answers to the screen
        # whenever they need to be updated
        self.answer_pos = (0, 0)

    def fullscreen(self):
        return self.term.fullscreen()

    def print_alert(self, message, bold=False, blink=False, vcenter=False):
        """ Prints message in the alert styling, bold and blink optional.
        vcenter is also optional and prints a clean terminal  and positions the
        cursor at the middle of the screen on the y axis"""
        if vcenter:
            self.print_clean_term()
            print(self.term.move_y(self.term.height // 2))
        if bold:
            message = self.term.bold(message)
        if blink:
            message = self.term.blink(message)

        print(self.term.black_on_darkkhaki(self.term.center(message)))

    def wait_for_user(self):
        """ Wait for any key input """
        with self.term.cbreak(), self.term.hidden_cursor():
            self.term.inkey()

    def print_clean_term(self):
        """ Print a new clean terminal screen """
        print(self.term.home + self.term.clear)

    def print_header(self, score):
        """ Function that prints the header that contains the player score """
        print(self.term.move_xy(0, 0))
        self.print_alert("YOUR CURRENT SCORE IS {}".format(score), bold=True)

    def print_welcome(self, num_questions):
        """ Receives the total number of questions and prints the welcome screen """

        self.print_alert('Hello! Welcome to this trivia game :D', vcenter=True)
        self.print_alert('We are doing {} questions!'.format(
            num_questions))
        self.print_alert('press any key to continue', blink=True)
        self.wait_for_user()

    def print_question(self, question_index, question_text):
        """ Prints a question to the terminal """
        # Print new lines and the question number
        print(self.term.down(5))
        print(self.term.bold(" Question {}".format(question_index + 1)))
        print(self.term.down(2))

        # Print the actual question
        print(" " + question_text)
        print(self.term.down(2))

        # Save the cursor position to print the alternatives
        self.answer_pos = self.term.get_location()

    def print_choices(self, answers, selection):
        """ Takes answer and selection as arguments.
        selection being an int that indexes answers
        and prints the alternatives to the terminal, with the selected line
        being highlighted """

        y, x = self.answer_pos

        if selection not in range(len(answers)):
            selection = 0

        # Prints the alternatives according to the selection position
        for j, answer in enumerate(answers):
            if j == selection:
                print(self.term.move_xy(x, y + j) + self.term.bold(self.term.reverse(
                    " > {}".format(answer))))
            else:
                print(self.term.move_xy(x, y + j) + "   {}".format(answer))

        print(self.term.down(2))

    def get_input(self, answers):
        """ Gets the user input by taking key presses to navigate the
        possible answers and returns the selected answer"""

        # A loop to get the user input
        selection = 0
        with self.term.cbreak(), self.term.hidden_cursor():
            while True:
                # Update the answer choices display
                self.print_choices(answers, selection)
                key = self.term.inkey()
                if key.name in ('KEY_TAB', 'KEY_DOWN'):
                    selection += 1
                elif key.name == 'KEY_UP':
                    selection -= 1
                elif key.name == 'KEY_ENTER':
                    break
                # Since there are limited options for the selection, let's make sure
                # it's in the correct range
                selection = selection % len(answers)

        return answers[selection]

    def print_new_score(self, score, question_index, total_questions):
        """ Updates score after each question is answered """

        self.print_alert("Your score is {} point(s) now.".format(score))
        # Update header
        self.print_header(score)
        self.wait_for_user()

    def print_end(self, score, total_questions):
        """ Prints the end game screen """

        self.print_alert("END OF GAME!", bold=True, vcenter=True)
        self.print_alert("Your final score is {}/{} point(s)!!".format(
            score, total_questions), bold=True)

        if score == total_questions:
            self.print_perfect()

        self.wait_for_user()

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
