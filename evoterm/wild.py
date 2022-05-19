import time
import itertools
import random
import blessed
import calc
import animal
import fungus
import genetics

	
class Wild:
	
	def __init__(self, args, neurons):
		self.args = args
		self.wild = self.init_wild()
		self.valid_wild = [(x, y) for x, y in itertools.product(
			range(1, self.args.environment + 1), 
			range(1, self.args.environment + 1))]
		self.animals = self.spawn_animals(args, neurons)
		self.init_animals()
		
		
	def init_wild(self):
		wild = {}
		for x in range(1, self.args.environment + 1):
			wild[x] = {}
			for y in range(1, self.args.environment + 1):
				wild[x][y] = {
				'occupant':None,
				'effect':None}
		return wild

	def spawn_animals(self, args, neurons):
		animals = []
		for i in range(args.animals):
			(x, y) = calc.random_coordinate(
				self.wild, self.args.environment)
			animals.append(animal.Animal(self.args,
				genetics.encode_genome(neurons, args.genes), neurons, x, y))
		return animals	

	def init_animals(self):
		for _animal in self.animals:
			self.wild[_animal.x][_animal.y]['occupant'] = _animal

	def set_wild_data(self, term, draw, x, y, occupant, effect, colour, char=''):	
		if draw == True:
			print(
				term.move_xy(x, y) + 
				term.color_rgb(colour[0], colour[1], colour[2]) + 
				char)
		self.wild[x][y]['occupant'] = occupant
		self.wild[x][y]['effect'] = effect

