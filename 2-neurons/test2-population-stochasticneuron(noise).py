# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 12:37:18 2018

@author: HSI
"""
#引入噪声
#通常当我们建立神经元模型时，我们包含了一个随机元素来模拟各种形式的神经噪声的影响。
#在Brian中，我们可以在微分方程中用符号xi来实现这个。严格说来，这个符号是一个随机
#神经元但你可以把它看成带有均值0和方差1的高斯随机变量。

from brian2 import *

start_scope()

N = 100
tau = 10*ms
v0_max = 3.
duration = 1000*ms
sigma = 0.2

eqs = '''
dv/dt = (v0-v)/tau+sigma*xi*tau**-0.5 : 1 (unless refractory)
v0 : 1
'''

G = NeuronGroup(N, eqs, threshold='v>1', reset='v=0', refractory=5*ms, method='euler')
M = SpikeMonitor(G)

G.v0 = 'i*v0_max/(N-1)'

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