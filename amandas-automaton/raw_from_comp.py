import numpy as np
import random

# Board dimensions
rows, cols = 21, 21


def print_board_str(board):
    board_string = ''
    for i in range(0,21):
        for j in range(0,21):
            board_string += str((int(board[i][j])))
            if j==20:
                board_string += '\n'
    print(board_string)

# Function to simulate ball movement
def simulate_movement(board):
    direction = 1  # Initial direction (Right/East)
    x, y = 10, 10  # Starting position (or any valid position on the board)
    rows, cols = 21, 21  # Assuming board is a 2D list
    steps = 0
    while 0 <= x < rows and 0 <= y < cols:
        if board[y][x] != 0:
            # Update the direction of the ball based on the arrow
            direction = board[y][x]
            # Flip the arrow's direction
            if board[y][x] <= 4: 
                board[y][x] = board[y][x] + 4
            else: 
                board[y][x] = board[y][x] - 4
        
        # print(f"at position {x}, {y} moving in {direction}")

        steps += 1
        # Update the position based on the direction
        if direction == 1:
            x += 1
        elif direction == 2:
            x += 1
            y += 1
        elif direction == 3:
            y += 1
        elif direction == 4:
            x -= 1
            y += 1
        elif direction == 5:
            x -= 1
        elif direction == 6:
            x -= 1
            y -= 1
        elif direction == 7:
            y -= 1
        elif direction == 8:
            x += 1
            y -= 1
    return steps


# Simulated annealing
def simulated_annealing():
    # Initial random board
    board = np.random.randint(0, 9, (rows, cols))
    current_score = simulate_movement(board.copy())

    temperature = 1000.0
    cooling_rate = 0.995

    for i in range(1000000):
        if i % 10000 == 0:
            print(i)
        # Select a random square
        x, y = random.randint(0, rows-1), random.randint(0, cols-1)
        new_board = board.copy()
        new_board[y][x] = (board[y][x] + random.randint(1, 7)) % 8
        new_score = simulate_movement(new_board.copy())
        
        # Acceptance probability
        delta_score = new_score - current_score
        if delta_score > 0 or random.random() < np.exp(delta_score / temperature):
            board = new_board.copy()
            current_score = simulate_movement(board.copy())
        
        # Cooling
        temperature *= cooling_rate

    return board, current_score

board, score = simulated_annealing()
print('+====================+')
print(f"Board configuration keeping the ball for {score} steps:")
print(board)
print_board_str(board)
