# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 21:21:57 2018

@author: HSI
"""

#更加复杂的连接
#一个可以显示连接模式的函数

from brian2 import *

start_scope()

N = 10
G = NeuronGroup(N, 'v:1')
S = Synapses(G, G)
S.connect(condition='i!=j', p=0.2)#定义连接，概率0.2 10个神经元互相连接，条件为i!=j,即排除自连接

def visualise_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10, 4))
    subplot(121)
    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10)
    for i, j in zip(S.i, S.j):
        plot([0, 1], [i, j], '-k')
    xticks([0, 1], ['Source', 'Target'])
    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    subplot(122)
    plot(S.i, S.j, 'ok')
    xlim(-1, Ns)
    ylim(-1, Nt)
    xlabel('Source neuron index')
    ylabel('Target neuron index')

visualise_connectivity(S)


#改变连接概率
for p in [0.1, 0.5, 1.0]:
    S = Synapses(G, G)
    S.connect(condition='i!=j', p=p)
    visualise_connectivity(S)
    suptitle('p = '+str(p))
    
#只连接附近的神经元。    
S.connect(condition='abs(i-j)<4 and i!=j')
visualise_connectivity(S)

#你也可以用生成器语法更高效地创建像这样的连接。在像这样的小例子里可能没什么，但对于大量神经元而言
#它可以比仅仅用条件来说明更高效地直接阐明哪一个神经元应该被连接。注意下面的例子中使用skip_if_invalid避免边界处的错误发生
#（比如不要尝试将索引为1的神经元和索引为-2的神经元连接）。

S = Synapses(G, G)
S.connect(j='k for k in range(i-3, i+4) if i!=k', skip_if_invalid=True)
visualise_connectivity(S)

#如果每个源神经元和一个目标神经元准确连接时（通常是两个同样尺寸的独立神经元组而不是像这个例子一样相同的源和目标），
#有一个语法将是异常有效。比如，看上去像这样的1对1连接：
S = Synapses(G, G)
S.connect(j='i')
visualise_connectivity(S)

#你也可以做一些像用字符串说明权重的值这样的事情。让我们来看一个例子，
#我们给每个神经元分配一个空间位置，并有一个与距离相关的连接函数。我们通过标记的大小来可视化一个突触的权重。

N = 30
neuron_spacing = 50*umetre#定义一个神经元空间
width = N/4.0*neuron_spacing

# Neuron has one variable x, its position
G = NeuronGroup(N, 'x : metre')#用x变量来表示神经元的位置
G.x = 'i*neuron_spacing'

# All synapses are connected (excluding self-connections)
S = Synapses(G, G, 'w : 1')
S.connect(condition='i!=j')
# Weight varies with distance
S.w = 'exp(-(x_pre-x_post)**2/(2*width**2))'

scatter(S.x_pre/um, S.x_post/um, S.w*20)
xlabel('Source neuron position (um)')
ylabel('Target neuron position (um)');