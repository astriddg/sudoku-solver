from cell import Cell, Block

class Sudoku:

    def __init__(self,):
        self._cells = []
        self._cols = []
        self._rows = []
        self._squares = []
        self.makeElms()

    def makeElms(self):
        for i in range(0, 9):
            self._cols.append(Block(i))
            self._rows.append(Block(i))
            self._squares.append(Block(i))



    def stringToCell(self, sudoku_string):
        if len(sudoku_string) != 81:
            raise ValueError("You have not entered the right number of digits.")

        # The column number -- 0-8
        col = 0
        # The position inside the column -- 0-8
        col_i = 0
        # The row number -- 0-8
        row = 0
        # The position inside the row -- 0-8
        row_i = 0
        # The square number  -- 0-8
        square = 0
        # The horizontal position of the square in the sudoku  -- 0-2
        square_i = 0
        # The horizontal position in the square  -- 0-2
        square_j = 0
        # The vertical position in the square  -- 0-2
        square_k = 0
        # That actual position I should have used all along
        square_pos = 0

        for nb in sudoku_string:
            try:
                number = int(nb)
            except:
                raise ValueError("What you entered was not a number.")

            initial = False
            if (number != 0):
                initial = True
            cell = Cell(self._rows[row], self._cols[col], self._squares[square], number, initial)
            self._cells.append(cell)
            self._rows[row][row_i] = cell
            self._cols[col][col_i] = cell
            self._squares[square][square_pos] = cell

            col += 1
            if col > 8:
                col_i += 1
                col = 0

            row_i += 1
            if row_i > 8:
                row += 1
                row_i = 0

            square_j += 1
            square_pos += 1
            if square_j > 2:
                square += 1
                square_i += 1
                square_j = 0
                square_pos -= 3
                if square_i > 2:
                    square_k += 1
                    square_pos += 3
                    if square_k > 2:
                        square_k = 0
                        square_pos = 0
                    else:
                        square -= 3
                    square_i = 0


            square_i += 1
            square_pos += 1
            if square_i > 2:
                square += 1
                square_j += 1
                square_i = 0
                square_pos = 0
                if square_j > 2:
                    square_k += 1
                    if square_k > 2:
                        square_k = 0
                    else:
                        square -= 3
                        square_pos += 3
                    square_i = 0
                else:
                    square_pos -= 3



    def __repr__(self):
        top = "|-----------------------------------------------------| \n"
        bottom = "-------------------------------------------------------"
        cont = ""

        for i in range(0, 9):
            row_string = "|"
            for j in range(0, 9):
                row_string += "  " + str(self._rows[i][j].number)
                if (j + 1) % 3 == 0:
                    row_string += " ||"
                else:
                    row_string += "  ¦"
            row_string += "\n"
            cont += row_string
            if i == 8:
                pass
            elif (i + 1) % 3 == 0:
                cont += "|=====|=====|====||=====|=====|====||=====|=====|=====| \n"
            else:
                cont += "|-----|-----|----||-----|-----|----||-----|-----|-----| \n"

        return top + cont + bottom

    def solve(self):
        i = 0
        j = 0
        back = False
        while i < 81:
            if i < 0:
                raise IndexError("Something went seriously wrong: your code is checking negative cells")
            i = self.isInitial(i, back)
            cell = self._cells[i]
            result = self.addAndCheck(cell)
            if result == True:
                print("[{}] This one's worked out: {} value {}".format(j, i, cell.number))
                back = False
                i += 1
            else:
                cell.number = 0
                back = True
                i -= 1
            j += 1


            # if cell.number != 0:
            #     result = self.checkRow(cell)
            #     if result == False & cell.initial == False:
            #         cell.number = 0

        return

    def isInitial(self, i, back):
        if self._cells[i].initial == True:
            if back:
                i -= 1
            else:
                i += 1
            i = self.isInitial(i, back)
        return i


    def addAndCheck(self, cell):
        if cell.number < 9:
            cell.number += 1
            valid = self.checkGroup(cell)
            if valid == False:
               result = self.addAndCheck(cell)
               return result
            else:
                return True
        else:
            return False

    def checkGroup(self, cell):
        singleInRow = self.checkRow(cell)
        if singleInRow == False:
            return False

        singleInCol = self.checkCol(cell)
        if singleInCol == False:
            return False

        singleInSquare = self.checkSquare(cell)
        if singleInSquare == False:
            return False

        return True


    def checkRow(self, cell):
        for k, nCell in cell.row.items():
            if (nCell.number == cell.number) & (nCell != cell):
                return False
        return True

    def checkCol(self, cell):
        for k, nCell in cell.col.items():
            if (nCell.number == cell.number) & (nCell != cell):
                return False
        return True

    def checkSquare(self, cell):
        for k, nCell in cell.square.items():
            if (nCell.number == cell.number) & (nCell != cell):
                return False
        return True



