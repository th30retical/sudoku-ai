from src.csp.csp import CSP
from copy import deepcopy

ALPHA = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I')

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
	constraints = {key: generate_constraints(ALPHA.index(key[0]), int(key[1])) for key in variables}
	return CSP(variables, domains, constraints)

def block(x): return range((x//3)*3, (x//3)*3+3)

def generate_constraints(x, y):
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
	constraints = ['{}{}'.format(ALPHA[i], j) for i in range(9) for j in range(1, 10) if
		((x != i) or (y != j)) and ((x == i) or (y == j) or (i in block(x) and j-1 in block(y-1)))]
	return constraints

def ac3(csp):
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
	queue = [(i,j) for i in csp.variables for j in csp.constraints[i]]

	while queue != []:
		node = queue.pop(0)
		if revise(csp, node[0], node[1]):
			if len(csp.domains[node[0]]) == 0:
				return False # not arc consistent
			# add the related arcs to update their domains
			for x in csp.constraints[node[0]]:
				if x is not node[1]: queue.append((x, node[0]))

	return True # is arc consistent

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
		if not any([x for y in csp.domains[x2] if x is not y]):
			csp.domains[x1].remove(x)
			revised=True
	return revised

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
	csp = deepcopy(csp_old)

	assignment = set_assignment(csp) if assignment == {} else assignment
	if all([assignment[key] for key in assignment]): return assignment

	var = select_unassigned_variable(csp)
	for value in csp.domains[var]:
		if [value] not in [assignment[key] for key in csp.constraints[var]]:
			csp.domains[var] = [value]

			if ac3(csp):
				result = backtrack(set_assignment(csp), csp)
				if result: return result
			csp.domains = deepcopy(csp_old.domains)

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
	var = (None, 10) # length that should never exist

	for key in csp.variables:
		length = len(csp.domains[key])

		if length is not 1 and var[1] > length:
			var = (key, length)
	return var[0]
