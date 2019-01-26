---
layout:     post
title:      To implement STDP(Spike-Timing Dependent Plasticity)
subtitle:   利用Brian2实现STDP
date:       2019-01-26
author:     HSI
header-img: img/post-bg-desk.jpg
catalog: 	 true
tags:
    - Brian2
    - synapse
    - STDP
    - synaptic plasticity
---
{% include lib/mathjax.html %}

How to implement the STDP?
===

**Summary**: It is found that the synapses between neurons may save the memory through the varying weights and so on, which is called as
the synaptic plasticity. In theorietical studies people usually assume that the synaptic weight stay constant, however, in fact, the 
synaptic weight changes via many parameters such as the interspike interval between the prespike and the postspike. In this post, I will 
introduce a type of synaptic plasticity called the Spike-Timing Dependent Plasticity(STDP).
### Learning 
STDP may be the underlying mechanism of learning and memory in the brain. As is shown in the eq. below, STDP is normally defined by an 
equation something like this:<br>
$$\Delta w = \sum_{t_{pre}}\sum_{t_{post}}W(t_{post}-t_{pre})$$     (1) <br>

That is, the change in synaptic weight $$w$$ is the sum over all presynaptic spike times $$t_{pre}$$ and postsynaptic spike times 
$$t_{post}$$ of some function $$W$$ of the difference in these spike times. A commonly used function $$W$$ is:
$$
W(\Delta t)=\left\{\begin{matrix}
A_{pre}e^{-\Delta t/\tau _{pre}} \quad\Delta t>0\\ 
A_{post}e^{-\Delta t/\tau _{post}} \quad\Delta t<0
\end{matrix}\right.
$$
, of which figure is shown below.

![](https://github.com/HardworkingChris/Brian2_Learning/raw/master/3-synapse/STDP.jpg)  

Through the Brian2 [tutorial on Synapse](https://brian2.readthedocs.io/en/stable/resources/tutorials/2-intro-to-brian-synapses.html) and
some [examples about STDP in Brian2 weibsites](https://brian2.readthedocs.io/en/stable/examples/synapses.STDP.html), I understand how to 
use STDP in Brian2.
Here are some codes for showing.
```py
start_scope()

taupre = taupost = 20*ms
wmax = 0.01
Apre = 0.01
Apost = -Apre*taupre/taupost*1.05

G = NeuronGroup(2, 'v:1', threshold='t>(1+i)*10*ms', refractory=100*ms)

S = Synapses(G, G,
             '''
             w : 1
             dapre/dt = -apre/taupre : 1 (clock-driven)
             dapost/dt = -apost/taupost : 1 (clock-driven)
             ''',
             on_pre='''
             v_post += w
             apre += Apre
             w = clip(w+apost, 0, wmax)
             ''',
             on_post='''
             apost += Apost
             w = clip(w+apre, 0, wmax)
             ''', method='linear')
S.connect(i=0, j=1)
run(30*ms)
```
, in which the $$a_{pre}$$ and $$a_{post}$$ are the parameters to record the trace of the presynaptic and postsynaptic activity, 
respectively. When a prespike occurs the $$a_{post}$$ updates and the synaptic weight changes by some rules we definite.
The _on_pre_ and _on_post_ are the corresponding events when the spike occurs.

#### A classical example from the Brian2 website from 
Spike-timing dependent plasticity Adapted from Song, Miller and Abbott (2000) and Song and Abbott (2001).
```py
from brian2 import *

N = 1000
taum = 10*ms
taupre = 20*ms
taupost = taupre
Ee = 0*mV
vt = -54*mV
vr = -60*mV
El = -74*mV
taue = 5*ms
F = 15*Hz
gmax = .01
dApre = .01
dApost = -dApre * taupre / taupost * 1.05
dApost *= gmax
dApre *= gmax

eqs_neurons = '''
dv/dt = (ge * (Ee-vr) + El - v) / taum : volt
dge/dt = -ge / taue : 1
'''

input = PoissonGroup(N, rates=F)
neurons = NeuronGroup(1, eqs_neurons, threshold='v>vt', reset='v = vr',
                      method='exact')
S = Synapses(input, neurons,
             '''w : 1
                dApre/dt = -Apre / taupre : 1 (event-driven)
                dApost/dt = -Apost / taupost : 1 (event-driven)''',
             on_pre='''ge += w
                    Apre += dApre
                    w = clip(w + Apost, 0, gmax)''',
             on_post='''Apost += dApost
                     w = clip(w + Apre, 0, gmax)''',
             )
S.connect()
S.w = 'rand() * gmax'
mon = StateMonitor(S, 'w', record=[0, 1])
s_mon = SpikeMonitor(input)

run(100*second, report='text')
```
From the example above, I know that the necessary parameters are <br>
`Apre,Apost` , record the trace of the pre and post activity.<br>
`on_pre`, `on_post`, definite the specifying events after a spike.<br>
`Apre` is showing in `on_pre`, Apost` is showing in `on_post`. <br>
`ge += w`, change the synaptic conductance.<br>
`w + Apost`, rules of synaptic weights.
