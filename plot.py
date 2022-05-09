import networkx as nx
import pydot
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt



def plot(creature, neurons):

	e_positive = [(u, v) for (u, v, d) in creature.brain.edges(data=True) if d["weight"] > 0.0]
	e_negative = [(u, v) for (u, v, d) in creature.brain.edges(data=True) if d["weight"] <= 0.0]

	# positions for all nodes - seed for reproducibility
	pos = nx.nx_pydot.graphviz_layout(creature.brain, prog='dot', root='sDet')  

	# nodes
	nx.draw_networkx_nodes(creature.brain, pos, node_size=700)

	# edges
	nx.draw_networkx_edges(
		creature.brain, pos, edgelist=e_positive, width=6, edge_color="tab:green")
	nx.draw_networkx_edges(
	    creature.brain, pos, edgelist=e_negative, width=6, edge_color="tab:red")

	# labels
	nx.draw_networkx_labels(
		creature.brain, pos, font_size=12, font_family="sans-serif")

	ax = plt.gca()
	ax.margins(0.08)
	plt.axis("off")
	plt.tight_layout()
	plt.show()