# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 18:30:46 2018

@author: HSI
"""

#add input
import os
from brian2 import *

#用正弦函数驱动的神经元，LIF
start_scope()
A = 2.5
f = 10*Hz
tau = 5*ms
eqs = '''
dv/dt = (I-v)/tau : 1
I = A*sin(2*pi*f*t) : 1
'''
G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='euler')#exact方法不可以
M = StateMonitor(G, variables=True, record=True)
run(200*ms)
plot(M.t/ms, M.v[0], label='v')
plot(M.t/ms, M.I[0], label='I')
xlabel('Time (ms)')
ylabel('v')
legend(loc='best');

#如果我们输入的电流是记录存储在一个文件中的会怎样呢？那种情况下，
#我们使用TimedArray。让我们用TimedArray来重现一下上面的图片。

start_scope()
A = 2.5
f = 10*Hz
tau = 5*ms
#创建一个TimedArray并设置使用它的方程
t_recorded = arange(int(200*ms/defaultclock.dt))*defaultclock.dt
I_recorded = TimedArray(A*sin(2*pi*f*t_recorded), dt=defaultclock.dt)
#TimeArray,来自Brian2，用于利用数组建立一个时间序列。TimedArray(array data, dt).第一个是数组，dt是每个数据之间的时间间隔。
#ta = TimedArray([1, 2, 3, 4] * mV, dt=0.1*ms)
#print(ta(0.3*ms))
#4. mV
eqs = '''
dv/dt = (I-v)/tau : 1
I = I_recorded(t) : 1
'''
G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='euler')
M = StateMonitor(G, variables=True, record=True)
run(200*ms)
plot(M.t/ms, M.v[0], label='v')
plot(M.t/ms, M.I[0], label='I')
xlabel('Time (ms)')
ylabel('v')
legend(loc='best');

#现在就看看TimedArray对任意的电流是怎么工作的，让我们创建一个奇怪的“已记录”电流并在其上运行。
start_scope()
A = 2.5
f = 10*Hz
tau = 5*ms
# 让我们创建一个不能被公式重现的数组
num_samples = int(200*ms/defaultclock.dt)
I_arr = zeros(num_samples)
for _ in range(100):
    a = randint(num_samples)
    I_arr[a:a+100] = rand()
I_recorded = TimedArray(A*I_arr, dt=defaultclock.dt)
eqs = '''
dv/dt = (I-v)/tau : 1
I = I_recorded(t) : 1
'''
G = NeuronGroup(1, eqs, threshold='v>1', reset='v=0', method='exact')
M = StateMonitor(G, variables=True, record=True)
Sp = SpikeMonitor(G)
run(200*ms)
plot(M.t/ms, M.v[0], label='v')
plot(M.t/ms, M.I[0], label='I')
xlabel('Time (ms)')
ylabel('v')
legend(loc='best')
figure
plot(Sp.t/ms, Sp.i,'.k');

#让我们以一个真正从一个文件读取数据的例子作为结束。看看你能否搞明白这个例子是如何工作的。
start_scope()

from matplotlib.image import imread
img = (1-imread('brian.png'))[::-1, :, 0].T
num_samples, N = img.shape
ta = TimedArray(img, dt=1*ms) # 228
A = 1.5
tau = 2*ms
eqs = '''
dv/dt = (A*ta(t, i)-v)/tau+0.8*xi*tau**-0.5 : 1
'''
G = NeuronGroup(N, eqs, threshold='v>1', reset='v=0', method='euler')
M = SpikeMonitor(G)
run(num_samples*ms)
plot(M.t/ms, M.i, '.k', ms=3)
xlim(0, num_samples)
ylim(0, N)
xlabel('Time (ms)')
ylabel('Neuron index');

