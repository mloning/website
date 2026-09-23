---
title: "New"
date: 2026-09-23T22:49:02+02:00
draft: true
tags: [ml, math]
---

One mathematical illustration I really like is using Condorcet’s Jury Theorem to show why ensembles of weak learners are effective.

It uses basic probability to show that combining independent, slightly accurate classifiers drives the overall error rate toward zero as the ensemble grows.

1. Problem Formulation

Suppose we have a classical binary classification problem, with classes $0$ and $1$, and independent and identically distributed (i.i.d.) samples.
To try to solve the problem, we can train a classifier.
Our classifier has an accuracy $p$, where $p > 0.5$, meaning the algorithm performs better than a random coin toss, but may not be very good.

Let $N$ be the number of independent classifiers (learners) in the ensemble, where $N$ is an odd integer.
Each classifier $h_i(x)$ has an accuracy $p$, where $p > 0.5$ (meaning each learner performs slightly better than a random coin toss).
The ensemble output $\hat{y}$ is determined by a majority vote:$$\hat{y} = \text{mode}\Big(\{h_1(x), h_2(x), \dots, h_N(x)\}\Big)$$

2. Mathematical Proof

The ensemble makes an incorrect prediction if and only if a majority of the individual classifiers make a mistake.

Let $X$ be the random variable representing the number of correct classifiers in the ensemble.

Since each classifier is independent and succeeds with probability $p$, $X$ follows a Binomial distribution:$$X \sim \text{Binomial}(N, p)$$

The ensemble succeeds if at least $k = \frac{N+1}{2}$ classifiers are correct.

Therefore, the probability that the ensemble predicts correctly, denoted as $P_{\text{ensemble}}$, is the cumulative binomial sum:

$$P_{\text{ensemble}} = P\left(X \ge \frac{N + 1}{2}\right) = \sum_{k = \frac{N+1}{2}}^{N} \binom{N}{k} p^k (1 - p)^{N - k}$$

3. Asymptotic Limit

By the Law of Large Numbers, as $N \to \infty$, the sample proportion of correct classifiers $\frac{X}{N}$ converges almost surely to its expected value, $p$:

$$\lim_{N \to \infty} \frac{X}{N} = p$$Since $p > 0.5$, the threshold $\frac{N+1}{2N} \approx 0.5$ lies strictly below $p$.
Therefore, as $N$ grows large, the probability mass shifts entirely above the majority threshold:

$$\lim_{N \to \infty} P_{\text{ensemble}} = 1$$

Conversely, the error probability of the ensemble $E_{\text{ensemble}} = 1 - P_{\text{ensemble}}$ vanishes completely:

$$\lim_{N \to \infty} E_{\text{ensemble}} = 0$$

4. Concrete Example

Suppose you train individual decision trees (weak learners) that each achieve an accuracy of $p = 0.60$ (60% accurate, 40% error rate).
Single Learner ($N = 1$): Accuracy = $60\%$
Ensemble of $N = 25$ learners:$$P_{\text{ensemble}} = \sum_{k=13}^{25} \binom{25}{k} (0.6)^k (0.4)^{25-k} \approx 0.846 \quad (\text{84.6\% accuracy})$$Ensemble of $N = 101$ learners:$$P_{\text{ensemble}} = \sum_{k=51}^{101} \binom{101}{k} (0.6)^k (0.4)^{101-k} \approx 0.979 \quad (\text{97.9\% accuracy})$$

Key Assumptions & Real-World Caveats

The proof relies on two strict conditions:$p > 0.5$:

- Individual models must be better than random guessing. If $p < 0.5$, $P_{\text{ensemble}} \to 0$ as $N \to \infty$.
- Independence: Errors made by classifiers must be uncorrelated.In practice (like in Random Forests), individual trees trained on the same dataset are never perfectly independent.
  Techniques like bagging (bootstrap aggregation) and subspace sampling (selecting random subsets of features at each split) are designed explicitly to reduce this inter-tree correlation, keeping the ensemble behavior as close to this ideal proof as possible.
