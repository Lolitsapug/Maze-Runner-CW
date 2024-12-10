import sys,argparse
sys.path.append('.')
from runner import *

filename = ""

def shortest_path(maze, starting=(0,0), goal=None) -> list[tuple[int, int]]:
    if goal == None:
        goal = get_dimensions(maze)[0]-1, get_dimensions(maze)[1]-1

        #resets goal to top right corner if none is given

    maze_width, maze_height = get_dimensions(maze) #check if starting and goal are in the maze
    maze_width-=1
    maze_height-=1
    if not (0 <= starting[0] <= maze_width and 0 <= starting[1] <= maze_height): 
        raise ValueError("ValueError starting coordinates not in maze") 
    if not (0 <= goal[0] <= maze_width and 0 <= goal[1] <= maze_height): 
        raise ValueError("ValueError goal coordinates not in maze")
    
    runner = create_runner(starting[0],starting[1])

    positions = [starting] #includes starting position
    with open("exploration.csv", mode='w', newline='') as file: #exploration.csv file
        writer = csv.writer(file)
        writer.writerow(["Step", "x-coordinate", "y-coordinate", "Actions"])
        step = 1
            
        #moves runner through the maze to the goal using the move function while logging all positions
        while get_x(runner) != goal[0] or get_y(runner) != goal[1]:
            position = get_x(runner),get_y(runner)
            action = move(runner,maze)[1]
            positions.append((get_x(runner),get_y(runner)))
            #display(maze,runner)
            writer.writerow([step, position[0], position[1], action]) #writes step, position before moving, action 
            step += 1
    
    i = 0
    characters = {}
    while i < len(positions):
        if positions[i] in characters:
            start = characters[positions[i]] + 1 #grabs the index of the first occurence
            #remove elements from first seen to duplicate so that the repetitions are removed for shortest path
            positions = positions[:characters[positions[i]]+1] + positions[i+1:] 
            
            i = start  
            characters.clear()
            for index in range(i): 
                characters[positions[index]] = index
            #resets the characters dictionary and index for the new positions array
           
        else:
            characters[positions[i]] = i #adds characters to the dictionary
            i += 1
     
    display_with_path(maze,positions)#display shortest path
    print("Shortest Path")   


    pathlength = len(positions) #line 5 length of shortest path
    score = step / 4 + pathlength #line 2 score

    with open("statistics.txt", mode='w') as file:
        file.write(f"{filename}\n") #line 1 filename
        file.write(f"{score:.1f}\n") #line 2 score
        file.write(f"{step}\n") #line 3 num exploration steps
        file.write(f"{positions}\n") #line 4 shortest path found
        file.write(f"{pathlength}") #line 5 length of shortest path

    return positions

def maze_reader(maze_file: str):
    try:
        with open(maze_file, 'r') as file:
            lines = file.readlines()
    except IOError:
        print("IOError cant open file")
        return None #returns nothing as IO error

    # Validate maze height and width format
    height = (len(lines)-1) // 2
    width = (len(lines[0].strip())-1) // 2

    for line in lines:
        for char in line:
            if char != "#" and char != "." and char != "\n": #checks for valid characters and line break
                raise ValueError("ValueError invalid character")
            

    if len(lines) != (2*height) +1: #checks if correct number of Y lines
        raise ValueError("ValueError invalid maze dimensions") 
    for line in lines:
        if len(line.strip()) !=(2*width)+1: #checks if correct length of X lines
            raise ValueError("ValueError invalid maze dimensions")

    #checks if the maze is fully enclosed in #
    for i in range((2*width)+1):
        if lines[0][i] != '#' or lines[2*height][i] != '#':
            raise ValueError("ValueError maze is not fully enclosed") #checks top and bottom
    for j in range((2*height) + 1):
        if lines[j][0] != '#' or lines[j][2*width] != '#':
            raise ValueError("ValueError Maze is not fully enclosed ") #checks left and right
        
    #checks if each wall intersection is a #
    for y in range(0, (2*height)+1, 2): 
        for x in range(0, (2*width)+1, 2): 
            if lines[y][x] != '#': 
                raise ValueError("ValueError intersection of walls must be a #")

    maze = [[[False, False, False, False] for x in range(width)] for y in range(height)] #creates the maze 2Darray

    for y in range(height):
        for x in range(width):
            row = height-1-y#reverse Y coordinate
            #checks if N E S W walls exist for each map
            if lines[2*y][(2*x)+1] == '#':
                maze[row][x][0] = True
            if lines[2*y+1][(2*x)+2] == '#':
                maze[row][x][1] = True
            if lines[2*y+2][(2*x)+1] == '#':
                maze[row][x][2] = True
            if lines[2*y+1][2*x] == '#':
                maze[row][x][3] = True

    #adds bottom and right wall
    for j in range(width):
        if lines[2*height][(2*j)+1] == '#':
            maze[0][j][2] = True
    for i in range(height):
        if lines[2*i+1][2*width] == '#':
            maze[height-1-i][width-1][1] = True

    #display(maze)
    return maze

def positionType(position):
    try:
        x, y = map(int, position.split(","))
        return (x, y)
    except ValueError:
        raise argparse.ArgumentTypeError("Starting and goal must be in x,y format")

def main():
    global filename
    parser = argparse.ArgumentParser(description='ECS Maze Runner')
    parser.add_argument('maze', type=str, help='The name of the maze file, e.g., maze1.mz')
    parser.add_argument('--starting', type=positionType, default="0,0", help='The starting position, e.g., "2, 1"')
    parser.add_argument('--goal', type=positionType, help='The goal position, e.g., "4, 5"')

    args = parser.parse_args()
    
    filename = args.maze
    try: #checks and reads the maze file
        maze = maze_reader(filename)
    except ValueError as errorline:
        print(errorline)
        return
    
    starting= args.starting
    goal= args.goal
    
    path = shortest_path(maze, starting=starting, goal=goal) 
    print(path)

if __name__ == "__main__":
    main()

