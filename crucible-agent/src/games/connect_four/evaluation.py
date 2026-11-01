ROWS = 6
COLUMNS = 7

WINDOWS = []

#Horizontal windows
for row in range(ROWS):
    for col in range(COLUMNS - 3):
        WINDOWS.append([(row, col + i) for i in range(4)])
        
#Vertical windows
for col in range(COLUMNS):
    for row in range(ROWS - 3):
        WINDOWS.append([(row + i, col) for i in range(4)])
        
#Diagonal windows (top-left to bottom-right)
for row in range(ROWS - 3):
    for col in range(COLUMNS - 3):
        WINDOWS.append([(row + i, col + i) for i in range(4)])

#Diagonal windows (bottom-left to top-right)
for row in range(3, ROWS):
    for col in range(COLUMNS - 3):
        WINDOWS.append([(row - i, col + i) for i in range(4)])
        
def evaluate_window(window, player):
  opponent = 3 - player
  
  own_count = window.count(player)
  opponent_count = window.count(opponent)
  empty_count = window.count(0)
  
  if own_count == 4:
    return 100000
  
  if opponent_count == 4:
    return -100000
  
  if own_count == 3 and empty_count == 1:
    return 100

  if opponent_count == 3 and empty_count == 1:
    return -120
  
  if own_count == 2 and empty_count == 2:
    return 10

  if opponent_count == 2 and empty_count == 2:
    return -10
  
  return 0

def evaluate_board(board, player):
  score = 0
  
  for window in WINDOWS:
    window_values = [board[row][col] for row, col in window]
    score += evaluate_window(window_values, player)
  
  return score
  