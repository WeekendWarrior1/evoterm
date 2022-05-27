from collections import defaultdict
import math
import random
import time


def normalise(polarity, x, x_min=0, x_max=2048):
	x = abs(x) if polarity else -abs(x)
	
	return (x - x_min) / (x_max - x_min)


def activation(x, func, bias=0):
	if func == 'tanh':
		return (math.tanh(x) + bias)
	elif func == 'ReLU':
		return (max(0, x) + bias)


def random_coordinate(habitat, environs_range, start=1,):
		(x, y) = (random.randint(start, environs_range) for _ in range(2))
		if habitat[x][y]['occupant'] != None:
			return random_coordinate(habitat, environs_range)			
		else:	
			return (x, y)


def thue_morse_index(number, base):
    # https://math.stackexchange.com/questions/776219/how-to-generalize-the-thue-morse-sequence-to-more-than-two-symbols
    # https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
    if number == 0:
        return 0
    digits = []
    while number:
        digits.append(int(number % base))
        number //= base
        if number == 1:
        	break
    return sum(digits[::-1]) % base


def nap_duration(timestamp, frame_rate=1):
	nap = ((1000000000 / frame_rate) - (time.time_ns() - timestamp)) / 1000000000
	if nap > 0: 
		time.sleep(nap)

def generate_topology(edges):
	""" copied from:
	https://stackoverflow.com/questions/29320556/finding-longest-path-in-a-graph
	"""
	G = defaultdict(list)
	for (s, t) in edges:
		G[s].append(t)
		G[t].append(s)
	return G

def DFS(G, v, seen=None, path=None):
	""" copied from:
	https://stackoverflow.com/questions/29320556/finding-longest-path-in-a-graph
	"""
	if seen is None: seen = []
	if path is None: path = [v]

	seen.append(v)

	paths = []
	for t in G[v]:
		if t not in seen:
			t_path = path + [t]
			paths.append(tuple(t_path))
			paths.extend(DFS(G, t, seen[:], t_path))
	return paths

