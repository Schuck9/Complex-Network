"""
A simple implementation of Ultimatum Game in complex network
@date: 2020.3.2
@author: Tingyu Mo
"""

import os
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

class UG_Complex_Network():
    def __init__(self,node_num = 10000,network_type = "SF",update_rule ="NS",player_type = "B",avg_degree = 4,check_point = None):
        self.node_num = node_num
        self.avg_degree = avg_degree
        self.network_type = network_type # "SF" or "ER"
        self.player_type = player_type # "A" or "B" "C"
        self.update_rule = update_rule # "SP" or "SP"

        if not os.path.exists("./result"):
            os.mkdir('./result')

        if check_point == None:
            self.dir_str = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
            os.mkdir("./result/{}".format(self.dir_str))
        else:
            self.dir_str = check_point
    
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
            for n in G.nodes():
                if G.degree(n) == 0:
                    while True:
                        nbr = np.random.choice(G.nodes(),size = 1)[0]
                        if nbr != n:
                            break
                    G.add_edge(n, nbr)
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
        A B C ,three types inBdividual
        '''
        if Type == 'B':
            for n in node_list:
                #Type-A player
                strategy = np.random.rand()
                G.nodes[n]['p'] = strategy 
                G.nodes[n]['q'] = 1-strategy
                G.nodes[n]['payoff'] = 0 
        elif Type == 'A':
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
            num_nbrs = G.degree(n)
            if num_nbrs != 0:
                G.nodes[n]['payoff'] /= G.degree(n)
        
    def natural_selection(self,G):
        '''
        each player i in the network selects at random one neighbor j 
        and compares its payoff Πi with that of j
        '''
        cnt = 0
        for n in list(G.nodes()):
            nbrs = list(G.adj[n])
            nbr = np.random.choice(nbrs,size = 1)[0]
            n_payoff = G.nodes[n]['payoff']
            nbr_payoff = G.nodes[nbr]['payoff']
            if nbr_payoff > n_payoff:
                probs_adopt =  (nbr_payoff - n_payoff)/(2*max(G.degree(n),G.degree(nbr)))
                if np.random.rand() < probs_adopt:
                    # n adopts nbr's strategy
                    cnt += 1
                    G.nodes[n]['p'] = G.nodes[nbr]['p']
                    G.nodes[n]['q'] = G.nodes[nbr]['q']
        # print("occur:",cnt)

    def social_penalty(self,G):
        '''
        remove the player with lowest payoff and replace it with random one
        '''
        lowest_n = 0
        for n in G.nodes():
            if G.nodes[n]['payoff'] < G.nodes[lowest_n]['payoff']:
                lowest_n = n

        lowest_cluster = list(G.adj[lowest_n])
        lowest_cluster.append(lowest_n)
        
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
        
    def save(self,G,Epoch):
        #Save Graph
        result_dir = './result/'
        info = "{}_{}_{}_{}".format(self.network_type,self.player_type,self.update_rule,Epoch)
        Epoch_dir = os.path.join(result_dir,self.dir_str,info)
        if not os.path.exists(Epoch_dir):
            os.mkdir(Epoch_dir)
        graph_path = os.path.join(Epoch_dir,info+"_Graph.yaml")
        nx.write_yaml(G,graph_path)
        #Save strategy
        p_vector = self.get_all_values(G,'p')
        q_vector = self.get_all_values(G,'q')
        pq_array = np.vstack((p_vector,q_vector))
        pq_path = os.path.join(Epoch_dir,info+"_strategy.csv")
        pq = pd.DataFrame(data = pq_array)
        pq.to_csv(pq_path)


    def retrain(self,filepath):
        '''
        continue evolution from specific check point
        '''
        print(filepath)
        filepath = os.path.join('./result/',filepath)
        lists = os.listdir(filepath)   
        lists.sort(key=lambda fn: os.path.getmtime(filepath + "/" + fn)) 
        result_dir = os.path.join(filepath, lists[-1])      
        result_list = os.listdir(result_dir)
        result_list.sort()
        parse_str = result_list[0][:-5].split("_")
        self.network_type = parse_str[0]
        self.player_type = parse_str[1]
        self.update_rule = parse_str[2]
        Epoch = int(parse_str[3])
        graph_path = os.path.join(result_dir,result_list[0])
        G = nx.read_yaml(graph_path)
        return G,Epoch+1
        

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
    network_type = "SF" #"SF or ER"
    update_rule ='SP'   #"NS or SP"
    player_type = "A"
    avg_degree = 4
    Epochs = 21000
    check_point = None
    # check_point = '2020-03-01-19-59-07'
    if check_point != None:
        UG = UG_Complex_Network(node_num,network_type,update_rule,player_type,avg_degree,check_point)
        G,Start  = UG.retrain(check_point)
    else:
        Start = 1
        UG = UG_Complex_Network(node_num,network_type,update_rule,player_type,avg_degree)
        #bulids network structure
        G = UG.build_network()
        #initialize the strategy of player in network
        UG.initialize_strategy(G)
    #play game
    for Epoch in range(Start,Epochs+1):
        UG.synchronous_play(G)
        UG.update(G)
        if Epoch % 100 == 0:
            print("Epoch[{}]".format(Epoch))
            UG.save(G,Epoch)
            # UG.viz(G)
            
        