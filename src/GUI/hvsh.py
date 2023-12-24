
def check_winner(board):
    # Check rows
      for row in board:
        if all(cell[0][-1] == 'R' for cell in row):
            return 'R'
        elif all(cell[0][-1] == 'B' for cell in row):
            return 'B'
      
    # Check columns
      for col in range(len(board[0])):
        if all(board[row][col][0][-1] == 'R' for row in range(len(board))):
            return 'R'
        elif all(board[row][col][0][-1] == 'B' for row in range(len(board))):
            return 'B'

    # Check diagonals
      if all(board[i][i][0][-1] == 'R' for i in range(len(board))):
        return 'R'
      elif all(board[i][i][0][-1] == 'B' for i in range(len(board))):
        return 'B'
      if all(board[i][len(board)-1-i][0][-1] =='R' for i in range(len(board))):
        return 'R'
      elif all(board[i][len(board)-1-i][0][-1] == 'B' for i in range(len(board))):
        return 'B'

      return 'No winner'

# Test the function
board = [
    [[['n'], 0], [['n'], 0], [['n', 'B'], 0, 4], [['n'], 0]],
    [[['n', 'B'], 0, 4], [['n', 'B'], 0, 3], [['n', 'B'], 0, 4], [['n', 'B'], 0, 4]],
    [[['n'], 0], [['n'], 0], [['n'], 0], [['n'], 0]],
    [[['n'], 0], [['n'], 0], [['n'], 0], [['n'], 0]]
]

print(f'V {check_winner(board)}')
