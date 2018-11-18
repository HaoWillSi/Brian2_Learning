# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 12:09:23 2018

@author: HSI
"""

from brian2 import *

start_scope()

N = 100
tau = 10*ms
v0_max = 3.
duration = 1000*ms

eqs = '''
dv/dt = (v0-v)/tau : 1 (unless refractory)
v0 : 1
'''#v0:1这行阐明了一个新的单位为1的单一神经元参数（也就是无量纲）。


G = NeuronGroup(N, eqs, threshold='v>1', reset='v=0', refractory=5*ms, method='exact')
M = SpikeMonitor(G)

G.v0 = 'i*v0_max/(N-1)'#为每个神经元初始化了从0到v0_max的值,i是指神经元索引
#就相当于神经元的v0值是在一直变化的
run(duration)

figure(figsize=(12,4))
subplot(121)
plot(M.t/ms, M.i, '.k')#spike raster
xlabel('Time (ms)')
ylabel('Neuron index')
subplot(122)
plot(G.v0, M.count/duration)#右边的图形展示了激发速率和v0的值的函数关系。这是改神经元模型的l-f曲线。
#使用了SpikeMonitor的count变量：这是spike group中每个神经元spike number的数组。用运行周期除以这个数得到spike rate
xlabel('v0')
ylabel('Firing rate (sp/s)');