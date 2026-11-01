import time
from .evaluation import evaluate_board

ROWS = 6
COLUMNS = 7

WIN_SCORE = 100000

MOVE_ORDER = [3, 2, 4, 1, 5, 0, 6]

class SearchTimeout(Exception):
  pass

def get_valid_moves(board):
  return [col for col in MOVE_ORDER if board[0][col] == 0]

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

def board_key(board):
  return tuple(cell for row in board for cell in row)

def minmax(board, depth, alpha, beta, maximizing_player, root_player, deadline, table):
  if time.perf_counter() >= deadline:
    raise SearchTimeout()
  
  key = (board_key(board), depth, maximizing_player)
  
  if key in table:
    return table[key]
  
  legal_moves = get_valid_moves(board)
  
  if not legal_moves:
    return 0
  
  if depth == 0:
    return evaluate_board(board, root_player)
  
  if maximizing_player:
    best_score = float('-inf')
    player = root_player 
  else:
    best_score = float('inf')
    player = 3 - root_player
    
  for col in legal_moves:
    row = drop_piece(board, col, player)
    if is_winning_move(board, row, col, player):
      undo_move(board, row, col)
      return (WIN_SCORE + depth) if player == root_player else -(WIN_SCORE + depth)
    
    score = minmax(board, depth - 1, alpha, beta, not maximizing_player, root_player, deadline, table)
    undo_move(board, row, col)
    
    if maximizing_player:
      best_score = max(best_score, score)
      alpha = max(alpha, best_score)
    else:
      best_score = min(best_score, score)
      beta = min(beta, best_score)
    
    if beta <= alpha:
      break
  
  table[key] = best_score
  return best_score

def find_best_move(board, root_player, deadline = 5.0):
  legal_moves = get_valid_moves(board)
  
  if not legal_moves:
    raise ValueError("No legal moves available")
  
  best_move = legal_moves[0]
  
  deadline = time.perf_counter() + deadline
  table = {}
  
  for depth in range(1, 43):
    try:
      depth_best_move = best_move
      depth_best_score = float('-inf')
      
      alpha = float('-inf')
      beta = float('inf')
      
      for column in legal_moves:
        if time.perf_counter() >= deadline:
          raise SearchTimeout()
        
        row = drop_piece(board, column, root_player)
        
        if is_winning_move(board, row, column, root_player):
          score = WIN_SCORE
        
        else:
          score = minmax(board, depth - 1, alpha, beta, False, root_player, deadline, table)
        
        undo_move(board, row, column)
        
        if score > depth_best_score:
          depth_best_score = score
          depth_best_move = column
        
        alpha = max(alpha, depth_best_score)
        if beta <= alpha:
          break
      
      best_move = depth_best_move
    except SearchTimeout:
      break
  return best_move