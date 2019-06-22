# This script implements connect four and highlights winning series,
# series with greater than three consecutive Xs or Os.

# The pick_markers module for the start of the game.
def pick_markers():
    ''' 
    Module to assign X or O to the two players. Returns a list with two elements,
    where index 0 is player 1's marker, index 1 is player 2's marker.
    '''
    import string
    plyr1 = input("Player 1, choose X or O as your marker:  ")
    plyr1_mkr = plyr1.lower()
    
    
    while True:
        if plyr1_mkr != 'x' and plyr1_mkr != 'o':
            plyr1 = input('ERROR. Invalid marker. Choose X or O:  ')
            plyr1_mkr = plyr1.lower()
        else:
            if plyr1_mkr == 'o':
                print('Player 2, your marker is X')
                plyr2_mkr = 'X'
            else:
                print('Player 2, you are O''s')
                plyr2_mkr = 'O'
            break
    
    return [plyr1.upper(), plyr2_mkr]

# Code to make clear() clear the command line console. NOTE!!! If on linux, replace 'cls' with 'clear'.
import os
clear = lambda: os.system('cls')
import colorama

# This module constructs the intitial, and print the updated board throughout the game.
def print_board(spaces):
    ''' Uses the the contents of spaces (list variable) to construct/update
    the gameboard on the console. '''
    
    clear() 
    while len(spaces) < 49:
        spaces.append(' ')

    # Start with 7 empty lists... Index 0 corresponds to the TOP ROW of the printed board!!!
    board = [[], [], [], [], [], [], []]
    for x1 in range(0,len(board)):
        single_row = [' '*20,'|  ', spaces[(42-x1*7+0)],'  |  ', spaces[(42-x1*7+1)], '  |  ', spaces[(42-x1*7+2)],'  |  ', spaces[(42-x1*7+3)], '  |  ', spaces[(42-x1*7+4)], '  |  ', spaces[(42-x1*7+5)], '  |  ', spaces[(42-x1*7+6)], '  |']
        board[x1] = single_row

    print('\n'*3)
    print(' '*20+'-'*43)
    # Nested for loops to print off the board. Top row, being at index 0
    # in board (list of lists variable) prints off first.
    for x1 in board:
        board_string = ''
        for x2 in x1:
            board_string = board_string + x2
        print(board_string)
        print(' '*20+'-'*43)
    print(' '*21+'  1  '+'   2  '+'   3  '+'   4  '+'   5  '+'   6  '+'   7  ')
    print('\n'*2)

def board_full(spaces):
    '''Check if board is full by checking if spaces (list variable) contains a char of a single whitespace.
    Returns a boolean of True is no whitespaces are found, else returns False.'''
    for x in spaces:
        if x == ' ':
            return False
        else:
            pass
    return True

