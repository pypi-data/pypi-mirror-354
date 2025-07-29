# -*- coding: utf-8 -*-
"""
Created on Sun Jun  8 15:06:18 2025

@author: admin
"""


from .BS import B_S


#from .Monte_Carlo import Eur_option_value
#from .Monte_Carlo import theoretical_value

# convertbonds/__init__.py

#from .BS import B_S as Eur_option  # 给外部提供 Eur_option 的名字
from .Monte_Carlo import *         # 如果有其他函数也要暴露可以加入

#__all__ = ["B_S", "Eur_option_value", "theoretical_value"]
