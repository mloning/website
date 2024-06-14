---
title: "Learning Deep Learning"
date: 2024-06-14T18:02:58+02:00
last_modified: .Lastmod
draft: true
---

* PyTorch Image Model library https://pypi.org/project/timm/

## Software design for deep Learning

FastAI `learner` class includes

* data loaders 
* preprocessing (labellers, data item transforms)

deep learning layer combines

* code 
* parameters 

https://www.kaggle.com/code/jhoward/which-image-models-are-best

http://matrixmultiplication.xyz/

blog by ML scientist focused on NLP https://www.ruder.io/

visualizing convolution layers https://arxiv.org/abs/1311.2901j

## Maths

https://explained.ai/matrix-calculus/
https://webspace.ship.edu/msrenault/geogebracalculus/derivative_intuitive_chain_rule.html

## Initialization/Normalization

All you need is a good init https://arxiv.org/abs/1511.06422
Fix up https://arxiv.org/abs/1901.09321
Transformer fixup https://paperswithcode.com/method/t-fixup

normalization during training:

batch norm
layer norm
instance norm
group norm

## Regularization

Dropout - set random subset of activations to zero

## Optimization

RMSProp - take variance of gradients from one batch to the next into account, higher variance means more uncertainty and smaller update
Momentum - exponentially moving average of previous batch gradients
Adam - combines RMSProp and Momentum

LR scheduling 
OneCycle super-conversion https://arxiv.org/abs/1708.07120
T-Fixup

## Batch size

* the bigger the mini-batch, the faster the training, but the less parameter updates

## Data augmentation

training-time augmentation
inference-time augmentation - a form of bagging, take samples to predict, augment, generate predictions for all augmented samples, average predictions

data-specific augmentations

image augmentations
* image translations (e.g. rotate, flip)
* crop
* random erase
* mix-based augmentation (e.g. random copy within/across items)

## Transformers

https://www.youtube.com/watch?v=wjZofJX0v4M
https://arxiv.org/pdf/2304.10557.pdf
https://web.stanford.edu/class/cs224n/readings/cs224n-self-attention-transformers-2023_draft.pdf
https://www.youtube.com/watch?v=kCc8FmEb1nY
https://arxiv.org/pdf/2207.09238.pdf
https://jalammar.github.io/illustrated-transformer/

## Distributed GPU computing

https://pytorch.org/tutorials/beginner/dist_overview.html
https://www.youtube.com/playlist?list=PL_lsbAsL_o2CSuhUhJIiW0IkdT5C2wGWj
torchrun

GPU memory stores both model parameters, other derived parameters like gradients, optimizer state, and data during training or inference

* Distributed Data-Parallel Training (DDP) is a widely adopted single-program multiple-data training paradigm. With DDP, the model is replicated on every process, and every model replica will be fed with a different set of input data samples. DDP takes care of gradient communication to keep model replicas synchronized and overlaps it with the gradient computations to speed up training.
* The FullyShardedDataParallel (FSDP) is a type of data parallelism paradigm which maintains a per-GPU copy of a model’s parameters, gradients and optimizer states, it shards all of these states across data-parallel workers. The support for FSDP was added starting PyTorch v1.11. 

