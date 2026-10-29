---
title: "Designing ML Libraries"
date: 2026-10-29T09:36:53+01:00
draft: true
tags: [ml]
---

-
- 2 types of ML model constructor/init hyper-parameters
  - runtime (e.g. `n_jobs`, device GPU/CPU): set at init, used in fit, can change after fit (at load/predict)
  - model definition (e.g. number of layers): set at init, used in fit and predict, cannot change after fit
