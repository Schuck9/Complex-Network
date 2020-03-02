"""
Ultimatum Game in complex network Visualization 
@date: 2020.3.2
@author: Tingyu Mo
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os


def pq_distribution(value_list):
    x_axis = np.arange(0,1.05,1/20) # 21 descrete points,range 0~1,step size 0.05
    y_axis = np.zeros(x_axis.size)
    for v in value_list:
        for i in range(x_axis.size):
            if abs(v-x_axis[i]) < 0.05:
                y_axis[i] += 1
    return y_axis

def viz(RecordName,time_option = "all"):
    # Epoch_list = ['1','100','1000','20000']
    Epoch_list = ['100','1000','20000']
    result_dir = "./result"
    record_dir = os.path.join(result_dir,RecordName)
    checkpoint_list = os.listdir(record_dir)
    parse_str = checkpoint_list[0].split("_")
    del(parse_str[-1])
    info_str = '_'.join(parse_str)
    save_path =os.path.join(record_dir, info_str+'.jpg')
    y_axis_plist = []
    y_axis_qlist = []
    for Epoch in Epoch_list:
        info_e = info_str+"_"+Epoch
        Epoch_dir = os.path.join(record_dir,info_e )
        strategy_path = os.path.join(Epoch_dir,info_e+"_strategy.csv")
        strategy = pd.read_csv(strategy_path)
        # strategy.reset_index(drop = True)
        pq_array = strategy.values
        # np.delete(pq_array,1,axis=1)
        p = pq_array[0][1:]
        q = pq_array[1][1:]
        # del(p[0])
        # del(q[0])
        p = pq_distribution(p)
        q = pq_distribution(q)
    
        y_axis_plist.append(p/10000)
        y_axis_qlist.append(q/10000)

    plt.figure()
    x_axis = np.arange(0,1.05,1/20)
    # plt.rcParams['font.sans-serif']=['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    # # plt.title("")
    plt.xlabel("p")#x轴p上的名字
    plt.ylabel("D(p)")#y轴上的名字
    plt.plot(x_axis, y_axis_plist[0] ,marker='^',linestyle='-',color='skyblue', label='t = 100')
    plt.plot(x_axis, y_axis_plist[1], marker='s',linestyle='-',color='green', label='t = 1000')
    plt.plot(x_axis, y_axis_plist[2], marker='*',linestyle='-',color='red', label='t = 20000')
    # plt.plot(x_axis, thresholds, color='blue', label='threshold')
    plt.legend(loc = 'upper right') # 显示图例
    plt.savefig(save_path)
    print("Figure has been saved to: ",save_path)
    plt.show()
    

    







if __name__ == '__main__':

    RecordName ='ER/2020-03-02-12-13-08'   
    time_option = "all"
    viz(RecordName,time_option)