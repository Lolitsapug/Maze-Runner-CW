import sys
sys.path.append('.')
from classes.maze_runner import *

maze = create_maze()
maze = add_vertical_wall(maze,2,2)
maze = add_vertical_wall(maze,2,3)
maze = add_horizontal_wall(maze,2,2)
maze = add_horizontal_wall(maze,2,3)
maze = add_horizontal_wall(maze,0,1)
maze = add_vertical_wall(maze,1,1)

print(shortest_path(maze))
