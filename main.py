import sys
sys.path.append('.')
from classes.runner import *

maze = create_maze()
runner = create_runner()
explore(runner,maze,None)
