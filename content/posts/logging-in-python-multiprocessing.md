---
title: "Logging in Python Multiprocessing"
date: 2024-12-02T09:38:37+01:00
last_modified: .Lastmod
draft: true
---

- overview of logging flow: https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
- logging to same file from multiple processes: https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes
-
- https://github.com/joblib/joblib/issues/381
- https://github.com/joblib/joblib/issues/1017

```python
import logging
from joblib import Parallel, delayed
import time
from contextlib import contextmanager
from copy import deepcopy


class MultiProcessFilter(logging.Filter):

    def __init__(self, prefix: str):
        self.prefix = prefix

    def filter(self, record):
        record.msg = f"process={self.prefix} {record.msg}"
        return True


def configure_logger(i):
    # logging.basicConfig(level="DEBUG", filename="test.log", format="%(asctime)s %(levelname)s %(processName)s %(process)d %(name)s %(message)s")
    logging.basicConfig(level="DEBUG", format="%(asctime)s %(levelname)s %(processName)s %(process)d %(name)s %(message)s")
    logger = logging.getLogger()

    # slightly abusing filters here; but see cookbook https://docs.python.org/3/howto/logging-cookbook.html#adding-contextual-information-to-your-logging-output
    # when using multiple handlers, attaching the filter to all of them will change the log record multiple times
    logger.filters = [MultiProcessFilter(prefix=i)]

    logging.info(f"Configured logger for parallel process: {i}")


def reconfigure_logging():
    logger = logging.getLogger()

    init_state = {
        "handlers": [],
        "formatters": [],
        "filters": []
    }
    attrs = init_state.keys()

    # copy state
    state = {}
    for attr in attrs:
        if hasattr(logger, attr):
            state[attr] = getattr(logger, attr)

    # reset logger to init state
    for attr in attrs:
        setattr(logger, attr, [])

    try:
        yield

    finally:
        # reset to previous state
        for attr, value in state.items():
            setattr(logger, attr, value)


def run_in_parallel(i):
    configure_logger(i)
    logging.info(f"Running process: {i} ...")
    time.sleep(0.1)
    logging.info("Done.")
    return i

def test(n_jobs):
    print(f"======> Running: {n_jobs=} ...")
    time.sleep(.5)
    configure_logger(i="main")
    logging.info("Starting ...")
    with reconfigure_logging():
        with Parallel(n_jobs=n_jobs, backend="loky") as parallel:
            results = parallel(delayed(run_in_parallel)(i) for i in range(1, 4))
    logging.info("Done.")
    print(results)

    root = logging.getLogger()
    assert len(root.handlers) == 1


test(n_jobs=1)
test(n_jobs=-1)
```
