import math


def normalise(polarity, x, x_min=0, x_max=2048):
	x = abs(x) if polarity else -abs(x)
	return (x - x_min) / (x_max - x_min)


def activation(x, func, bias=1):
	if func == 'tanh':
		return (math.tanh(x) + bias) / 2
	elif func == 'ReLU':
		return (max(0, x) + bias) / 2