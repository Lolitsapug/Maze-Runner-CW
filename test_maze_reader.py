def dfs_explore(runner, maze, goal=None):
    if goal is None:
        goal = get_dimensions(maze)  # Set goal to maze dimensions if not provided

    stack = [(get_x(runner), get_y(runner))]  # Initialize stack with starting position
    visited = set()  # Set to track visited positions
    parent = {}  # Dictionary to track parent of each position for backtracking
    actions_log = []  # List to log actions

    # Function to get valid neighbors based on current position's walls
    def get_neighbors(position):
        x, y = position
        neighbors = []
        walls = get_walls(maze, x, y)
        if not walls[0]:  # North
            neighbors.append((x, y + 1))
        if not walls[1]:  # East
            neighbors.append((x + 1, y))
        if not walls[2]:  # South
            neighbors.append((x, y - 1))
        if not walls[3]:  # West
            neighbors.append((x - 1, y))
        return neighbors

    while stack:
        current = stack.pop()  # Get the current position from the stack
        if current in visited:
            continue  # Skip if already visited
        visited.add(current)  # Mark current position as visited
        if current == goal:
            break  # Stop if goal is reached

        # Explore neighbors
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                stack.append(neighbor)
                parent[neighbor] = current  # Track parent for backtracking

        runner.x, runner.y = current  # Update runner's position
        actions = move_to(current, get_orientation(runner), parent.get(current))
        actions_log.append((current[0], current[1], actions))  # Log actions
        display(maze, runner)  # Display maze

    print("Reached Goal")
    return actions_log

# Function to generate actions to move from previous position to current position
def move_to(position, orientation, previous_position):
    x, y = position
    px, py = previous_position if previous_position else (None, None)
    actions = ""

    if px is not None and py is not None:
        if x > px:
            # Moving East
            actions = "RF" if orientation == "N" else "F" if orientation == "E" else "LF" if orientation == "S" else "RRF"
        elif x < px:
            # Moving West
            actions = "LF" if orientation == "N" else "RRF" if orientation == "E" else "RF" if orientation == "S" else "F"
        elif y > py:
            # Moving North
            actions = "F" if orientation == "N" else "LF" if orientation == "E" else "RRF" if orientation == "S" else "RF"
        elif y < py:
            # Moving South
            actions = "RRF" if orientation == "N" else "RF" if orientation == "E" else "F" if orientation == "S" else "LF"

    return actions

