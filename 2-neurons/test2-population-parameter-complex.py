# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 12:45:27 2018

@author: HSI
"""

from brian2 import *

start_scope()

N = 1000
tau = 10*ms
vr = -70*mV
vt0 = -50*mV
delta_vt0 = 5*mV
tau_t = 100*ms
sigma = 0.5*(vt0-vr)
v_drive = 2*(vt0-vr)
duration = 100*ms

eqs = '''
dv/dt = (v_drive+vr-v)/tau + sigma*xi*tau**-0.5 : volt
dvt/dt = (vt0-vt)/tau_t : volt
'''

reset = '''
v = vr
vt += delta_vt0
'''
#有点像Izhikevich的模型，但是阈值vt是dynamic的
G = NeuronGroup(N, eqs, threshold='v>vt', reset=reset, refractory=5*ms, method='euler')
spikemon = SpikeMonitor(G)

G.v = 'rand()*(vt0-vr)+vr'#给v赋初值
G.vt = vt0#给vt赋初值

run(duration)

_ = hist(spikemon.t/ms, 100, histtype='stepfilled', facecolor='r', weights=ones(len(spikemon))/(N*defaultclock.dt))#应该是population firing rate，PSTH
xlabel('Time (ms)')
ylabel('Instantaneous firing rate (sp/s)');

figure(2);
plot(spikemon.t/ms,spikemon.i,'.k')
