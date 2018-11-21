# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 19:43:52 2018

@author: HSI
"""

#simulations 

#multi-runs 多次运行

from brian2 import *

#：实现一个参数改变的仿真的多进程。让我们从简单的开始，由泊松突触脉冲神经元驱动的
#一个LIF的触发时间如何随其膜时间常量改变
# 记住，这句话是为了在同一个笔记（程序，py文件）中运行单独的仿真
start_scope()
# 参数，poisson输入的
num_inputs = 100
input_rate = 10*Hz
weight = 0.1
# 时间常量范围，膜时间常数
tau_range = linspace(1, 10, 30)*ms
# 用这个列表存储输出速率
output_rates = []
# 在时间常数范围中进行迭代
for tau in tau_range:
    # 每个时间都构建网络
    P = PoissonGroup(num_inputs, rates=input_rate)
    eqs = '''
    dv/dt = -v/tau : 1
    '''
    G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
    S = Synapses(P, G, on_pre='v += weight')
    S.connect()
    M = SpikeMonitor(G)
    # 运行仿真并将输出spike rate存储在列表中
    run(1*second)
    output_rates.append(M.num_spikes/second)
# 绘制出来
plot(tau_range/ms, output_rates)
xlabel(r'$\tau$ (ms)')
ylabel('Firing rate (sp/s)');

#运行这个笔记，你会发现它运行起来有点慢。原因是对每个循环，你都重新创建了对象。
#我们可以通过只创建一次网络来改进。我们在循环前存储了网络状态的副本，并在每个迭代的开始恢复。

start_scope()
num_inputs = 100
input_rate = 10*Hz
weight = 0.1
tau_range = linspace(1, 10, 30)*ms
output_rates = []
# 仅构造一次网络
P = PoissonGroup(num_inputs, rates=input_rate)
eqs = '''
dv/dt = -v/tau : 1
'''
G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
S = Synapses(P, G, on_pre='v += weight')
S.connect()
M = SpikeMonitor(G)
# 存储当前网络状态
store()
for tau in tau_range:
    # 恢复网络原始状态
    restore()
    # 用新的tau值运行
    run(1*second)
    output_rates.append(M.num_spikes/second)
plot(tau_range/ms, output_rates)
xlabel(r'$\tau$ (ms)')
ylabel('Firing rate (sp/s)');
#以上是一个使用存储和恢复的简单例子，但你可以将其用在更复杂的情形。
#比如，你可能想运行一个很长时间的训练进程，然后运行多个测试进程，
#只需要简单得在长时间得训练进程后存储并在每个测试进程之间恢复。

#但是
#也可以看到，上面的图都比较曲折不是单调递增的，主要是因为我们每一次都产生了新的poisson input，
#然而，我们这里想要探究的是时间常数的影响，因此我们应该确保每次实验的输入是相同的。
#所以，我们接下来只产生一次poisson输入，复制然后用SpikeGeneratorGroup重现。
start_scope()
num_inputs = 100
input_rate = 10*Hz
weight = 0.1
tau_range = linspace(1, 10, 30)*ms
output_rates = []
# 只创建一次泊松脉冲
P = PoissonGroup(num_inputs, rates=input_rate)
MP = SpikeMonitor(P)
# 我们使用一个Network对象因为之后我们
# 不想再包含这些对象
net = Network(P, MP)
net.run(1*second)
# 暂存那些脉冲的副本
spikes_i = MP.i
spikes_t = MP.t
# 现在创建我们每次运行的网络
# SpikeGeneratorGroup获得我们之前创建的脉冲
SGG = SpikeGeneratorGroup(num_inputs, spikes_i, spikes_t)#SpikeGeneratorGroup(Nums, indecies, times)
eqs = '''
dv/dt = -v/tau : 1
'''
G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
S = Synapses(SGG, G, on_pre='v += weight')
S.connect()
M = SpikeMonitor(G)
# 存储网络的当前状态
net = Network(SGG, G, S, M)#我们使用Network来明确指明我们想要包含哪个对象。
net.store()
for tau in tau_range:
    # 恢复网络的初始状态
    net.restore()   
    # 用新的tau值运行
    net.run(1*second)
    output_rates.append(M.num_spikes/second)
plot(tau_range/ms, output_rates)
xlabel(r'$\tau$ (ms)')
ylabel('Firing rate (sp/s)');

#我们到现在看到的计数是实现多进程的概念上最简单的方式，但通常不是最有效的。
#既然上面的模型中只有一个输出神经元，我们可以简单的复制输出神经元使得时间常数成为这个组的参数。

start_scope()
num_inputs = 100
input_rate = 10*Hz
weight = 0.1
tau_range = linspace(1, 10, 30)*ms
num_tau = len(tau_range)
P = PoissonGroup(num_inputs, rates=input_rate)
#我们让tau成为这个组的参数
eqs = '''
dv/dt = -v/tau : 1
tau : second
'''
# 我们有num_tau个输出神经元，每个神经元的tau不同
G = NeuronGroup(num_tau, eqs, threshold='v>1', reset='v=0', method='exact')
G.tau = tau_range
S = Synapses(P, G, on_pre='v += weight')
S.connect()
M = SpikeMonitor(G)
# 现在我们不需要循环，只需运行一次
run(1*second)
output_rates = M.count/second # 激发速率是count/duration
plot(tau_range/ms, output_rates)
xlabel(r'$\tau$ (ms)')
ylabel('Firing rate (sp/s)');

#Let’s finish with this example by having a quick look at how the mean and standard deviation 
#of the interspike intervals depends on the time constant.
#看看ISI的统计特性是如何随膜时间常数变化的
trains = M.spike_trains()
isi_mu = full(num_tau, nan)*second#Return a new array of given shape and type, filled with fill_value.用full建立新的数组
isi_std = full(num_tau, nan)*second
for idx in range(num_tau):
    train = diff(trains[idx])#计算序列里连续两个元素之间的差值，这里也就是ISI
    if len(train)>1:
        isi_mu[idx] = mean(train)
        isi_std[idx] = std(train)
errorbar(tau_range/ms, isi_mu/ms, yerr=isi_std/ms)#来自matplotlib
xlabel(r'$\tau$ (ms)')
ylabel('Interspike interval (ms)');