import argparse
import os


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-g', '--genes', 
		metavar='', type=int, nargs='?', const=16, default=16, 
		help='number of genes')
	parser.add_argument(
		'-n', '--neurons', 
		metavar='', type=int, nargs='?', const=4, default=4, 
		help='number of internal neurons')
	parser.add_argument(
		'-c', '--cells',
		metavar='', type=int, nargs='?', const=1, default=50, 
		help='number of cells')
	
	return parser.parse_args()	


def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

