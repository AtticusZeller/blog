---
title: 神经网络基础组件
date: '2026-10-22'
draft: false
tags:
- deep-learning
- mlp
- pytorch
categories:
- learning-notes
summary: 神经网络基础组件速记：线性层、MLP、激活函数、残差连接、LayerNorm/BatchNorm 与 Dropout。
math: true
showtoc: true
tocopen: true
---

# nn

## activation 

激活函数引入非线性, 如果不用激活函数,多个 线性层自然会退化, 本身也是非线性选择

## Linear layer 

`nn.Linear`线性**层**/full connect全连接层就是 **线性/仿射变换**的操作, 接受input_feature,output_feature , 中间的权重是参数矩阵 (还有偏置参数)
[^2]
$\mathbf{y}=\mathbf{x}\mathbf{W}^{\mathsf T}+\mathbf{b}$![Pasted image 20260826114000](/images/nn-basics-ce4e69c3304f.png)
[^1]

##  Multilayer Perceptrons

数学角度就是 $输入 → 仿射变换 → 非线性激活 → 再做仿射变换 → 输出$
$W_1$将输入转换成大量候选特征的匹配分数(哪些方向有用?)；激活函数根据这些分数进行内容依赖的门控。


![mlp](/images/nn-basics-23ead86aced1.svg)[^4]

MLP = 多层全连接（Linear）层 + 层间非线性激活函数。

比如上图是两层

$$\mathbf{H} = \operatorname{ReLU} \left( \mathbf{X}\mathbf{W}_1^{\mathsf T}+\mathbf{b}_1 \right)$$
$$ \mathbf{O} = \mathbf{H}\mathbf{W}_2^{\mathsf T}+\mathbf{b}_2$$
```
4维原始特征
    ↓ Linear：重新组合特征
5维中间结果
    ↓ ReLU：加入非线性、截断负数
5维隐藏表示
    ↓ Linear：再次组合隐藏特征
3维输出
```

```python
import torch
from torch import nn
mlp = nn.Sequential(
    nn.Linear(4, 5),  # 4 → 5：隐藏层
    nn.ReLU(),        # 非线性激活
    nn.Linear(5, 3),  # 5 → 3：输出层
)
x = torch.randn(32, 4)
output = mlp(x)
print(output.shape)  # torch.Size([32, 3])
```


## 残差连接

对于一层网络f(x_l),残差连接把输入x_l加到f(x_l)的输出

也就是最终fx输出是
x_{l+1}=x_l+ F(x_l) 
这时候网络有点像不是学习完全学习新的表示而是 而是原来的信息先保留，我这一层只需要学习应该在它上面改什么F(x_l)

这个结构出自resnet，解决深层网络的梯度的反向传播梯度爆炸问题，就是梯度传不回去多层情况下可以走残差的捷径传回来

## layernorm and batch norm

都是减去均值除标准差的操作，只不过一个的针对 特征维度的，一个是批次维度
增加训练稳定性的
 `LayerNorm`：明确指定“最后几个维度”一起归一化。`normalized_shape` 有几个维度，它就处理最后几个维度。
 - `norm = nn.LayerNorm(d)`
 - `nn.LayerNorm((N, d))`

`BatchNorm` 假设输入采用 channel-first并且有多个变体函数
batch norm在视觉，卷积网络常见，但是nlp transformer里面通常用 layernorm因为x，token序列长度通常都不一致，批次上norm没啥意义


现代transformer(比如ViT)在 输入sublayer之前norm(pre-norm)，经典教程一般在残差输出之后norm

## dropout 

![dropout2](/images/nn-basics-ad463729d07a.svg)
>MLP before and after dropout.[^5]

平时直接用就是 `nn.dropout` 其input/output形状不变, 从伯努利分布中采样, 按照p概率对 元素置0, 其余元素同时用$1/(1-p)$ 缩放保证期望不变


$$\boldsymbol{x}'= \begin{cases} 0, & \text{概率 }p,\\ \dfrac{\boldsymbol{x}}{1-p}, & \text{概率 }1-p, \end{cases} \qquad \mathbb{E}[\boldsymbol{x}']=\boldsymbol{x}$$
只在训练时候生效
就是对一些元素随机置为0，剩下元素缩放保证期望不变
通常层级比较高 一般一个功能性模块刚刚输出就用
用来正则化的 防止过拟合 




## tanh
[^3]
它把任意实数压缩到 $(-1,1)$：
- \(x\) 很大时，接近 \(1\)
- \(x\) 很小时，接近 \(-1\)
- \(x\approx0\) 时，\(\tanh(x)\approx x\)
在神经网络里，`tanh` 是逐元素激活函数，用来给 MLP 引入非线性。

[^1]: [PyTorch For Deep Learning — nn.Linear and nn.ReLU Explained \| by Ashwin Prasad \| Medium](https://ashwinhprasad.medium.com/pytorch-for-deep-learning-nn-linear-and-nn-relu-explained-77f3e1007dbb)

[^2]: [Fetching Title#hi96](https://docs.pytorch.org/docs/2.13/generated/torch.nn.Linear.html)

[^3]: [Fetching Title#trut](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html#tanh-function)

[^4]: [5.1. Multilayer Perceptrons — Dive into Deep Learning 1.0.3 documentation](https://d2l.ai/chapter_multilayer-perceptrons/mlp.html#tanh-function)

[^5]: [5.6. Dropout — Dive into Deep Learning 1.0.3 documentation](https://d2l.ai/chapter_multilayer-perceptrons/dropout.html#dropout)
