### Learn Synapse through examples frompapaers

The central part of Brian2 code I think is the Synapse, which directly relates to the network.
In the Brian2 tutorial files, I did not learn it carefully. Therefore, I will learn it in the examples from papers. 

* Diesmann et al. (1999)<br>

The network part in the code of this paper is:<br>
```py
S = Synapses(P, P, on_pre='y+=weight')
S.connect(j='k for k in range((int(i/group_size)+1)*group_size, (int(i/group_size)+2)*group_size) '
            'if i<N_pre-group_size')
Sinput = Synapses(Pinput, P[:group_size], on_pre='y+=weight')
Sinput.connect()
```
From which we could see the key roles of Synapse.
```py
S = Synapses(P, P, on_pre='y+=weight')
```
Note that #groupsize = 100,total number=1000.<br>
In the Synapse function, `P` is the neurongroup we created before, the note we should know is it is a full-connected network (?). `y` is 
a dynamic parameter of neuron model (integrate and fire model). The string in `on_pre` will be executed after every **pre-synaptic spike**.
The sentence above is used to create synapses in the neurongroup, and when the presynaptic spike is emmitted the parameter `y` will add the `weight`.
The `Synapse` is used to model synapse of neurons. The connections among neurons are still not created yet which will be seen in `connect`.<br>
(在Synapse这个语句中，这里应该是先在神经元集群中建立突触，至于连接关系还没有赋予，在下面的connect函数里进行连接，赋予耦合关系。)

Now, let's see more about the `Synapse class` in Brian2 documetions.<br>
**Synapse class**<br>
You could use it like this:
```py
Synapses(source, target=None, model=None, on_pre=None, pre=None, on_post=None, post=None, connect=None, 
delay=None, on_event='spike', multisynaptic_index=None, namespace=None, dtype=None, codeobj_class=None, 
dt=None, clock=None, order=0, method=('exact', 'euler', 'heun'), method_options=None, name='synapses*')
```
Class representing synaptic connections.

