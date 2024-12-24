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
