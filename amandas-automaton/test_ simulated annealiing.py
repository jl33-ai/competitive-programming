import numpy as np
import pandas as pd
import random
import json
import time

rows, cols = 21, 21
iterations_list = []
scores_list = []

def print_board_str(board):
    return '\n'.join(''.join(map(str, row)) for row in board)

'''
def heuristic_score(board):
    score = 0   
    for y in range(rows):
        for x in range(cols):
            if x > 10 and board[y][x] in [1, 2, 8]:
                score -= 1
            elif x < 10 and board[y][x] in [5, 6, 4]:
                score -= 1
            if y > 10 and board[y][x] in [1, 8, 7]:
                score -= 1
            elif y < 10 and board[y][x] in [3, 4, 5]:
                score -= 1
    return score
    '''

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

def simulated_annealing():
    # Create a board with random integers between 0 and 8 (inclusive) for the interior
    board = np.random.randint(0, 9, (rows, cols))

    # Top row: arrows pointing down (3)
    board[0, :] = 2
    # Bottom row: arrows pointing up (7)
    board[-1, :] = 6
    # Left column: arrows pointing right (1)
    board[1:-1, 0] = 8
    # Right column: arrows pointing left (5)
    board[1:-1, -1] = 4
    
    current_score = simulate_movement(board.copy()) #+ heuristic_score(board)
    
    temperature = 10000.0           
    itemperature = temperature
    cooling_rate = 0.9999       
    icooling_rate = cooling_rate
    iterations = 1000000

    initial_print = f'''
Running simulated annealing on board size {cols}x{rows}
Starting with seed score of: {current_score}
Parameters:
    Temperature: {temperature}
    Cooling Rate: {cooling_rate}
    Iterations: {iterations}
'''
    
    print(initial_print)

    try: 
        for i in range(iterations):
            if i % (int(iterations/1000)) == 0: 
                print(f"Annealing {round(i/iterations*100, 2)}% complete 🔨")
                print(f"Current score: {current_score}\n")
            # Select a random square    
            x, y = random.randint(0, rows-1), random.randint(0, cols-1)
            new_board = board.copy()
            new_board[y][x] = (board[y][x] + random.randint(1,7)) % 8 
            new_score = simulate_movement(new_board.copy())

            
            # Acceptance probability
            delta_score = new_score - current_score
            if delta_score > 0 or random.random() < np.exp(delta_score / temperature):
                board = new_board.copy()
                current_score = new_score
            
            # Cooling
            temperature *= cooling_rate

            # Data recording 
            iterations_list.append(i)
            scores_list.append(current_score)
            
    except KeyboardInterrupt:
        print("Execution interrupted! Returning the best current board. ⏹️")

    # Generate dataframe and save as csv
    data = {'Iterations' : iterations_list, 'Scores' : scores_list}
    df = pd.DataFrame(data)
    csv_filepath = f"{itemperature}_{icooling_rate}_{iterations}_results.csv"
    df.to_csv(csv_filepath, index=False)

    return board, current_score



start_time = time.time() 

print('+==========================+')
board, score = simulated_annealing()

end_time = time.time()
elapsed_time = end_time - start_time    

print(f"Board configuration keeping the ball for {score} steps:")
print(f"Search took: {round(elapsed_time, 2)} seconds")
print(board)
print(print_board_str(board))
