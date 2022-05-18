import itertools
import random
import networkx as nx


class Fungus:
	
	def __init__(self, x, y):
		self.type = 'fungus'
		self.energy = 0
		self.x = x
		self.y = y
		self.mycelium = nx.DiGraph()
		self.mycelium.add_node(f'{self.x}{self.y}', data = Mycelium(self.x, self.y))
		self.spores = []

	def action(self, wild, soil):
		for node in self.mycelium.nodes:
			self.mycelium.nodes[node]['data'].action(self, wild, soil)
		for i, spore in enumerate(self.spores):
			self.mycelium.add_edge(spore[0], spore[1])
			self.mycelium.nodes[spore[1]]['data'] = Mycelium(spore[2], spore[3])
			soil.soil[spore[2]][spore[3]]['occupant'] == spore[1]
			soil.soil[spore[2]][spore[3]]['dung'] = None
			#print('bloom!')
		self.spores = []

		
class Mycelium:

	def __init__(self, x, y):
		self.energy = 0
		self.x = x
		self.y = y
		self.soil_range = []

	def get_soil_range(self, soil, soil_range):
		for x, y in itertools.product([-1, 1], [-1, 1]):
			if (self.x + x, self.y + y) in soil.valid_soil:
				soil_range.append((self.x + x, self.y + y))
		return soil_range

	def action(self, fungus, wild, soil):
		if len(self.soil_range) == 0:
			self.soil_range = self.get_soil_range(soil, self.soil_range)
		
		self.sense_soil(fungus, wild, soil)
		#self.fertilise_soil(soil)
		if self.energy >= 1:
			fungus.energy += self.energy
			self.energy = 0

	def sense_soil(self, fungus, wild, soil):
		for x, y in self.soil_range:
			if soil.soil[x][y]['detritus'] == 'animal':
				self.decompose(soil.soil[x][y])
			if soil.soil[x][y]['dung'] == True:
				if soil.soil[x][y]['occupant'] == None:
					if self.energy >= 10 and soil.soil[x][y]['occupant'] == None:
						self.reproduce(fungus, x, y)
					elif (self.energy + fungus.energy) >= 10:
						while self.energy < 10:
							self.energy += 1
							fungus.energy -= 1
						self.reproduce(fungus, x, y)

	def decompose(self, soil_patch):
		self.energy += soil_patch['detritus_energy']
		soil_patch['detritus_energy'] = 0
		soil_patch['detritus'] = False

	def reproduce(self, fungus, x, y):
		fungus.spores.append([
			f'{self.x}{self.y}', 
			f'{x}{y}', x, y])	
		self.energy -= 10

	def fertilise_soil(self, soil):
		for x, y in self.soil_range:
			if self.energy > 0:
				if soil.soil[x][y]['fertility'] < 20:
					soil.soil[x][y]['fertility'] += 1
					self.energy -= 1
	