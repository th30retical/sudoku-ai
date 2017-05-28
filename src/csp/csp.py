
class CSP():
	"""
    ------------------------------------------------------
    A CSP object that holds the variables, domains and
    constraints
    ------------------------------------------------------
    """
	def __init__(self, variables, domains, constraints):
		self.variables = variables
		self.domains = domains
		self.constraints = constraints
