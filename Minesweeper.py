# Minesweeper
import random  # Purely for assigning random mines only


class Square(object):  # Object that will hold the information about a tile

    def __init__(self, xCoord, yCoord):

        self.__x = xCoord
        self.__y = yCoord

        self.__status = None  # Toggle this to Mine, Flagged ETC
        self.__value = 0  # The value assigned to the square (equivalent to the number of mines near)
        self.__children = []  # This will contain the squares surrounding it

    def __str__(self):  # String output, useful for displaying coords
        output = f"{self.__x},{self.__y}"
        return output

    def setMine(self): # Sets a square to the mine status
        self.__status = "Mine"

    def flagSquare(self): # Sets a square to the flag status
        self.__status = "Flag"

    def add_child(self, child): # Adds a Square object reference to this squares '.__children' attribute
        self.__children.append(child)

    def addOne(self): # Adds one to the value of the value attribute
        self.__value += 1

    def addValue(self): # Adds 1 to the value of its children squares

        if self.__status == "Mine":
            
            for child in self.__children:
                child.addOne()

    def fetchCode(self):  # For visual representation

        if self.__status is None:
            return str(self.__value)  # Returns the value in that square if it is not a mine or flag

        else:
            return str(self.__status[0])  # If it is a mine or a flag then the first letter is returned

    def isMine(self):   # Returns true if the square is a mine

        if self.__status == "Mine":
            return True

        else:
            return False

    def returnFieldSquares(self, visitedSquares):  # Depth traversal to locate all of the field squares

        for child in self.__children:

            if child.fetchCode() == "0" and child not in visitedSquares:
                visitedSquares.append(child)

                #  Adding new squares to the list (prevents duplication of already existing squares)
                for newSquare in child.returnFieldSquares(visitedSquares):

                    if newSquare not in visitedSquares:
                        visitedSquares.append(newSquare)

        return visitedSquares


