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

def compatability_distance(genotype_a, genotype_b):
	if genotype_a.fitness > genotype_b:
		dom_parent = genotype_a
		sub_parent = genotype_b
	elif genotype_a.fitness < genotype_b.fitness:
		dom_parent = genotype_b
		sub_parent = genotype_a
	elif genotype_a.fitness == genotype_b.fitness:
		fit_parent = both
	innovation_max = max([connection.innovation_id for connection in dom_parent.connections])



	CD = E + D + avgW

