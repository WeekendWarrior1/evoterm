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
	
def cell():
	

grid()







"""'
for x, y in product(range(12), range(12)):
	print(term.home + term.move_xy(x, y) + term.black_on_white('#') + '')
	#print(term.black_on_white('#') + '')
	#time.sleep(1)
"""

"""
print(term.home + term.clear + term.move_y(term.height // 2))
print(term.black_on_darkkhaki(term.center('press any key to continue.')))


with term.cbreak(), term.hidden_cursor():
	inp = term.inkey()

print(term.move_down(2) + 'You pressed ' + term.bold(repr(inp)))
"""
