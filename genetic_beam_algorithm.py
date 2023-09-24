import numpy as np
import random
import pandas as pd

# Unadapted 
# encode everything as string, for the dictionary. *i
# board[20*(x) + y]

# Constants
rows, cols = 21, 21

population_size = 100
beam_width = 10
generations = 1000
mutation_rate = 0.05

# HELPER FUNCTIONS

# Prints board in indented string format
# Depracated
def print_board_str(board):
    return '\n'.join(''.join(map(str, row)) for row in board)

# Function to simulate ball movement (objective function)
# Returns the number of steps a ball stays on a given board 

fitness_cache = {}  # key: board_string, value: fitness_score

def simulate_movement(board):
    if board in fitness_cache:
        return fitness_cache[board]

    direction = 1  # Initial direction (Right/East)
    x, y = 10, 10  # Starting position (or any valid position on the board)
    rows, cols = 21, 21  # Assuming board is a 2D list
    steps = 0
    while 0 <= x < rows and 0 <= y < cols:
        cell_arrow = board[20*(x) + y]
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

# Crossover function
def crossover(parent1, parent2):
    row = random.randint(0, rows - 1)
    child1 = np.vstack((parent1[:row], parent2[row:]))
    child2 = np.vstack((parent2[:row], parent1[row:]))
    return child1, child2

# Mutation function
def mutate(board):
    for i in range(rows):
        for j in range(cols):
            if random.random() < mutation_rate:
                board[i][j] = random.randint(0, 8)
    return board

# Genetic beam search function
def genetic_beam_search(iters, beam_width):
    # Initialize population
    population = [np.random.randint(0, 9, (rows, cols)) for _ in range(population_size)]

    # For data recording
    iterations_list = []
    scores_list = []

    try:
        for generation in range(iters):
            print('done')
            # Evaluate fitness
            fitness = [simulate_movement(board) for board in population]
            
            # Select best individuals (beam)
            best_indices = np.argsort(fitness)[-beam_width:]
            beam = [population[i] for i in best_indices]
            
            # Crossover and mutation
            children = []
            for i in range(0, len(beam), 2):
                child1, child2 = crossover(beam[i], beam[i + 1])
                children.append(mutate(child1))
                children.append(mutate(child2))

            # Replacement
            population = beam + children

            # Data recording
            iterations_list.append(generation)
            scores_list.append(max(fitness))

    except KeyboardInterrupt:
        print("Execution interrupted!")

    # Generate dataframe and save as csv
    data = {'Iterations': iterations_list, 'Scores': scores_list}
    df = pd.DataFrame(data)
    # Uncomment below to save as CSV
    # df.to_csv("beam_search_results.csv", index=False)

    best_board = population[np.argmax([simulate_movement(board) for board in population])]
    return best_board

# Run the algorithm
iters = 10000  # Number of generations
beam_width = 10  # Width of the beam
best_board = genetic_beam_search(iters, beam_width)
print(f"Best board configuration:")
print("Score: ", simulate_movement(best_board))
print(print_board_str(best_board))
