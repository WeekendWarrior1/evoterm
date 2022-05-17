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
		self.cells = self.init_cells(args, neurons)

	def init_cells(self, args, neurons):
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

	def init_env_ui(self):
		def ui_into_coordinates(char, x, y):
			self.coordinates[x][y]['occupied'] = True
			self.coordinates[x][y]['occupant'] = char
			print(term.move_xy(x, y) + term.white(char))

		env_range = range(self.env_size + 2)
		env_edge = [0, self.env_size + 1]

		for x, y in itertools.product(env_range, env_range):
			if x not in env_edge and y in env_edge:
				ui_into_coordinates('-', x, y)
			elif x not in range(1, self.env_size + 1) and y not in env_edge:	
				ui_into_coordinates('|', x, y)
		for x, y in itertools.product(env_edge, env_edge):
			self.coordinates[x][y]['occupied'] = True
			self.coordinates[x][y]['occupant'] = ' '

		for i, e in enumerate(['Time', 'Cells']):
			print(term.move_xy(self.env_size + 2, i) + term.white(f'{e}: '))	

	def random_positions(self):
		def random_coordinates():
			(x, y) = (random.randint(1, self.env_size) for _ in range(2))
			if self.coordinates[x][y]['occupied']:
				return random_coordinates()			
			else:	
				return (x, y)
		
		for cell in self.cells:
			(x, y) = random_coordinates()
			self.coordinates[x][y]['occupied'] = True
			self.coordinates[x][y]['occupant'] = cell
			cell.x = x
			cell.y = y

	def simulate_generation(self):
		with term.hidden_cursor():
			self.init_env_ui()
			self.random_positions()
			t = 0	
			while len(self.cells):	
				timestamp = time.time_ns()
				print(term.move_xy(self.env_size + 8, 0) + term.white(str(t)))
				print(term.move_xy(self.env_size + 8, 1) + term.white(
					str(len(self.cells))))	
				index = calc.thue_morse_index(t, len(self.cells))
				
				self.action_cell(self.cells[index], index)
				self.spawn_food()
				
				calc.nap_duration(timestamp, frame_rate = len(self.cells))
				t += 1

	def spawn_food(self, chance=10):
		if random.randint(0, chance) == 0:
			x, y = (
				random.randint(1, self.env_size), 
				random.randint(1, self.env_size))
			if self.coordinates[x][y]['occupied'] == False:
				if self.coordinates[x][y]['occupant'] == None:
					self.set_coordinate_data(
							x, y, [0, 255, 0],
							False, 'plant', 'Y')
	
	def action_cell(self, cell, index):		
		self.set_coordinate_data(
			cell.x, cell.y, cell.colour,
			occupied = False, occupant = None, char = ' ')
		if cell.fire_neurons(
		self.cells, index, self.env_size, self.coordinates, term):
			self.set_coordinate_data(
				cell.x, cell.y, cell.colour,
				occupied = False, occupant = None, char = ' ')
			del self.cells[index]
		else:
			self.set_coordinate_data(
				cell.x, cell.y, cell.colour, 
				occupied = True, occupant = cell, char = '@')

	def set_coordinate_data(self, x, y, colour, occupied, occupant, char=''):	
		print(
			term.move_xy(x, y) + 
			term.color_rgb(colour[0], colour[1], colour[2]) + 
			char)
		self.coordinates[x][y]['occupied'] = occupied
		self.coordinates[x][y]['occupant'] = occupant

