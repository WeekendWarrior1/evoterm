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
		metavar='', type=int, nargs='?', const=4, default=2, 
		help='number of internal neurons')
	parser.add_argument(
		'-c', '--cells',
		metavar='', type=int, nargs='?', const=1, default=100, 
		help='number of cells')
	parser.add_argument(
		'-e', '--environment',
		metavar='', type=int, nargs='?', const=1, default=64,
		help='size of environment')
	
	return parser.parse_args()	


def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

