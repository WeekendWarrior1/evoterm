import time
import itertools
import random
from blessed import Terminal

term = Terminal()



print(term.clear)

		
class Environment:
	
	def __init__(self, cells, env_size=32):
		self.cells = cells
		self.env_size = env_size
		
	def draw_border(self, env_size):
		for x, y in itertools.product(range(env_size), range(env_size)):
			if y in [0, env_size - 1] and x not in [0, env_size - 1]:
				print(term.move_xy(x, y) + term.white('-'))
			elif y not in [0, env_size - 1] and x not in range(1, env_size - 1):
				print(term.move_xy(x, y) + term.white('|'))

	def draw_info_panel(self):
		for i, e in enumerate(['Step', 'Cell']):
			print(term.move_xy(self.env_size + 2, i) + term.white(f'{e}: '))	
		
	def move_cell(self, cell, colour, char=''):
		#pos_x += 1
		#pos_y = (self.env_size // 2) + pos_y + 1

		if cell.pos_x > 0 and cell.pos_x < self.env_size:
			if cell.pos_y > 0 and cell.pos_y < self.env_size:

				print(term.move_xy(cell.pos_x + 1, cell.pos_y + 1) + term.color_rgb(
					colour[0], colour[1], colour[2]) + char)

	def simulate(self, steps=24):
		with term.hidden_cursor():
			self.draw_border(self.env_size + 2)
			self.draw_info_panel()
			for i, cell in self.cells.items():
				cell.pos_x = random.randint(0, self.env_size)
				cell.pos_y = random.randint(0, self.env_size)

			# move this into test.py
			# renderer.py should just be functions for drawing, not sim logic	
			for step in range(steps):	
				print(term.move_xy(self.env_size + 8, 0) + term.white(str(step)))
				for i, cell in self.cells.items():	
					print(term.move_xy(self.env_size + 8, 1) + term.white(str(i)))
					self.move_cell(cell.pos_x, cell.pos_y, cell.colour, ' ')
					cell.step()
					self.move_cell(cell.pos_x, cell.pos_y, cell.colour, '@')
				time.sleep(0.041666666666666664)

