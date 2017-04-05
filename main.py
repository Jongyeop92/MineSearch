# -*- coding: utf8 -*-

EMPTY = 0
MINE  = "M"
COVER = "C"


import random


class MineBoard():

    def __init__(self, width, height, mineCount=10):
        self.width = width
        self.height = height
        self.mineCount = mineCount

        self.board = self.makeBoard(width, height)
        self.cover = self.makeBoard(width, height, True)
        self.coverCount = width * height
        self.settingBoard()

    def makeBoard(self, width, height, initValue=EMPTY):
        board = []

        for i in range(height):
            board.append([initValue] * width)

        return board

    def showBoard(self, isAll=False):
        if isAll:
            print "\n".join(" ".join(str(c) for c in row) for row in self.board)
        else:
            for y in range(self.height):
                row = ""
                for x in range(self.width):
                    if self.cover[y][x]:
                        row += COVER
                    else:
                        row += str(self.board[y][x])

                print " ".join(row)

    def settingBoard(self):
        count = 0

        while count < self.mineCount:
            y = random.randint(0, self.height - 1)
            x = random.randint(0, self.width - 1)

            if self.board[y][x] == EMPTY:
                self.board[y][x] = MINE
                count += 1

        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == MINE:
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if (dy == 0 and dx == 0) or not self.isInBoard(y + dy, x + dx) or self.board[y + dy][x + dx] == MINE:
                                continue
                            else:
                                self.board[y + dy][x + dx] += 1

    def isInBoard(self, y, x):
        return 0 <= y and y < self.height and 0 <= x and x < self.width

    def openCover(self, y, x, firstCall=True):
        if not self.isInBoard(y, x) or self.cover[y][x] == False:
            return None

        recursiveCall = False

        self.coverCount -= 1
        
        if firstCall:
            self.cover[y][x] = False

            if self.board[y][x] == MINE:
                return MINE
            elif self.board[y][x] == EMPTY:
                recursiveCall = True
        else:
            if self.board[y][x] != MINE:
                self.cover[y][x] = False

                if self.board[y][x] == EMPTY:
                    recursiveCall = True
            else:
                self.coverCount += 1

        if recursiveCall:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    self.openCover(y + dy, x + dx, False)

    def isWin(self):
        return self.coverCount == self.mineCount


def test():

    mineBoard = MineBoard(10, 10, 5)

    mineCount = 0
    for y in range(mineBoard.height):
        for x in range(mineBoard.width):
            if mineBoard.board[y][x] == MINE:
                mineCount += 1

    assert mineCount == mineBoard.mineCount


    mineBoard.showBoard()
    print
    mineBoard.showBoard(True)
    print

    mineBoard.openCover(0, 0)
    mineBoard.showBoard()
    print

    coverCount = 0
    for y in range(mineBoard.height):
        for x in range(mineBoard.width):
            if mineBoard.cover[y][x] == True:
                coverCount += 1

    assert coverCount == mineBoard.coverCount

    assert mineBoard.isWin() == False


    print "success"


def main():
    
    mineBoard = MineBoard(10, 10)

    mineBoard.showBoard()
    print

    while True:
        
        y, x = map(int, raw_input("Input y, x: ").split())

        result = mineBoard.openCover(y, x)

        print
        mineBoard.showBoard()
        print

        if result == MINE:
            print "Game Over!"
            break
        elif mineBoard.isWin():
            mineBoard.showBoard(True)
            print
            print "You win!"
            break


if __name__ == "__main__":
    #test()
    main()
