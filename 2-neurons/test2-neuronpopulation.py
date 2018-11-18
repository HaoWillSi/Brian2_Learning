# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 10:23:38 2018

@author: HSI
"""

#neuron population
from brian2 import *

start_scope()

N = 100
tau = 10*ms
eqs = '''
dv/dt = (2-v)/tau : 1
'''
G = NeuronGroup(N, eqs, threshold='v>1',reset='v=0',method='exact')
G.v = 'rand()'#这句表达式做的是用0和1之间不同的均匀随机值初始化每个神经元

spikemon = SpikeMonitor(G)

run(50*ms)

plot(spikemon.t/ms, spikemon.i, '.k')#变量spikemon.i给每个脉冲相应的神经元索引
xlabel('Time (ms)')
ylabel('Neuron index');