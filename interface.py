from blessed import Terminal


class InputOutput:
    """ Class that takes care of inputs and outputs """

    def __init__(self):
        self.term = Terminal()
        self.answer_pos = (0, 0)

    def fullscreen(self):
        return self.term.fullscreen()

    def print_alert(self, message, bold=False, blink=False, vcenter=False):
        """ Prints message in the alert styling, bold and blink optional """
        if vcenter:
            print(self.term.home + self.term.clear +
                  self.term.move_y(self.term.height // 2))

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

    def get_any_key(self):
        """ Wait for any key input """
        with self.term.cbreak(), self.term.hidden_cursor():
            self.term.inkey()

    def print_welcome(self, num_questions):
        """ Prints the welcome screen """
        self.print_alert('Hello! Welcome to this trivia game :D', vcenter=True)
        self.print_alert('We are doing {} questions!'.format(
            num_questions))
        self.print_alert('press any key to continue', blink=True)
        self.get_any_key()

    def print_question(self, score, question_index, question_text):
        """ Prints a question to the terminal """
        # Print the terminal screen
        print(self.term.home + self.term.clear)
        self.print_alert("YOUR CURRENT SCORE IS {}".format(score), bold=True)
        print(self.term.down(5))
        print(self.term.bold(" Question {}".format(question_index + 1)))
        print(self.term.down(2))

        # Print the actual question
        print(" " + question_text)
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

        print(self.term.down(2))

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

    def print_new_score(self, score, question_index, total_questions):
        """ Prints messages after each question is answered """
        # End game messages
        if question_index == total_questions - 1:
            self.print_alert("END OF GAME!", bold=True)
            self.print_alert("Your total score is {}/{} point(s)!!".format(
                score, total_questions), bold=True)

            if score == total_questions:
                self.print_perfect()

        # Or just update the player on their score
        else:
            self.print_alert(
                "Your score is {} point(s) now.".format(score))

        print(self.term.move_xy(0, 0))
        self.print_alert("YOUR CURRENT SCORE IS {}".format(score), bold=True)

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