class Grid(object):  # This object will contain the basic functions of minesweeper

    def __init__(self, width, height, mines):
        def setSquareChildren():

            for square in self.__grid:  # For each square in the grid
                nSquares = []  # Neighbouring squares to the current one

                x, y = int(square[0]), int(square[2])  # Sets up the coordinates of that square

                if x - 1 >= 0:  # Left side of the square
                    nSquares.append(f"{x-1},{y}")

                    if y -1 >= 0:  # Above
                        nSquares.append(f"{x-1},{y -1}")
                                            
                    # Below
                    if y + 1 < self.__dimensions[1]:
                        nSquares.append(f"{x-1},{y+1}")

                if x + 1 < self.__dimensions[0]: # Right Side of the Square
                    nSquares.append(f"{x + 1},{y}")
                    
                    # Above
                    if y - 1 >= 0:
                        nSquares.append(f"{x + 1},{y -1}")

                    # Below
                    if y + 1 < self.__dimensions[1]:
                        nSquares.append(f"{x + 1},{y + 1}")

                if y + 1 < self.__dimensions[1]: # Below the current square
                    nSquares.append(f"{x},{y + 1}")

                if y -1 >= 0: # Above the current square
                    nSquares.append(f"{x},{y - 1}")

                for nSquare in nSquares:  # For each square that neighbours this square
                    self.__grid[square].add_child(self.__grid[nSquare])  # Adds a reference to the neigbouring square to the currently selected square
                
        def setMines(mines):  # Function that will set a random entry to mine status

            currentMines = 0  # The entries in the grid that are currently of the status "mine"
            while currentMines != mines:
                currentIndex = str(random.randint(0,self.__dimensions[0] - 1)) + "," + str(random.randint(0,self.__dimensions[1] - 1))
                """ The above sets a random index for a mine to be """

                if self.__grid[currentIndex].isMine() is False:
                    self.__grid[currentIndex].setMine()
                    currentMines += 1

        def setValues():  # A function that is responsible for correcting the values of the squares on instantiation

            for square in self.__grid:

                if self.__grid[square].isMine():
                    self.__grid[square].addValue()

        self.__grid = {}  # Dictionary that stores the grid
        self.__visible = {}  # This will be a copy of the grid which will interface with the user
        self.__blankTile = "/"
        self.__mineAmount = mines # The amount of mines that will be present in the board
        """The grid system will work like the pygame system. So X goes from left to right positive 
        | X--> is +, X <-- is -| and Y goes from up to down positive."""
        self.__dimensions = [width, height]  # Still in the form X,Y
        # Grid Setup

        for x in range(width):  # For each possible X Coordinate

            for y in range(height):  # For each possible Y Coordinate

                coord = f"{x},{y}"  # Coordinates of this new square

                self.__grid[coord] = Square(x, y)  # Sets the dictionary key at [coord] to the new Square object
                self.__visible[coord] = self.__blankTile  # Empty square for the user to interact with

        setSquareChildren()  # Sets the children
        setMines(mines)  # Sets the mines
        setValues()  # Sets the values of the squares

    def getDimensions(self):
        return self.__dimensions

    def __str__(self):
        output = ""
        currentY = 0
        while currentY != self.__dimensions[1]:  # While the height limit hasn't been reached
            
            for square in self.__visible:  # Iterates through each square in the grid
                if int(square[2]) == currentY:
                    output = output + self.__visible[square] + ","

            output += "\n"
            currentY += 1

        return output

    def checkWin(self):  # Checks to see if the player has beaten the game

        remainingSquares = 0

        for square in self.__visible:

            if self.__visible[square] is self.__blankTile:
                remainingSquares += 1

        if remainingSquares == self.__mineAmount:
            print("Congratulations, You have won!")

            return False

        return True

    def displayLogicalBoard(self):
        
        output = ""
        currentY = 0
        while currentY != self.__dimensions[1]:  # While the height limit hasn't been reached

            for square in self.__grid:  # Iterates through each square in the grid
                if int(square[2]) == currentY:
                    output = output + self.__grid[square].fetchCode() + ","

            output += "\n"
            currentY += 1

        return output

    def recieveInput(self, inCoords):

        # Guard Clause to prevent the program from checking a square twice
        if self.__visible[inCoords] is not self.__blankTile:
            print("Tile has already been checked!")
            return True

        elif self.__grid[inCoords].isMine():  # If the user hits a mine, the game ends
            self.__visible[inCoords] = self.__grid[inCoords].fetchCode()
            # Display's the player's death message
            print("""-----------------------------------------------------

            You Hit a Mine. You Have Died!
-----------------------------------------------------
                     """)
            return False

        else:
            tackledSquare = self.__grid[inCoords].fetchCode()
            self.__visible[inCoords] = tackledSquare

            if tackledSquare == "0":
                # Now using the children relationship, remove show all of the squares that have the value of 0
                squareList = self.__grid[inCoords].returnFieldSquares([]) # List of field square objects
                for square in squareList:
                    for item in self.__grid.items():

                        if item[1] is square:
                            self.__visible[item[0]] = self.__grid[item[0]].fetchCode()
                            # Sets the visible board entry to be the same as the hidden board

            if self.checkWin():
                return True

            return True


grid = Grid(5, 10, 1)  # A grid with the width of 5, height of 10 and with 9 mines


gameplayLoop = True

while gameplayLoop:  # A bunch of validation to make sure the inputs are legal
    print(grid)
    usersCoords = ""

    try:
        userIn = int(input("Please enter the x coordinate of the desired square"))

        if grid.getDimensions()[0] >= userIn > 0:
            usersCoords += str(userIn - 1) + ","

            userIn = int(input("Please enter the y coordinate of the desired square"))

            if grid.getDimensions()[1] >= userIn > 0:
                usersCoords += str(userIn - 1)

                # Game Logic here
                gameplayLoop = grid.recieveInput(usersCoords)
                gameplayLoop = grid.checkWin()

            else:
                print("Coordinate is out of bounds")
        else:
            print("Coordinate is out of bounds")
    except ValueError as error:  # For debugging
        print(f"Invalid Input, please enter an integer value \n{error} : Please try a different Input")

print("Final Board State")
print(grid)

        

        

            

        
                

                
            

        
