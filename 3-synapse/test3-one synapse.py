# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 20:09:27 2018

@author: HSI
"""

#synapse突触
from brian2 import *
#%matplotlib inline

start_scope()

eqs = '''
dv/dt = (I-v)/tau : 1
I : 1
tau : second
'''
G = NeuronGroup(2, eqs, threshold='v>1', reset='v = 0', method='exact')
G.I = [2, 0]
G.tau = [10, 100]*ms
#我们创建了两个神经元，每个神经元有相同的微分方程，但参数I和tau的值不同。神经元0有I=2和tau=10*ms，
#这意味着该神经元被以相当高的速率驱动反复产生脉冲。神经元1有参数I=0和tau=100*ms，这意味着在没有突触时
#该神经元本身根本不会触发（驱动电流是0）.你可以通过注释掉定义突触的两行来自己证明。

# Comment these two lines out to see what happens without Synapses
S = Synapses(G, G, on_pre='v_post += 0.2')
S.connect(i=0, j=1)#S.connect(i=0, j=1)创建了从神经元0到神经元1的突触连接。
#Synapses(source, target, ...)意思是我们定义一个从source到target的突触模型。在这里，源和目标都是相同的，是组G。
#语句on_pre='v_post += 0.2'含义是当一个脉冲发生在突触前神经元时（即on_pre），它会引起一个瞬时变化v_post += 0.2。_post指提到的v的值为突触后值，
#且增加了0.2。
M = StateMonitor(G, 'v', record=True)

run(100*ms)

plot(M.t/ms, M.v[0], label='Neuron 0')
plot(M.t/ms, M.v[1], label='Neuron 1')
xlabel('Time (ms)')
ylabel('v')
legend();
