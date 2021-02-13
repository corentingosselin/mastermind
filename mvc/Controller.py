import MasterMind
from mvc.Model import Model
from mvc.View import View
from tkinter.messagebox import showinfo
from tkinter import messagebox, Text, INSERT


#
# Controller.class
#
# @Description:
#
#  The controller is the bridge between the view and the model
#  It is able to listen interaction, and handle all the game mechanic
#
class Controller:

    def __init__(self, root):
        self.view = View(self, root)
        self.model = Model()

    def set_color(self, event):
        if not self.model.started:
            return
        item = event.widget.find_closest(event.x, event.y)
        tag = event.widget.itemcget(item, "tag")
        pos = tag.replace("{", "").replace("}", "").replace(" current", "").split(";")
        column = int(pos[0])
        row = int(pos[1])

        # No color selected by player
        if self.model.color_selected is not None:
            # If the slot clicked is right
            if row == self.model.currentLine:
                self.model.set_slot(column, self.model.color_selected)
                self.view.update_color(event, self.model.color_selected)

    def set_answer(self, event):
        if self.model.started:
            return
        item = event.widget.find_closest(event.x, event.y)
        tag = event.widget.itemcget(item, "tag")
        slot = int(tag.replace("{", "").replace("}", "").replace(" current", "").replace("answer_", ""))
        # get selected color
        if self.model.color_selected is not None:
            self.view.update_color_answer(event, self.model.color_selected)
            self.model.answer[slot] = self.model.color_selected

        for answer in self.model.answer:
            if answer is None:
                return
        # start game if answer is ready
        self.start_game()

    def start_game(self):

        self.view.answer.delete(self.view.text_help)
        self.model.started = True

        # hide back answer
        i = 0
        for answer in self.model.answer:
            id = "answer_" + str(i)
            item = self.view.answer.find_withtag(id)
            self.view.answer.itemconfig(item, fill="black")
            i += 1
        # Display the button
        self.view.setup_button()

    def test(self):

        # check if 4 colors are selected
        for c in self.model.get_colors():
            if c is None:
                showinfo("Info", "Vous devez remplir la ligne " + str(
                    self.model.currentLine + 1) + " pour tester cette dernière")
                return

        # check if the color combination has not been tested yet
        if self.model.currentLine > 0:
            current = 0
            for list in self.model.slots:

                if current != self.model.currentLine:
                    if list == self.model.get_colors():
                        showinfo("Attention", "Il semblerait que vous ayez déjà testé cette combinaison...")
                        self.reset_slot()
                        return
                current += 1

        # check if win
        if self.model.has_won():
            result = messagebox.askquestion("Bravo", "Vous avez gagné ! Désirez-vous rejouer ?")
            if result == 'yes':
                self.view.window.destroy()
                MasterMind.MasterMind()
            else:
                self.view.window.destroy()
            return

        # Update helpers

        # First look for right position (red)
        colors = []
        for a in self.model.answer:
            colors.append(a)

        found = []
        last_index = 0
        for id in range(0, 4):
            answer = self.model.answer[id]
            test = self.model.get_colors()[id]
            if answer == test:
                self.view.update_color_helper(self.model.currentLine, last_index, "red")
                colors.remove(answer)
                found.append(id)
                last_index += 1


        # First check, impossible to have only 1 white
        white_amount = 0
        if len(found) < 3:
            for id in range(0, 4):
                if id not in found:
                    # check color
                    color = self.model.get_colors()[id]
                    if colors.__contains__(color):
                        white_amount += 1


        if white_amount > 0:
            for i in range(0, white_amount):
                self.view.update_color_helper(self.model.currentLine, last_index, "white")
                last_index+=1

        # Allow the player to place color to the next line
        self.model.next_line()

        # check loose
        if self.model.currentLine >= self.model.maxLine:
            self.game_over()
            self.view.display_answer(self.model.answer)

    def game_over(self):
        # Prevent interaction
        self.model.started = False

        # change button name
        self.view.button.config(text="Rejouer")
        self.view.button.config(highlightbackground='#353434')
        self.view.button.config(command=self.retry)

        # add text lost
        lost = Text(self.view.window, font="Times 20 bold", bg="#353434", highlightthickness=0)
        lost.insert(INSERT, "VOUS AVEZ PERDU")
        lost.place(anchor="w", y=300, x=450, height=30, width=200)

    # Restart
    def retry(self):
        self.view.window.destroy()
        MasterMind.MasterMind()

    # Set all line black color and reset the model
    def reset_slot(self):
        self.view.reset_colors(self.model.currentLine)
        self.model.slots[self.model.currentLine] = [None] * 4
