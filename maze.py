def create_maze(width = 5, height = 5):
	maze = []
	for i in range(height):
		maze.append([])
		for j in range(width):
			maze[i].append([False,False,False,False]) #[North, East, South, West]
			if i == height-1: #if doing top height, wall to north
				maze[i][j][0] = True
			elif i == 0: #if doing bottom height, wall to south
				maze[i][j][2] = True
			
			if j == 0: #if doing left side, wall to west
				maze[i][j][3] = True
			elif j == width-1: #if doing right side, wall to east
				maze[i][j][1] = True
			
	#maze[[[1,0],[2,0],[3,0]],[1,1],[2,1],[3,1]]
	#maze[[[North,East,South,West],[2,0],[3,0]],[1,1],[2,1],[3,1]]

	return maze

def add_horizontal_wall(maze, x_coordinate, horizontal_line):
	x = x_coordinate
	y = horizontal_line

	maze[y][x][2] = True #new wall below so adds wall to south

	if y >0: #checks that horizontal line is not bottom most
		maze[y-1][x][0] = True #new wall above so adds wall to north

	return maze

def add_vertical_wall(maze, y_coordinate, vertical_line):
	x = vertical_line
	y = y_coordinate

	maze[y][x][3] = True #new wall to left so adds wall to west

	if x >0: #checks that vertical line is not the left most
		maze[y][x-1][1] = True #new wall to right so adds wall to east

	return maze

def get_dimensions(maze) -> tuple[int, int]:
	#(width,height)
	return (len(maze[0]),len(maze))

def get_walls(maze, x_coordinate: int, y_coordinate: int) -> tuple[bool, bool, bool, bool]:
	#(North,East,South,West)
	return tuple(maze[y_coordinate][x_coordinate])




