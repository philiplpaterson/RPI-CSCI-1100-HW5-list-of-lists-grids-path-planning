# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 16:42:54 2022

@author: Philip Paterson
HW 5 Part 1
This program:
    -Takes a grid of elevations
    -Finds and prints the associated starting locations
    -Finds and prints the neighbors of the starting locations
    -Finds a path and determines if it's valid
    -Analyzes the path and determines how many units of elevation one
     goes downward along the path and upward along the path
"""

# Import the given functions
from hw5_util import num_grids, get_grid, get_start_locations, get_path


# Defining Function get_nbrs
def get_nbrs(coords, total_row, total_col):
    '''
    This function returns the neighbors of a given location within the
    bounds of the given grid.

    Parameters
    ----------
    coords : TUPLE
        A tuple with the row and column number of the given location.
    total_row : INT
        The total number of rows in the given grid.
    total_col : INT
        The total number of columns in the given grid.

    Returns
    -------
    nbrs : LIST
        A list of all the neighbors of the given location within the bounds
        of the given grid

    '''
    nbrs = []
    if coords[0] - 1 >= 0:
        nbrs.append((coords[0] - 1, coords[1]))
    if coords[1] - 1 >= 0:
        nbrs.append((coords[0], coords[1] - 1))
    if coords[1] + 1 < total_col:
        nbrs.append((coords[0], coords[1] + 1))
    if coords[0] + 1 < total_row:
        nbrs.append((coords[0] + 1, coords[1]))
    return nbrs


# Main Body of Code
if __name__ == "__main__":
    total_grids = num_grids()
    
    # Asking for the Grid Number until Valid
    valid_index = False
    while not valid_index:
        n = input("Enter a grid index less than or equal to {} (0 to end): ".format(total_grids)).strip()
        print(n)
        n = int(n)
        
        if n <= total_grids:
            valid_index = True
    grid = get_grid(n)
    
    # Asking if the grid should be printed
    should_print = input("Should the grid be printed (Y or N): ").strip()
    print(should_print)
    should_print = should_print.lower()
    
    # Find max digits in the heights
    digit_max = 0
    for row in grid:
        for height in row:
            height_len = len(str(height))
            if height_len > digit_max:
                digit_max = height_len
    
    # Printing the grid
    if should_print == 'y':
        print("Grid", n)
        for row in grid:
            for height in row:
                print('  {1:{0}d}'.format(digit_max, height), end= '')
            print()
    
    # Finding & printing the total rows and columns
    total_rows = len(grid)
    total_columns = len(grid[0])
    print("Grid has {0} rows and {1} columns".format(total_rows, total_columns))
    
    # Finding & printing the neighbors of the starting locations
    start_locations = get_start_locations(n)
    for start in start_locations:
        print("Neighbors of {0}:".format(start), end= '')
        for neighbor in get_nbrs(start, total_rows, total_columns):
            print(' ', neighbor, sep= '', end='')
        print()
        
    # Determining if the path is valid
    path = get_path(n)
    i = 1
    valid_path = True
    while i < len(path) and valid_path:
        if path[i - 1] not in get_nbrs(path[i], total_rows, total_columns):
            invalid_step = path[i - 1], path[i]
            valid_path = False
        i += 1
    
    # Actions for valid or invalid path, respectively
    if valid_path:
        upward = 0
        downward = 0
        # Finds how many units traversed downward and upward, respectively
        i = 1
        while i < len(path):
            start_height = grid[path[i - 1][0]][path[i - 1][1]]
            end_height = grid[path[i][0]][path[i][1]]
            height_step = end_height - start_height
            if height_step < 0:
                downward -= height_step
            elif height_step > 0:
                upward += height_step
            i += 1
        print("Valid path")
        print("Downward", downward)
        print("Upward", upward)
    else:
        print("Path: invalid step from {0} to {1}".format(invalid_step[0], invalid_step[1]))            