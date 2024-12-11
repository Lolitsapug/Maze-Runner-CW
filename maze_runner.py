import sys,argparse
sys.path.append('.')
from runner import *

filename = ""

def shortest_path(parent, start, goal):
	path = []
	current = goal
	while current != start:
		path.append(current)
		current = parent[current] #goas back from goal through parent nodes to get the 'shortest' path
	path.append(start)
	path.reverse()
	return path

def dfs_explore(maze, starting=(0, 0), goal=None):
	#Depth first search. For a tree. Goes all the way to the bottom and then back up again
	if goal is None:
		goal = get_dimensions(maze)[0]-1, get_dimensions(maze)[1]-1  

	runner = create_runner(starting[0], starting[1])

	stack = [(starting[0], starting[1])]  
	visited = []  #track visited nodes to skip them
	parent = {}  #tracks parent nodes for backtracking
	path = []  #store full path

	while stack:
		current = stack.pop()  #current position from stack
		path.append(current)  #log every position moved to in order 

		if current not in visited:
			visited.append(current)  #add new positions to visited list

			runner.x, runner.y = current  #move runner to current position

			if current == goal:
				parent[current] = parent.get(current,current)  
				break  

			#gets free neighbour nodes
			x, y = current
			neighbours = []
			walls = get_walls(maze, x, y)
			if not walls[0]:  # North
				neighbours.append((x, y + 1))
			if not walls[1]:  # East
				neighbours.append((x + 1, y))
			if not walls[2]:  # South
				neighbours.append((x, y - 1))
			if not walls[3]:  # West
				neighbours.append((x - 1, y))
			#in this the runner should prioritize first West, South, East, then North if no visited nodes
			#if runner reaches dead end it goes back to previous node
			#then clears all other neighbours who are not yet visited

			#Add unvisited paths to the stack
			for neighbour in neighbours:
				if neighbour not in visited:
					stack.append(neighbour)
					parent[neighbour] = current  #adds parent coordinate to backtrack later
			#will always go towards newly added neighbours first before visiting existing ones

	shortest = shortest_path(parent, starting, goal) #the 'shortest' path the algorithm can take. 

	display_with_path(maze, shortest)

	explorationsteps = len(path)
	shortestpathlength = len(shortest) #line 5 length of shortest path
	score = explorationsteps / 4 + shortestpathlength #line 2 score

	with open("statistics.txt", mode='w') as file:
		file.write(f"{filename}\n") #line 1 filename
		file.write(f"{score:.1f}\n") #line 2 score
		file.write(f"{explorationsteps}\n") #line 3 num exploration steps
		file.write(f"{shortest}\n") #line 4 shortest path found
		file.write(f"{shortestpathlength}") #line 5 length of shortest path

	return shortest

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
	
	path = dfs_explore(maze, starting=starting, goal=goal) 
	print(path)

if __name__ == "__main__":
	main()


