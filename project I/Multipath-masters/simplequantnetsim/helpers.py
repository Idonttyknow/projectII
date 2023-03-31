import networkx as nx
import numpy as np
import math
import random

import os.path
import datetime
import tqdm as tqdm
import tqdm.notebook as tq

from networkx.algorithms.approximation.steinertree import steiner_tree

current_directory = os.getcwd()
dataset_dir =  os.path.join(current_directory, 'datasets')
if not os.path.exists(dataset_dir):
    os.mkdir(dataset_dir)
    
graphs_dir =  os.path.join(current_directory, 'graphs')
if not os.path.exists(graphs_dir):
    os.mkdir(graphs_dir)
    
# helper functions

def reset_graph_state(G):
    nx.set_edge_attributes(G, False, 'entangled')
    nx.set_node_attributes(G,False, 'entangled')
    nx.set_edge_attributes(G, 0, 'age')
    nx.set_node_attributes(G,0, 'age')
    
def entangled_state_sizes(G):
    return [len(a) for a in sorted(nx.connected_components(G), key = len, reverse=True)]


def get_shortest_path(G,source,destination):
    if nx.has_path(G,source,destination):
        return nx.shortest_path(G,source,destination)
    else:
        return []
    
def update_graph_params(G,p=None,Qc=None):
    
    if Qc is not None:
        nx.set_node_attributes(G, Qc, 'Qc')
        nx.set_edge_attributes(G, Qc, 'Qc')
    if p is not None:
        nx.set_edge_attributes(G, p, 'p_edge')
        nx.set_edge_attributes(G, -np.log(p), 'p_edge_log')

        
def set_p_edge (G,p_const = 0.8, loss_dB = None):
    # loss_dB is attenuation in dB/km
    reset_graph_state(G)
    if loss_dB is None:
        update_graph_params(G,p=p_const)
    else:
        for edge in G.edges:
            length = G.edges[edge]['length'] 
            p_loss = 10** -(loss_dB*length / 10)
            #print(p_loss)
            G.edges[edge]['p_edge'] =p_const * p_loss
            G.edges[edge]['p_edge_log'] =-np.log(p_const * p_loss)
            #print(G.edges[edge]['p_edge'])
        
        
def get_entangled_subgraph(G):
    # Create a subgraph G' of G, G' includes all nodes in G, and all edges with successful entanglement links 
    G_prime = nx.Graph()
    G_prime.add_nodes_from(G)
    eligible_edges = [(from_node,to_node,edge_attributes) for from_node,to_node,edge_attributes in G.edges(data=True) if edge_attributes['entangled']]
    G_prime.add_edges_from(eligible_edges)
    return G_prime

def multipartite_rate(gen_times,max_timesteps):
    y = gen_times[np.where(gen_times >= 0)] 
    fail_count = len(gen_times) - len(y)
    t_total = sum(y)+ fail_count*max_timesteps # sum of successful time periods + sum of failures 
    return len(y)/t_total # successes / total time)


def get_star(G,users): # non-optimal # TDM
    #### get edge disjoint shortest paths from set source (first node in list)
    #### if edge disjoint paths don't exist, allow shared edge use
    source_node = users[0]
    node_list= users[1:]
    # copy G twice H for calculation and J for reduced graph  
    H = G.__class__()
    H.add_nodes_from(G.nodes(data=True))
    H.add_edges_from(G.edges(data=True))
    J = G.__class__()
    J.add_nodes_from(G.nodes(data=True))
    for sink_node in node_list:
        try:
            # get a shortest path in subgraph of unused connections
            paths = [p for p in nx.all_shortest_paths(H,source_node,sink_node)]
            for k in range(len(paths[0])-1):
                H.remove_edge(paths[0][k],paths[0][k+1])
                J.add_edge(paths[0][k],paths[0][k+1])
                data = G.get_edge_data(paths[0][k],paths[0][k+1])  # default edge data is {}
                J[paths[0][k]][paths[0][k+1]].update(data)
        except:
                        # if it fails there was no feasible route, seach in G instead of H
            paths = [p for p in nx.all_shortest_paths(G,source_node,sink_node)] 
            for k in range(len(paths[0])-1):
                J.add_edge(paths[0][k],paths[0][k+1])
                data = G.get_edge_data(paths[0][k],paths[0][k+1]) 
                J[paths[0][k]][paths[0][k+1]].update(data) #?
    
    return J 



