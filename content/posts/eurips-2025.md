---
title: "Eurips 2025"
date: 2025-12-02T11:33:55+01:00
draft: false
---
I attended EurIPS 2025 in Copenhagen, the first edition of the European version of NeurIPS.
My notes are mainly about topics related to my current work, that is, time series analysis and biosignals.
## Tuesday (ELLIS UnConference)
ELLIS is a European research network for AI.

- Klaus-Rudolf Kladny "Aligning Generative Models with Reality", causal backtracking
- Shih-Chii Liu (ETH and University of Zurich): Brain-inspired dynamic sparsity for neuromorphic AI; voice commands, low-power speech decoding, end-to-end hardware/software systems
- Nasir Ahmad (Radboud University Nijmegen): Two steps forward and no steps back: Training neural networks in noisy hardware without backward passes; starting with observation of relative cheapness of neural network inference to training, weight/layer/node perturbation learning as alternative to back propagation, utilizing information from multiple forward passes for each training update; utilizing gradient information to inform search direction; would allow perturbing models at inference and aggregating results across servers (decentralised, federated training); however, backward pass is only about twice as expensive as forward pass;
- Learning Interpretable Hierarchical Dynamical Systems Models from Time Series Data (poster), modelling user specific parameters for time series, with applications on EEG data ([repo](https://github.com/DurstewitzLab/HierarchicalDSR))
## Wednesday (first conference day)
- Is Limited Participant Diversity Impeding EEG-based Machine Learning? ([paper](https://arxiv.org/abs/2503.13497))
- Framework for Emotion Evaluation using Physiological Signal Data ([repo](https://github.com/alchemy18/FEEL))
- Brain Capture, easy-to-use, medical wet-electrode EEG device ([website](https://www.braincapture.dk/))
- Adaptive Bayesian Intelligence and the Road to Sustainable AI by Emtiyaz Khan; keynote on Bayesian Learning Principles to keep memory of most important examples during training and improve information
- NEED: Cross-Subject and Cross-Task Generalization for Video and Image Reconstruction from EEG Signals (presented at NeurIPS, [paper](https://openreview.net/pdf?id=L3aEdxJMHl))
- From AI Research to Startups workshop; generative AI tools for prototyping: https://replit.com/, https://n8n.io/, https://lovable.dev/, https://v0.app/, https://github.com/obra/superpowers
## Thursday
- Riemannian Flow Matching for Brain Connectivity Matrices ([repo](https://github.com/antoinecollas/DiffeoCFM))
- Sequence Modeling with Spectral Mean Flows ([paper](https://arxiv.org/abs/2510.15366))
- Sustainable, Low-Energy, and Fast AI Made in Europe by Sepp Hochreiter; keynote arguing we have reached diminishing returns for Transformer-based scaling and that there are more efficient solutions like his xLSTM model, and TiRex for time series forecasting
- https://eurips.cc/conference/posters/#poster:117226 (job opening with social science background)
- A Collectivist, Economic Perspective on AI by Micheal Jordan (keynote)
  - We should think about AI more in terms of economics (inter-personal relationships, incentives, contracts, markets, asymmetric information)
  - "Don't regulate the algorithm, regulate the equilibrium", game-theoretic analysis on which equilibria emerge under specific conditions, e.g. GDPR which he considers a failure because it sets a fixed level of privacy, not a minimum, and disproportionally favours large firms
  - Statistical contract theory, how should the FDA test new drugs? randomized control trials, principal (FDA) vs agent (pharmaceutical company), asymmetric information, concept of a statistical contract
  - Metrics for ML ecosystem, who knows more what a good metric would be for a hospital? hospital know better which metrics are good, but don't want to reveal them to the principal (health insurance, government), asymmetric information (see e.g. [paper](https://arxiv.org/abs/2402.14005))
  - Problematic use of large pretrained models for science where we are mainly interested in new, out-of-distriubtion cases on which pretrained models don't perform well
  - We should see AI/ML as an emerging engineering discipline, building on top of statistical/inferential, algorithmic and economic ideas; we should think about what problems we're trying to solve, instead of getting distracted by AI hype/aspirations; compare with emerging chemical and electrical engineering as a discipline building on prior ideas while having clear goals
- The Art of (Artificial) Reasoning by Yejin Choi (NeurIPS keynote, speaker's [website](https://yejinc.github.io/), [TedTalk](https://www.ted.com/talks/yejin_choi_why_ai_is_incredibly_smart_and_shockingly_stupid)); trade-offs between pretraining and reinforcement learning for reasonsing capabilities; her vision: (1) democratizing generative AI, "of humans, by humans and for humans"; (2) need for unconventional collaboration, data and algorithms, e.g. [The OpenThoughts Team](https://github.com/open-thoughts/open-thoughts); (3) art of artificial reasoning (pretraining, sequential fine tuning, reinforcement learning) requires more data and data that is not available on the internet (e.g. human knowledge and reasoning, simulations, theory of intelligence)
## Friday
- Learning long range dependencies through time reversal symmetry breaking ([paper](https://arxiv.org/abs/2506.05259))
- Uncertainty in the LLM era - Science, more than scale by Gaël Varoquaux (keynote)
  - As computer scientists, we should report trade-offs, including resource efficiency
  - Research fixation on scale disempowers a large group of GPU-poor researchers, compute-rich actors set social norms for more compute
  - Bubble dynamics in AI, based on promises rather than results
  - Research and technology is not value-neutral (see contextual values in https://plato.stanford.edu/entries/scientific-objectivity/)
  - Uncertainty quantification for black-box models, strictly proper scoring rules, epistemic (model-based) vs aleatoric (inherent in data generating process or available data) uncertainty, epistemic loss decomposition into calibration and grouping loss
## Workshops (weekend)
Multimodal Representation Learning for Healthcare workshop ([website](https://multimodal-rep-learning-for-health.github.io/))
- Multimodal Alignment for Synthetic Clinical Time Series
- iMML: A Python package for multi-modal learning with incomplete data ([repo](https://github.com/ocbe-uio/imml)); related [paper](https://arxiv.org/abs/2302.12247) on redundancy estimation for multi-modal data; mostly limited to tabular data, but may be easy to extend to time series
- NAP: Attention-Based Late Fusion for Automatic Sleep Staging ([paper](https://multimodal-rep-learning-for-health.github.io/papers/10_NAP_Attention_Based_Late_Fu.pdf)), multi-modal EEG/EMG/EOG attention-basee modelling 

Workshop on Principles of Generative Modeling ([website](https://sites.google.com/view/prigm-eurips-2025/home))
- FrèqFlow: Long-term forecasting using lightweight flow matching
- GRITS: Iterative Graphical Imputation for Multivariate Time Series (Samuel Joray)
- Diffusion Language Models: Problem Solving and Reasoning (Anej Svete); 
	- Transformer-based masked diffusion models with multiple denoising/demasking steps
	- In training, iteratively mask input text using a special mask token, and learn steps to demask text
	- For inference, pass prompt plus space with mask tokens for response, with early stopping; iterating over a two-step process: (1) use predictor/denoiser model component to predict tokens for all masks, and then (2) planner component to decide which token(s) to unmask first (e.g. based on predictors confidence), iterating until all tokens are demasked or some other stopping criterion is met
	- Padded, looped transformers, which include padded tokens in input sequence, are closely related to masked diffusion models
	- Masked diffusion models can do sequential chain-of-thought reasoning, but also enable parallel reasoning
## Interesting ideas
- Fixed point iterations in state-space models (SSM) and RNNs
- Flow matching
- Diffusion models, score matching
- Continual test-time adaptation/learning, which updates a pretrained model on a non-stationary stream of unlabelled test data to handle changing distribution shifts during deployment ([paper](https://arxiv.org/pdf/2006.10726), [paper](https://openaccess.thecvf.com/content/CVPR2022/papers/Wang_Continual_Test-Time_Domain_Adaptation_CVPR_2022_paper.pdf))