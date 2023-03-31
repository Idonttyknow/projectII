from simplequantnetsim.helpers import entangled_state_sizes, get_entangled_subgraph
import numpy as np

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

   
    for node in G.nodes().values():

        if node['entangled']:
            node['age'] +=1

            if node['age'] >= node["Qc"]:
                node['entangled'] = False
                edge['age'] = 0

            
def run_sim(G,reps = 1, timesteps = 1):
    sub_graph_sizes = []
    for i in range(reps):
        for t in range(timesteps):
            run_entanglement_step(G) # Edge entanglment generation             
        H = get_entangled_subgraph(G)
        sub_graph_sizes.append(entangled_state_sizes(H))
    return G,H,sub_graph_sizes 