def get_star1(G,users,replace_node,list_of_newnodes): # non-optimal # TDM
    #### get edge disjoint shortest paths from set source (first node in list)
    #### if edge disjoint paths don't exist, allow shared edge use
    if replace_node==users[0]:
        centreornot=1 
    else:
        centreornot=0
    if centreornot==0:
        
   
    # copy G twice H for calculation and J for reduced graph  
        H = G.__class__()
        H.add_nodes_from(G.nodes(data=True))
        H.add_edges_from(G.edges(data=True))
        J = G.__class__()
        J.add_nodes_from(G.nodes(data=True))
        for sink_node in node_list:
            try:
            # get a shortest path in subgraph of unused connections
                paths = [p for p in nx.all_shortest_paths(H,source_node,sink_node)]
                for k in range(len(paths[0])-1):
                    H.remove_edge(paths[0][k],paths[0][k+1])
                    J.add_edge(paths[0][k],paths[0][k+1])
                    data = G.get_edge_data(paths[0][k],paths[0][k+1])  # default edge data is {}
                    J[paths[0][k]][paths[0][k+1]].update(data)
            except:
                            # if it fails there was no feasible route, seach in G instead of H
                paths = [p for p in nx.all_shortest_paths(G,source_node,sink_node)] 
                for k in range(len(paths[0])-1):
                    J.add_edge(paths[0][k],paths[0][k+1])
                    data = G.get_edge_data(paths[0][k],paths[0][k+1]) 
                    J[paths[0][k]][paths[0][k+1]].update(data) #?
    
    return J 



def get_node_distance(G,source_node,dest_node,name):
    # if Grid get manhatten distance, else get euclidean distance from "pos" coordinate which is a parameter
    if name == "L1": # manhatten distance (L1)
        (x1,y1)= source_node
        (x2,y2)= dest_node
        dist = abs(x2-x1)+abs(y2-y1)
    elif name == "L2":
        (x1,y1) = G.nodes[source_node]['pos']
        (x2,y2) = G.nodes[dest_node]['pos']
        dist = np.sqrt((x2-x1)**2+(y2-y1)**2)
    else:
        raise ValueError("invalid name input")
    return dist

def set_new_node(node):
    theta = 2 * math.pi * random.random()
    return (node[0] + 1 * math.cos(theta), node[1] + 1 * math.sin(theta))
#remove the original node, add three subnode, return the new graph and list of coordinate of new node
def modify_the_graph(G, node):
    list_of_newnodes=[]
    list_of_neighbors=list(G.neighbors(node))
    G.remove_node(node)
    
    for i in range(len(list_of_neighbors)):
        new_node=set_new_node(list_of_neighbors[i])
        list_of_newnodes.append(new_node)
        G.add_node(new_node)
        G.add_edge(new_node,list_of_neighbors[i])
        nx.set_node_attributes(G, 1, 'Qc')
        nx.set_edge_attributes(G, 1, 'length') #km
        nx.set_edge_attributes(G, 0.45, 'p_edge') # 
        nx.set_edge_attributes(G, 1, 'Qc')
        reset_graph_state(G)
    return G,list_of_newnodes
def get_modifiedcentralJ(edge_node_num,users):
    G=network(edge_node_num,edge_node_num)
    J=get_star(G,users)
    R=modify_the_graph(J,users[0])
    return R
def network(n,m): # function to generate 2d grid networkx graph with needed extra data (length, is entangled and entanglement age)
    G = nx.grid_2d_graph(n, m)  # n times m grid
    nx.set_edge_attributes(G, 1, 'length') #km
    nx.set_edge_attributes(G, 0.45, 'p_edge') # 
    nx.set_edge_attributes(G, 1, 'Qc')
    nx.set_node_attributes(G, 1, 'Qc')
    reset_graph_state(G)
    return G
def get_modifiedcornerJ(edge_node_num,users,replace_node):
    G=network(edge_node_num,edge_node_num)
    J=get_star(G,users)
    R=modify_the_graph(J,replace_node)
    return R