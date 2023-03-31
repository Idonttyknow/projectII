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
'''
#generate the graph a with new subnodes
G=network(5,5)
n=5
pos = dict( (n,n) for n in G.nodes() )
users=[(2,2),(0,0),(0,4),(4,4),(4,0)]
nx.draw(G, pos, font_size=8)



plt.show()
#print('\n',MPG_protocol(G,users))
#print(MPG_protocol(G, users))
replace_node=(1,3)

R=modify_the_graph(G,replace_node)#R is a 2-tuple
a=R[0]#graph stored in a
list_of_newnodes=R[1]
reset_graph_state(a)
#print('\n',MPG_protocol1(a,users,replace_node,list_of_newnodes,5000,500))
n=5
pos = dict( (n,n) for n in a.nodes() )
nx.draw(a, pos, font_size=8)
print(replace_node)


plt.show()
'''
users=[(2,2),(0,0),(0,4),(4,4),(4,0)]
remove_list=[(2,2),(0,0),(0,4),(4,4),(4,0),(1,0),(0,1),(3,0),(4,1),(0,3),(1,4),(3,4),(4,3),(0,2),(2,0),(4,2),(2,4),(1,1),(3,1),(1,3),(3,3)]
result_list=[]

for i in remove_list:
    print(i)
    print(users)
    G=network(5,5)
    replace_node=i
    R=modify_the_graph(G,replace_node)#R is a 2-tuple
    a=R[0]#graph stored in a
    list_of_newnodes=R[1]
    reset_graph_state(a)
    result_list.append(MPG_protocol1(a,users,replace_node,list_of_newnodes,50000,300)[0])
    reset_graph_state(a)
print(result_list)
#print('\n',MPG_protocol1(a,users,replace_node,list_of_newnodes,5000,500))
