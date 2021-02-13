#
# Model.class
#
# @Description:
#
#  The Model contains all data of the game,
#  Also, some useful methods to access data faster
#
#
from Pos import Pos


class Model:

    def __init__(self):
        self.started = False

        # Size of 4 max
        self.answer = [None] * 4
        self.color_selected = None

        self.slots = [[None] * 4 for _ in range(10)]
        self.currentLine = 0
        self.maxLine = 10

    def set_slot(self, slot, color):
        self.slots[self.currentLine][slot] = color

    #   Get colors of the current line
    def get_colors(self):
        return self.slots[self.currentLine]

    def get_colors_line(self, line):
        return self.slots[line]

    def next_line(self):
        self.currentLine += 1

    def has_won(self):
        # Better solution
        currentAnswer = self.slots[self.currentLine]
        return currentAnswer == self.answer
        #for i in currentAnswer:
        #    if currentAnswer[i] != self.answer[i]:
        #        return False
        #return True














