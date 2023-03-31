from simplequantnetsim.helpers import *
from simplequantnetsim.sim import *
import random
from copy import deepcopy
import matplotlib.pyplot as plt
def MPG_protocol(G,users,timesteps=5000,reps=500):
    #     """
    #     Multipath protocol - Greedy. Protoocol attempts shortest path routing between centre node and each other user seqentially to generate N bell pairs (1 shared between centre and each of N users). The protocol terminates once bell pairs is shared as this is sufficent for generating a GHZ. 
    #     Input Pararmeters:
    #     G         - Networkx graph G(V,E) which defines the topology of the network. see graphs.py for more details
    #     users     - List of nodes in G that must share a GHZ state.  users[0] is the centre of the star which should be calculated before sending to SP_protocol
    #     timesteps - number of timesteps the protocol will run for before terminating without a successful GHZ generation, 
    #     reps      - number of repetions the protocol will run for the imput parameters to generate a dataset.
    #     Outputs: 
    #     rate                   -  entanglement rate (ER) (average G   HZs generated per timeslot)
    #     multipartite_gen_time  -  array (length of reps)  array of timeslots until successful GHZ generated, if no successful GHZ generated value is -1
    #    """
    source_node = users[0]
    destination_nodes = users[1:]
    multipartite_gen_time = -1 * np.ones((reps))
    for i in range(reps):
        reset_graph_state(G)
        t= 0
        while t<timesteps and multipartite_gen_time[i]==-1: # for t timesteps or until success
            t+=1
            run_entanglement_step(G)    
            H = get_entangled_subgraph(G)
            for destination_node in destination_nodes:
                if nx.has_path(H,source_node,destination_node):
                    route = nx.shortest_path(H,source_node,destination_node)
                    #MPG_regraph(route,G,H)
                    for k in range(len(route)-1):
                        H.remove_edge(route[k],route[k+1])
                        edge = G.edges[route[k],route[k+1]]
                        edge['entangled'] = False
                        edge['age'] = 0

                    G.nodes[route[-1]]['entangled'] = True # end node is last value in route?
                    G.nodes[route[-1]]['age'] = 0# use route [0]?
            if all([G.nodes[x]['entangled'] for x in destination_nodes]):
                multipartite_gen_time[i] = t
    rate = multipartite_rate(multipartite_gen_time,timesteps)
    return rate,multipartite_gen_time

def SP_protocol(G,users,timesteps,reps):
#     """
#     Shortest Path protocol taken from [SPsource] The protocol attempts to generate bell pairs between a central node and a set of users.
#     This is done by attmepting entanglement along a set of edge disjoint paths, all connected to the centre node. The protocol 
#     requires a graph with only the edges required for SP routing are present. The protocol terminates once an entanglement is shared between 
#     the centre and all other users
    
    #     Input Pararmeters:
    #     G         - Networkx graph G(V,E) which defines the topology of the network. see graphs.py for more details
    #     users         - List of nodes in G which between which a GHZ should be shared
    #     timesteps - number of timesteps the protocol will run for before terminating without a successful GHZ generation, 
    #     reps      - number of repetions the protocol will run for the imput parameters to generate a dataset.

    #     Outputs: 
    #     rate                   -  entanglement rate (ER)
    #     multipartite_gen_time  -  array (length of reps)  array of timesteps until successful GHZ generated, if no successful GHZ generated value is -1
    #    """
    #G, source_node,destination_nodes = check_graph_input(G,nodes,p,Qc)
    source_node = users[0]
    destination_nodes = users[1:]
    J = get_star(G,users) # double check getting correct data
    print(nx.node_connected_component(J,(2,2)))
    print(nx.edges(J))
    #J, unused1,unused2 = check_graph_input(J,[None,None],p,Qc)
    multipartite_gen_time = -1 * np.ones((reps))
    for i in range(reps):
        reset_graph_state(J)
        t= 0
        while t<timesteps and multipartite_gen_time[i]==-1:
            
            run_entanglement_step(J)
            H = get_entangled_subgraph(J)
            for destination_node in destination_nodes:
                route = get_shortest_path(H,source_node,destination_node)
                if len(route)>0:
                    for k in range(len(route)-1):
                        H.remove_edge(route[k],route[k+1])
                        edge = J.edges[route[k],route[k+1]]
                        edge['entangled'] = False
                        edge['age'] = 0
                        
                    J.nodes[route[-1]]['entangled'] = True # last value in route is destination node
                    J.nodes[route[-1]]['age'] = 0
                    
            if all([J.nodes[x]['entangled'] for x in destination_nodes]):
                multipartite_gen_time[i] = t+1
                
                
            t+=1
    rate = multipartite_rate(multipartite_gen_time,timesteps)
    return rate,multipartite_gen_time







