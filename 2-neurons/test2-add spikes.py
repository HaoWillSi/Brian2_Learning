# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 09:54:28 2018

@author: HSI
"""

#add spikes
from brian2 import *

start_scope()

tau = 10*ms
eqs = '''
dv/dt = (1-v)/tau : 1(unless refractory)
'''#不应期必须在这里指出
G = NeuronGroup(1, eqs, threshold='v>0.8',reset='v=0',refractory=5*ms,method='exact')
#threshold='v>0.8'和reset='v = 0'。这个的含义是当v>0.8时我们激发一个脉冲，并在脉冲之后立即重置v=0。
M = StateMonitor(G, 'v', record = 0)
spikemon = SpikeMonitor(G)#记录放电时刻

run(50*ms)
print('Spike times: %s' % spikemon.t[:])
plot(M.t/ms,M.v[0])
for t in spikemon.t:
    axvline(t/ms, ls='--',c='C1',lw=3)
xlabel('time (ms)')
ylabel('v');


