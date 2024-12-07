import sys,time
sys.path.append('.')
from classes.runner import *

def shortest_path(maze, starting=(0,0), goal=None) -> list[tuple[int, int]]:
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
    return remove_duplicates(positions)


def remove_duplicates(arr):
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

def maze_reader(path:str):
    try:
        with open(path, 'r') as file:
            lines = file.readlines()
    except IOError:
        print("IOError cant open file")
        return None #returns nothing as IO error

    # Validate maze format
    valid_symbols = ["#", ".", "\n"]
    height = (len(lines)-1) // 2
    width = (len(lines[0].strip())-1) // 2

    for line in lines:
        for char in line:
            if char not in valid_symbols:
                raise ValueError("ValueError invalid character")
            

    if len(lines) != 2*height +1: #checks if correct number of Y lines
        raise ValueError("ValueError invalid maze dimensions") 
    for line in lines:
        if len(line.strip()) !=2*width+1: #checks if correct length of X lines
            raise ValueError("ValueError invalid maze dimensions")

    # Check if the maze is fully enclosed
    for j in range(2 * width + 1):
        if lines[0][j] != '#' or lines[2*height][j] != '#':
            raise ValueError("ValueError maze is not fully enclosed") #checks top and bottom
    for i in range(2 * height + 1):
        if lines[i][0] != '#' or lines[i][2*width] != '#':
            raise ValueError("ValueError Maze is not fully enclosed ") #checks left and right

    maze = [[[False, False, False, False] for x in range(width)] for y in range(height)] #creates the maze 2Darray

    for i in range(height):
        for j in range(width):
            row = height-1-i#reverse Y coordinate
            #checks N E S W walls for each space
            if lines[2*i][2*j+1] == '#':
                maze[row][j][0] = True
            if lines[2*i+1][2 * j + 2] == '#':
                maze[row][j][1] = True
            if lines[2*i+2][2 * j + 1] == '#':
                maze[row][j][2] = True
            if lines[2*i+1][2 * j] == '#':
                maze[row][j][3] = True

    #adds bottom and right wall
    for j in range(width):
        if lines[2*height][2*j+1] == '#':
            maze[0][j][2] = True
    for i in range(height):
        if lines[2*i+1][2*width] == '#':
            maze[height-1-i][width-1][1] = True

    display(maze)
    return maze


# Test the function
#arr = [(0, 1), (0, 2), (0, 3), (0, 2), (1, 2), (2, 2), (1, 2), (1, 1), (1, 0)]
#new_arr = removeduplicates(arr)
#print(new_arr)  
#Output should be [(0, 1), (0, 2), (1, 2), (2, 2), (1, 1), (1, 0)]


