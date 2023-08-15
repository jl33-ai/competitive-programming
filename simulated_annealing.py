import numpy as np
import random

rows, cols = 21, 21

def print_board_str(board):
    return '\n'.join(''.join(map(str, row)) for row in board)

def simulate_movement(board):
    directions = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    direction = 0
    x, y = 10, 10
    steps = 0
    while 0 <= x < cols and 0 <= y < rows:
        if board[y][x] != 0:
            direction = board[y][x] - 1
            board[y][x] = (direction + 4) % 8 + 1
        dx, dy = directions[direction]
        x += dx
        y += dy
        steps += 1
    return steps

def simulated_annealing():
    board = np.random.randint(0, 9, (rows, cols))
    current_score = simulate_movement(board.copy())

    temperature = 1000.0
    cooling_rate = 0.995
    iterations = 100

    initial_print = f'''
Running simulated annealing on board size {cols}x{rows}
Starting with seed score of: {current_score}
Parameters:
    Temperature: {temperature}
    Cooling Rate: {cooling_rate}
    Iterations: {iterations}
'''
    print(initial_print)

    for i in range(iterations):
        if i % 10000 == 0:
            print(f"Step: {i}\nCurrent Score: {current_score}")

        x, y = random.randint(0, cols-1), random.randint(0, rows-1)
        board[y][x] = (board[y][x] + random.randint(1, 7)) % 8
        new_score = simulate_movement(board.copy())

        delta_score = new_score - current_score

        if delta_score > 0 or random.random() < np.exp(delta_score / temperature):
            current_score = new_score

        temperature *= cooling_rate

    return board, current_score

print('+==========================+')
board, score = simulated_annealing()
print(f"Board configuration keeping the ball for {score} steps:")
print(board)
print(print_board_str(board))
