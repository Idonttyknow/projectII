import numpy as np
import networkx as nx
import random
import itertools
from simplequantnetsim.protocols import *
from simplequantnetsim.graphs import network
import math
from simplequantnetsim.helpers import *
from simplequantnetsim.sim import *

import matplotlib.pyplot as plt
import matplotlib.colors as colors
from networkx.drawing.layout import *

#creates a new node in the place of no repeater
#return the coordinate of new nodeA
def set_new_node(node):
    theta = 2 * math.pi * random.random()
    return (node[0] + 1 * math.cos(theta), node[1] + 1 * math.sin(theta))
#remove the original node, add three subnode, return the new graph and list of coordinate of new node
def modify_the_graph(G, node):
    list_of_newnodes=[]
    list_of_neighbors=list(G.neighbors(node))
    for a in list_of_neighbors:
        G.remove_edge(node,a)
    G.remove_node(node)
    
    for i in range(len(list_of_neighbors)):
        new_node=set_new_node(list_of_neighbors[i])
        list_of_newnodes.append(new_node)
        G.add_node(new_node)
        G.add_edge(new_node,list_of_neighbors[i])
        nx.set_node_attributes(G, 1, 'Qc')
        nx.set_edge_attributes(G, 1, 'length') #km
        nx.set_edge_attributes(G, 0.6, 'p_edge') # 
        nx.set_edge_attributes(G, 1, 'Qc')
        reset_graph_state(G)
    return G,list_of_newnodes

#generate the graph a with new subnodes
G=network(3,3)
users=[(1,1),(0,0),(0,2),(2,2),(2,0)]
print(MPG_protocol(G, users))
print(SP_protocol(G,users,5000,500))
replace_node=(0,2)

R=modify_the_graph(G,replace_node)#R is a 2-tuple
a=R[0]#graph stored in a
list_of_newnodes=R[1]
reset_graph_state(a)

print(replace_node)
print('\n',MPG_protocol1(a,users,replace_node,list_of_newnodes,1000,500))
print('\n',SP_protocol1(a,users,replace_node,list_of_newnodes,1000,500))



    
'''


nx.draw(a)

plt.show()



'''