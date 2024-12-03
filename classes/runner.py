import sys,time
sys.path.append('.')
from classes.maze import *

runners = []

class Runner:
    def __init__(self, x, y, orientation):
        self.x = x
        self.y = y

        self.orientation = orientation

    def turn(self, direction):
        directions = ["N","E","S","W"]
        index = directions.index(self.orientation)
        if direction == "Right" or direction == "R":
            index+=1
        elif direction == "Left" or direction == "L":
            index -=1
        if index <0:
            index = 3
        elif index >3:
            index = 0
        self.orientation = directions[index]

    def move(self,vector):
        #vector = [forward vector, right vector]
        if self.orientation == "N":
            self.y+=vector
        elif self.orientation == "E":
            self.x +=vector
        elif self.orientation == "S":
            self.y-=vector
        elif self.orientation == "W":
            self.x-=vector

def create_runner(x: int=0, y: int=0, orientation: str="N"):
    return Runner(x,y,orientation)


def get_x(runner):
    return runner.x

def get_y(runner):
    return runner.y

def get_orientation(runner):
    return runner.orientation

def turn(runner, direction: str):
    runner.turn(direction)
    return runner

def forward(runner):
    runner.move(1)
    return runner

def sensewalls(runner,maze)  -> tuple[bool, bool, bool]:
    walls = get_walls(maze,get_x(runner),get_y(runner))
    direction = get_orientation(runner)
    if direction == "N":
        return (walls[3],walls[0],walls[1])
    elif direction == "E":
        return (walls[0],walls[1],walls[2])
    elif direction == "S":
        return (walls[1],walls[2],walls[3])
    elif direction == "W":
        return (walls[2],walls[3],walls[0])

def go_straight(runner, maze):
    if sensewalls(runner,maze)[1] == False:
        return forward(runner)
    else: 
        raise ValueError

def move(runner, maze):
    walls = sensewalls(runner,maze)
    if walls[0] == False: #turn and move left
        runner = turn(runner,"Left")
        runner = forward(runner)
        actions = "LF"
    elif walls[1] == False: #move forward
        runner = forward(runner)
        actions = "F"
    elif walls[2] == False: #turn and move right
        runner = turn(runner,"Right")
        runner = forward(runner)
        actions = "RF"
    else: #turn runner around and move back
        runner = turn(runner,"Right")
        runner = turn(runner,"Right")
        runner = forward(runner)
        actions = "RRF"
    

    print(actions)
    return (runner,actions)

def explore(runner,maze,goal):
    actions = []
    if goal == None:
        goal = get_dimensions(maze)
    print(goal)
    
    while get_x(runner) != goal[0] or get_y(runner) != goal[1]:
        actions.append(move(runner,maze)[1])
        print((get_x(runner),get_y(runner)))

    print("Reached Goal")
    print(actions)

def display(maze,runner):
    test = []
    wall = "#"
    empty = "."
    for i in range((get_dimensions(maze)[1]+1)*3):
        test.append([])

    h = get_dimensions(maze)[1]*3

    for y in range(get_dimensions(maze)[1]+1):
        for x in range(get_dimensions(maze)[0]+1):
            walls = get_walls(maze,x,y)            
            test[h-y*3+2].append(wall)
            if not walls[2]:
                test[h-y*3+2].append(empty)
            else:
                test[h-y*3+2].append(wall)
            test[h-y*3+2].append(wall)

            if not walls[3]:
                test[h-y*3+1].append(empty)
            else:
                test[h-y*3+1].append(wall)
            if walls == (True,True,True,True):
                test[h-y*3+1].append("#")
            else:   
                test[h-y*3+1].append("+")
            if not walls[1]:
                test[h-y*3+1].append(empty)
            else:
                test[h-y*3+1].append(wall)       

            test[h-y*3].append(wall)
            if not walls[0]:
                test[h-y*3].append(empty)
            else:
                test[h-y*3].append(wall)
            test[h-y*3].append(wall)


    index = ["N","E","S",""].index(get_orientation(runner))
    playerSymbols = ["^",">","v","<"]
    test[get_dimensions(maze)[1]*3-runner.y*3+1][runner.x*3+1] = playerSymbols[index]

    for array in test:
        print(" ".join(array))

player = create_runner()
maze = create_maze()
maze = add_vertical_wall(maze,2,2)
maze = add_vertical_wall(maze,2,3)
maze = add_horizontal_wall(maze,2,2)
maze = add_horizontal_wall(maze,2,3)

display(maze,player)