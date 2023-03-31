'''

replace_node=(1,1)
users=[(0,0),(1,1),(0,2),(2,0),(2,2)]
list_of_newnodes=[(0.4093655442023737, 0.08762954277338941), (0.02121207319084084, 2.2048760462636574), (1.9338514286807544, 1.9978097847347573), (1.4829848569707995, -0.8756287043815412)]
connectedcomponents=[{(0, 1), (0.4093655442023737, 0.08762954277338941), (0.02121207319084084, 2.2048760462636574), (1, 2), (0, 0), (0, 2)}, {(1, 0), (2, 0), (2, 1), (1.9338514286807544, 1.9978097847347573)}, {(2, 2)}, {(1.4829848569707995, -0.8756287043815412)},{(0, 0), (0, 2), (2, 0), (2, 2), (0.4093655442023737, 0.08762954277338941)}]
if replace_node in users:
                for i in range(len(list_of_newnodes)):
                    print(i)
                    if list_of_newnodes[i] in max(connectedcomponents, key=len):
                        connected_new_node=list_of_newnodes[i]
                        users.remove(replace_node)
                        users.append(connected_new_node)
                        print(connected_new_node)
                        break
                
print(users)
for c in range(len(connectedcomponents)): 
                check1=all(item in connectedcomponents[c] for item in users)
                print(check1)

values = [{'a','a'}, {'a','b','b'}, {'a','b','b','a'}, {'a','b','c','a'}]
set={1,3,4,6,7,8,9,0}
print(len(set))
print(max(values, key=len))

a=[{1,2,3,4,5},{100,10310}]
b=1
if b in a:
  print('1')
else:
  print('23')

  
L = [{'G'}, {'D'}, {'B','C'}]
print(any([ 'C' in i for i in L]))
'''
import networkx as nx
import numpy as np


import os.path
import datetime
import tqdm as tqdm
import tqdm.notebook as tq
def reset_graph_state(G):
    nx.set_edge_attributes(G, False, 'entangled')
    nx.set_node_attributes(G,False, 'entangled')
    nx.set_edge_attributes(G, 0, 'age')
    nx.set_node_attributes(G,0, 'age')
def network(n,m): # function to generate 2d grid networkx graph with needed extra data (length, is entangled and entanglement age)
    G = nx.grid_2d_graph(n, m)  # n times m grid
    nx.set_edge_attributes(G, 1, 'length') #km
    nx.set_edge_attributes(G, 0.5, 'p_edge') # 
    nx.set_edge_attributes(G, 1, 'Qc')
    nx.set_node_attributes(G, 1, 'Qc')
    reset_graph_state(G)
    return G
def get_shortest_path(G,source,destination):
    if nx.has_path(G,source,destination):
        return nx.shortest_path(G,source,destination)
    else:
        return []
def run_entanglement_step(G):
    r_list = np.random.rand(len(G.edges()))
    for edge,r in zip(G.edges().values(),r_list):
        if edge['entangled']: #  if entangled edge exists inc age
            edge['age'] +=1
            
            if edge['age'] >= edge["Qc"]: # If the edge is now too old then discard it - only required for entangled edges
                edge['entangled'] = False 
                edge['age'] = 0
                  

        if not edge['entangled'] and edge['p_edge'] > r: # greater is correct (hint p_edge = 0, rand =  0) and (hint p_edge = 1, rand =  0.999...) 
            edge['entangled'] = True     
            edge['age'] = 0
def get_entangled_subgraph(G):
    # Create a subgraph G' of G, G' includes all nodes in G, and all edges with successful entanglement links 
    G_prime = nx.Graph()
    G_prime.add_nodes_from(G)
    eligible_edges = [(from_node,to_node,edge_attributes) for from_node,to_node,edge_attributes in G.edges(data=True) if edge_attributes['entangled']]
    G_prime.add_edges_from(eligible_edges)
    return G_prime
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from networkx.drawing.layout import *

G = nx.grid_2d_graph(9,9)  # 4x4 grid
n=9
pos = dict( (n,n) for n in G.nodes() )
# Create a 2x2 subplot

for a in range(9):
    for b in range(9):
        name=('9-9'+'-'+str(a)+'-'+str(b))
        nx.draw(G, pos, font_size=8)
        nx.draw_networkx_nodes(G, pos, nodelist=[(a,b)], node_color="tab:red")
        
        plt.savefig(str((name))+'.png')



'''

G = nx.grid_2d_graph(5,5)  # 4x4 grid
n=5
pos = dict( (n,n) for n in G.nodes() )
# Create a 2x2 subplot
a=3
b=2
name=('5-5'+'-'+str(a)+'-'+str(b))
nx.draw(G, pos, font_size=8)
nx.draw_networkx_nodes(G, pos, nodelist=[(a,b)], node_color="tab:red")
        
plt.savefig(str((name))+'.png')


'''

'''


users=[(1,1),(0,0),(0,2),(2,2),(2,0)]
source_node = users[0]
destination_nodes = users[1:] 
G=network(3,3)
replace_node=(0,2)
index=users.index(replace_node)
run_entanglement_step(G)
H = get_entangled_subgraph(G)
node_to_be_used=[(-0.38672169545619695, 0.07780352946702052),(0.21944110632337133, 1.3749177546095894)]
for added_new_node in node_to_be_used:
              users.insert(index,added_new_node) 
           
              source_node = users[0]
              destination_nodes = users[1:] 
              for destination_node in destination_nodes:
                if nx.has_path(H,source_node,destination_node):
                      #  print('1',destination_node)
                        route = get_shortest_path(H,source_node,destination_node)
                        print(route,'route')
                        if len(route)>0:
                    #MPG_regraph(route,G,H)
                            for k in range(len(route)-1):
                                H.remove_edge(route[k],route[k+1])
                                edge = G.edges[route[k],route[k+1]]
                                edge['entangled'] = False
                                edge['age'] = 0

                            G.nodes[route[-1]]['entangled'] = True # end node is last value in route?
                            G.nodes[route[-1]]['age'] = 0# use route [0]?

               #  connectedcomponents = list(nx.connected_components(H))
              #   print(connectedcomponents)
  '''               