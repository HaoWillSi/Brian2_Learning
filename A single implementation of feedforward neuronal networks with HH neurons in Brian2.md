This is my code of implementation of FFN wiht HH neurons, which is from 
[Sentao Wang et.al. Propagation of Firing Rate in a Feed-Forward Neuronal Network. (2006). PRL.](https://www.semanticscholar.org/paper/Propagation-of-firing-rate-in-a-feed-forward-Wang-Wang/dbed466d7ff39da4794386609b5fd543d1cd739e).
But it is still in debugging because the activity in the input layer could hardly reach to the output layer.

This version is better than the previous ones in the feedforward network part. In the previous version, I used some group variables to saving the neuron groups and synapses sparating into 10 groups, which means 10 layers, as well as 
`Network` function is also used to create the FF architecture. However, it took high cost of time and CPU in such a implemention ways.
```python
net_sub = [] #storre neurongroups , one for each population
for ix in range(0,n_layer):
    if ix == 0:
        net_sub.append(group[:groupsize])
    else:
        net_sub.append(group[ix*groupsize:(ix+1)*groupsize])
#create connections
con = []#stores connections
for m in range(0,n_layer-1):
    con.append(Synapses(net_sub[m], net_sub[m+1], on_pre='v += weight'))
    con[m].connect(p=0.1)

net = Network(collect())
net.add(group,net_sub, con)    # Adding objects to the simulation
```
After consulting on the Brian team, I learned a new and efficient way to creat a feedforward network. From . Through the example code from [Diesmann et al. (1999). Nature.](https://brian2.readthedocs.io/en/stable/examples/frompapers.Diesmann_et_al_1999.html),
`S.connect(j='k for k in range((int(i/group_size)+1)*group_size, (int(i/group_size)+2)*group_size) ''if i<N_pre-group_size')`, we just need to replace 
`range()` with `sample(size,size,p=0.1) ` . Diesmann's synfire chain is a feedforward network with all-to-all connections between neighbouring layers, while the model 
in Sentao Wang's paper is a random connecting feedforward network.

```python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 23:19:49 2019

@author: HSI
"""
#smaple建立前馈连接

from brian2 import *
from random import gauss
import time

start1 = time.perf_counter()
start2 = time.process_time()
#使用 H-H neuron model，仿真，输入神经元常电流
#仿真FFN，PRL 2006
duration = 200*ms
weight = 1*mV

sigma = 0.1*mV
tau = 10*ms
# Parameters
area = 20000*umetre**2  #面积。
Cm = 1*ufarad*cm**-2 * area  #电容
gl = 5e-5*siemens*cm**-2 * area #漏电导
El = -65*mV
EK = -90*mV
ENa = 50*mV
g_na = 100*msiemens*cm**-2 * area
g_kd = 30*msiemens*cm**-2 * area
VT = -63*mV  

eta = 1*gauss(0.0, 1.0)
# The model
eqs_HH = '''
dv/dt = (gl*(El-v) - g_na*(m*m*m)*h*(v-ENa) - g_kd*(n*n*n*n)*(v-EK) + I )/Cm + D*eta*mV/ms: volt
dm/dt = 0.32*(mV**-1)*(13.*mV-v+VT)/
    (exp((13.*mV-v+VT)/(4.*mV))-1.)/ms*(1-m)-0.28*(mV**-1)*(v-VT-40.*mV)/
    (exp((v-VT-40.*mV)/(5.*mV))-1.)/ms*m : 1
dn/dt = 0.032*(mV**-1)*(15.*mV-v+VT)/
    (exp((15.*mV-v+VT)/(5.*mV))-1.)/ms*(1.-n)-.5*exp((10.*mV-v+VT)/(40.*mV))/ms*n : 1
dh/dt = 0.128*exp((17.*mV-v+VT)/(18.*mV))/ms*(1.-h)-4./(1+exp((40.*mV-v+VT)/(5.*mV)))/ms*h : 1
I : amp
D : 1
'''

groupsize = 100;
n_layer = 10;

group = NeuronGroup(n_layer*groupsize, eqs_HH,
                    threshold='v > -40*mV',
                    refractory='2*ms',
                    method='exponential_euler')
group.v = El
group[0:groupsize].I = 1.5*nA
group[0:groupsize].D = 1
group[groupsize:].D = 0
# The network structure

S = Synapses(group, group, on_pre='v+=weight')
S.connect(j='k for k in sample((int(i/groupsize)+1)*groupsize, (int(i/groupsize)+2)*groupsize,p=0.1) '
            'if i<N_pre-groupsize')
spikemon = SpikeMonitor(group, variables='v')#记录>=阈值的点

run(duration,report='stdout')


plot(spikemon.t/ms, spikemon.i/groupsize, 'k.')
plot([0, duration/ms], np.arange(n_layer).repeat(2).reshape(-1, 2).T, 'k-')
ylabel('group number')
yticks(np.arange(n_layer))
xlabel('time (ms)')
show()

end1 = time.perf_counter()
end2 = time.process_time()

print('Elapsed time/s: ',end1 - start1 )
print('CPU执行时间: ',end2 - start2)


```
