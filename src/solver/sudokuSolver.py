from flask_restful import Resource
from flask_restful import reqparse

from src.solver.functions import ac3, backtracking_search, generate_constraints, setup

VARS = '-123456789'
ALPHA = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I')

class SudokuSolver(Resource):
	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('sudoku', type=str, required=True)
		args = parser.parse_args()

		if len(args['sudoku']) != 81:
			return {"message": "Incorrect sudoku format."}

		data = []
		i, j = -1, 0
		for value in args['sudoku']:
			if value not in VARS: return {"message": "Unrecognized character: {}.".format(value)}
			index = (j % 9) + 1
			if j % 9 == 0: i += 1

			data.append(('{}{}'.format(ALPHA[i], index), value))

			j += 1

		csp = setup(data)
		consistent = ac3(csp)
		
		if consistent:
			if not any([x for x in csp.variables if len(csp.domains[x]) > 1]):
				return csp.domains
			else:
				result = backtracking_search(csp)
				if result:
					return result

		return {"message": "Not a solvable sudoku problem."}