def SP_tree_protocol(G,users,timesteps=1,reps=1):
    #### Terminates once all users are part of same CC. Only difference to MPC is that entanglement is only attempted along shortest tree.
    # Can do better by doing edges independantly?
    J = steiner_tree(G,users,weight='p_edge_log')
    return MPC_protocol(J,users,timesteps=timesteps,reps=reps)






















def SP_protocol1(G,users,replace_node,list_of_newnodes,timesteps,reps):
#     """
#     Shortest Path protocol taken from [SPsource] The protocol attempts to generate bell pairs between a central node and a set of users.
#     This is done by attmepting entanglement along a set of edge disjoint paths, all connected to the centre node. The protocol 
#     requires a graph with only the edges required for SP routing are present. The protocol terminates once an entanglement is shared between 
#     the centre and all other users
    
    #     Input Pararmeters:
    #     G         - Networkx graph G(V,E) which defines the topology of the network. see graphs.py for more details
    #     users         - List of nodes in G which between which a GHZ should be shared
    #     timesteps - number of timesteps the protocol will run for before terminating without a successful GHZ generation, 
    #     reps      - number of repetions the protocol will run for the imput parameters to generate a dataset.

    #     Outputs: 
    #     rate                   -  entanglement rate (ER)
    #     multipartite_gen_time  -  array (length of reps)  array of timesteps until successful GHZ generated, if no successful GHZ generated value is -1
    #    """
    #G, source_node,destination_nodes = check_graph_input(G,nodes,p,Qc)
    
    if replace_node==users[0]:
        center_node_ornot=1
    else:
        center_node_ornot=0

    if replace_node in users:
        in_user=1
        result=get_modifiedcornerJ(7,users,replace_node)
        changedJ=result[0]
        newnew_nodelist=result[1]
        users.remove(replace_node)
        users_1=deepcopy(users)
        
        
    else:
        in_user=0
  
    
    
    
  #  for a in list_of_newnodes:
   #     users.append(a)
 #   J = get_star(G,users) # double check getting correct data
    #J, unused1,unused2 = check_graph_input(J,[None,None],p,Qc)
  #  run_entanglement_step(J)
   # H = get_entangled_subgraph(J)
    multipartite_gen_time = -1 * np.ones((reps))
    for i in range(reps):
        reset_graph_state(changedJ)
        t= 0
        while t<timesteps and multipartite_gen_time[i]==-1:
          t+=1
          if in_user==1 and center_node_ornot==0:
          #  for newnode in list_of_newnodes:
                users_2=deepcopy(users_1)
    
               # users_2.append(newnode)
           #     J = get_star(G,users_2)
                run_entanglement_step(changedJ)
          #  nx.draw(J)

            #plt.show()
                H = get_entangled_subgraph(changedJ)                
     #       J = get_star(G,users)
                
                source_node=users_2[0]
                list_of_results=[]
                destination_nodes=users_2[1:]
              
                for destination_node in destination_nodes:
                    if destination_node in nx.node_connected_component(H,source_node):#
                        list_of_results.append(1)
                    else:
                        list_of_results.append(0)
                failue_value=0
                
                    
                if (failue_value not in list_of_results) and any(cornernode in newnew_nodelist for cornernode in nx.node_connected_component(H,source_node)):
                    multipartite_gen_time[i] = t+1
               
        '''
            else:
                users=deepcopy(users_1)
                users.append(list_of_newnodes[1])
                J = get_star(G,users)
                run_entanglement_step(J)
                H = get_entangled_subgraph(J)
                source_node=users[0]
                destination_nodes=users[1:]
                '''


            
                
                
            
    rate = multipartite_rate(multipartite_gen_time,timesteps)
    return rate,multipartite_gen_time


