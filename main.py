# By: Theodore Tan
#python3

# imports
import sys
from functions import ac_3, alpha, check_solved, open_file, setup

# variables
filename = sys.argv[1] # get the filename from the terminal

csp = setup(open_file(filename)) # setup the csp using the data
check_solved(ac_3(csp), csp) # check if the ac3 algorithm solved the problem
