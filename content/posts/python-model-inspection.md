---
title: "Python Model Inspection"
date: 2025-08-16T12:03:32+02:00
last_modified: .Lastmod
draft: true
---

## Problem

- building a Python ML framework for composing, training, evaluating and comparing ML/AI models
- based on torch, lightning and scikit-learn.
- Hydra for configuration
- MLflow for experiment tracking

During development and model training, I often want to inspect models, to understand how data is being transformed and how training progresses.
This usually involves adding auxilliary code into the models for logging and visualizing parameters and data.
This code is usually deep inside models, and specific to the algorithm we're trying to inspect.

While for production runs, we want to skip model inspection, during development and training we want to easily toggle it on.

- how can we organize this cross-cutting code? (aspect-oriented programming)
- how can I easily switch between code paths at all levels, without having to pass some parameter down into every function?
- how can we easily toggle model inspection on and off?
- could we have more fine-grained control over which model parts we want to inspect without always turning on model inspection everywhere?
- how can we store and display model inspection output?

```python
features = ...
if is_inspection():
  inspect_features(features, output_path=???)
```

```python
features = ...
if_inspect(inspect_features(features))
```

```python
# decorator
def inspect(fn: Callable, *args, **kwargs) -> Callable:
  if is_enabled():
    output_path = get_inspect_path()
    return fn(*args, **kwargs, path=output_path)

@inspect
def inspect_features(features: np.ndarray, output_path: Path) -> None:
  pass

def complicated_algorithm() -> None:
  feature ...
  inspect_features(features)
```

## Ideas

- if-statements based on env variable, but how to handle other shared functionality (e.g. common output directory)
- custom logging level (e.g. `INSPECT` between `INFO` and `DEBUG`) but inspection seems orthogonal to logging level, since logging encompasses many aspects, not just modelling
- Hydra + env variables
- global singleton `inspector` class (taking care of boolean toggle and other context like output path)
- tags to enable fine-grained control which inspection code to turn on (tag matching)
- decorators but defined where inspection function is defined, not where it's called
