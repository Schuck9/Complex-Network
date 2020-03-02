"""
Ultimatum Game in complex network Visualization 
@date: 2020.3.2
@author: Tingyu Mo
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def pq_distribution(self,value_list):
    x_axis = np.arange(0,1.05,1/20) # 21 descrete points,range 0~1,step size 0.05
    y_axis = np.zeros(x_axis.size)
    for v in value_list:
        for i in range(x_axis.size):
            if abs(v-x_axis[i]) < 0.05:
                y_axis[i] += 1
    return y_axis

def viz(RecordName,time_option = "all"):
    Epoch_list = ['1','100','1000','20000']
    result_dir = "./result"
    record_dir = os.path.join(result_dir,record_name)
    checkpoint_list = os.listdir(record_dir)
    parse_str = checkpoint_list[0].split("_")
    del(parse_str[-1]]
    info_str = '_'.join(parse_str)
    y_axis_plist = []
    y_axis_qlist = []
    for Epoch in Epoch_list:
        info_e = info,"_"+Epoch
        Epoch_dir = os.path.join(record_dir,info_e )
        stratagy_path = os.path.join(Epoch_dir,info_e+"_stratagy.csv")
        strategy = pd.read_csv(strategy_path)
        pq_array = strategy.values
        # p = pq_array[0][:]
        # q = pq_array[1][:]
        p = pq_distribution(pq_array[0][:])
        q = pq_distribution(pq_array[1][:])
        y_axis_plist.append(p)
        y_axis_qlist.append(q))

        plt.figure()
    
        plt.plot(x_axis,y_data,label='p')
        for i,Epoch in enumerate(Epoch_list):
            plt.plot(x_axis,y_axis_plist[i],label=str(Epoch) )
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
    







if __name__ == '__main__':

    RecordName ='2020-03-01-23-14-38'   
    time_option = "all"
    viz(RecordName,time_option)