import math
import time


def normalise(polarity, x, x_min=0, x_max=2048):
	x = abs(x) if polarity else -abs(x)
	
	return (x - x_min) / (x_max - x_min)


def activation(x, func, bias=0):
	if func == 'tanh':
		return (math.tanh(x) + bias)
	elif func == 'ReLU':
		return (max(0, x) + bias)


def thue_morse_index(number, base):
    # https://math.stackexchange.com/questions/776219/how-to-generalize-the-thue-morse-sequence-to-more-than-two-symbols
    # https://stackoverflow.com/questions/2267362/how-to-convert-an-integer-to-a-string-in-any-base
    if number == 0:
        return 0
    digits = []
    while number:
        digits.append(int(number % base))
        number //= base
    return sum(digits[::-1]) % base

def nap_duration(timestamp, frame_rate=1):
	nap = ((1000000000 / frame_rate) - (time.time_ns() - timestamp)) / 1000000000
	if nap > 0: 
		time.sleep(nap)







