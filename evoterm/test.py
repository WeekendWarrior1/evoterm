import random
import time
import blessed
import matplotlib.pyplot as plt
import networkx as nx
import calc
import genetics
import soil
import ui
import wild



def let_there_be_life(args):
	term = blessed.Terminal()
	print(term.clear)
	ui.init_ui(args, term)
	neurons = genetics.populate_neurons(args.neurons)
	env_wild = wild.Wild(args, neurons)
	env_soil = soil.Soil(args)
	turn_stack = []
	for e in env_wild.animals:
		turn_stack.append(e)
	for e in env_soil.fungi:
		turn_stack.append(e)
	random.shuffle(turn_stack)
	draw = True
	with term.hidden_cursor():
		t = 0
		while True:
			timestamp = time.time_ns()
			print(term.move_xy(args.environment + 12, 0) + term.white(str(t)))
			print(term.move_xy(args.environment + 12, 1) + term.white('     '))
			print(term.move_xy(args.environment + 12, 1) + term.white(str(len(env_wild.animals))))
			index = calc.thue_morse_index(t, len(turn_stack))
			
			parse_turn(term, draw, env_wild, env_soil, turn_stack, index)
			env_soil.spawn_plant(term, draw)
			env_soil.raise_fertility()

			#calc.nap_duration(timestamp, len(turn_stack))
			#calc.nap_duration(timestamp, 24)
			t += 1
			#if len(env_wild.animals) == 0:
			#	print(term.white())
			#	break

	#plot(env.cells[0], env.cells[0].neurons)
	
def parse_turn(term, draw, wild, soil, turn_stack, index):
	turn = turn_stack[index]
	if turn.type == 'animal':
		turn_animal(term, draw, wild, soil, turn_stack, index, turn_stack[index])
	elif turn.type == 'fungus':
		turn_fungi(term, draw, wild, soil, turn_stack[index])

def turn_animal(term, draw, wild, soil, turn_stack, index, _animal):
	wild.set_wild_data(
		term, draw, _animal.x, _animal.y, None, None, [0, 0, 0], ' ')

	birth, death = _animal.action(term, wild, soil)
	
	if birth == True:
		turn_stack.append(wild.animals[-1])		
	if death == True:
		soil.soil[_animal.x][_animal.y]['detritus'] = 'animal'
		soil.soil[_animal.x][_animal.y]['detritus_energy'] += _animal.energy
		wild.set_wild_data(
			term, draw, _animal.x, _animal.y, None, None, [0, 0, 0], ' ')
		wild.animals.remove(_animal)
		del turn_stack[index]
	elif death == False:
		wild.set_wild_data(
			term, draw, _animal.x, _animal.y, _animal, None, _animal.colour, '@')		

def turn_fungi(term, draw, wild, soil, _fungus):
	
	_fungus.action(wild, soil)
	for i, f in enumerate(soil.fungi):
		for i, m in enumerate(f.mycelium.nodes):
		#if soil.soil[x][y]['occupant']:
			soil.set_soil_data(
				term, draw, f.mycelium.nodes[m]['data'].x, f.mycelium.nodes[m]['data'].y, None, None, f.colour, '%')

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

