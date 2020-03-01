"""
A simple implementation of Ultimatum Game in complex network
@date: 2020.2.29
@author: Tingyu Mo
"""

import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class UG_Complex_Network():
    def __init__(self,node_num = 10000,network_type = "SF",update_rule ="NS",player_type = "B",avg_degree = 4):
        self.node_num = node_num
        self.avg_degree = avg_degree
        self.network_type = network_type # "SF" or "ER"
        self.player_type = player_type # "A" or "B" "C"
        self.update_rule = update_rule # "NS" or "SP"

    
    def build_network(self,network_type = None):
        '''
        building network
        '''
        print("Building network!")

        if network_type == None:
            network_type = self.network_type
        
        if network_type == "SF":
            G = nx.random_graphs.barabasi_albert_graph(self.node_num, int(self.avg_degree/2))
        elif network_type == "ER":
            G = nx.random_graphs.erdos_renyi_graph(self.node_num, self.avg_degree/self.node_num)
        elif "other":
            pass      

        print("平均连接度为: ",self.avg_degree_caculate(G))
        return G

    def initialize_strategy(self,G):
        '''
        initialize every node's strategy
        '''
        self.strategy_asigned(G,list(G.nodes()),Type = self.player_type)
        

    def strategy_asigned(self,G,node_list,Type = 'B'):
        '''
        A B C ,three types individual
        '''
        if Type == 'A':
            for n in node_list:
                #Type-A player
                strategy = np.random.rand()
                G.nodes[n]['p'] = strategy 
                G.nodes[n]['q'] = 1-strategy
                G.nodes[n]['payoff'] = 0 

        elif Type == 'B':
            for n in node_list:
                #Type-A player
                strategy = np.random.rand()
                G.nodes[n]['p'] = strategy 
                G.nodes[n]['q'] = strategy
                G.nodes[n]['payoff'] = 0 
        elif Type == 'C':
            for n in node_list:
                #Type-A player
                G.nodes[n]['p'] = np.random.rand()
                G.nodes[n]['q'] = np.random.rand()
                G.nodes[n]['payoff'] = 0 

    def synchronous_play(self,G):
        '''
        using synchronous method to play ultimatum game 
        and update graph every generation
        '''
        for n, nbrs in G.adjacency():
            for nbr, _ in nbrs.items():
                # proposer = n ,responder = nbr
                offer = G.nodes[n]['p']
                demand = G.nodes[nbr]['q']
                if offer > demand:
                    G.nodes[n]['payoff'] += 1-offer
                    # G.nodes[nbr]['payoff'] += offer

                # proposer = nbr ,responder = n
                offer = G.nodes[nbr]['p']
                demand = G.nodes[n]['q']
                if offer > demand:
                    # G.node[nbr]['payoff'] += 1-offer
                    G.nodes[n]['payoff'] += offer
            G.nodes[n]['payoff'] /= G.degree(n)
        
    def natural_selection(self,G):
        '''
        each player i in the network selects at random one neighbor j 
        and compares its payoff Πi with that of j
        '''
        for n in list(G.nodes()):
            nbrs = list(G.adj[n])
            nbr = np.random.choice(nbrs,size = 1)[0]
            n_payoff = G.nodes[n]['payoff']
            nbr_payoff = G.nodes[nbr]['payoff']
            if nbr_payoff > n_payoff:
                probs_adopt =  (nbr_payoff - n_payoff)/(2*max(G.degree(n),G.degree(nbr)))
                if np.random.rand() < probs_adopt:
                    # n adopts nbr's strategy
                    G.nodes[n]['p'] = G.nodes[nbr]['p']
                    G.nodes[n]['q'] = G.nodes[nbr]['q']

    def social_penalty(self,G):
        '''
        remove the player with lowest payoff and replace it with random one
        '''
        lowest_n = 0
        for n in G.nodes():
            if G.nodes[n]['payoff'] < G.nodes[lowest_n]['payoff']:
                lowest_n = n

        lowest_cluster = list(G.adj[lowest_n]).append(lowest_n)
        
        self.strategy_asigned(G,lowest_cluster,Type = self.player_type)
        # for n in lowest_cluster:
        #     #Type-A player
        #     strategy = np.random.rand()
        #     G.nodes[n]['p'] = strategy 
        #     G.nodes[n]['q'] = strategy
        #     G.nodes[n]['payoff'] = 0 


    def update(self,G):
        '''
        natural seletion an social penalty
        '''
        if self.update_rule == "NS":
            self.natural_selection(G)
        elif self.update_rule == "SP":
            self.social_penalty(G)

    def viz(self,G,x_data = None,y_data = None):
        '''
        Visualize  p distribution and q distribution
        '''
        p_distribution = self.pq_distribution(G,'p')
        # q_distribution = self.pq_distribution(G,'q')
        
        x_data,y_data = p_distribution
        plt.figure()
        plt.plot(x_data,y_data,label='p')
        # plt.plot(x_data,y_data,color='red',label=)
        plt.rcParams['font.sans-serif']=['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # plt.title("")
        # ax_label = ['0',' ','1/6',' ','1/3',' ','1/2',' ','2/3',' ','5/6',' ','1']
        # plt.xticks(x_data,ax_label,fontsize=16)
        # plt.yticks(,ax_label,fontsize=16)
        plt.xlabel("p")#x轴p上的名字
        plt.ylabel("D(p)")#y轴上的名字
        plt.legend(loc = 'upper right')
        plt.show()
        

    def get_all_values(self,G,attr_name):
        '''
        get specific attribute values of all nodes
        '''
        value_dict = nx.get_node_attributes(G,attr_name)
        value_list = list(value_dict.values())
        return value_list

    def pq_distribution(self,G,attr_name):

        x_axis = np.arange(0,1.05,1/20) # 21 descrete points,range 0~1,step size 0.05
        y_axis = np.zeros(x_axis.size)
        value_list = self.get_all_values(G,attr_name)
        for v in value_list:
            for i in range(x_axis.size):
                if abs(v-x_axis[i]) < 0.05:
                    y_axis[i] += 1
        
        return (x_axis,y_axis)


        
    def avg_degree_caculate(self,G):
        '''
        caculate average degree of graph
        '''
        degree_total = 0
        for x in range(len(G.degree())):
            degree_total = degree_total + G.degree(x)
        return degree_total/self.node_num

        
if __name__ == '__main__':

    node_num = 10000
    network_type = "SF"
    update_rule ='NS'
    player_type = "B"
    avg_degree = 4
    UG = UG_Complex_Network(node_num,network_type,update_rule,player_type,avg_degree)
    #bulids network structure
    G = UG.build_network()
    #initialize the strategy of player in network
    UG.initialize_strategy(G)
    #play game
    Start = 1
    Epochs = Epochs = pow(10,6)
    for Epoch in range(Start,Epochs+1):
        UG.synchronous_play(G)
        UG.update(G)
        if Epoch % 500 == 0:
            # UG.Save()
            UG.viz(G)
            print("Running!")
        