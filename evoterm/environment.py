import time
import itertools
import random
from blessed import Terminal
import calc
import cell
import genetics


term = Terminal()
print(term.clear)

		
class Environment:
	
	def __init__(self, args, neurons):
		self.env_size = args.environment
		self.coordinates = self.init_env_coordinates()
		self.cells = self.generate_cells(args, neurons)

	def generate_cells(self, args, neurons):
		cells = []
		for i in range(args.cells):
			cells.append(cell.Cell(genetics.encode_genome(neurons, args.genes), neurons))
		return cells	

	def init_env_coordinates(self):
		coordinates = {}
		for x in range(0, self.env_size + 2):
			coordinates[x] = {}
			for y in range(0, self.env_size + 2):
				coordinates[x][y] = {
				'occupied':False,
				'occupant':None}
		return coordinates

	def simulate_generation(self):
		with term.hidden_cursor():
			self.init_env_ui()
			self.random_positions()
			i = 0	
			while len(self.cells):	
				timestamp = time.time_ns()
				print(term.move_xy(self.env_size + 8, 0) + term.white(str(i)))
				print(term.move_xy(self.env_size + 8, 1) + term.white(str(len(self.cells))))	
				
				index = calc.thue_morse_index(i, len(self.cells))
				self.process_cell(self.cells[index], index)
				
				calc.nap_duration(timestamp, frame_rate = len(self.cells))

				i += 1

	def init_env_ui(self):
		self.draw_env_border()
		self.draw_env_info()

	def draw_env_border(self):
		env_size_range = range(self.env_size + 2)
		env_edge_range = [0, self.env_size + 1]

		for x, y in itertools.product(env_size_range, env_size_range):
			if y in env_edge_range and x not in env_edge_range:
				self.coordinates[x][y]['occupied'] = True
				self.coordinates[x][y]['occupant'] = '-'
				print(term.move_xy(x, y) + term.white('-'))
			elif y not in env_edge_range and x not in range(1, self.env_size + 1):	
				self.coordinates[x][y]['occupied'] = True
				self.coordinates[x][y]['occupant'] = '|'
				print(term.move_xy(x, y) + term.white('|'))
		for x, y in itertools.product([0, self.env_size + 1], [0, self.env_size + 1]):
			self.coordinates[x][y]['occupied'] = True
			self.coordinates[x][y]['occupant'] = ' '

	def draw_env_info(self):
		for i, e in enumerate(['Step', 'Cell']):
			print(term.move_xy(self.env_size + 2, i) + term.white(f'{e}: '))	

	def random_positions(self):
		for cell in self.cells:
			(x, y) = self.random_coordinates()
			self.coordinates[x][y]['occupied'] = True
			self.coordinates[x][y]['occupant'] = cell
			cell.x = x
			cell.y = y

	def random_coordinates(self):
		(x, y) = (random.randint(1, self.env_size) for _ in range(2))
		if self.coordinates[x][y]['occupied']:
			return self.random_coordinates()			
		else:	
			return (x, y)
	
	def process_cell(self, cell, index):		
		self.move_cell(cell, occupied = False, occupant = None, char = ' ')
		if cell.fire_neurons(self.cells, index, self.env_size, self.coordinates):
			self.move_cell(cell, occupied = False, occupant = None, char = ' ')
		else:
			self.move_cell(cell, occupied = True, occupant = cell, char = '@')

	def move_cell(self, cell, occupied, occupant, char=''):	
		print(
			term.move_xy(cell.x, cell.y) + 
			term.color_rgb(cell.colour[0], cell.colour[1], cell.colour[2]) + 
			char)
		self.coordinates[cell.x][cell.y]['occupied'] = occupied
		self.coordinates[cell.x][cell.y]['occupant'] = occupant





	









