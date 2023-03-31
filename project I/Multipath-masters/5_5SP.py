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


G=network(5,5)
users=[(2,2),(0,0),(0,4),(4,4),(4,0)]
'''
G=network(3,3)
users=[(1,1),(0,0),(0,2),(2,2),(2,0)]
'''


#print('\n',MPG_protocol(G,users))
print(SP_protocol(G, users,5000,500))
replace_node=(0,0)

R=modify_the_graph(G,replace_node)#R is a 2-tuple
a=R[0]#graph stored in a
list_of_newnodes=R[1]
reset_graph_state(a)
#print(SP_protocol(a, users,5000,500))
print('\n',SP_protocol2(a,users,replace_node,list_of_newnodes,1500,100))

print(replace_node)



'''
users=[(2,2),(0,0),(0,4),(4,4),(4,0)]
remove_list=[(2,2),(0,0),(0,4),(4,4),(4,0),(1,0),(0,1),(3,0),(4,1),(0,3),(1,4),(3,4),(4,3),(0,2),(2,0),(4,2),(2,4),(1,1),(3,1),(1,3),(3,3)]
result_list=[]

for i in remove_list:
    print(i)
    
    users=[(2,2),(0,0),(0,4),(4,4),(4,0)]
    
    G=network(5,5)
    replace_node=i
    R=modify_the_graph(G,replace_node)#R is a 2-tuple
    a=R[0]#graph stored in a
    list_of_newnodes=R[1]
    reset_graph_state(a)
    result_list.append(SP_protocol2(a,users,replace_node,list_of_newnodes,5000,500)[0])
    reset_graph_state(a)
print(result_list)
'''