Creating a new `Synapses` object does by default not create any synapses, you have to call the `Synapses.connect()` method for that.<br>
（如果你指调用了Synapse，默认情况是没有任何实际的突触，你必须再调用Synapses.connect()之后，才会创建真正的突触。）<br>
```py
class Synapses(Group):
    '''
    Class representing synaptic connections.

    Creating a new `Synapses` object does by default not create any synapses,
    you have to call the `Synapses.connect` method for that.

    Parameters
    ----------

    source : `SpikeSource`
        The source of spikes, e.g. a `NeuronGroup`.#spike来源，相当于突触前神经元
    target : `Group`, optional
        The target of the spikes, typically a `NeuronGroup`. If none is given,
        the same as `source`#突触后神经元，通常是NeronGroup，如果没给的话，默认是source
    model : `str`, `Equations`, optional
        The model equations for the synapses.#突触的模型
    on_pre : str, dict, optional#突触前神经元放电时突触进行的活动，这里可以写string（单一），也可以是dictionary（多路映射）
        The code that will be executed after every pre-synaptic spike. Can be
        either a single (possibly multi-line) string, or a dictionary mapping
        pathway names to code strings. In the first case, the pathway will be
        called ``pre`` and made available as an attribute of the same name.
        In the latter case, the given names will be used as the
        pathway/attribute names. Each pathway has its own code and its own
        delays.
    pre : str, dict, optional
        Deprecated. Use ``on_pre`` instead.
    on_post : str, dict, optional#突触后神经元放电时突触进行的活动，和on_pre类似
        The code that will be executed after every post-synaptic spike. Same
        conventions as for `on_pre``, the default name for the pathway is
        ``post``.
    post : str, dict, optional
        Deprecated. Use ``on_post`` instead.
    delay : `Quantity`, dict, optional#可改变突触的delay 
        The delay for the "pre" pathway (same for all synapses) or a dictionary
        mapping pathway names to delays. If a delay is specified in this way
        for a pathway, it is stored as a single scalar value. It can still
        be changed afterwards, but only to a single scalar value. If you want
        to have delays that vary across synapses, do not use the keyword
        argument, but instead set the delays via the attribute of the pathway,
        e.g. ``S.pre.delay = ...`` (or ``S.delay = ...`` as an abbreviation),
        ``S.post.delay = ...``, etc.
    on_event : str or dict, optional#定义能够激发起突触前后动作的事件，默认是spike，也可以写成threshold
        Define the events which trigger the pre and post pathways. By default,
        both pathways are triggered by the ``'spike'`` event, i.e. the event
        that is triggered by the ``threshold`` condition in the connected
        groups.
    multisynaptic_index : str, optional#存储突触index的变量
        The name of a variable (which will be automatically created) that stores
        the "synapse number". This number enumerates all synapses between the
        same source and target so that they can be distinguished. For models
        where each source-target pair has only a single connection, this number
        only wastes memory (it would always default to 0), it is therefore not
        stored by default. Defaults to ``None`` (no variable).
    namespace : dict, optional
        A dictionary mapping identifier names to objects. If not given, the
        namespace will be filled in at the time of the call of `Network.run`,
        with either the values from the ``namespace`` argument of the
        `Network.run` method or from the local context, if no such argument is
        given.
    dtype : `dtype`, dict, optional
        The `numpy.dtype` that will be used to store the values, or a
        dictionary specifying the type for variable names. If a value is not
        provided for a variable (or no value is provided at all), the preference
        setting `core.default_float_dtype` is used.
    codeobj_class : class, optional
        The `CodeObject` class to use to run code.
    dt : `Quantity`, optional#time step步长值
        The time step to be used for the update of the state variables.
        Cannot be combined with the `clock` argument.
    clock : `Clock`, optional
        The update clock to be used. If neither a clock, nor the `dt` argument
        is specified, the `defaultclock` will be used.
    order : int, optional
        The priority of of this group for operations occurring at the same time
        step and in the same scheduling slot. Defaults to 0.
    method : str, `StateUpdateMethod`, optional
        The numerical integration method to use. If none is given, an
        appropriate one is automatically determined.
    name : str, optional
        The name for this object. If none is given, a unique name of the form
        ``synapses``, ``synapses_1``, etc. will be automatically chosen.
    '''
```
Through the grammar of `Synapse` above, we know how to use it. But as refered above, <br>
Creating a new `Synapses` object does by default not create any synapses, you have to call the `Synapses.connect()` method for that.<br>
Therefore, we then read the grammar about `connect()`:

`connect(**kwds)`<br>
Add synapses.<br>
```
Parameters:	
condition : str, bool, optional

A boolean or string expression that evaluates to a boolean. The expression can depend on indices i and j and on
pre- and post-synaptic variables. Can be combined with arguments n, and p but not i or j.
布尔型或者字符串的表达式，用来描述/执行/计算一个布尔值。这个表达式基于突触前和突触后变量的索引`i`和`j`。

i : int, ndarray of int, optional#突触前神经元的索引，必须和j组合使用

The presynaptic neuron indices (in the form of an index or an array of indices). Must be combined with j argument.

j : int, ndarray of int, str, optional#突触后神经元的索引

The postsynaptic neuron indices. It can be an index or array of indices if combined with the i argument, or it
can be a string generator expression.

p : float, str, optional#连接概率，p=0~1

The probability to create n synapses wherever the condition evaluates to true. Cannot be used with <br>
generator syntax for j.

n : int, str, optional#两个神经元之间的连接中，突触的数量，默认为1

The number of synapses to create per pre/post connection pair. Defaults to 1.

skip_if_invalid : bool, optional

If set to True, rather than raising an error if you try to create an invalid/out of range pair (i, j) 
it will just quietly skip those synapses.

namespace : dict-like, optional

A namespace that will be used in addition to the group-specific namespaces (if defined). If not specified, 
the locals and globals  around the run function will be used.

level : int, optional

How deep to go up the stack frame to look for the locals/global (see namespace argument).
```
See some examples about `Synapse` and `connect`:
```py
>>> from brian2 import *
>>> import numpy as np
>>> G = NeuronGroup(10, 'dv/dt = -v / tau : 1', threshold='v>1', reset='v=0')#创建10个神经元
>>> S = Synapses(G, G, 'w:1', on_pre='v+=w')#在这10个神经元里建立突触，并未连接
>>> S.connect(condition='i != j') # all-to-all but no self-connections，全连接，除了自耦合
>>> S.connect(i=0, j=0) # connect neuron 0 to itself，自耦合
>>> S.connect(i=np.array([1, 2]), j=np.array([2, 1])) # connect 1->2 and 2->1
>>> S.connect() # connect all-to-all默认，全连接
>>> S.connect(condition='i != j', p=0.1)  # Connect neurons with 10% probability, exclude self-connections，0.1的概率耦合，排除自耦合
>>> S.connect(j='i', n=2)  # Connect all neurons to themselves with 2 synapses，每个神经元都与自己耦合，并且突触数量有2个
>>> S.connect(j='k for k in range(i+1)') # Connect neuron i to all j with 0<=j<=i，突触前神经元一定要比突触后神经元的索引大=
>>> S.connect(j='i+(-1)**k for k in range(2) if i>0 and i<N_pre-1') # connect neuron i to its neighbours if it has both neighbours
#range(2),输出0,1.在i非边缘数时，耦合相邻的神经元
>>> S.connect(j='k for k in sample(N_post, p=i*1.0/(N_pre-1))') # neuron i connects to j with probability i/(N-1)
```
Come back to the code above, I try to understand it.
```py
S.connect(j='k for k in range((int(i/group_size)+1)*group_size, (int(i/group_size)+2)*group_size) '
            'if i<N_pre-group_size')
#设置突触后神经元的条件。int(i/group_size)=0(0-99),1(100-199),...,9(900-999).则(int(i/group_size)+1)*group_size
分别等于100,200,...,1000.(int(i/group_size)+2)*group_size)分别为200,300,...,1100.而突触前神经元 i 要符合i<1000-100=900,
也就是只能前9层。所以，前面的j的条件就改为int(i/group_size)=0(0-99),1(100-199),...,8(800-899).
则(int(i/group_size)+1)*group_size分别等于100,200,...,900.(int(i/group_size)+2)*group_size)分别为200,300,...,1000.
所以这样的设置正好是设置了10层的耦合关系，而且只有前馈。大有用处，学习记下。
```
```py
Sinput = Synapses(Pinput, P[:group_size], on_pre='y+=weight')
Sinput.connect()
```
The two sentences are used to inject input into the first layer including the neurons from 0~99.


