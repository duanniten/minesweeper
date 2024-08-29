import random

from typing import List

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count
    
    def __hash__(self):
        return hash((frozenset(self.cells), self.count))

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        
        if len(self.cells) == self.count and len(self.cells)> 0 :
            return self.cells
        return set()
    
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()
    
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
        
            self.cells.remove(cell)

        
            


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge : List[Sentence] = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        "1)"
        self.moves_made.add(cell)

        "2)"
        self.mark_safe(cell)

        "3)"
        self.addNewStement(cell, count)

        "4)"
        self.update_knowledge()

        "5)"
        self.checkNewStement()
        self.update_knowledge()
        

            
    def checkNewStement(self):
        new_statements = []
        
        for i, sentence in enumerate(self.knowledge):
            for j, sentenceC in enumerate(self.knowledge):
                if i != j and sentence.cells.issubset(sentenceC.cells):
                    difSentenceCells = sentenceC.cells - sentence.cells
                    difSentenceCount = sentenceC.count - sentence.count
                    new_sentence = Sentence(
                          cells= difSentenceCells,
                          count= difSentenceCount  
                        )
                    
                    
                    if difSentenceCount >= 0:
                        new_sentence = Sentence(
                          cells=difSentenceCells,
                          count=difSentenceCount  
                        )
                    
                    if (new_sentence not in new_statements and
                        new_sentence not in self.knowledge):
                        new_statements.append(new_sentence)
                        
                    
        self.knowledge.extend(new_statements)
       
    def update_knowledge(self):
        change = True
        while change:
            safes = set()
            mines = set()
            change = False
            for sentence in self.knowledge:
                safes = safes.union(sentence.known_safes())
                mines = mines.union(sentence.known_mines())

            newSafes = safes - self.safes
        if newSafes:
            change = True
            for safe in newSafes:
                self.mark_safe(safe)
        
        # Marcar novas minas
        newMines = mines - self.mines
        if newMines:
            change = True
            for mine in newMines:
                self.mark_mine(mine)
        self.knowledge = [sentence for sentence in self.knowledge if len(sentence.cells) > 0]
    
    def addNewStement(self, cell, count):
        "new sentence to the AI's knowledge base on the value of `cell` and `count`"
        i, j = cell
        cellsNewStement = set()
        for di in range(-1,2):
            for dj in range(-1,2):
                #to dont add the current cells
                if di == 0 and dj == 0:
                    continue

                #to dont add already know as safe
                if (i + di,j + dj) in self.safes:
                    continue

                #to dont add already know as mine, and reduce de count -1
                if (i + di,j + dj) in self.mines:
                    count-=1
                    continue

                #check if current cell in grid
                if(
                    (i+di) >= 0 and (i+di) < self.width and
                    (j+dj) >= 0 and (j+dj) < self.height
                   ):  
                    dcell = (i+di,j+dj)
                    cellsNewStement.add(dcell)
        
        sentence0 = Sentence(
                cellsNewStement,
                count)
        self.knowledge.append(sentence0)

              

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        move = self.safes - self.moves_made -self.mines
        if len(move) > 0:
            move = next(iter(move))
 
            return move

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        allcells = set()
        for i in range(0,self.width):
            for j in range(0,self.height):
                allcells.add((i,j))
        move = (allcells - self.mines) - self.moves_made
        
        if len(move) > 0:
            move = next(iter(move))
            return move

        return None
