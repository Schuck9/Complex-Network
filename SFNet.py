#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-04 10:06:14
# @Author  : liulichao (llc@ruc.edu.cn)

import os

import networkx as nx
import matplotlib.pyplot as plt
import random

#总的节点数
node_num = 2000
#初始节点数
m_0 = 5
#每次给定概率分布，该分布期望值为q，也就是平均连接度/2所得值，用于确定每次增加的连接数
p = [0.86, 0.08, 0.06]

#根据概率分布取相应位置数
def random_choice(seq):
	ran = random.random()*sum(seq)
	sumtmp = 0
	N = seq.__len__()
	for i in range(N):
		sumtmp += seq[i]
		if sumtmp > ran:
			a = i
			return a + 1
	return -1

def barabasi_albert_graph(n, m_0):
	# 生成一个包含m个节点的空图 (即BA模型中t=0时的m0个节点) 
	G = nx.empty_graph(m_0)
	
	# 添加其余的 n-m 个节点，第一个节点编号为m（Python的数组编号从0开始）
	source = m_0
	repeated_nodes=[]

	# 初始阶段,连接每一个点
	init_node = list(range(m_0))
	while(len(init_node) > 0):
		edge = random_choice(p)
		targets = []
		while(len(targets) < edge and len(init_node) > 0):
			x = random.choice(init_node)
			targets.append(x)
			init_node.remove(x)

		G.add_edges_from(zip([source] * edge, targets))
		repeated_nodes.extend(targets)
		repeated_nodes.extend([source] * edge)
		source += 1

	
	#主体阶段
	while(source < n):
		# 定义新加入边要连接的边的数量
		edge = random_choice(p)
		targets=set()
		# 按正比于度的概率进行优先连接
		while(len(targets) < edge):
			#按正比于度的概率随机选择一个节点
			x = random.choice(repeated_nodes) 
			#将其添加到目标节点数组targets中
			targets.add(x)

		# 从源节点连接m条边到选定的m个节点targets上（注意targets是上一步生成的）
		# zip函数将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表
		G.add_edges_from(zip([source] * edge, targets)) 
		# 对于每个被选择的节点，将它们加入到repeated_nodes数组中（它们的度增加了1）
		repeated_nodes.extend(targets)
		# 将源点m次加入到repeated_nodes数组中（它的度增加了m）
		repeated_nodes.extend([source] * edge) 
		
		#挑选下一个源点，转到循环开始，直到达到给定的节点数n
		source += 1 
	#返回所得的图G
	return G

# G = barabasi_albert_graph(node_num , m_0)
# G = nx.random_graphs.barabasi_albert_graph(node_num, 2)
G = nx.random_graphs.erdos_renyi_graph(node_num, 4.0/node_num)

degree_total = 0
for x in range(len(G.degree())):
	degree_total = degree_total + G.degree(x)

print('平均连接度为：',degree_total/node_num)
# print(nx.average_neighbor_degree(G))
ps=nx.spring_layout(G)  #布置框架  
nx.draw(G , ps, with_labels=False, node_size=30)  
plt.show()

#返回图中所有节点的度分布序列
degree = nx.degree_histogram(G)
#生成x轴序列，从1到最大度
x = range(len(degree))
#将频次转换为频率，这用到Python的一个小技巧：列表内涵，Python的确很方便：）           
y = [z / float(sum(degree)) for z in degree]
#在双对数坐标轴上绘制度分布曲线
plt.loglog(x, y, color="blue", linewidth=2)
#显示图表       
plt.show()