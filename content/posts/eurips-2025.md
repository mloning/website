---
title: "Eurips 2025"
date: 2025-12-02T11:33:55+01:00
draft: true
---

I went to EurIPS 2025 in Copenhagen, the first edition of the European version of NeurIPS.
Here are my notes, mostly focusing on time series analysis, EEG and other biosignals due to my current work.

Tuesday (ELLIS UnConference)

- Klaus-Rudolf Kladny "Aligning Generative Models with Reality", causal backtracking
- Shih-Chii Liu (ETH and University of Zurich): Brain-inspired dynamic sparsity for neuromorphic AI; voice commands, low-power speech decoding, end-to-end hardware/software systems
- Nasir Ahmad (Radboud University Nijmegen): Two steps forward and no steps back: Training neural networks in noisy hardware without backward passes; starting with observation of relative cheapness of neural network inference to training, weight/layer/node perturbation learning as alternative to back propagation, utilizing information from multiple forward passes for each training update; utilizing gradient information to inform search direction; would allow perturbing models at inference and aggregating results across servers (decentralised, federated training); however, backward pass is only about twice as expensive as forward pass;
- Learning Interpretable Hierarchical Dynamical Systems Models from Time Series Data (poster), modelling user specific parameters for time series, with applications on EEG data ([repo](https://github.com/DurstewitzLab/HierarchicalDSR))

Wednesday (first conference day)

- Is Limited Participant Diversity Impeding EEG-based Machine Learning? ([paper](https://arxiv.org/abs/2503.13497))
- Framework for Emotion Evaluation using Physiological Signal Data ([repo](https://github.com/alchemy18/FEEL))
- Brain Capture, easy-to-use, medical wet-electrode EEG device ([website](https://www.braincapture.dk/))
- Adaptive Bayesian Intelligence and the Road to Sustainable AI by Emtiyaz Khan; keynote on Bayesian Learning Principles to keep memory of most important examples during training and improve information
- NEED: Cross-Subject and Cross-Task Generalization for Video and Image Reconstruction from EEG Signals (presented at NeurIPS, [paper](https://openreview.net/pdf?id=L3aEdxJMHl))
- From AI Research to Startups workshop; start-up/prototyping tools: https://replit.com/, https://n8n.io/, https://lovable.dev/, https://v0.app/, https://github.com/obra/superpowers

Concepts to investigate further:

- fixed point iterations in state-space models and RNNs