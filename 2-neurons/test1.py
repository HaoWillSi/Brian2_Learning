# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 10:26:04 2018

@author: HSI
"""

from brian2 import *

start_scope()

tau = 10*ms
eqs = '''
dv/dt = (1-v)/tau : 1
'''
eqs1 = '''
dv/dt = (sin(2*pi*100*Hz*t)-v)/tau : 1
'''

G = NeuronGroup(1, eqs, method='exact')#只能使用NeuronGroup类创建神经元组。你创建这些实例时前两个参数是神经元的数量（在这儿，1）和定义的微分方程。
G1 = NeuronGroup(1, eqs1, method='euler')# Change to Euler method because exact integrator doesn't work here
M = StateMonitor(G1, 'v', record=0)#使用StateMonitor实例。这用来记录当仿真运行时一个神经元变量的值,前两个变量是记录的组和你要记录的变量

run(30*ms)

plot(M.t/ms, M.v[0],'C0',label='Brian')
#plot(M.t/ms, 1-exp(-M.t/tau),'C1--',label='Analytic')
xlabel('Time (ms)')
ylabel('v')
legend();