def SP_protocol2(G,users,replace_node,list_of_newnodes,timesteps,reps):
#     """
#     Shortest Path protocol taken from [SPsource] The protocol attempts to generate bell pairs between a central node and a set of users.
#     This is done by attmepting entanglement along a set of edge disjoint paths, all connected to the centre node. The protocol 
#     requires a graph with only the edges required for SP routing are present. The protocol terminates once an entanglement is shared between 
#     the centre and all other users
    
    #     Input Pararmeters:
    #     G         - Networkx graph G(V,E) which defines the topology of the network. see graphs.py for more details
    #     users         - List of nodes in G which between which a GHZ should be shared
    #     timesteps - number of timesteps the protocol will run for before terminating without a successful GHZ generation, 
    #     reps      - number of repetions the protocol will run for the imput parameters to generate a dataset.

    #     Outputs: 
    #     rate                   -  entanglement rate (ER)
    #     multipartite_gen_time  -  array (length of reps)  array of timesteps until successful GHZ generated, if no successful GHZ generated value is -1
    #    """
    #G, source_node,destination_nodes = check_graph_input(G,nodes,p,Qc)
    
    if replace_node==users[0]:
        center_node_ornot=1
        
        users_3=deepcopy(users[1:])
        result=get_modifiedcentralJ(7,users)
       # print(users)
        modified_J=result[0]
        new_list_of_newnodes=result[1]
    else:
        center_node_ornot=0

    if replace_node in users:
        in_user=1
        
        
        
    else:
        in_user=0
        J=get_star(G,users)
       # print(nx.node_connected_component(J,(2,2)))
    if in_user==1 and center_node_ornot==0:
    
        result1=get_modifiedcornerJ(7,users,replace_node)
        changedJ=result1[0]
        newnew_nodelist=result1[1]
        users.remove(replace_node)
        users_1=deepcopy(users)
        
        
    

    
    
    
    
  #  for a in list_of_newnodes:
   #     users.append(a)
 #   J = get_star(G,users) # double check getting correct data
    #J, unused1,unused2 = check_graph_input(J,[None,None],p,Qc)
  #  run_entanglement_step(J)
   # H = get_entangled_subgraph(J)
    multipartite_gen_time = -1 * np.ones((reps))
    for i in range(reps):
        if in_user==0:

            reset_graph_state(J)
        if center_node_ornot==1:
            reset_graph_state(modified_J)
        if center_node_ornot==0 and in_user==1:
            reset_graph_state(changedJ)
        t= 0
        while t<timesteps and multipartite_gen_time[i]==-1:
          t+=1
          if in_user==1 and center_node_ornot==0:
                
                users_2=deepcopy(users_1)
                
               # users_2.append(newnode)
           #     J = get_star(G,users_2)
                run_entanglement_step(changedJ)
          #  nx.draw(J)

            #plt.show()
                H = get_entangled_subgraph(changedJ)                
     #       J = get_star(G,users)
                
                source_node=users_2[0]
                list_ofresults=[]
                destination_nodes=users_2[1:]
              
                for destination_node in destination_nodes:
                    if destination_node in nx.node_connected_component(H,source_node):#
                        list_ofresults.append(1)
                        
                        
                    else:
                        list_ofresults.append(0)
                failue_value=0
               # print(list_ofresults)
                    
                if (failue_value not in list_ofresults) and any(corner_node in newnew_nodelist for corner_node in nx.node_connected_component(H,source_node)):
                    multipartite_gen_time[i] = t+1
                            
          if in_user==0:
            run_entanglement_step(J)
            H = get_entangled_subgraph(J)
            source_node=users[0]
            destination_nodes=users[1:]
            for destination_node in destination_nodes:
                route = get_shortest_path(H,source_node,destination_node)
                if len(route)>0:
                    for k in range(len(route)-1):
                        H.remove_edge(route[k],route[k+1])
                        edge = J.edges[route[k],route[k+1]]
                        edge['entangled'] = False
                        edge['age'] = 0
                        
                    J.nodes[route[-1]]['entangled'] = True # last value in route is destination node
                    J.nodes[route[-1]]['age'] = 0
                    
            if all([J.nodes[x]['entangled'] for x in destination_nodes]):
                multipartite_gen_time[i] = t+1
          if center_node_ornot==1:
              run_entanglement_step(modified_J)
              H = get_entangled_subgraph(modified_J)
              list_of_results=[]
              for newnew_node in new_list_of_newnodes:
                  if any(cornernode in users_3 for cornernode in nx.node_connected_component(H,newnew_node)):
                       list_of_results.append(1)
                  else:
                      list_of_results.append(0)
              failue_value=0
              if failue_value not in list_of_results:
                  multipartite_gen_time[i]=t+1
              

              
              
              


            
                
                
            
    rate = multipartite_rate(multipartite_gen_time,timesteps)
    return rate,multipartite_gen_time















    





