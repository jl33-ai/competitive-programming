rows, cols = 21, 21

import random

fitness_cache = {}

def simulate_movement(board):
    if board in fitness_cache:
        return fitness_cache[board]

    direction = 1  # Initial direction (Right/East)
    x, y = 10, 10  # Starting position (or any valid position on the board)
    rows, cols = 21, 21  # Assuming board is a 2D list
    steps = 0
    while 0 <= x < rows and 0 <= y < cols:
        cell_arrow = int(board[20*(x) + y])
        if cell_arrow:
            # Update the direction of the ball based on the arrow
            direction = cell_arrow
            # Flip the arrow's direction using the modulus operator
            board[20*(x) + y] = (cell_arrow + 3) % 8 + 1
        
        # print(f"at position {x}, {y} moving in {direction}")
        #97
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
    fitness_cache[board] = steps
    return steps


board = [[str(random.randint(0, 8)) for _ in range(21)] for _ in range(21)]
board_string = "\n".join(" ".join(row) for row in board)
print(simulate_movement(board_string))