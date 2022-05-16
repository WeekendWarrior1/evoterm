import time
import itertools
import random
from blessed import Terminal
import calc


term = Terminal()
print(term.clear)

		
class Environment:
	
	def __init__(self, env_size):
		self.env_size = env_size
		self.occupied_coordinates = []

	def simulate_generation(self, cells, steps=24):
		with term.hidden_cursor():
			self.init_env_ui()
			self.random_positions(cells)
			i = 0	
			while len(cells):	
				print(term.move_xy(self.env_size + 8, 0) + term.white(str(i)))
				print(term.move_xy(self.env_size + 8, 1) + term.white(str(len(cells))))	
				
				self.process_cell(cells, calc.thue_morse_index(i, len(cells)))

				#time.sleep(0.041666666666666664)
				i += 1

	def init_env_ui(self):
		self.draw_env_border()
		self.draw_env_info()

	def draw_env_border(self):
		env_size_range = range(self.env_size + 2)
		env_edge_range = [0, self.env_size + 1]

		for x, y in itertools.product(env_size_range, env_size_range):
			if y in env_edge_range and x not in env_edge_range:
				print(term.move_xy(x, y) + term.white('-'))
			elif y not in env_edge_range and x not in range(1, self.env_size + 1):
				print(term.move_xy(x, y) + term.white('|'))

	def draw_env_info(self):
		for i, e in enumerate(['Step', 'Cell']):
			print(term.move_xy(self.env_size + 2, i) + term.white(f'{e}: '))	

	def random_positions(self, cells):
		for cell in cells:
			(x, y) = self.random_coordinates()
			cell.pos_x = x
			cell.pos_y = y

	def random_coordinates(self):
		(x, y) = (random.randint(1, self.env_size) for _ in range(2))
		if (x, y) in self.occupied_coordinates:
			return self.random_coordinates()
		else:
			self.occupied_coordinates.append((x, y))
			return (x, y)
	
	def process_cell(self, cells, index):
		self.move_cell(cells[index], ' ')
		self.occupied_coordinates.remove(
			(cells[index].pos_x, cells[index].pos_y))
		cells[index].fire_neurons(self.env_size, self.occupied_coordinates)
		if random.randint(1, 250) == 0:
			del cells[index]
		else: 
			self.move_cell(cells[index], '@')
			self.occupied_coordinates.append(
			(cells[index].pos_x, cells[index].pos_y))

	def move_cell(self, cell, char=''):	
		print(
			term.move_xy(cell.pos_x, cell.pos_y) + 
			term.color_rgb(cell.colour[0], cell.colour[1], cell.colour[2]) + 
			char)







	









