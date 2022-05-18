import random
import time
import blessed
import matplotlib.pyplot as plt
import networkx as nx
import animal
import calc
import cli
import wild
import genetics
import soil
import ui



def let_there_be_life(args):
	neurons = genetics.populate_neurons(args.neurons)

	term = blessed.Terminal()
	print(term.clear)
	ui.init_ui(args, term)
	env_wild = wild.Wild(args, neurons)
	env_soil = soil.Soil(args)
	
	turn_stack = []
	for e in env_wild.animals:
		turn_stack.append(e)
	for e in env_soil.fungi:
		turn_stack.append(e)
	random.shuffle(turn_stack)
	with term.hidden_cursor():
		t = 0
		while len(env_wild.animals):
			timestamp = time.time_ns()
			print(term.move_xy(args.environment + 12, 0) + term.white(str(t)))
			print(term.move_xy(args.environment + 12, 1) + term.white(str(len(env_wild.animals))))
			index = calc.thue_morse_index(t, len(turn_stack))
			
			parse_turn(term, env_wild, env_soil, turn_stack, index)
			env_soil.spawn_plant(term)
			#env_soil.raise_fertility()

			#calc.nap_duration(timestamp, len(turn_stack))
			t += 1

	#plot(env.cells[0], env.cells[0].neurons)
	
def parse_turn(term, wild, soil, turn_stack, index):
	turn = turn_stack[index]
	if turn.type == 'animal':
		turn_animal(term, wild, soil, turn_stack, turn_stack[index])
		#wild.animals[turn[2:]].process()
	elif turn.type == 'fungus':
		turn_fungi(wild, soil, turn_stack[index])
		#soil.fungi[turn[2:]].process()

def turn_animal(term, wild, soil, turn_stack, animal):
	wild.set_wild_data(
		term, animal.x, animal.y, None, None, [0, 0, 0], ' ')
	if animal.action(term, wild, soil, turn_stack) == True:
		soil.soil[animal.x][animal.y]['detritus'] = 'animal'
		soil.soil[animal.x][animal.y]['detritus_energy'] += animal.energy
		wild.animals.remove(animal)
	else:
		wild.set_wild_data(
			term, animal.x, animal.y, animal, None, animal.colour, '@')		


def turn_fungi(wild, soil, fungus):
	fungus.action(wild, soil)	





def plot(cell, neurons):
	e_positive = \
	[(u, v) for (u, v, d) in cell.brain.edges(data=True) if d["weight"] > 0.0]
	e_negative = \
	[(u, v) for (u, v, d) in cell.brain.edges(data=True) if d["weight"] <= 0.0]
	
	# positions for all nodes - seed for reproducibility
	pos = nx.spring_layout(cell.brain, seed=7)  
	# nodes
	nx.draw_networkx_nodes(cell.brain, pos, node_size=700)
	# edges
	nx.draw_networkx_edges(
		cell.brain, pos, edgelist=e_positive, width=6, edge_color="tab:green")
	nx.draw_networkx_edges(
	    cell.brain, pos, edgelist=e_negative, width=6, edge_color="tab:red")
	# labels
	nx.draw_networkx_labels(
		cell.brain, pos, font_size=12, font_family="sans-serif")

	ax = plt.gca()
	ax.margins(0.08)
	plt.axis("off")
	plt.tight_layout()
	plt.show()	

