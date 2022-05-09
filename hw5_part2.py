# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 16:17:09 2022

@author: Philip Paterson
HW 5 Part 2
This program uses functions defined in the hw5_util file to access a grid of 
elevations and starting locations associated with the grid depending on the 
user input. This program then finds both the steepest and most gradual 
paths for each respective starting point, and determines if each path 
ends up at a global maximum, local maximum, or no maximum. Then a new 
"path grid" of how many times each corresponding location on the 
given grid is traversed within all the steepest and most gradual paths. 
"""

# Import the given functions
from hw5_util import num_grids, get_grid, get_start_locations


# Defining Functions
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
        

def get_global_max(given_grid):
    '''
    Finds the global maximum of a given grid.

    Parameters
    ----------
    given_grid : LIST
        A grid of elevation heights.

    Returns
    -------
    global_maximum_height : INT
        The highest elevation on the given grid.
    global_maximum_coords : TUPLE
        The coordinates of the highest elevation on the given grid.

    '''
    global_maximum_height = 0
    global_maximum_coords = (0, 0)
    r = 0
    while r < len(given_grid):
        c = 0
        while c < len(given_grid[r]):
            height = given_grid[r][c]
            if height > global_maximum_height:
                global_maximum_height = height
                global_maximum_coords = (r, c)
            c += 1
        r += 1        
    return global_maximum_height, global_maximum_coords


def check_local_max(given_grid, coords, height):
    '''
    This functions checks if the given coordinates are a local maximum
    on the given grid.

    Parameters
    ----------
    given_grid : LIST
        A grid of elevation heights.
    coords : TUPLE
        A tuple with the row and column number of the given location.
    height : INT
        The associated elevation to the given coordinates on the given
        grid.

    Returns
    -------
    its_local_max : BOOL
        Returns True if it is a local max. Returns False if not.

    '''
    nbrs = get_nbrs(coords, len(given_grid), len(given_grid[0]))
    i = 0
    its_local_max = True
    while its_local_max and i < len(nbrs):
        if height <= given_grid[nbrs[i][0]][nbrs[i][1]]:
            its_local_max = False
        i += 1
    return its_local_max


def get_extreme_path(given_grid, start_coords, step_maximum, path_type):
    '''
    This function generates and returns a path starting from the given 
    coordinates, that follows the maximum step constraint and is either the 
    steepest or the most gradual path, depending on the inputs.

    Parameters
    ----------
    given_grid : LIST
        A grid of elevation heights.
    start_coords : TUPLE
        A tuple with the row and column number of the starting location.
    step_maximum : INT
        The maximum change in elevation from one location to another.
    path_type : STR
        Determines if the function finds the steepest path if "steep" or
        the most gradual path if "gradual".

    Returns
    -------
    the_path : LIST
        A list of the coordinates that are traveled to along the
        generated path.

    '''
    keep_going = True
    the_path = [start_coords]
    while keep_going:
        largest_step = 0
        smallest_step = 100000000
        next_coords = start_coords
        # Determines the next location to travel to, if at all, depending
        # on the inputs.
        for nbr in get_nbrs(start_coords, len(given_grid), len(given_grid[0])):
            step = given_grid[nbr[0]][nbr[1]] - given_grid[start_coords[0]][start_coords[1]]
            if step <= step_maximum:
                if path_type == 'steep' and step > largest_step:
                    largest_step = step
                    next_coords = nbr
                elif path_type == 'gradual' and step > 0 and step < smallest_step:
                    smallest_step = step
                    next_coords = nbr
        if start_coords == next_coords:
            keep_going = False
        else:
            the_path.append(next_coords)
            start_coords = next_coords
    return the_path


def path_data_print(given_grid, path, global_maximum_coords):
    '''
    This function prints these path data:
        -All the coordinates, formatted, within the path
        -Whether the final position is a global maximum, local maximum,
         or not a maximum
         
    Parameters
    ----------
    given_grid : LIST
        A grid of elevation heights.
    path : LIST
        A list of the coordinates of the locations traveled across along
        the given path.
    global_maximum_coords : TUPLE
        A tuple of the row and column number of the location of the global
        maximum elevation.

    Returns
    -------
    None.

    '''
    i = 0
    final_coords = path[-1]
    final_height = given_grid[path[-1][0]][path[-1][1]]
    while i < len(path):
        print(path[i], end=' ')
        if (i + 1) % 5 == 0 or i == len(path) - 1:
            print()
        i += 1
    if final_coords == global_maximum_coords:
        print("global maximum")
    elif check_local_max(given_grid, final_coords, final_height):
        print("local maximum")
    else:
        print("no maximum")


def gen_path_grid(given_grid, paths):
    '''
    This function generates a new "path grid" of how many times each 
    corresponding location on the given grid is traversed within all
    the steepest and most gradual paths. 

    Parameters
    ----------
    given_grid : LIST
        A grid of elevation heights.
    paths : LIST
        A list of the coordinates of the locations traveled across along
        all of the paths.

    Returns
    -------
    None.

    '''
    rows_num = len(given_grid)
    cols_num = len(given_grid[0])
    path_matrix = []
    r = 0
    while r < rows_num:
        path_row = []
        c = 0
        while c < cols_num:
            coord_count = paths.count((r, c))
            if coord_count > 0:
                path_row.append(coord_count)
            else:
                path_row.append('.')
            c += 1
        path_matrix.append(path_row)
        r += 1
    print("Path grid")
    for row in path_matrix:
        for coordinate_count in row:
            print('  {0}'.format(coordinate_count), end= '')
        print()


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
    
    # Asking for the maximum step height
    step_max = input("Enter the maximum step height: ").strip()
    print(step_max)
    step_max = int(step_max)
    
    # Asking if the grid should be printed
    should_print = input("Should the path grid be printed (Y or N): ").strip()
    print(should_print)
    should_print = should_print.lower()
    
    # Finding total rows and columns
    total_rows = len(grid)
    total_columns = len(grid[0])
    print("Grid has {0} rows and {1} columns".format(total_rows, total_columns))
    
    # Getting the global max data
    global_max_height, global_max_coords = get_global_max(grid)
    print("global max:", global_max_coords, global_max_height)
    
    # Printing the path data
    start_locations = get_start_locations(n)
    every_path = []
    print("===")
    for start in start_locations:
        steepest_path = get_extreme_path(grid, start, step_max, 'steep')
        gradual_path = get_extreme_path(grid, start, step_max, 'gradual')
        every_path += steepest_path + gradual_path
        print("steepest path")
        path_data_print(grid, steepest_path, global_max_coords)
        print("...")
        print("most gradual path")
        path_data_print(grid, gradual_path, global_max_coords)
        print("===")
    
    # Printing the path grid
    if should_print == 'y':
        gen_path_grid(grid, every_path)