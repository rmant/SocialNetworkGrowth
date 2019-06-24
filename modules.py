import networkx as nx
import matplotlib.pyplot as plt
from random import random, sample
import numpy as np
import matplotlib.animation as animation
import pylab

class Node:
    def __init__(self, i, state = 0, infection_rate=0.06, recovery_rate=0.15):
        self.id = i
        self.state = state
        self.ir = infection_rate
        self.rr = recovery_rate
        
    
    @property
    def color(self):
        if self.state == 1:
            return 'red'
        else:
            return 'lightblue'
    
    @property
    def nneighbors(self, G):
        return len(G[self.id])
    
    @property
    def infectedNeighbors(self, G, nodes):
        return len([nbr for nbr in G[self.id] if nodes[nbr].state == 1])
    
    @property
    def healthyNeighbors(self):
        return self.nneighbors - self.infectedNeighbors
        
    def infect(self, Graph, node_list):
        if self.state == 1:
            for nbr in Graph[self.id]:
#                 print(node_list[nbr])
                if node_list[nbr].state == 0 and random()<self.ir:
                    node_list[nbr].state = 1
                    
    def recover(self):
        if self.state ==1:
            if random() < self.rr:
                self.state = 0



def initialize():
#     global pos
    pass

def observe():
#     plt.cla()
    fig = pylab.figure()
    nx.draw(G, pos = pos ,node_color=list(map(lambda x: x.color, nodes)), with_labels=True)
#     im = plt.draw()
#     images.append(fig)
    fig.savefig('fig.png')
    
def update(history, nodes, G):
    infected_count = 0
    for n in nodes:
        n.infect(G, nodes)
        n.recover()
        if n.state == 1:
            infected_count += 1
    history.append(infected_count)
    
    
# this update is used if you only want the number of infected nodes at the end    
def update2(graph, node_list):
    for n in node_list:
        n.infect(graph, node_list)
        n.recover()
    return node_list

def resetNodes(nodes):
    for node in nodes:
        node.state = 0

# Method to run the simulation and get the history to be plotted.
def simulate(G, t, IR, RR, infection_type='random', initial_infected=25, neighbors=5):
    # We create a list of nodes.
    nodes=[]
    for n in G:
        nodes.append(Node(n, infection_rate=IR, recovery_rate=RR))
    # Check wich type of initial infection we have to realize.
    if infection_type == 'random':
        #We do a random infection of intial_infected in our nodes
        infected = sample(range(0,len(nodes)), initial_infected)
        for n in infected:
            nodes[n].state = 1
    elif infection_type == 'popular':
        top = sorted(nx.pagerank(G).items(), key=lambda x: x[1], reverse=True)
        infected = [x[0] for x in top[:initial_infected]]
        for n in infected:
            nodes[n].state = 1
    elif infection_type == 'cluster':
        infected = sample(range(0,len(nodes)), initial_infected//5)
        for n in infected:
            nodes[n].state = 1
            for nbr in np.random.choice(G[n], neighbors):
                nodes[nbr].state = 1
    else:
        print('Not supported parameter infection type.')
        return None  
    
    history = []
    for _ in range(t):
        update(history, nodes, G)

    return history

