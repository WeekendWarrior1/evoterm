import time
import matplotlib.pyplot as plt
import networkx as nx
import cell
import cli
import genetics


def run(args, duration=100):
	neurons = genetics.populate_neurons(args.neurons)	
	cells = {}
	
	for i in range(args.cells):
		cells[i] = cell.Cell(genetics.encode_genome(neurons, args.genes), neurons)
	
	for i in range(duration):
		cli.clear()
		cells[0].step()
		print(f'Current step : {i}\n')
		if 'aMvX' in cells[0].brain.nodes:
			print(f'Current x    : {cells[0].pos_x}\n')
			print(f'aMvX output  : {cells[0].brain.nodes["aMvX"]["output"]}\n')
		if 'aMvY' in cells[0].brain.nodes:
			print(f'Current y    : {cells[0].pos_y}\n')
			print(f'aMvY output  : {cells[0].brain.nodes["aMvY"]["output"]}\n')
		time.sleep(0.1)


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

