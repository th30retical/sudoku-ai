import os

from flask import Flask
from flask_restful import Resource, Api

from src.solver import sudokuSolver

app = Flask(__name__)
api = Api(app)

api.add_resource(sudokuSolver.SudokuSolver, '/solve')

if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
