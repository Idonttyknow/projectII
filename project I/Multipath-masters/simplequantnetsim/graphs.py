import networkx as nx
import numpy as np

from simplequantnetsim.helpers import *
from networkx.generators import * 


def network(n,m): # function to generate 2d grid networkx graph with needed extra data (length, is entangled and entanglement age)
    G = nx.grid_2d_graph(n, m)  # n times m grid
    nx.set_edge_attributes(G, 1, 'length') #km
    nx.set_edge_attributes(G, 0.45, 'p_edge') # 
    nx.set_edge_attributes(G, 1, 'Qc')
    nx.set_node_attributes(G, 1, 'Qc')
    reset_graph_state(G)
    return G

def fidelity_network(n,m): # function to generate 2d grid networkx graph with needed extra data (length, is entangled and entanglement age)
    network(n,m) # TODO
    nx.set_edge_attributes(G, -1, 'W_init')
    nx.set_edge_attributes(G, -1, 'T_coh')
    nx.set_edge_attributes(G, -1, 'W')
    nx.set_node_attributes(G, -1, 'W')
    nx.set_node_attributes(G, -1, 'T_coh')
    return G


def make_graphs_list():
    G = network(6,6)
    set_p_edge (G,p_const = 0.7, loss_dB = 0.2)
    save_graph(G,"grid_6_6")
    for file in [file for file in os.listdir(graphs_dir) if file.endswith(".txt")]:
        print(os.path.join(graphs_dir, file))
        file_name = file.split("\\")[0]
        G = load_from_file(file =file_name)
        nom = file_name[:-4]
        set_p_edge (G,p_const = 0.7, loss_dB = 0.2)
        nx.set_edge_attributes(G, 1, 'Qc')
        nx.set_node_attributes(G, 1, 'Qc')
        save_graph(G,name = file_name)
        
        
def get_G_list():
    nom_list_smart = ['ARPA','EON','Eurocore','NSFnet','UKnet','USnet','Grid']
    # Create list of graphs G
    G_list,nom_list = [],[]
    for file in os.listdir(graphs_dir):
        if file.endswith(".txt"):
            #print(os.path.join(graphs_dir, file))
            file_name = file.split("\\")[0]
            G = load_from_file(file =file_name)
            G_list.append(G)
            nom = file_name[:-4]
            nom_list.append(nom)
    #         save_graph(G,name = file_name)
            #print(nom)
    G_list.append(load_graph('grid_6_6'))   
    nom_list.append('grid_6_6')
    # zipped = zip(G_list,nom_list_smart,nom_list)
    # t_prime = sorted(zipped, key = lambda t: t[1])
    # x,y,z = zip(*t_prime)
    return G_list,nom_list_smart
