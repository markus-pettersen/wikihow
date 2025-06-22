import networkx as nx
from itertools import combinations
import numpy as np
from pyvis.network import Network


def create_subgraph(graph, target_node):
	subgraph_nodes = nx.node_connected_component(graph, target_node)
	subgraph = graph.subgraph(subgraph_nodes).copy()
	return subgraph

def get_subgraph_metrics(sub_graph):
	number_of_nodes = sub_graph.number_of_nodes()
	number_of_edges = sub_graph.number_of_edges()
	density = round(nx.density(sub_graph), 2)

	return(number_of_nodes, number_of_edges, density)

def prune_nodes(sub_graph, selected_node):
	
	nodes_to_keep = [n for n in sub_graph.nodes() if sub_graph.nodes[n]["category"] != "Redundant" or n == selected_node]
	pruned_subgraph = sub_graph.subgraph(nodes_to_keep).copy()

	
	return pruned_subgraph

def prune_edges(sub_graph, selected_node, threshold=0.8):
	
	strong_edges = [(u, v, d) for u, v, d in sub_graph.edges(data=True) if d["weight"] >= threshold]
	pruned_subgraph = nx.Graph()
	pruned_subgraph.add_nodes_from(sub_graph.nodes(data=True))
	pruned_subgraph.add_edges_from(strong_edges)

	return pruned_subgraph

def calculate_shortest_paths(sub_graph):
	paths = []
	for node1, node2 in combinations(sub_graph.nodes, 2):
		try:
			path_len = nx.shortest_path_length(sub_graph, source=node1, target=node2)
			paths.append(path_len)
		except nx.NetworkXNoPath:
			continue

	avg_shortest_path = np.mean(paths).round(2)
	return avg_shortest_path

def create_pyvis_graph(sub_graph, filename):

	net = Network(height="400px", width="100%", notebook=False)

	for node, data in sub_graph.nodes(data=True):
		hover_text = (
			f"{data['title']}\nTopic: {data['topic']}\nCategory: {data['category']}\nPopularity: {data['popularity']}"
			)
		sub_graph.nodes[node]['title'] = hover_text

	net.from_nx(sub_graph)	
	net.save_graph(filename)

	with open(filename, "r", encoding="utf-8") as f:
		html_content = f.read()

	return html_content