def winning_combo(spaces, markers):
    '''Returns False, 'NO_WINNER' if no winning combination is detected. Else, returns (True, winning_coor1, ..., 
    winning_coor4, direction_of_the_winning_combination).'''
    
    # The (list) variable markers is either ['X', 'O'] or ['O','X'] depending on
    # marker choice by player 1 at start of game. The list variable, spaces, contains
    # where markers have been placed.

    def horizontal_win(marker):   
        # Check for horizontal four-in-a-row
        for x2 in [0,7,14,21,28,35,42]:
            for x3 in range(0,4): # Can't be 7
                if marker == spaces[x2+x3]  == spaces[x2+x3+1] == spaces[x2+x3+2] == spaces[x2+x3+3]:
                    return [True, x2+x3, x2+x3+1, x2+x3+2, x2+x3+3]
                    #return True, and the first winning horizontal combo (searches board left to right)
    # Check for vertical three-in-a-row. Iterate up and down (inner x3 for) on a single column (outter x2 for).
        return (False, 0)  
    def vertical_win(marker):
        for x2 in range(0,7):
            # Iterate up a columns checking for four-in-a-row. Run this check on spaces in first four rows (x3) of the
            # to avoid going off the board (an indexing error).
            for x3 in range(0,4):
                if marker == spaces[x2+x3*7] == spaces[x2+x3*7+7] == spaces[x2+x3*7+14] == spaces[x2+x3*7+21]:
                    return [True, x2+x3*7+0, x2+x3*7+7, x2+x3*7+14, x2+x3*7+21]
                    #return True, the first found winning four vertical coordinates (searches bottom to top).
        return (False, 0)
    def ascending_diagonal_win(marker):               
        # Check for an ascending left-right diagonal four-in-a-row. Left-right ascending diagonals are 8 indeces apart.
        # Iterate on first four columns.
        for x2 in range(0,4):
            # Iterate on first four rows
            for x3 in range(0,4):    
                if marker == spaces[x2+x3*7+0] == spaces[x2+x3*7+8] == spaces[x2+x3*7+16] == spaces[x2+x3*7+24]:
                    return [True, x2+x3*7+0, x2+x3*7+8, x2+x3*7+16, x2+x3*7+24]
                    #return True, first found winning diagonal found. Searches 0-3, then moves over 1 column.
        return (False, 0)
    def descending_diagonal_win(marker):
        # Check for a descending left-right diagonal. Left-right descending diagonals are 6 indeces apart.
        # Iterate on first four columns (0-3)
        for x2 in range(0,4):
            # Iterate on highest four rows (3-6)
            for x3 in range(3,7):
                if marker == spaces[x2+x3*7-0] == spaces[x2+x3*7-6] == spaces[x2+x3*7-12] == spaces[x2+x3*7-18]:
                    return [True, x2+x3*7-0, x2+x3*7-6, x2+x3*7-12, x2+x3*7-18]
                    #return True
        return (False, 0)

    # Iterate over both markers (X and O).
    for t in markers:
        hor_win = horizontal_win(t)
        ver_win = vertical_win(t)
        asc_d_win = ascending_diagonal_win(t)
        des_d_win = descending_diagonal_win(t)
        if hor_win[0]==True or ver_win[0]==True or asc_d_win[0]==True or des_d_win[0]==True:
            return [True, t, hor_win, ver_win, asc_d_win, des_d_win]
    return False, 'NO_WINNER'

def extend_winning_combos(list_with_winning_combo_info, spaces):

    winners_marker = list_with_winning_combo_info[1]

    # If a horizontal win occurred, highlight all consecutive markers in that winning series.
    if list_with_winning_combo_info[2][0] == True:
        # Set the off-board limit to the last winning coordinate the horizontal series
        last_winning_coor = list_with_winning_combo_info[2][-1]
        board_limit = last_winning_coor
        initial_last_coor = last_winning_coor
        # Determine the rightmost board position in the row of the winning horizontal combinations
        while board_limit % 7 != 6:
            board_limit += 1

        # While we haven't moved to far right on the board, <= test, and the marker there matches,
        # and this while loop is not executing the first time (inner if test), append the board index
        # contained in last_winning_coor to the winning_combo to the tuple inside of list_with_winning_combo_info
        while last_winning_coor <= board_limit and spaces[last_winning_coor]==winners_marker:
            if initial_last_coor != last_winning_coor:
                list_with_winning_combo_info[2].append(last_winning_coor)
            last_winning_coor += 1
    else:
        pass

    # If a vertical win occurred
    if list_with_winning_combo_info[3][0] == True:
        last_winning_coor = list_with_winning_combo_info[3][-1]
        board_limit = (last_winning_coor % 7) + 42 #Find column number with %7, add 42 to get index of highest board position in that column
        initial_last_coor = last_winning_coor
        while last_winning_coor <= board_limit and spaces[last_winning_coor]==winners_marker:
            if initial_last_coor != last_winning_coor:
                list_with_winning_combo_info[3].append(last_winning_coor)
            last_winning_coor += 7

    # If an ascending diagonal win occurred
    if list_with_winning_combo_info[4][0] == True:
        last_winning_coor = list_with_winning_combo_info[4][-1]
        board_limit = last_winning_coor
        initial_last_coor = last_winning_coor
        # The ascending diagonal board limit is always 7th (index 6) column spot, or row 7 columns 4-7. 
        while (board_limit % 7 != 6 and board_limit < 45):
            board_limit += 8 # Ascending diagonals are 8 indeces apart
        while last_winning_coor <= board_limit and spaces[last_winning_coor]==winners_marker:
            if initial_last_coor != last_winning_coor:
                list_with_winning_combo_info[4].append(last_winning_coor)
            last_winning_coor += 8
    else:
        pass

    # If a descending diagonal win occurred
    if list_with_winning_combo_info[5][0] == True:
        last_winning_coor = list_with_winning_combo_info[5][4]
        board_limit = last_winning_coor
        initial_last_coor = last_winning_coor
        # The descending diagonal board limit calculation
        while (board_limit - 6 > 0) and (board_limit % 7 != 6):
            board_limit -= 6
        while last_winning_coor >= board_limit and spaces[last_winning_coor]==winners_marker:
            if initial_last_coor != last_winning_coor:
                list_with_winning_combo_info[5].append(last_winning_coor)
            last_winning_coor -= 6
    else:
        pass

    return list_with_winning_combo_info

