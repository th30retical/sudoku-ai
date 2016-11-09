# By: Theodore Tan
#python3

# imports
import sys
from copy import deepcopy
from time import sleep

# variables
alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

class CSP():
    """
    ------------------------------------------------------
    A CSP object that holds the variables, domains and
    constraints
    ------------------------------------------------------
    """
    def __init__(self, variables , domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

def open_file(filename):
    """
    ------------------------------------------------------
    Opens the file and sets the data
    ------------------------------------------------------
    Inputs:
        filename - the textfile name
    Returns:
        data - the data from the textfile (key, value)
    ------------------------------------------------------
    """
    data = []
    with open(filename, 'r') as f: # automatically closes file
        for i, line in enumerate(f): # line number, line contents
            for j, value in enumerate(line, start=1): # value number, value
                if j < 10: data.append(('{}{}'.format(alpha[i],j), value)) # dont get the new line character
    return data

def setup(data):
    """
    ------------------------------------------------------
    Creates the Variables, Domains and Constraints for
    the CSP
    ------------------------------------------------------
    Inputs:
        data - the data from the textfile (key, value)
    Returns:
        csp - the generated csp
    ------------------------------------------------------
    """
    variables = [key for (key, value) in data]
    domains = {key: [x for x in range(1, 10)] if value is '-' else [int(value)] for (key, value) in data}
    constraints = {key: generate_constraints(alpha.index(key[0]), int(key[1])) for key in variables}
    return CSP(variables, domains, constraints)

# returns the range for each 3x3 block given x
def block(x): return range((x//3)*3, (x//3)*3+3)

def generate_constraints(x,y):
    """
    ------------------------------------------------------
    Generate constraints for each variable
    ------------------------------------------------------
    Inputs:
        x - the index of the letter (row)
        y - the column of the puzzle
    Returns:
        constraints - the set of constraints for the
            cell
    ------------------------------------------------------
    """
    # gets the cells that are in the same row, column and block
    constraints = ['{}{}'.format(alpha[i],j) for i in range(9) for j in range(1,10) if
        ((x != i) or (y != j)) and ((x == i) or (y == j) or (i in block(x) and j-1 in block(y-1)))]
    return constraints

def ac_3(csp):
    """
    ------------------------------------------------------
    Attempt to see if the CSP is arc consistent
    ------------------------------------------------------
    Inputs:
        csp - a binary CSP with components(X, D, C)
    Returns:
        result - false if an inconsistency is found,
            true otherwise
    ------------------------------------------------------
    """
    # initialize the queue with all the arcs in the sudoku
    queue = [(i,j) for i in csp.variables for j in csp.constraints[i]]
    # print("Initial length of queue: {}".format(len(queue)))
    status_bar(len(queue))
    while queue != []:
        node = queue.pop(0)
        # print("Current length of queue: {}".format(len(queue)), end="\t\t")
        status_bar(len(queue)) # show the length of the queue in a status bar
        # if the domain is revised
        if revise(csp, node[0], node[1]):
            # make sure the domain is not empty
            if len(csp.domains[node[0]]) == 0:
                sys.stdout.write('\n')
                sys.stdout.flush()
                print()
                return False
            # add the remaining arcs to the queue to update their domains
            for x in csp.constraints[node[0]]:
                if x is not node[1]: queue.append((x, node[0]))
    print()
    return True

def revise(csp, x1, x2):
    """
    ------------------------------------------------------
    See if we revise the domain of x1
    ------------------------------------------------------
    Inputs:
        csp - a binary CSP with components(X, D, C)
        x1 - variable 1
        x2 - variable 2
    Returns:
        revised - true iff we revise the domain of x1
    ------------------------------------------------------
    """
    revised = False
    for x in csp.domains[x1]:
        # if there are no values in the second domain that satisfy the constraint
        if not any([x for y in csp.domains[x2] if x is not y]):
            csp.domains[x1].remove(x)
            revised=True
    return revised

def check_solved(ac3, csp):
    """
    ------------------------------------------------------
    Checks if the CSP is solved after applying AC-3
    ------------------------------------------------------
    Inputs:
        csp - a binary CSP with components(X, D, C)
    ------------------------------------------------------
    """
    if ac3:
        # if every domain only has one value
        print('The CSP is arc-consistent', end='')
        if not any([x for x in csp.variables if len(csp.domains[x]) > 1]):
            print()
            print_sudoku(csp)
        else:
            print(', but it is not solved.')
            input('Use backtracking search to find the solution. Press any key to Continue...')
            result = backtracking_search(csp)
            if result:
                # set the domain to be the complete assignment
                csp.domains = result
                print_sudoku(csp)
    else:
        print('Failure: No Solution Found')
    return

def print_sudoku(csp):
    """
    ------------------------------------------------------
    Print the solved sudoku
    ------------------------------------------------------
    Inputs:
        csp - a binary CSP with components(X, D, C)
    ------------------------------------------------------
    """
    sudoku = [['-' for x in range(9)] for y in range(9)]
    # sets the values in the sudoku variable
    for key in csp.variables:
        sudoku[alpha.index(key[0])][int(key[1])-1] = csp.domains[key][0]
    print()
    # prints the sudoku all pretty like
    for x in sudoku:
        for y in x:
            print(y, end=' ')
        print()
    print()
    return

def backtracking_search(csp):
    """
    ------------------------------------------------------
    Implements a backtracking search
    ------------------------------------------------------
    Inputs:
        csp - a binary CSP that has already gone through
            the ac-3 algorithm with components(X, D, C)
    Returns:
        A solution or failure
    ------------------------------------------------------
    """
    return backtrack({}, csp)

def backtrack(assignment, csp_old):
    """
    ------------------------------------------------------
    Backtracking search algorithm
    ------------------------------------------------------
    Inputs:
        assignment - the assignment
        csp_old - a binary CSP that has already gone through
            the ac-3 algorithm with components(X, D, C)
    Returns:
        A solution or failure
    ------------------------------------------------------
    """
    csp = deepcopy(csp_old) # make a copy of the csp for later use
    # initialize the assignment to be the values that are assigned (on first run)
    assignment = set_assignment(csp) if assignment == {} else assignment
    # if all the values in the assignment have been set
    if all([assignment[key] for key in assignment]): return assignment
    # use the MVR heuristic to get an unassigned variable
    var = select_unassigned_variable(csp)
    for value in csp.domains[var]: # order domain variables part
        # make sure the value is consistent with the assignment
        if [value] not in [assignment[key] for key in csp.constraints[var]]:
            csp.domains[var] = [value]
            # perform inference using ac-3 and if success
            if ac_3(csp):
                # put all the inferences in the assignment and call backtrack again
                result = backtrack(set_assignment(csp), csp)
                if result: return result
            csp.domains = deepcopy(csp_old.domains) # remove all inferences if failure
    return False

# initialize/update the assignment for the backtracking algorithm
def set_assignment(csp): return {key: [csp.domains[key][0]] if len(csp.domains[key]) is 1 else [] for key in csp.variables}

def select_unassigned_variable(csp):
    """
    ------------------------------------------------------
    Selecting a variable using the Minimum Remaining
    Values (MVR) heuristic
    ------------------------------------------------------
    Inputs:
        csp - a binary CSP that has already gone through
            the ac-3 algorithm with components(X, D, C)
    Returns:
        var - the variable with the smallest remaining
            values
    ------------------------------------------------------
    """
    var = (None, 10) # using a value that will never exist
    for key in csp.variables:
        length = len(csp.domains[key])
        # get the variable with the least remaining values
        if length is not 1 and var[1] > length:
            var = (key, length)
    return var[0]

def status_bar(length):
    """
    ------------------------------------------------------
    Display a visual representation of how many items
    are left in the queue for the AC-3 algorithm
    ------------------------------------------------------
    Inputs:
        length - the number of items left in the queue
    ------------------------------------------------------
    """
    sleep(0.0003) # so we can see the length of the queue change
    barlength = 50
    total = 6500
    filled = int(barlength * length / total)
    bar = '█' * filled + '-' * (barlength - filled)
    sys.stdout.write('\r%s |%s| %s' % ('Length of Queue:', bar, '{:>4d}'.format(length)))
    if length == 0: # start a new line if the queue is empty
        sys.stdout.write('\n')
    sys.stdout.flush()
    return
