import time
import matplotlib.pyplot as plt
import networkx as nx
import cell
import cli
import environment
import genetics



def run_environment(args):
	neurons = genetics.populate_neurons(args.neurons)	
	#plot(cells[0], cells[0].neurons)
	env = environment.Environment(args, neurons)
	env.simulate_generation()


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