def make_winning_combos_green(list_with_winning_combo_info):
    for x1 in range(2,6):
        if list_with_winning_combo_info[x1][0] == True:
            for x2 in range(1, len(list_with_winning_combo_info[x1])):
                spaces[list_with_winning_combo_info[x1][x2]]='\u001b[1m\u001b[32m'+spaces[list_with_winning_combo_info[x1][x2]]+'\u001b[0m'

def place_move(spaces, markers, turn):
    
    def valid_column(Move):
        while True:
            if  (Move < '1') or ('7' < Move) or (len(Move) > 1):
                Move = input('Error. Invalid move. Try again player {}?  '.format(turn))
            else:
                Move = int(Move)
                return Move  

    def column_full(spaces, move):
        for x2 in range(0,7):
            if spaces[(move-1)+7*x2] == ' ':
                return (False, x2)
        return (True, x2)

    while True:
        move = input('Where would you like to go player {}?  '.format(turn))
        move = valid_column(move)
        move = int(move)
        ColumnFullTuple = column_full(spaces, move)
        if ColumnFullTuple[0] == True:
            print('Column {} is full. I''ll ask you again.'.format(move))
        else:
            spaces[(move-1)+ColumnFullTuple[1]*7] = markers[turn-1]
            break

def ConnectFour():
    Markers = pick_markers()
    global spaces
    spaces = [' ']
    print_board(spaces)
    Winner = winning_combo(spaces, Markers)
    Board_Full = board_full(spaces)
    Turn = 1

    while Winner[0] == False and Board_Full == False:
        place_move(spaces, Markers, Turn)
        print_board(spaces)
        Winner = winning_combo(spaces, Markers)
        Board_Full = board_full(spaces)
    
        if Winner[0] == True:
            # Replaces the first four detected winning coordinates with the ANSI codes to make them green.
            list_with_winning_combos_info = extend_winning_combos(Winner, spaces)
            make_winning_combos_green(list_with_winning_combos_info)
            print_board(spaces)
            print('Congratulations Player {}! YOU WIN!'.format(Turn))
            break
        elif Winner[0] == False and Board_Full == True:
            print('Draw. No winner.')
            break
        else:
            pass
    
        if Turn == 1:
            Turn = 2
        else:
            Turn = 1

# Start the game            
ConnectFour()
while True:
    play_again = input("Would you like to play again? (Y/N):   ")
    play_again = play_again.lower()
    while True:
        if play_again[0] != 'y' and play_again[0] != 'n':
            play_again = input("I don't understand. Try again (Y/N):   ")
            play_again = play_again.lower()
        else:
            break
    if play_again == 'y':
        ConnectFour()
    else:
        print('Goodbye!')
        break