def MPG_protocol1(G,users,replace_node,list_of_newnodes,timesteps,reps):
    #     """
    #     Multipath protocol - Greedy. Protoocol attempts shortest path routing between centre node and each other user seqentially to generate N bell pairs (1 shared between centre and each of N users). The protocol terminates once bell pairs is shared as this is sufficent for generating a GHZ. 

    #     Input Pararmeters:
    #     G         - Networkx graph G(V,E) which defines the topology of the network. see graphs.py for more details
    #     users         - List of nodes in G which between which a GHZ should be shared
    #     timesteps - number of timesteps the protocol will run for before terminating without a successful GHZ generation, 
    #     reps      - number of repetions the protocol will run for the imput parameters to generate a dataset.

    #     Outputs: 
    #     rate                   -  entanglement rate (ER)
    #     multipartite_gen_time  -  array (length of reps)  array of timesteps until successful GHZ generated, if no successful GHZ generated value is -1
    #    """
    #G, source_node,destination_nodes = check_graph_input(G,nodes,p,Qc)
    
    multipartite_gen_time = -1 * np.ones((reps))
    if replace_node in users:
      index=users.index(replace_node)
    for i in range(reps):
        reset_graph_state(G)
        t= 0
      #  print('11111111111111111111111111111111')
        while t<timesteps and multipartite_gen_time[i]==-1:
            
            t+=1
            users=[(2,2),(0,0),(0,4),(4,4),(4,0)]
       #     print(users,'original')
            run_entanglement_step(G)    
            H = get_entangled_subgraph(G)
            connectedcomponents = list(nx.connected_components(H))#get the list of connected nodes
           # print(connectedcomponents)
          #  print(connectedcomponents)
            if replace_node==users[0]:
                centreornot=1 
            else:
                centreornot=0

#to verify if the node to be replaced is a user node
#if it is , check which subnode is in the longest connected components list 
# remove the node from the users list and add the subnode to the user list
            node_to_be_used=[]
            usernodeornot=0
            if replace_node in users:
                usernodeornot=1
                if centreornot==0:
                     users.remove(replace_node)
                
                
                
           

                        
#double checking if the replace node is still in the user list, if yes, remove the node and add a newnode
        #    if replace_node in users:
         #               users.remove(replace_node)
          #              users.insert(index,random.choice(list_of_newnodes))
                        
           
            
           
            
          #  print(source_node,'source')
           # print(destination_nodes,'destination')
       

