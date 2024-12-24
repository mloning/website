---
title: "Logging in a multiprocessing context in Python"
date: 2024-12-02T09:38:37+01:00
last_modified: .Lastmod
draft: false
---

Configuring loggers in a Python application with multiprocessing isn't straightforward.

If you're new to logging in Python, there's a [basic tutorial](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial).

Some complications are that

- each process may require a different logging configuration, for example to include contextual information about the process in the log messages
- common libraries like [joblib] [don't propagate loggers] from the main process to each child process
- logging should work consistently when running in multiple, parallel processes and when running in a single, sequential process (e.g. when debugging)

[joblib]: https://joblib.readthedocs.io/en/stable/
[don't propagate loggers]: https://github.com/joblib/joblib/issues/1017#issuecomment-711723073

Below is a hacky but simple solution, which uses a context manager to resets the root logger to an initial, empty state before launching each child process, so that each process can separately reconfigure the logger and then restores the root logger when exiting the context.
This is hacky because it makes certain assumptions about what constitutes the state of the root logger and changes that state without using the common interfaces to configure loggers.

When running this from a [Python file](https://github.com/mloning/website/tree/main/scripts/logging-in-python-multiprocessing.py), this gives me the desired results for both single and multiple processes.

For a single process:

```bash
python scripts/logging-in-python-multiprocessing.py --n-jobs=1
```

> Running: n_jobs=1 ...  
> 2024-12-24 14:04:12,762 INFO MainProcess 847 root process=main Starting ...  
> 2024-12-24 14:04:12,763 DEBUG MainProcess 847 root process=1 Configured logger for process: 1  
> 2024-12-24 14:04:12,763 DEBUG MainProcess 847 root process=1 Running process: 1 ...  
> 2024-12-24 14:04:12,865 DEBUG MainProcess 847 root process=1 Done.  
> 2024-12-24 14:04:12,866 DEBUG MainProcess 847 root process=2 Configured logger for process: 2  
> 2024-12-24 14:04:12,866 DEBUG MainProcess 847 root process=2 Running process: 2 ...  
> 2024-12-24 14:04:12,968 DEBUG MainProcess 847 root process=2 Done.  
> 2024-12-24 14:04:12,968 DEBUG MainProcess 847 root process=3 Configured logger for process: 3  
> 2024-12-24 14:04:12,968 DEBUG MainProcess 847 root process=3 Running process: 3 ...  
> 2024-12-24 14:04:13,069 DEBUG MainProcess 847 root process=3 Done.  
> 2024-12-24 14:04:13,070 INFO MainProcess 847 root process=main Done.

For multiprocessing, using 3 parallel processes:

```bash
python scripts/logging-in-python-multiprocessing.py --n-jobs=3
```

> Running: n_jobs=3 ...  
> 2024-12-24 14:04:38,753 INFO MainProcess 1715 root process=main Starting ...  
> 2024-12-24 14:04:38,916 DEBUG LokyProcess-1 1718 root process=1 Configured logger for process: 1  
> 2024-12-24 14:04:38,916 DEBUG LokyProcess-1 1718 root process=1 Running process: 1 ...  
> 2024-12-24 14:04:38,921 DEBUG LokyProcess-2 1719 root process=2 Configured logger for process: 2  
> 2024-12-24 14:04:38,921 DEBUG LokyProcess-2 1719 root process=2 Running process: 2 ...  
> 2024-12-24 14:04:38,924 DEBUG LokyProcess-3 1720 root process=3 Configured logger for process: 3  
> 2024-12-24 14:04:38,924 DEBUG LokyProcess-3 1720 root process=3 Running process: 3 ...  
> 2024-12-24 14:04:39,021 DEBUG LokyProcess-1 1718 root process=1 Done.  
> 2024-12-24 14:04:39,023 DEBUG LokyProcess-2 1719 root process=2 Done.  
> 2024-12-24 14:04:39,029 DEBUG LokyProcess-3 1720 root process=3 Done.  
> 2024-12-24 14:04:39,036 INFO MainProcess 1715 root process=main Done.

There are less hacky, more complicated solutions which may be preferred depending on the application, for example using a `multiprocessing.Queue`, as described [here](https://docs.python.org/3/howto/logging-cookbook.html#logging-to-a-single-file-from-multiple-processes).

Note that this solution also slightly abuses the `logging.Filter` interface. Filters are meant to drop messages before they are being emitted, not change the message itself.
However, this use of filters is also suggested in the Python [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html#adding-contextual-information-to-your-logging-output).

For more discussions on how to implement logging in multiprocessing with [joblib], see their [issue #1017](https://github.com/joblib/joblib/issues/1017).
An alternative to the context manager would be to change how [joblib] initializes each child process, but this isn't exposed through a public interface, see e.g. [issue #381](https://github.com/joblib/joblib/issues/381).

```python
import argparse
import logging
import time
from contextlib import contextmanager
from typing import Any, Iterator

from joblib import Parallel, delayed


class PrefixFilter(logging.Filter):
    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = f"process={self.prefix} {record.msg}"
        return True


def configure_logger(process_name: str, level: str) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(processName)s %(process)d %(name)s %(message)s",
    )
    logger = logging.getLogger()
    logger.filters = [PrefixFilter(prefix=process_name)]
    logging.debug(f"Configured logger for process: {process_name}")


@contextmanager
def restore_root_logger() -> Iterator[None]:
    logger = logging.getLogger()
    state = remove_logger_state(logger=logger)
    try:
        yield
    finally:
        set_logger_state(logger=logger, state=state)


def remove_logger_state(logger: logging.Logger) -> dict[str, Any]:
    init_state = {"handlers": [], "formatters": [], "filters": []}
    state = {}
    for attr in init_state.keys():
        if hasattr(logger, attr):
            state[attr] = getattr(logger, attr)
    set_logger_state(logger=logger, state=init_state)
    return state


def set_logger_state(logger: logging.Logger, state: dict[str, Any]) -> None:
    for attr, value in state.items():
        setattr(logger, attr, value)


def run_in_parallel(process_name: str, log_level: str) -> str:
    configure_logger(process_name=process_name, level=log_level)
    logging.debug(f"Running process: {process_name} ...")
    time.sleep(0.1)
    logging.debug("Done.")
    return process_name


def test(n_jobs: int) -> None:
    print(f"Running: {n_jobs=} ...")
    time.sleep(0.5)
    configure_logger(process_name="main", level="INFO")
    parallel = Parallel(n_jobs=n_jobs, backend="loky")
    logging.info("Starting ...")
    n_tasks = 3
    with restore_root_logger():
        results = parallel(
            delayed(run_in_parallel)(process_name=str(i), log_level="DEBUG")
            for i in range(1, n_tasks + 1)
        )
    logging.info("Done.")
    print(results)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-jobs", required=True, type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    test(n_jobs=args.n_jobs)


if __name__ == "__main__":
    main()
```
