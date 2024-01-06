import random


class Minesweeper:
    """
    Represents a Minesweeper game.

    Attributes:
        height (int): The height of the game board.
        width (int): The width of the game board.
        mines (set of tuples): A set containing the coordinates (i, j) of all mines.
        board (list of lists): A 2D list representing the game board where each element is a boolean indicating whether a mine is present.
        mines_found (set of tuples): A set containing the coordinates of mines that have been found.
    """

    def __init__(self, height=8, width=8, mines=8):
        """
        Initializes a new game of Minesweeper.

        Args:
            height (int): The height of the game board (default is 8).
            width (int): The width of the game board (default is 8).
            mines (int): The number of mines on the board (default is 8).
        """
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
        Prints a text representation of the game board to the console.
        Mines are represented by 'X', and empty spaces by ' '.
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
        """
        Checks if a given cell contains a mine.

        Args:
            cell (tuple): A tuple (i, j) representing the cell coordinates.

        Returns:
            bool: True if the cell contains a mine, False otherwise.
        """
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Counts the number of mines adjacent to a given cell.

        Args:
            cell (tuple): A tuple (i, j) representing the cell coordinates.

        Returns:
            int: The number of mines surrounding the given cell.
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
        Checks if the player has won the game by finding all mines.

        Returns:
            bool: True if all mines have been found, False otherwise.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Represents a logical statement about the Minesweeper game.
    A statement consists of a set of cells and the count of mines in these cells.

    Attributes:
        cells (set of tuples): A set of tuples representing the coordinates of cells.
        count (int): The number of mines in these cells.
    """

    def __init__(self, cells, count):
        """
        Initializes a new logical sentence.

        Args:
            cells (set of tuples): A set of coordinates (i, j) representing cells.
            count (int): The number of mines in these cells.
        """
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        """
        Checks equality between two Sentence instances.

        This method is used to compare two Sentence objects. Two sentences are considered equal
        if they have the same cells and the same count of mines.

        Args:
            other (Sentence): Another Sentence object to compare with.

        Returns:
            bool: True if both sentences have the same cells and mine count, False otherwise.
        """
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        """
        Provides a string representation of the Sentence.

        This method returns a string that shows the cells in the sentence and the count of mines in these cells,
        making it easier to understand the state of the sentence at a glance.

        Returns:
            str: A string representation of the Sentence.
        """
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Identifies cells in the sentence known to be mines.

        This method returns a set of all cells in this sentence that are definitely mines.
        This can be inferred when the number of cells equals the count of mines.

        Returns:
            set: A set of tuples representing the coordinates of known mine cells.
        """
        if len(self.cells) == self.count:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Identifies cells in the sentence known to be safe.

        This method returns a set of all cells in this sentence that are definitely safe.
        This can be inferred when the count of mines in the sentence is zero.

        Returns:
            set: A set of tuples representing the coordinates of known safe cells.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates the sentence when a cell is known to be a mine.

        When a cell in the sentence is identified as a mine, this method removes it from the sentence
        and decreases the count of mines accordingly.

        Args:
            cell (tuple): A tuple (i, j) representing the coordinates of the mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates the sentence when a cell is known to be safe.

        When a cell in the sentence is identified as safe, this method removes it from the sentence.
        The count of mines remains unchanged.

        Args:
            cell (tuple): A tuple (i, j) representing the coordinates of the safe cell.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Represents an AI player for the Minesweeper game.

    Attributes:
        height (int): The height of the game board.
        width (int): The width of the game board.
        moves_made (set of tuples): A set of tuples representing the coordinates of moves made.
        mines (set of tuples): A set containing the coordinates of discovered mines.
        safes (set of tuples): A set containing the coordinates of discovered safe cells.
        knowledge (list of Sentences): A list of Sentences representing the AI's knowledge about the game.
    """

    def __init__(self, height=8, width=8):
        """
        Initializes a new AI player for Minesweeper.

        Args:
            height (int): The height of the game board (default is 8).
            width (int): The width of the game board (default is 8).
        """
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine in the AI's knowledge base.

        Updates the AI's knowledge to reflect that a specific cell is a mine, and adjusts
        all sentences in the knowledge base accordingly.

        Args:
            cell (tuple): A tuple (i, j) representing the coordinates of the cell identified as a mine.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe in the AI's knowledge base.

        Updates the AI's knowledge to reflect that a specific cell is safe, and adjusts
        all sentences in the knowledge base accordingly.

        Args:
            cell (tuple): A tuple (i, j) representing the coordinates of the cell identified as safe.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Updates the AI's knowledge base when a cell is revealed.

        This method is called with a newly revealed cell and the number of mines surrounding it.
        It updates the AI's knowledge base with this new information and revises existing knowledge accordingly.

        Args:
            cell (tuple): The coordinates (i, j) of the cell that was revealed.
            count (int): The number of mines surrounding the revealed cell.
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Gather all neighboring cells
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) != cell and 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))

        # Remove known mines and adjust count
        known_mines = set()
        for neighbor in neighbors:
            if neighbor in self.mines:
                known_mines.add(neighbor)
                count -= 1

        neighbors -= known_mines

        # Remove known safes
        neighbors -= self.safes

        # Add the new sentence
        self.knowledge.append(Sentence(neighbors, count))

        # Update the knowledge base
        self.update_knowledge()

    def update_knowledge(self):
        """
        Iteratively updates the knowledge base of the AI.

        This method goes through the knowledge base to identify and mark new mines and safes.
        It also refines the existing sentences based on the new information and removes redundant sentences.
        """
        updated = True
        while updated:
            updated = False
            new_safes = set()
            new_mines = set()

            # Identify new safes and mines
            for sentence in self.knowledge:
                new_safes |= sentence.known_safes()
                new_mines |= sentence.known_mines()

            if new_safes or new_mines:
                updated = True

            # Update sentences with new information
            for safe in new_safes:
                self.mark_safe(safe)
            for mine in new_mines:
                self.mark_mine(mine)

            # Remove empty sentences and update subset logic
            new_knowledge = []
            for sentence in self.knowledge:
                if len(sentence.cells) > 0:
                    new_knowledge.append(sentence)
                    for other in self.knowledge:
                        if sentence != other and sentence.cells.issubset(other.cells):
                            other.cells -= sentence.cells
                            other.count -= sentence.count
                            updated = True

            self.knowledge = new_knowledge

    def make_safe_move(self):
        """
        Determines a safe move for the AI to make.

        Returns a cell that is known to be safe and has not been already chosen. This method
        does not modify the game state but only provides a recommendation based on current knowledge.

        Returns:
            tuple or None: The coordinates (i, j) of a safe cell to move to, or None if no safe moves are available.
        """
        for move in self.safes:
            if move not in self.moves_made:
                return move
        return None

    def make_random_move(self):
        """
        Chooses a random move from the available options.

        This method is used when the AI does not have sufficient knowledge to determine a safe move.
        It randomly selects a cell that has not been chosen yet and is not known to be a mine.

        Returns:
            tuple or None: The coordinates (i, j) of the cell chosen, or None if no moves are possible.
        """
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    return (i, j)
        return None
