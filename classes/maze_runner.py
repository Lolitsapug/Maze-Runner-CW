import sys,time
sys.path.append('.')
from classes.runner import *

def shortest_path(maze, starting=None, goal=None) -> list[tuple[int, int]]:
    if starting == None:
        starting = (0,0)
    if goal == None:
        goal = get_dimensions(maze)
    
    runner = create_runner(starting[0],starting[1])

    positions = []
    if goal == None:
        goal = get_dimensions(maze)
    print(goal)
    
    while get_x(runner) != goal[0] or get_y(runner) != goal[1]:
        move(runner,maze)[1]
        positions.append((get_x(runner),get_y(runner)))
        display(maze,runner)

    print("Reached Goal")
    print(positions)
    return remove_tuple_duplicates(positions)


def remove_tuple_duplicates(arr):
    seen = {}
    i = 0
    
    while i < len(arr):
        if arr[i] in seen:
            # When a duplicate is found, 
            start = seen[arr[i]] + 1
            arr = arr[:seen[arr[i]] + 1] + arr[i+1:] # remove elements from first seen to duplicate so that the repititions are removed for shortest path
            i = start  #reset from current position
            seen.clear()  #reset dictionaries so it can work on later duplicates
        else:
            seen[arr[i]] = i
            i += 1
    
    return arr

# Test the function
#arr = [(0, 1), (0, 2), (0, 3), (0, 2), (1, 2), (2, 2), (1, 2), (1, 1), (1,0)]
#new_arr = remove_tuple_duplicates(arr)
#print(new_arr)  # Output should be [(0, 1), (0, 2), (1, 2), (2, 2), (1, 1)]