#check if all the user nodes are connected, if yes , end loop
           
 #           check1=all(item in max(connectedcomponents, key=len) for item in users)
  #          if check1 is True:
                    
 
            if usernodeornot==1:
             for b in range(len(list_of_newnodes)):
                   
                    
                    if list_of_newnodes[b] in max(connectedcomponents, key=len):
                        connected_new_node=list_of_newnodes[b]
                        node_to_be_used.append(connected_new_node)
     #                   print('1')
      #                  print(users)  

          #  print(max(connectedcomponents, key=len))
             if centreornot==0:
              for added_new_node in node_to_be_used:
              
                source_node = users[0]
                destination_nodes = users[1:] 
                destination_nodes.insert(index-1,added_new_node) 
        #      print(destination_nodes)
                H_original = H
              
                for destination_node in destination_nodes:
                   H = H_original
                
                   if nx.has_path(H,source_node,destination_node):
                      #  print('1',destination_node)
                        route = get_shortest_path(H,source_node,destination_node)
           #             print(route,'route')
                        if len(route)>0:
                    #MPG_regraph(route,G,H)
                            for k in range(len(route)-1):
                                H.remove_edge(route[k],route[k+1])
                                edge = G.edges[route[k],route[k+1]]
                                edge['entangled'] = False
                                edge['age'] = 0

                            G.nodes[route[-1]]['entangled'] = True # end node is last value in route?
                            G.nodes[route[-1]]['age'] = 0# use route [0]?
                if all([G.nodes[x]['entangled'] for x in destination_nodes]):
                        multipartite_gen_time[i] = t
               #  connectedcomponents = list(nx.connected_components(H))
              #   print(connectedcomponents)
                        break
           
             else:
                destination_nodes=[(0,0),(0,4),(4,4),(4,0)]
                list_of_subnodes=list_of_newnodes
                for destination_node in destination_nodes:
                    list_of_routes=[] 
                    for sub_node in list_of_subnodes:
                        
                        if nx.has_path(H,sub_node,destination_node):
                      #  print('1',destination_node)
                            route = get_shortest_path(H,sub_node,destination_node)
                            
                            list_of_routes.append(route)
                            
                    if len(list_of_routes)>0:     

                        selected_route=min(list_of_routes, key=len)
                    #    print(selected_route)       
                       # print(route,'route')
                        if len(selected_route)>0:
                    #MPG_regraph(route,G,H)
                                for k in range(len(selected_route)-1):
                                    H.remove_edge(selected_route[k],selected_route[k+1])
                                    edge = G.edges[selected_route[k],selected_route[k+1]]
                                    edge['entangled'] = False
                                    edge['age'] = 0

                                G.nodes[selected_route[-1]]['entangled'] = True # end node is last value in route?
                                G.nodes[selected_route[-1]]['age'] = 0# use route [0]?
                if all([G.nodes[x]['entangled'] for x in destination_nodes]):
                        multipartite_gen_time[i] = t
            else:
               source_node = users[0]
               destination_nodes = users[1:]  
            
               for destination_node in destination_nodes:
                           if nx.has_path(H,source_node,destination_node):
                                   route = nx.shortest_path(H,source_node,destination_node)
                    #MPG_regraph(route,G,H)
                                   for k in range(len(route)-1):
                                      H.remove_edge(route[k],route[k+1])
                                      edge = G.edges[route[k],route[k+1]]
                                      edge['entangled'] = False
                                      edge['age'] = 0

                                   G.nodes[route[-1]]['entangled'] = True # end node is last value in route?
                                   G.nodes[route[-1]]['age'] = 0# use route [0]?
               if all([G.nodes[x]['entangled'] for x in destination_nodes]):
                        multipartite_gen_time[i] = t 
           # print(t)
                        
            
    rate = multipartite_rate(multipartite_gen_time,timesteps)
    return rate,multipartite_gen_time

