---
title: "Dynamically create code in Python"
date: 2025-08-29T23:25:57+02:00
last_modified: .Lastmod
draft: true
---

## Dynamically create class constructor (init)

pattern inspired by:

- https://github.com/heidelbergcement/hcrystalball/blob/master/src/hcrystalball/wrappers/_base.py
- https://ericmjl.github.io/blog/2025/8/23/wicked-python-trickery-dynamically-patch-a-python-functions-source-code-at-runtime/
- https://philip-trauner.me/blog/post/python-tips-dynamic-function-definition

* preferable CodeType replace method, but only available for Python >=3.8 https://bugs.python.org/issue37032
* ideally, we would add minor extensions to unify parameter names (e.g. `sp` for seasonality, `n_jobs` for multiprocessing)?
* can we also dynamically update docstring?

```python
import inspect
from types import FunctionType
from fbprophet import Prophet
from sktime.forecasting.base._base import BaseForecaster

def _get_param_dict(signature):
    return {
        p.name: p.default if p.default != inspect.Parameter.empty else None
        for p in signature.parameters.values()
        if p.name != "self" and p.kind != p.VAR_KEYWORD and p.kind != p.VAR_POSITIONAL
    }

def _get_params(func):
    signature = inspect.signature(func)
    return _get_param_dict(signature)

def create_init(model_cls):
    """Decorator to dynamically create init function based on wrapped `model_cls`"""

    def new_init(base_init):
        # combine params from wrapper class and wrapped model
        params = _get_params(model_cls.__init__)
        params.update(_get_params(base_init))

        # compile function code from string representation
        assignments = "; ".join([f"self.{name} = {name}" for name in params.keys()])
        string = f'def __init__(self, {", ".join(params.keys())}): {assignments}'
        code = compile(string, "<string>", "exec")

        return FunctionType(code.co_consts[0], base_init.__globals__, name="__init__", argdefs=tuple(params.values()))

    return new_init

# create new class using dynamic init creator
class ProphetForecaster(BaseForecaster):
    """Test docstring"""

    @create_init(Prophet)
    def __init__(a=1):
        pass

print(ProphetForecaster.__init__)

f = ProphetForecaster()
print(f.get_params())
```
