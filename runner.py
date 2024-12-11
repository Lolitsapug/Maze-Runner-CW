import sys,csv
sys.path.append('.')
from maze import *

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
	

	return (runner,actions)

def explore(runner,maze,goal=None):
	actions = []
	log = []
	if goal == None:
		goal = get_dimensions(maze)[0]-1, get_dimensions(maze)[1]-1

	while get_x(runner) != goal[0] or get_y(runner) != goal[1]:
		position = (get_x(runner), get_y(runner))
		action = move(runner,maze)[1]
		actions.append(action)
		log.append((position[0], position[1], action))
		display(maze,runner)
	#print("Reached Goal")
	#print(actions)

	with open("exploration.csv", mode='w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(["Step", "x-coordinate", "y-coordinate", "Actions"])
		step = 1
		for x, y, action in log:
			writer.writerow([step, x, y, action])
			step += 1
   
	return "".join(actions)

def display(maze,runner=None):
	test = []
	wall = "#"
	empty = "."
	for i in range((get_dimensions(maze)[1])*3):
		test.append([])

	h = (get_dimensions(maze)[1]-1)*3

	for y in range(get_dimensions(maze)[1]):
		for x in range(get_dimensions(maze)[0]):
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

	if runner != None:
		index = ["N","E","S","W"].index(get_orientation(runner))
		playerSymbols = ["^",">","v","<"]
		test[(get_dimensions(maze)[1]-1)*3-runner.y*3+1][runner.x*3+1] = playerSymbols[index]

	for array in test:
		print(" ".join(array))

def display_with_path(maze, positions):
	test = []
	wall = "#"
	empty = "."
	start_symbol = "\033[93m□\033[0m"
	path_symbol = "\033[91m□\033[0m"
	end_symbol = "\033[92m□\033[0m"

	for i in range((get_dimensions(maze)[1]) * 3):
		test.append([])

	height = (get_dimensions(maze)[1] - 1) * 3

	for y in range(get_dimensions(maze)[1]):
		for x in range(get_dimensions(maze)[0]):
			walls = get_walls(maze, x, y)
			test[height-y*3+2].append(wall)
			if not walls[2]:
				test[height-y*3+2].append(empty)
			else:
				test[height-y*3+2].append(wall)
			test[height-y*3+2].append(wall)

			if not walls[3]:
				test[height-y*3 + 1].append(empty)
			else:
				test[height - y*3 + 1].append(wall)
			if walls == (True, True, True, True):
				test[height - y*3 + 1].append(wall)
			else:
				test[height - y*3 + 1].append("+")
			if not walls[1]:
				test[height - y*3 + 1].append(empty)
			else:
				test[height - y*3 + 1].append(wall)

			test[height - y*3].append(wall)
			if not walls[0]:
				test[height - y*3].append(empty)
			else:
				test[height - y*3].append(wall)
			test[height - y*3].append(wall)

	# Mark the path in the maze
	for pos in positions:
		x, y = pos  #positions have the format (x, y)
		test[height - y*3 + 1][x*3 + 1] = path_symbol

	for index, pos in enumerate(positions): #for loop to count and loop through positions
		x, y = pos 
		if index == 0: 
			test[height-y*3+1][x*3+1] = start_symbol #first symbol
		elif index == len(positions) - 1: 
			test[height-y*3+1][x*3+1] = end_symbol #last symbol
		else: 
			if test[height-y*3+1][x*3+1] == empty: 
				test[height-y*3+1][x*3+1] = path_symbol

	for array in test:
		print(" ".join(array))


