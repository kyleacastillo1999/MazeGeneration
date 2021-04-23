"""
Created with Pycharm
Author: Kyle Castillo
Date: 02/05/2021
Contact: kylea.castillo1999@gmail.com
"""

from random import shuffle
from point import Point

"""
Generates a 2D array that consists entirely of walls only.
It passes through a specified maze value size and generates
a size x size maze based on that value.

In this case the starting point will always be treated as the first value
in the array. Borders will the the outermost values.

This maze is also encoded as each cell having ¯| to designate where the walls of the maze are.
"""


class RandomMaze:

    # Constructor
    def __init__(self, width, height, start_x=0, start_y=0, goal_x=0, goal_y=0):
        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.maze = [['¯|'] * self.width for _ in range(self.height)]

    def get_maze(self):
        return self.maze

    # ------------------------------------------------
    # Generates a maze based on the parameters based within
    # the class.
    # ------------------------------------------------
    def generate_maze(self):
        """
        :return: Returns a 2D array which represents the maze.
        """
        # --------------------------------------------------------------------------------
        # Height and width of the 2D cell array
        # We are subtracting 1 for the purposes of marking the bottom and left as visited
        # in order to prevent the program from attempting to go beyond the bounds of the
        # maze.
        # --------------------------------------------------------------------------------

        c_height = self.height - 1
        c_width = self.width - 1

        # ------------------------------------------------------------------------------
        #  An array to keep track which cells have been visited and which cells are
        # open to carve a maze.
        # -------------------------------------------------------------------------------

        visited_cells = [[0] * c_width + [1] for _ in range(c_height)] + [[1] * (c_width + 1)]

        # ---------------------------------------------------------------------------------
        # Recursive back tracking implementation for generating the maze.
        # ---------------------------------------------------------------------------------
        def traverse(x, y):
            """
            :param x: The x coordinate of a cell we are examining.
            :param y: The y coordinate of a cell we are examining.
            :return: A newly populated maze.
            """
            # -------------------------------------------------------
            # To ensure the maze is random we first need to select
            # a random direction. The array has the directions which
            # we shuffle and select the first in the array to use.
            # -------------------------------------------------------
            directions = ['N', 'E', 'W', 'S']
            shuffle(directions)
            dir_index = 0

            # ----------------------------------------------------------------------------------------------------
            # For a cell at x,y a random direction is chosen and is checked to see if it open or already visited.
            # - If the cell in the the selected direction is open remove the wall and go to that cell.
            # - If the cell has been visited in the chosen direction update the dir index to select a new direction.
            # - If no new directions exist break the loop.
            # ----------------------------------------------------------------------------------------------------

            # Loops until a new direction is chosen or until all directions have been used.
            while dir_index <= 4:
                if dir_index == 4:
                    break
                selected_dir = directions[dir_index]

                # North - remove the wall north if it has not been visited.
                # Do not remove the wall if you are as far north as you can go
                if selected_dir.__eq__('N'):
                    # If the cell has already been visited update the dir_index
                    if visited_cells[y - 1][x] == 1 or y == 0:
                        dir_index += 1
                    # Otherwise the cell has not been visited, carve a path and update coordinates.
                    else:
                        s = self.maze[y][x].replace("¯", " ")
                        self.maze[y][x] = s
                        visited_cells[y - 1][x] = 1
                        y -= 1
                        traverse(x, y)

                # East - remove the wall to the east if it has not been visited.
                # Do not remove the wall if you are at the eastern most side.
                elif selected_dir.__eq__('E'):
                    # If the cell has already been visited update the dir_index
                    if visited_cells[y][x + 1] == 1 or x == self.width - 1:
                        dir_index += 1
                    # Otherwise the cell has not been visited, carve a path and update coordinates.
                    else:
                        s = self.maze[y][x].replace("|", " ")
                        self.maze[y][x] = s
                        visited_cells[y][x + 1] = 1
                        x += 1
                        traverse(x, y)

                # West - remove the wall from the adjacent cell if it has not been visited.
                # Do not remove the wall if you are at the western most side.
                elif selected_dir.__eq__('W'):
                    if visited_cells[y][x - 1] == 1 or x == 0:
                        dir_index += 1
                    # Otherwise the cell has not been visited, carve a path and update coordinates.
                    else:
                        s = self.maze[y][x - 1].replace("|", " ")
                        self.maze[y][x - 1] = s
                        visited_cells[y][x - 1] = 1
                        x -= 1
                        traverse(x, y)

                # South - remove the wall from the bottom cell if it has not been visited.
                # Do not remove the wall if you are at the southernmost side.
                elif selected_dir.__eq__('S'):
                    if visited_cells[y + 1][x] == 1 or y == self.height - 1:
                        dir_index += 1
                    # Otherwise the cell has not been visited, carve a path and update coordinates.
                    else:
                        s = self.maze[y + 1][x].replace("¯", " ")
                        self.maze[y + 1][x] = s
                        visited_cells[y + 1][x] = 1
                        y += 1
                        traverse(x, y)

            # Printing for debugging purposes, uncomment to see parts of the maze generation
            # print("Direction: ", directions[0], "Point: ", x, ",", y)
            # print_maze(maze)
            # print("")

        traverse(self.start_x, self.start_y)

        # ------------------------------------------------------------------------------------------
        # Before the maze is returned the goal is carved, in this case its assumed to be the bottom.
        # Due to the nature of the maze we only need to remove the north wall to create a goal.
        # ------------------------------------------------------------------------------------------
        self.maze[self.goal_x][self.goal_y] = self.maze[self.goal_y][self.goal_x].replace("¯", "G")
        if self.maze[self.start_x][self.start_y].__contains__("¯"):
            # Note this part is entirely optional since the agent doesn't need to have a character for the start.
            self.maze[self.start_x][self.start_y] = self.maze[self.start_x][self.start_y].replace("¯", "S")
        else:
            self.maze[self.start_x][self.start_y] = self.maze[self.start_x][self.start_y].replace(" ", "S")
        return self.maze

    # ------------------------------------------------
    # Creates a solution to the maze using breadth-first
    # searching.
    # ------------------------------------------------

    def solve_breadth_first(self):
        """
        :return: Returns a solution or a failure
        """

        # Starting point an and empty path to be returned as a solution
        start_pt = Point(self.start_x, self.start_y)
        path = []

        # A 2D array to create visited and unvisited cells (0 = unvisited, 1 = visited)
        c_width = self.width - 1
        c_height = self.height - 1
        visited_cells = [[0] * c_width + [1] for _ in range(c_height)] + [[1] * (c_width + 1)]

        # Setting the goal point as unvisited.
        visited_cells[self.goal_x][self.goal_y] = 0

        # A queue for the BFS, filled with the starting point
        queue = [start_pt]

        # Marking the starting cell as visited.
        visited_cells[self.start_x][self.start_y] = 1

        # ------------------------------------------------
        # Below is a function that helps the agent
        # decide which direction it can go. If the chosen
        # direction is open then the function returns true
        # Otherwise it returns false.
        # ------------------------------------------------
        def reachable(x, y, direction):
            """
            :param x: The x coordinate of the current cell
            :param y: The y coordinate of the current cell
            :param direction: The selected direction (N,S,E,W)
            :return: Boolean, true if there are no walls, false if there are.
            """

            # ------------------------------------------------------
            # Heading north is a decrease in y,
            # Don't go north if you are at y = 0
            # Don't go north if the cell you are in has ¯ in it.
            # Go north if the above two are met.
            # ------------------------------------------------------
            if direction == 'N':
                if y == 0:
                    return False
                elif self.maze[y][x].__contains__('¯'):
                    return False
                else:
                    return True

            # ------------------------------------------------------
            # Heading east is an increase in x,
            # Don't go east if you are at the width of the maze
            # Don't go east if the cell you are in has | in it.
            # Go east if the above two are met.
            # ------------------------------------------------------
            if direction == 'E':
                if x == self.width - 1:
                    return False
                elif self.maze[y][x].__contains__('|'):
                    return False
                else:
                    return True

            # ------------------------------------------------------
            # Heading south is an increase in y,
            # Don't go south if you are at the height of the maze
            # Don't go south if the cell below you has a ¯ in it
            # Go south if the above two are met.
            # ------------------------------------------------------
            if direction == 'S':
                if y == self.height - 1:
                    return False
                elif self.maze[y + 1][x].__contains__('¯'):
                    return False
                else:
                    return True

            # -----------------------------------------------------
            # Heading west is a decrease in x,
            # Don't go west if you are at 0
            # Don't go west if the cell next you as as a | in it
            # Go west if the above two are met.
            # -----------------------------------------------------
            if direction == 'W':
                if y == 0:
                    return False
                elif self.maze[y][x - 1].__contains__('|'):
                    return False
                else:
                    return True

        # ------------------------------------------------
        # Breadth first part of the solution
        # Tests for a cell and checks for any possible
        # neighbors, while they exist add the neighbors to
        # The queue. Once the queue is empty or once a goal
        # point has been reached return the path.
        # ----------------------------------------------
        while queue:

            # Test point in question as FIFO queue
            test_pt = queue.pop(0)
            test_x = test_pt.get_x()
            test_y = test_pt.get_y()

            # If we reach the goal at any point in time return the current path
            if self.maze[test_y][test_x].__contains__("G"):
                path.append(test_pt)
                while test_pt.get_parent():
                    path.append(test_pt.get_parent())
                    test_pt = test_pt.get_parent()
                return path

            # Check North
            if reachable(test_x, test_y, "N"):
                if visited_cells[test_y - 1][test_x] == 0:
                    visited_cells[test_y - 1][test_x] = 1
                    next_pt = Point(test_x, test_y - 1, test_pt)
                    queue.append(next_pt)

            # Check South
            if reachable(test_x, test_y, "S"):
                if visited_cells[test_y + 1][test_x] == 0:
                    visited_cells[test_y + 1][test_x] = 1
                    next_pt = Point(test_x, test_y + 1, test_pt)
                    queue.append(next_pt)

            # Check East
            if reachable(test_x, test_y, "E"):
                if visited_cells[test_y][test_x + 1] == 0:
                    visited_cells[test_y][test_x + 1] = 1
                    next_pt = Point(test_x + 1, test_y, test_pt)
                    queue.append(next_pt)

            # Check West
            if reachable(test_x, test_y, "W"):
                if visited_cells[test_y][test_x - 1] == 0:
                    visited_cells[test_y][test_x - 1] = 1
                    next_pt = Point(test_x - 1, test_y, test_pt)
                    queue.append(next_pt)

        # If the goal has not been found print a message and return nothing
        print("No goal found!")
        return None

    # ------------------------------------------------
    # Solves the maze using depth first searching.
    # ------------------------------------------------
    def solve_depth_first(self):
        """
        :return: Returns a solution or a failure
        """

        # Like breadth first we have the starting point and an empty path
        start_pt = Point(self.start_x, self.start_y)
        path = []

        # A 2D array to keep track of visited and unvisited cells
        c_width = self.width - 1
        c_height = self.height - 1
        visited_cells = [[0] * c_width + [1] for _ in range(c_height)] + [[1] * (c_width + 1)]

        # Setting the goal point as unvisited
        visited_cells[self.goal_x][self.goal_y] = 0

        # A stack for the DFS
        stack = [start_pt]

        # Marking the starting cell as visited.
        visited_cells[self.start_x][self.start_y] = 1

        # Using reachable again, not the best practice here
        def reachable(x, y, direction):
            """
            :param x: The x coordinate of the current cell
            :param y: The y coordinate of the current cell
            :param direction: The selected direction (N,S,E,W)
            :return: Boolean, true if there are no walls, false if there are.
            """

            # ------------------------------------------------------
            # Heading north is a decrease in y,
            # Don't go north if you are at y = 0
            # Don't go north if the cell you are in has ¯ in it.
            # Go north if the above two are met.
            # ------------------------------------------------------
            if direction == 'N':
                if y == 0:
                    return False
                elif self.maze[y][x].__contains__('¯'):
                    return False
                else:
                    return True

            # ------------------------------------------------------
            # Heading east is an increase in x,
            # Don't go east if you are at the width of the maze
            # Don't go east if the cell you are in has | in it.
            # Go east if the above two are met.
            # ------------------------------------------------------
            if direction == 'E':
                if x == self.width - 1:
                    return False
                elif self.maze[y][x].__contains__('|'):
                    return False
                else:
                    return True

            # ------------------------------------------------------
            # Heading south is an increase in y,
            # Don't go south if you are at the height of the maze
            # Don't go south if the cell below you has a ¯ in it
            # Go south if the above two are met.
            # ------------------------------------------------------
            if direction == 'S':
                if y == self.height - 1:
                    return False
                elif self.maze[y + 1][x].__contains__('¯'):
                    return False
                else:
                    return True

            # -----------------------------------------------------
            # Heading west is a decrease in x,
            # Don't go west if you are at 0
            # Don't go west if the cell next you as as a | in it
            # Go west if the above two are met.
            # -----------------------------------------------------
            if direction == 'W':
                if y == 0:
                    return False
                elif self.maze[y][x - 1].__contains__('|'):
                    return False
                else:
                    return True

        # Like the breadth first search we are looping until our stack is empty
        while stack:

            # Here is the difference, this is a LIFO queue while breadth uses a FIFO queue.
            test_pt = stack.pop()
            test_x = test_pt.get_x()
            test_y = test_pt.get_y()

            # If we reach the goal return the current path
            if self.maze[test_y][test_x].__contains__("G"):
                path.append(test_pt)
                while test_pt.get_parent():
                    path.append(test_pt.get_parent())
                    test_pt = test_pt.get_parent()
                return path

            # Check North
            if reachable(test_x, test_y, 'N'):
                if visited_cells[test_y - 1][test_x] == 0:
                    visited_cells[test_y - 1][test_x] = 1
                    next_pt = Point(test_x, test_y - 1, test_pt)
                    stack.append(next_pt)

            # Check South
            if reachable(test_x, test_y, 'S'):
                if visited_cells[test_y + 1][test_x] == 0:
                    visited_cells[test_y + 1][test_x] = 1
                    next_pt = Point(test_x, test_y + 1, test_pt)
                    stack.append(next_pt)

            # Check East
            if reachable(test_x, test_y, 'W'):
                if visited_cells[test_y][test_x - 1] == 0:
                    visited_cells[test_y][test_x - 1] = 1
                    next_pt = Point(test_x - 1, test_y, test_pt)
                    stack.append(next_pt)

            # Check West
            if reachable(test_x, test_y, 'E'):
                if visited_cells[test_y][test_x + 1] == 0:
                    visited_cells[test_y][test_x + 1] = 1
                    next_pt = Point(test_x + 1, test_y, test_pt)
                    stack.append(next_pt)

        print("No path found!")
        return None

    # --------------------------------
    # Prints the maze as a 2D array.
    # --------------------------------

    def print_maze(self):
        """
        :return: None
        """
        row_length = len(self.maze)
        # This isn't entirely correct but if the map is square we can get away with it.
        col_length = len(self.maze)
        for row in range(row_length):
            for col in range(col_length):
                print(self.maze[row][col], end='')
            print('')
        return None
