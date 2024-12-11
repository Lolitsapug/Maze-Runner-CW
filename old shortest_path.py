import sys
sys.path.append('.')
from runner import *






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