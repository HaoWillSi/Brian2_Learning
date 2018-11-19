# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 21:13:24 2018

@author: HSI
"""

#给突触加上权重

from brian2 import *

start_scope()

eqs = '''
dv/dt = (I-v)/tau : 1
I : 1
tau : second
'''
G = NeuronGroup(3, eqs, threshold='v>1', reset='v = 0', method='exact')
G.I = [2, 0, 0]
G.tau = [10, 100, 100]*ms

# Comment these two lines out to see what happens without Synapses
S = Synapses(G, G, 'w : 1', on_pre='v_post += w')#标注了权重w的量纲为1
S.connect(i=0, j=[1, 2])#0-->1,0-->2
S.w = 'j*0.2'#j目标神经元*0.2
#我们创建了和第二个神经元变现完全一样的第三个神经元，并将神经元0同时和神经元1与神经元2连接。
#我们也通过S.w = 'j*0.2'设置了权重。当i和j出现在突触表达式中时，i值源神经元的索引，j指目标神经元的索引。
#因此这会给神经元0到1值为0.2=0.2*1的权重，给神经元0到2值为0.4=0.2*2的权重

M = StateMonitor(G, 'v', record=True)

run(50*ms)

plot(M.t/ms, M.v[0], label='Neuron 0')
plot(M.t/ms, M.v[1], label='Neuron 1')
plot(M.t/ms, M.v[2], label='Neuron 2')
xlabel('Time (ms)')
ylabel('v')
legend();