import itertools
import random
import calc
import fungus

class Soil:

	def __init__(self, args):
		self.args = args
		self.soil = self.init_soil()
		self.valid_soil = [(x, y) for x, y in itertools.product(
			range(1, self.args.environment + 1), 
			range(1, self.args.environment + 1))]
		self.fungi = self.init_fungi()

	def init_soil(self):
		soil = {}
		environs_range = range(1, self.args.environment + 1)
		for x in environs_range:
			soil[x] = {}
			for y in environs_range:
				soil[x][y] = {
				'occupant':None,
				'fertility':10,
				'plant':None,
				'plant_energy':10,	
				'dung':None,
				'detritus':None,
				'detritus_energy':0}
		return soil

	def init_fungi(self):
		fungi = []
		for i in range(self.args.fungi):
			(x, y) = calc.random_coordinate(
				self.soil, self.args.environment)
			self.soil[x][y]['occupied'] = True
			self.soil[x][y]['occupant'] = f'{i}{x}{y}'
			fungi.append(fungus.Fungus(x, y))
		return fungi

	def spawn_plant(self, term):
		if not random.randint(0, self.args.environment):
			x, y = calc.random_coordinate(
			self.soil, self.args.environment)

			if self.soil[x][y]['fertility'] >= 10:
				self.soil[x][y]['plant'] = True
				self.soil[x][y]['plant_energy'] = self.soil[x][y]['fertility']
				self.soil[x][y]['fertility'] = 0
				print(
					term.move_xy(x, y) + 
					term.color_rgb(0, 255, 0) + 
					'.,vyVYf4q?P'[self.soil[x][y]['plant_energy'] - 10])

	def raise_fertility(self):
		for x, y in self.valid_soil:
			if self.soil[x][y]['fertility'] < 10:
				self.soil[x][y]['fertility'] += 1