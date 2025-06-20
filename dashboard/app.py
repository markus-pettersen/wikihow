import streamlit as st
import pandas as pd
import numpy as np
import pickle
import networkx as nx
from streamlit.components.v1 import html
from itertools import combinations
from graph_utils import create_subgraph, create_pyvis_graph, get_subgraph_metrics, prune_nodes, prune_edges

@st.cache_data
def load_data():
	df = pd.read_csv("../data/final/completed_articles.csv")
	with open("../data/models/full_graph.gpickle", "rb") as f:
		network_graph = pickle.load(f)
	return df, network_graph

df, G = load_data()

df["Popularity"] = pd.qcut(df["Views"], 4, labels=["Low", "Medium", "High", "Very High"])

filtered_df = df.copy()

edges_removed = False
nodes_removed = False

# Sidebar

# filter
st.sidebar.header("Filters")


topic_options = ["All"] + sorted(list(df["Topic"].unique()))

popularity_order = ["Low", "Medium", "High", "Very High"]

popularity_filtered = [p for p in popularity_order if p in df["Popularity"].unique()]
popularity_options = ["All"] + popularity_filtered

selected_topic = st.sidebar.selectbox("Select Topic", topic_options)
selected_popularity = st.sidebar.selectbox("Select Popularity", popularity_options)


if selected_topic != "All":
	filtered_df = filtered_df[filtered_df["Topic"] == selected_topic]


if selected_popularity != "All":
	filtered_df = filtered_df[filtered_df["Popularity"] == selected_popularity]

st.sidebar.write(f"{len(filtered_df)} articles found.")

st.sidebar.header("Select")
title_id_map = dict(zip(filtered_df["Title"], filtered_df["Article_Id"]))
select_article = st.sidebar.selectbox("Select article", filtered_df["Title"])

st.sidebar.header("Navigation")
page = st.sidebar.radio("Choose section", ["Article Information", "View Subgraph"])

selected_node = title_id_map[select_article]
selected_row = filtered_df[filtered_df["Article_Id"] == selected_node].iloc[0]


subgraph = create_subgraph(G, selected_node)
subgraph_nodes, subgraph_edges, subgraph_density = get_subgraph_metrics(subgraph)

if subgraph_edges > 50 and subgraph_density > 0.5:
	subgraph = prune_edges(subgraph, selected_node)
	edges_removed = True
	

elif subgraph_edges > 50:
	subgraph = prune_nodes(subgraph, selected_node)
	nodes_removed = True


for node in subgraph.nodes:
	if node == selected_node:	 
		subgraph.nodes[node]["color"] = "#FFD700"
		subgraph.nodes[node]["borderWidth"] = 3
		subgraph.nodes[node]["shape"] = "star"
		subgraph.nodes[node]["size"] = 30

subgraph_degree = nx.degree_centrality(subgraph)
local_node_degree = subgraph_degree[selected_node]
subgraph_betweenness = nx.betweenness_centrality(subgraph)
local_node_betweenness = subgraph_betweenness[selected_node]

# shortest path
paths = []
for a1, a2 in combinations(subgraph.nodes, 2):

    try:
        path_len = nx.shortest_path_length(subgraph, source=a1, target=a2)
        paths.append(path_len)
    except nx.NetworkXNoPath:
        continue  # skip pairs not connected

avg_shortest_path = np.mean(paths).round(2)

nodes_in_graph = subgraph.nodes()

# ==== Main === 
st.header("Article Network Dashboard")


if page == "Article Information":

	art_col1, art_col2 = st.columns(2)

	st.subheader(selected_row["Title"])
	with art_col1:
		st.markdown(f'**Topic**: {selected_row["Topic"]}')
		st.markdown(f'**Article category**: {selected_row["Category"]}')
		st.markdown(f'**Popularity**: {selected_row["Popularity"]}')
	with art_col2:
		st.markdown(f'**Neighbours**: {selected_row["Neighbours"]}')
		st.markdown(f'**Normalized degree centrality**: {round(selected_row["Degree_norm"], 2)}')
		st.markdown(f'**Normalized betweenness centrality**: {round(selected_row["Betweenness_norm"], 2)}')
	st.write(selected_row["Intro"])

	reveal_button = st.toggle(label="Show full article")
	if reveal_button:
		st.write(selected_row["Article Content"])
		
# Graph
elif page == "View Subgraph":
	if edges_removed:
		st.write("For technical reasons, edges below a similarity threshold have been removed. Isolated nodes are part of the larger subgraph, \
			and included for completeness")
	elif nodes_removed:
		st.write("For technical reasons, redundant nodes have been removed.")
	html_content = create_pyvis_graph(subgraph, "graph.html")
	html(html_content, height=400, width=600)

	graph_col1, graph_col2 = st.columns(2)
	with graph_col1:
		st.subheader("Subgraph metrics")
		st.metric(value=subgraph_nodes, label="Nodes")
		st.metric(value=subgraph_edges, label="Edges")
		st.metric(value=subgraph_density, label="Density")
		
	with graph_col2:
		st.subheader("Centrality (target node)")
		st.metric(value=round(local_node_degree, 2), label="Local degree centrality")
		st.metric(value=round(local_node_betweenness, 2), label="Local betweenness centrality")  
		st.metric(value=avg_shortest_path, label="Average shortest path (subgraph)")
			
elif page == "About Project":
	pass