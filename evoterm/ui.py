import itertools
import blessed

def init_ui(args, term):
		horizontal = [range(0, args.environment + 2), [0, args.environment + 1]]
		vertical = [[0, args.environment + 1], range(1, args.environment + 2)] 

		for x, y in itertools.product(horizontal[0], horizontal[1]):
			print(term.move_xy(x, y) + term.white('+'))
		for x, y in itertools.product(vertical[0], vertical[1]):
			print(term.move_xy(x, y) + term.white('+'))

		for i, e in enumerate(['Time', 'Cells']):
			print(term.move_xy(args.environment + 3, i) + term.white(f'{e}: '))