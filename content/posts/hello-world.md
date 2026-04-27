---
title: "Hello World — Obsidian Syntax Showcase"
date: 2026-04-27
draft: false
showtoc: true
tocopen: true
tags: ["meta", "test"]
categories: ["general"]
math: true
summary: "First post demonstrating all supported Obsidian-flavored markdown syntax for this blog."
---

## Welcome

This is the first post — a comprehensive test of every Obsidian syntax feature that `obs2hugo.py` handles. Write freely in Obsidian; the sync pipeline converts everything automatically.

## Math

Inline math: the Bellman equation $V(s) = \max_a \left[ R(s,a) + \gamma \sum_{s'} P(s'|s,a) V(s') \right]$ is central to RL.

Block math — the policy gradient theorem:

$$
\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta} \left[ \nabla_\theta \log \pi_\theta(a|s) \cdot Q^{\pi_\theta}(s,a) \right]
$$

Also works with `\(...\)` inline notation: \(E = mc^2\), and `\[...\]` blocks:

\[
\mathcal{L}(\theta) = -\sum_{i} y_i \log \hat{y}_i
\]

## Code

```python
import numpy as np

def policy_gradient(env, policy, lr=0.01, episodes=1000):
    """REINFORCE algorithm."""
    for ep in range(episodes):
        states, actions, rewards = [], [], []
        state = env.reset()
        done = False
        while not done:
            action = policy.sample(state)
            next_state, reward, done, _ = env.step(action)
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            state = next_state
        # Compute returns and update
        returns = compute_returns(rewards, gamma=0.99)
        policy.update(states, actions, returns, lr)
    return policy
```

## Wikilinks

This is a link to [reinforcement-learning-basics](/posts/reinforcement-learning-basics/) and here's one with display text: [the attention mechanism](/posts/transformer-attention/).

Cross-references work too: see [hello-world](/posts/hello-world/) for the intro.

## Embeds

Here's an embedded image:

![loss-curve](/images/loss-curve.png)

And a diagram:

![architecture-overview](/images/architecture-overview.svg)

## Callouts

> [!NOTE]
> This blog uses a dual-branch architecture. Write on `main`, deploy from `page`.

> [!TIP]
> Use `$...$` for inline math and `$$...$$` for display math. No special escaping needed.

> [!WARNING]
> Literal dollar signs like $5.00 or $10M should be written as `\$5.00` to avoid being parsed as math delimiters.

> [!CAUTION]
> Wikilinks like `[page](/posts/page/)` are auto-converted during sync. Do not use standard markdown links for internal posts — use wikilinks.

## Footnotes

Reinforcement learning has deep roots in optimal control theory[^1] and Markov decision processes[^2].

[^1]: Bellman, R. (1957). *Dynamic Programming*. Princeton University Press.
[^2]: Sutton, R. S., & Barto, A. G. (2018). *Reinforcement Learning: An Introduction*. MIT Press.

## Obsidian Comments

<!-- This section is a draft note visible only in Obsidian — not published. -->

The published post will not show the comment above.

## Standard Markdown Links

For external references, use standard markdown:

- [Hugo Documentation](https://gohugo.io/documentation/)
- [PaperMod Theme](https://adityatelange.github.io/hugo-PaperMod/)
- [Lilian Weng's Blog](https://lilianweng.github.io/) — style reference for this blog

## Tables

| Algorithm | Type | On-policy | Model-free |
|:--|:--|:--|:--|
| Q-learning | Value-based | No | Yes |
| SARSA | Value-based | Yes | Yes |
| REINFORCE | Policy gradient | Yes | Yes |
| PPO | Actor-critic | Yes | Yes |
| SAC | Actor-critic | No | Yes |
