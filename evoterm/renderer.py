import time
import itertools
from blessed import Terminal

term = Terminal()

print(term.clear)


def grid(bound_x, bound_y):
	for x, y in itertools.product(range(18), range(18)):
		if y in [0, 17] and x not in [0, 17]:
			print(term.home + term.move_xy(x, y) + term.white('-') + '')
		elif y in range(1,17) and x in [0, 17]:
			print(term.home + term.move_xy(x, y) + term.white('|') + '')
		
class Environment:
	
	def __init__(self, cells, grid_size):
		self.cells = cells
		self.grid_size = grid_size
		self.grid(self.grid_size+2)

	def grid(self, grid_size):
		for x, y in itertools.product(range(grid_size), range(grid_size)):
			if y in [0, grid_size - 1] and x not in [0, grid_size - 1]:
				print(term.home + term.move_xy(x, y) + term.white('-') + '')
			elif y in range(1,grid_size - 1) and x in [0, grid_size - 1]:
				print(term.home + term.move_xy(x, y) + term.white('|') + '')

	def move_cell(self, pos_x, pos_y, colour=[0, 0, 0], char=''):
		if pos_x < self.grid_size and pos_y < self.grid_size:
			print(term.home + term.move_xy(pos_x+1, pos_y+1) + term.color_rgb(
				colour[0], colour[1], colour[2]) + '@')

	def simulate(self, steps=24):
		
		for step in range(steps):
			self.grid(self.grid_size+2)
			print(term.home + term.move_xy(self.grid_size+2, 0) + term.white(f'Step: {step}') + '')
			for i, cell in self.cells.items():
				print(term.home + term.move_xy(self.grid_size+2, 1) + term.white(f'Cell: {i}') + '')
				cell.step()
				self.move_cell(
					(self.grid_size//2)+cell.pos_x, 
					(self.grid_size//2)+cell.pos_y, 
					cell.colour, '@')
			time.sleep(0.041666666666666664)
			for i, cell in self.cells.items():
				self.move_cell((self.grid_size//2)+cell.pos_x, (self.grid_size//2)+cell.pos_y, cell.colour)

