import time
from blessed import Terminal
from itertools import product


term = Terminal()

print(term.clear)

def grid():
	for x, y in product(range(18), range(18)):
		if y in [0, 17] and x not in [0, 17]:
			print(term.home + term.move_xy(x, y) + term.white('-') + '')
		else:
			print(term.home + term.move_xy(0, y) + term.white('|') + '')
			print(term.home + term.move_xy(17, y) + term.white('|') + '')
		

grid()
