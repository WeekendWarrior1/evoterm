import argparse
import os


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'-a', '--animals',
		metavar='', type=int, default=100, 
		help='number of animals')
	parser.add_argument(
		'-e', '--environment',
		metavar='', type=int, default=64,
		help='size of environment')
	parser.add_argument(
		'-f', '--fungi', 
		metavar='', type=int, default=5, 
		help='number of fungi')
	parser.add_argument(
		'-g', '--genes', 
		metavar='', type=int, default=16, 
		help='number of genes')
	parser.add_argument(
		'-n', '--neurons', 
		metavar='', type=int, default=2, 
		help='number of internal neurons')
	
	
	return parser.parse_args()	


def clear():
	os.system('cls' if os.name == 'nt' else 'clear')

