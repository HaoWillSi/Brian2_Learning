
{% include lib/mathjax.html %}

How to implement the alpha-function-type synapse?
===

**Summary**: In the last post (very long long ago), I studied the Synapse. However, in fact I still didn't know how to implement the synapse 
model from the equation (eg. alpha function) in the paper I read. Therefore, I turned to the Brian Google Groups and my senior who ever used 
the Brian. 
### Learning 
In the paper I have read, most synapses were modeled as alpha function. As is shown in the pic below:
![](https://github.com/HardworkingChris/Brian2_Learning/raw/master/3-synapse/synapse_alpha.PNG)  
, which is from the paper [_Propagation of Firing Rate in a Feed-Forward Neuronal Network_](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.96.018103)

I learned that in Brian2 the authors give an introduction named [_Converting from integrated form to ODEs_](https://brian2.readthedocs.io/en/stable/user/converting_from_integrated_form.html)
to show how to implement ordinary differential equations.
Some examples shown in the introduction include the Alpha synapse, $$V(t)=(t/τ)e^{−t/τ}$$:
```py
eqs = '''
dV/dt = (x-V)/tau : 1
dx/dt = -x/tau    : 1
'''
on_pre = 'x += w'
```
### How  
According to the introduction about ODEs implementation and examples, I write the python-brian2 code to implement excitatory and inhibitory 
synaptic currents.

#### excitatory synaptic current
(1) synaptic conductance (alpha function)<br>
```py
dge/dt = -ge/taue: 1 

dv/dt = +ge*(Ee-v) :volt # the right part is the iterative part in the main equation of membrane potential
```
(2) synaptic weight <br>
```py
con_ee.append(Synapses(group_e[m*groupsize_e:(m+1)*groupsize_e], group_e[m*groupsize_e:(m+1)*groupsize_e], 'w: 1', on_pre='ge += w'))#updating
con_ee.connect(p=epsilon)#synaptic connacting probability
con_ee.w = J_e#synaptic weight
```
#### inhibitory synaptic current
The inhibitory synaptic current is similar as the excitatory one.
