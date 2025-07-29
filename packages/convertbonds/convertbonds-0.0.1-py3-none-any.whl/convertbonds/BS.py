# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 15:06:46 2025

@author: admin
"""

from scipy import stats
from math import exp, sqrt ,log 


  
def B_S( S=float(5.9),X=float(5.43) ,a= float(0.2616),T=float(1.353),r=float(0.018482) ,B=float(104.05),C1=float(122.82)):
        ###公式运算
        d1= ( log(S/X) + (r + 0.5*a**2)*T ) /(  a *sqrt(T))        
        d2= ( log(S/X) + (r - 0.5*a**2)*T ) /(  a *sqrt(T))
        
        C=S*stats.norm.cdf(d1, 0.0, 1.0)  - X*exp(-r*T)*stats.norm.cdf(d2,0.0,1.0)
        C
        
        ###可转债的期权价值
        print1 = 100/X*C

        ###可转债的理论价值（纯债价值+期权价值）
        print2 = B+100/X*C

        ##对比差距
        print3 = C1-(B+100/X*C)##可转债的理论价格与现价之间差额
        print4 = ( C1-(B+100/X*C) ) /C1#可转债的理论价格与现价之间差额之比例
        
        
        

        print('可转债的期权价值:{0}\n可转债的理论价值（纯债价值+期权价值）:{1}\n可转债的理论价格与现价之间差额:{2}\n可转债的理论价格与现价之间差额之比例:{3}  '.format(print1,print2,print3,print4))
        
        return(print1,print2,print3,print4)

