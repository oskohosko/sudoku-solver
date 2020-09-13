"""
Program to solve sudoku.

In this piece of code, I represent the sudoku board as a list of its rows.
Each empty space is represented by a '0', otherwise everything else is normal.

I solve the sudoku by inputting a coordinate, checking possible values for its
corresponding row, column and 3x3 square, and using the intersection of sets
I'm able to find values for that given coordinate. If there is only one value,
then it can be placed in that coordinate, otherwise we pass on that one temporarily.
We continue this for all values that are 0 and are left with a finished sudoku!
"""

__author__ = 'Oskar Hosken'

# sudoku board
board = [[0,0,0,0,0,0,0,0,0],
         [0,3,0,0,0,0,1,6,0],
         [0,6,7,0,3,5,0,0,4],
         [6,0,8,1,2,0,9,0,0],
         [0,9,0,0,8,0,0,3,0],
         [0,0,2,0,7,9,8,0,6],
         [8,0,0,6,9,0,3,5,0],
         [0,2,6,0,0,0,0,9,0],
         [0,0,0,0,0,0,0,0,0]]

# set of 1-9 for comparison
full_set = set(range(1,10))

# Gets the 3x3 square the coordinate is in
def get_square(i: int, j: int) -> list:
    """Gets the coordinates of each value in the same
       3 x 3 square that (i, j) is in.

    Args:
        i (int): Index corresponding to the row
        j (int): Index corresponding to the column

    Returns:
        list: A list of 9 coordinates of the 3x3 square that (i,j) is in.
    """
    indexes = []
    for y in range(int(j/3)*3,(int(j/3)+1)*3):
        for x in range(int(i/3)*3,(int(i/3)+1)*3):
            indexes.append((x,y))
    return indexes

# Function to check a row for possible values
def check_row(i: int, j: int) -> set:
    """Computes all values missing from row i.

    Args:
        i (int): Index corresponding to the row
        j (int): Index corresponding to the column

    Returns:
        set: A set containing the missing values from 1 to 9
             that aren't in the row.
    Example:
        >>> check_row(1,3)
        >>> {2,4,5,7,8,9}       # missing 1,3,6 since they were in the row.
    """
    row = []
    for x in range(9):
        row.append(board[i][x])
    return full_set - set(row)

# Function to check a column for possible values
def check_column(i: int, j: int) -> set:
    """Computes all values missing from column j.

    Args:
        i (int): Index corresponding to the row
        j (int): Index corresponding to the column

    Returns:
        set: A set containing values that aren't in the column.
    Example:
        >>> check_column(1,3)
        >>> {2,3,4,5,7,8,9}      # missing 1,6 since they were in the column.
    """
    col = []
    for y in range(9):
        col.append(board[y][j])
    return full_set - set(col)

# Function to check squares
def check_square(i: int, j: int) -> set:
    """Computes all values missing from the 3x3 square that (i, j) is in.

    Args:
        i (int): Index corresponding to the row
        j (int): Index corresponding to the column

    Returns:
        set: A set containing all values that aren't in the square.
    """
    square_y, square_x = int(i/3), int(j/3)
    square = []
    for y in range(square_x*3,(square_x+1)*3):
        for x in range(square_y*3,(square_y+1)*3):
            square.append(board[x][y])
    return full_set - set(square)

# Function to check for all possible values of a coordinate
def get_vals(i: int, j: int) -> set:
    """Computes all possible values that the coordinate (i, j) could be.

    Args:
        i (int): Index corresponding to the row
        j (int): Index corresponding to the column

    Returns:
        set: A set containing values that (i, j) could be.
    """
    row = check_row(i, j)
    col = check_column(i, j)
    square = check_square(i, j)

    return row.intersection(col,square)

def get_all_vals(i: int, j: int) -> list:
    """Determines whether (i,j) can have a certain value and if so,
       places the value there, otherwise it passes.

    Args:
        i (int): Index corresponding to the row
        j (int): Index corresponding to the column

    Returns:
        list: The sudoku board updated if there was a value that could be placed,
              otherwise a non-updated board.
    """
    # getting all possible values for every other box in the 3x3 square
    table = []
    for pair in get_square(i, j):
        if board[pair[0]][pair[1]] == 0:
            if (pair[0],pair[1]) != (i,j):
                table.append(get_vals(pair[0],pair[1]))

    # puts all possible numbers of other boxes into a list
    all_other_vals = []
    for sett in table:
        for item in sett:
            if item not in all_other_vals:
                all_other_vals.append(item)

    # if a number in (i,j)'s values isn't in any of the others then it can be placed!
    nums_to_place = list(get_vals(i,j) - set(all_other_vals))

    if len(nums_to_place) == 1:         # checking if only one item can be placed
        board[i][j] = nums_to_place[0]
    else:                               # otherwise we pass and try the next coordinate
        pass
    return board

# Main loop of the program.
filled = False
while not filled:
    current_values = []                 # gets all current numbers on the board
    for x in range(9):
        for y in range(9):
            current_values.append(board[x][y])
    if 0 in current_values:             # if there is still an empty space, keep looping
        for i in range(9):
            for j in range(9):
                get_all_vals(i, j)
    else:                               # if not, the board has been filled and we are done!
        filled = True

# printing the board row by row so it's easier to see.
for row in board:
    print(row)


