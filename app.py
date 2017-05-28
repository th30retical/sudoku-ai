from flask import Flask
from flask_restful import Resource, Api

from src.solver import sudokuSolver

app = Flask(__name__)
api = Api(app)

api.add_resource(sudokuSolver.SudokuSolver, '/solve')

if __name__ == '__main__':
	app.run()
