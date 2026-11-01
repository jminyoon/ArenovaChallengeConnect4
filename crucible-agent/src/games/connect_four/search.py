import time
from .evaluation import evaluate_board

ROWS = 6
COLUMNS = 7

WIN_SCORE = 100000

MOVE_ORDER = [3, 2, 4, 1, 5, 0, 6]

class SearchTimeout(Exception):
  pass

def get_valid_moves(board):
  valid_moves = []
  for col in range(COLUMNS):
    if board[0][col] == 0:
      valid_moves.append(col)
  return valid_moves

def drop_piece(board, col, player):
  for row in range(ROWS - 1, -1, -1):
    if board[row][col] == 0:
      board[row][col] = player
      return row
  return -1

def undo_move(board, row, col):
  board[row][col] = 0
  
def is_winning_move(board, row, col, player):
  directions = [
    (0, 1),  # horizontal
    (1, 0),  # vertical
    (1, 1),  # diagonal
    (1, -1)  # anti-diagonal
  ]
  
  for dr, dc in directions:
    count = 1
    for i in range(1, 4):
      r, c = row + dr * i, col + dc * i
      if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
        count += 1
      else:
        break
    for i in range(1, 4):
      r, c = row - dr * i, col - dc * i
      if 0 <= r < ROWS and 0 <= c < COLUMNS and board[r][c] == player:
        count += 1
      else:
        break
    if count >= 4:
      return True
  return False