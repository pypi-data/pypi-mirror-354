# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 15:05:56 2025

@author: admin
"""

from time import time
from math import exp, sqrt ,log 
from random import gauss,seed

import matplotlib.pyplot as plt 
#Monte Carlo


def Eur_option_value( S_0=5.9, K=5.43,  T=1.353, r=0.018482,sigma=0.2616, M=50, I=200000 , seed_num=2000   ):
        dt=T/M
        
        seed(seed_num)
        
        start=time() 
        
        S=[]
        for i in range (I):
           path=[] #时间间隔上的模拟路径 
           for t in range( M + 1): 
             if t==0:
               path.append(S_0) 
             
             else:
               z=gauss(0.00, 1.00 )
               S_t= path[t-1]*exp((r-0.5*sigma**2)*dt + sigma*sqrt(dt)*z)
               path.append(S_t) 
              
           S.append(path)

        #计算期权现值
        C_0=exp(-r*T)*sum([max(path[-1]-K,0)for path in S])/I #贴现 
        total_time=time()-start
        
        print('European Option value 每股正股的欧式期权的价值： %.6f'%  C_0) 
        print('total time 所花费的时间： %.6f seconds'% total_time)
        
        #选取部分模拟路径可视化，前 50000条路径模拟 

        plt.figure(figsize=(10,7)) 
        plt.grid(True)
        plt.xlabel ('Time step') 
        plt.ylabel ('market cap') 
        for i in range(50000):##这是是路径数量的参数
            plt.plot(S[i])
            
            
            

        return( C_0 )


        
        
def  theoretical_value(bond,C_0,K=5.43):
    
        ###可转债的理论价值（纯债价值+期权价值）
        t_v = bond + 100/K*C_0
        
        print('可转债的理论价值（纯债价值+期权价值）： %.6f'%  t_v ) 
        return(  t_v )


