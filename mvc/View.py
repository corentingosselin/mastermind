from tkinter import *
from Pos import Pos


class View:

    def __init__(self, controller, window):
        self.controller = controller
        self.colors = [
            "green",
            "blue",
            "orange",
            "red",
            "yellow",
            "purple"
        ]

        self.window = window
        self.window.title("MasterMind")
        self.window.geometry("720x900")

        self.window.minsize(720, 900)
        self.window.maxsize(720, 900)
        self.window.config(background="#353434")

        # will be removed after the game start
        self.help = Canvas(self.window, width=265, height=20, background='#9F9F9F', highlightthickness=0)
        self.help.pack(padx="85", pady="0", anchor="w")
        self.help.create_text(130,10,text="Cliquez sur une couleur pour selectionner")

        # setup
        self.setup_color_picker()
        self.setup_grid()

        self.text = Canvas(self.window, width=265, height=20, background='#9F9F9F', highlightthickness=0)
        self.text.pack(padx="85", pady="20", anchor="w")
        self.text.create_text(130, 10, text="REPONSE")
        self.setup_answer()

        self.last_picked_color_pos = None

    def setup_grid(self):
        width = 350
        height = 600
        self.canvas = Canvas(self.window, width=width, height=height, background='#9F9F9F', highlightthickness=0)
        self.canvas.pack(padx="50", pady="0", anchor="w")
        # columns
        for i in range(0, 6):
            self.canvas.create_line(width / 6 * i, 0, width / 6 * i, height, fill="#353434")

        radius = 15
        offset = 20
        # lines
        for i in range(0, 10):
            self.canvas.create_text(30, (height / 10 * i) + 30, text=(i+1))
            self.canvas.create_line(0, height / 10 * i, width, height / 10 * i, fill="#353434")


            xHelper = (width / 6 * 5) + 15
            yHelper = (height / 10 * i) + 15
            # Helper cell
            for k in range(0, 4):
                y = 0
                x = 0
                if k >= 2:
                    y = 20

                if k % 2 == 0:
                    x = 20
                id = "helper_" + str(i) + ";" + str(k)
                self.canvas.create_oval(xHelper + x, yHelper + y, xHelper + 10 + x, yHelper + y + 10, fill="black", outline="", tags=id)

            # row color
            for k in range(1, 5):
                # column : row
                tag = str(k - 1) + ";" + str(i)
                self.canvas.create_oval((width / 6 * k) + offset, (height / 10 * i) + offset, ((width / 6 * k) + radius) + offset, (height / 10 * i) + radius + offset, fill="black", outline="", tags=tag)
                self.canvas.tag_bind(tag, "<Button-1>", self.controller.set_color)

    # draw all color possible
    def setup_color_picker(self):
        width = 350
        height = 45
        self.color_picker = Canvas(self.window, width=width, height=height, background='#353434', highlightthickness=0)
        self.color_picker.pack(padx="55", pady="50", anchor="w")
        i = 0
        for color in self.colors:
            self.color_picker.create_oval(width / 6 * i, 0, (width / 6 * i) + 40, 40, fill=color, outline="", tags=color)
            self.color_picker.tag_bind(color, "<Button-1>", self.select_color)
            i += 1

    # answer + first help
    def setup_answer(self):
        width = 700
        height = 100
        self.answer = Canvas(self.window, width=width, height=height, background='#353434', highlightthickness=0)
        self.answer.pack(padx="120", pady="0", anchor="w")

        radius = 20
        y_offset = 0
        for i in range(0, 4):
            id = "answer_" + str(i)
            self.answer.create_oval(240 / 4 * i, y_offset, (240 / 4 * i) + radius, radius + y_offset, fill="black", outline="", tags=id)
            self.answer.tag_bind(id, "<Button-1>", self.controller.set_answer)

        self.text_help = self.answer.create_text(360, y_offset + radius - 10, text="<< SELECTIONNER 4 COULEURS", font="Times 13 bold")

    # Test button
    def setup_button(self):
        self.button = Button(self.window, text="TESTER", background='#9F9F9F', fg='black', highlightbackground='#353434', font="Times 13 bold",command=self.controller.test)
        self.button.place(anchor="w", y=400, x=500, height=100, width=100)

    # Update the color of helper
    def update_color_helper(self, slot, id, color):
        tag = "helper_" + str(slot) + ";" + str(id)
        item = self.canvas.find_withtag(tag)
        self.canvas.itemconfig(item, fill=color)

    # useful when the player has already used the same pattern
    def reset_colors(self, slot):
        for column in range(0, 4):
            id = str(column) + ";" + str(slot)
            item = self.canvas.find_withtag(id)
            self.canvas.itemconfig(item, fill="black")

    # show the answer to the looser
    def display_answer(self, answer):
        i = 0
        for color in answer:
            tag = "answer_" + str(i)
            item = self.answer.find_withtag(tag)
            self.answer.itemconfig(item, fill=color)
            i += 1

    # grow size and color change
    def update_color(self, event, color):
        item = self.canvas.find_closest(event.x, event.y)
        x0, y0, x1, y1 = self.canvas.coords(item)
        x1 = x0 + 20
        y1 = y0 + 20
        self.canvas.coords(item, x0, y0, x1, y1)
        self.canvas.itemconfig(item, fill=color)

    # just for answer (no need to grow up)
    def update_color_answer(self, event, color):
        item = self.answer.find_closest(event.x, event.y)
        self.answer.itemconfig(item, fill=color)

    # color selection, add white border
    def select_color(self, event):
        if self.last_picked_color_pos is not None:
            last_item = self.color_picker.find_closest(self.last_picked_color_pos.posX, self.last_picked_color_pos.posY)
            self.color_picker.itemconfig(last_item, outline='')

        self.last_picked_color_pos = Pos(event.x, event.y)
        item = self.color_picker.find_closest(event.x, event.y)
        self.controller.model.color_selected = self.color_picker.itemcget(item, "tags").replace("current", "").replace(" ", "")

        self.color_picker.itemconfig(item, outline='white')
        if self.help is not None:
            self.help.destroy()
            self.help = None





