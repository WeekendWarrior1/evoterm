class Env:
	def __init__(self, string_a, string_b):
		self.name = string_a
		self.type = string_b

class Cell:
	def __init__(self, string_a, string_b):
		self.name = string_a
		self.type = string_b

	def print_env(self):
		print(self.name)

new = Env('Garden', Cell('Green', 'Leaf'))
print(new.name)
print(new.type)
print(new.type.print_env())