import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.colors as colors

import json
from networkx.readwrite import json_graph

def save_graph(G,name="tree"):
    with open('graphs//'+name+'.json', 'w') as outfile1:
        outfile1.write(json.dumps(json_graph.node_link_data(G)))
        
def load_graph(filename):
    with open('graphs//'+filename+'.json', 'r') as f:
        js_graph = json.loads(f.read())
    return json_graph.node_link_graph(js_graph)
#json_graph.node_link_data(G)

def plot_fig(G,destination_nodes = [],savename=""):
    plt.figure(figsize=(8,8))
    color_state_map = {1: 'green', 0: 'lightgrey'}
    [color_state_map[node[0] in destination_nodes] for node in G.nodes(data=True)]
    pos = {(x,y):(y,-x) for x,y in G.nodes()}
    nx.draw(G, pos=pos, 
            edge_color="blue",
            style='--',
            node_color= [color_state_map[node[0] in destination_nodes] for node in G.nodes(data=True)], 
            with_labels=False,
            width = 5,
            node_size=1600)
    if savename=="":
        plt.show()
    else:
        plt.savefig(savename+".png")
        