def MPC_protocol(G,users,timesteps=1500,reps=100):
    #     """
    #     Multipath protocol - Cooperative. Entanglement is attempted along all edges for input graph. If all uers are in the same CC of nodes connected by links, this is sufficent for a GHZ state and protocol is assumed successful

    #     Inputs:
    #     G         - Networkx graph G(V,E) which defines the topology of the network. see graphs.py for more details
    #     users         - List of nodes in G which between which a GHZ should be shared
    #     timesteps - number of timesteps the protocol will run for before terminating without a successful GHZ generation, 
    #     reps      - number of repetions the protocol will run for the imput parameters to generate a dataset.
    
    #     Outputs: 
    #     rate                   -  entanglement rate (ER) of protocol averaged over number of runs, including runs where no GHZ was successfully generated 
    #     multipartite_gen_time  -  array (length of reps)  results ER in GHZ/tslot where tslot is number of timesteps, if no successful GHZ generated value is -1
    #     """
    multipartite_gen_time = -1 * np.ones((reps))
    for i in range(reps):
        reset_graph_state(G)
        t= 0
        while t<timesteps and multipartite_gen_time[i]==-1:
            run_entanglement_step(G)            
            H = get_entangled_subgraph(G)
            source_entangled_graph = nx.node_connected_component(H, users[0])
            if set(users) <=  set(source_entangled_graph): #success, all destination nodes connected
                multipartite_gen_time[i] = t+1
            t+=1
    rate = multipartite_rate(multipartite_gen_time,timesteps)
    return rate,multipartite_gen_time




def MPC_protocol1(G,users,replace_node,list_of_newnodes,timesteps,reps):
    #     """
    #     Multipath protocol - Cooperative. Entanglement is attempted along all edges for input graph. If all uers are in the same CC of nodes connected by links, this is sufficent for a GHZ state and protocol is assumed successful

    #     Inputs:
    #     G         - Networkx graph G(V,E) which defines the topology of the network. see graphs.py for more details
    #     users         - List of nodes in G which between which a GHZ should be shared
    #     timesteps - number of timesteps the protocol will run for before terminating without a successful GHZ generation, 
    #     reps      - number of repetions the protocol will run for the imput parameters to generate a dataset.
    
    #     Outputs: 
    #     rate                   -  entanglement rate (ER) of protocol averaged over number of runs, including runs where no GHZ was successfully generated 
    #     multipartite_gen_time  -  array (length of reps)  results ER in GHZ/tslot where tslot is number of timesteps, if no successful GHZ generated value is -1
    #     """
    multipartite_gen_time = -1 * np.ones((reps))
    users_1=deepcopy(users)
    if replace_node==users[0]:
        center_node_ornot=1
    else: 
        center_node_ornot=0
    for i in range(reps):
        reset_graph_state(G)
        t= 0
        while t<timesteps and multipartite_gen_time[i]==-1:
            users=deepcopy(users_1)
            
            if replace_node not in users:
                
                
                run_entanglement_step(G)            
                H = get_entangled_subgraph(G)
                source_entangled_graph = nx.node_connected_component(H, users[0])
                if set(users) <=  set(source_entangled_graph): #success, all destination nodes connected
                    multipartite_gen_time[i] = t+1
            if replace_node in users and center_node_ornot==0:
                run_entanglement_step(G)            
                H = get_entangled_subgraph(G)
                users.remove(replace_node)
                #for a in list_of_newnodes:
                 #   users.append(a)
                source_entangled_graph = nx.node_connected_component(H, users[0])
                if set(users) <=  set(source_entangled_graph) and any(cornernode in list_of_newnodes for cornernode in source_entangled_graph): #success, all destination nodes connected
                    multipartite_gen_time[i] = t+1
            if center_node_ornot==1:
              run_entanglement_step(G)            
              H = get_entangled_subgraph(G)
              list_of_results=[]
              users.remove(replace_node)
              #print(users)
              for cornernode in users:
                  if any(new_sub_node in list_of_newnodes for new_sub_node in nx.node_connected_component(H,cornernode)):
                       list_of_results.append(1)
                  else:
                      list_of_results.append(0)
              failue_value=0
              #print(list_of_results)
              if failue_value not in list_of_results:
                  multipartite_gen_time[i]=t+1
            t+=1
    rate = multipartite_rate(multipartite_gen_time,timesteps)
    return rate,multipartite_gen_time

