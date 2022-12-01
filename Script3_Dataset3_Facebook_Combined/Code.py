import networkx as nx #For Cnstructing and working on Graphs
from collections import OrderedDict #For Sorting the Dictionaries
import matplotlib.pyplot as plt #For Graph Visualization
import operator #For Itemgetter() Function as we useto get value from a dictionary key
from networkx import common_neighbors
import pandas as pd #For Data Manipulation
import numpy as np #For Data Manipulation

data = open('facebook_combined.txt').readlines()
G = nx.DiGraph()
for row in data:
    nodeStrip = row.split()
    G.add_edges_from([(nodeStrip[0], nodeStrip[1])])
G = G.to_undirected()
G = nx.convert_node_labels_to_integers(G)

def truss_decomposition_nx(G):
    i = 2
    G1 = None
    trns_dict = dict()
    while len(G.edges()) > 0: 
        G = nx.k_truss(G, i)
        if i>2:
            edges = set(list(G1.edges())) - set(list(G.edges()))
            edges = list(edges)
            trns_dict[i-1] = edges
        G1 = G.copy()
        i += 1
    return trns_dict
trussness_dict_algo1 = truss_decomposition_nx(G)
algo1 = open("Algo1_Output.txt", "w")
algo1.write(str(trussness_dict_algo1))
algo1.close()

def get_key(val):
    found = False
    for key, value in trussness_dict_algo1.items():
        if val in value:
            found = True 
            return int(key)
    if found == False:
        return 0
    
def query_processing_using_k_truss(G,k,q):
    if k == 0 or k == 1:
        return 0
    elif k == 2:
        return G.edges()
    visited = []
    k_truss_index = 0   #Initializing the k-truss index to 0
    n_q=list(G.neighbors(q))    #Getting the neighbors of the query node
    Communities = []  #List to store the nodes of the community
    for u in n_q:
        if (get_key((q,u))>=k or get_key((u,q))>=k) and (q,u) not in visited: #If the nodes are k-truss connected
            k_truss_index+=1
            C1=()
            Q=[]
            Q.append((q,u))
            visited.append((q,u))
            while Q != []:
                (x,y)=Q.pop()
                C1=tuple(set(C1 + (x,y)))
                n_x=list(G.neighbors(x))
                n_y=list(G.neighbors(y))
                for z in (list(set(n_x) & set(n_y))):
                    if (get_key((x,z))>=k or get_key((z,x))>=k) and (get_key((y,z))>=k or get_key((z,y))>=k) :
                        if (x,z) not in visited and (z,x) not in visited:
                            Q.append((x,z))
                            visited.append((x,z))
                        if (y,z) not in visited and (z,y) not in visited:
                            Q.append((y,z))
                            visited.append((y,z))
            Communities.append(C1)
    return Communities 
communities_algo2 = query_processing_using_k_truss(G,3,5)
algo2 = open("Algo2_Output.txt", "w")
algo2.write(str(communities_algo2))
algo2.close()

def TCP_Index(G):
    weight={}
    T={}
    S={}
    for x in G.nodes():
        n_x=list(G.neighbors(x))
        Gx=nx.Graph()
        Gx.add_edges_from(G.edges(G.neighbors(x)))
        for edge in Gx.edges():
            y=edge[0]
            z=edge[1]
            temp=[get_key((x,y)),get_key((x,z)),get_key((y,z))]
            weight[(y,z)]=min(temp)
        T[x]=n_x
        kmax=max(weight.values())
        for k in range(2,kmax+1):
            if weight[(y,z)]==k:
                S[x]=(y,z)
            for (y,z) in S.values():
                if y not in T[x] and z not in T[x]:
                    T[(y,z)]=weight[(y,z)]
    return T
trussness_dict_algo3 = TCP_Index(G)
algo3 = open("Algo3_Output.txt", "w")
algo3.write(str(trussness_dict_algo3))
algo3.close()

def Query_Processing_TCP(G,k,q):
    T=trussness_dict_algo3
    visited = []
    l=0
    Communities = []
    n_q=list(G.neighbors(q))
    for u in n_q:
        if (get_key((q,u))>=k or get_key((u,q))>=k) and (q,u) not in visited:
            l+=1
            V={}
            C1=()
            Q=[]
            Q.append((q,u))
            while Q != []:
                (x,y)=Q.pop()
                if x != q:
                    y = x
                    x = q
                if ((x,y)) not in visited:
                    V[tuple([x,y])]=T[x]
                    for V_lst in V.values():
                        for z in V_lst:
                            visited.append((x,z))
                            C1=tuple(set(C1 + (x,z)))
                            if (z,x) not in visited:
                                Q.append((z,x))
            Communities.append(C1)
    return Communities
communities_algo4 = Query_Processing_TCP(G,3,5)
algo4 = open("Algo4_Output.txt", "w")
algo4.write(str(communities_algo4))
algo4.close()
