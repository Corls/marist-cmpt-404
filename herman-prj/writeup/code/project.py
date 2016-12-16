import numpy as np
import random as rand
import math

class Match:
    def __init__(self, matchValue):
        self.cards = []
        self.value = matchValue
        self.complete = False

    def addCard(self, card):
        self.cards.append(card)

    def getMatchedCard(self, card):
        for pos in self.cards:
            if not pos.__is__(card):
                return pos
        return card


class Card:
    def __init__(self, row, column, value):
        self.x = column
        self.y = row
        self.v = value
        self.e = 0.0

    def updateError(self):
        self.e += rand.uniform(0,1)/2
        return self.e

    def updateValue(self, value):
        self.v = value
        self.e = 0

    def __is__(self, card):
        return self.x == card.x and self.y == card.y


class AI:
    def __init__(self, difficulty, cards):
        self.board = cards
        self.known = []
        self.memory = difficulty

    def random(self):
        rand.shuffle(self.board)
        for card in self.board:
            if card.v == 0:
                return card
        return self.board[0]

    def pick(self):
        if len(self.known) > 0:
            return self.known[0].cards[0]
        return self.random()

    def match(self, card):
        for match in self.known:
            if match.value == card.v:
                return match.getMatchedCard(card)
        return self.random()

    def member(self, flipped):
        for card in self.board:
            if not card.__is__(flipped):
                card.updateError()
                if card.e > self.memory:
                    self.forget(card.v)
                    card.updateValue(0)
                elif card.v == flipped.v and not any(match.value == card.v for match in self.known):
                    match = Match(card.v)
                    match.addCard(card)
                    match.addCard(flipped)
                    self.known.append(match)

    def forget(self, value):
        for match in self.known:
            if match.value == value:
                self.known.remove(match)
                break

    def updateBoard(self, flip1, flip2):
        self.forget(flip1.v)
        self.board.remove(flip1)
        self.board.remove(flip2)


class Grid:
    def __init__(self, total):
        cards = list(range(1, total+1))
        cards.extend(range(1, total+1))
        rand.shuffle(cards)
        ncols = min(math.floor(math.sqrt(total*2)), 50)

        board = []
        for i in range(0, total*2, ncols):
            board.append(cards[i:i+ncols])
        self.map = board
        self.state = []
        for row in self.map:
            self.state.append([0] * len(row))

    def valueAt(self, x, y):
        return self.map[y][x]

    def generateBoard(self):
        cards = []
        for row in range(0, len(self.map)):
            for col in range(0, len(self.map[row])):
                cards.append(Card(row, col, 0))
        return cards

    def viewMap(self):
        for row in self.map:
            print(str(row))

    def debugBoard(self, cards):
        for card in cards:
            self.state[card.y][card.x] = card.v
        for row in self.state:
            print(str(row))


def main():
    #grid = Grid([[1, 2, 3, 4, 5], [2, 3, 5, 4, 1]])
    grid = Grid(100)
    print("Game Board")
    grid.viewMap()

    ai = AI(0.5, grid.generateBoard())
    # print("\nAI's View - Initial")
    # grid.debugBoard(ai.board)
    # print("")

    matches = 0
    turn = 1
    while turn < 10000 and len(ai.board) > 1:
        flip1 = ai.pick()
        flip1.updateValue(grid.valueAt(flip1.x, flip1.y))
        ai.member(flip1)

        flip2 = ai.match(flip1)
        flip2.updateValue(grid.valueAt(flip2.x, flip2.y))
        ai.member(flip2)

        # print("AI's View - Move " + str(turn) + ", Found: " + str(flip1.v) + " & " + str(flip2.v))
        # grid.debugBoard(ai.board)

        if flip1.v == flip2.v and not flip1.__is__(flip2):
            ai.updateBoard(flip1, flip2)
            matches += 1
        turn += 1
    print("\nFound All " + str(matches) + " match(es) in " + str(turn) + " turn(s).")


main()