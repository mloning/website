import asyncio
import random
import time
from typing import Callable, Set

ALL_VALUES = [
    "apple",
    "banana",
    "cherry",
    "date",
    "elderberry",
    "fig",
    "pineapple",
    "strawberry",
]


async def discover_fast() -> str:
    """Simulates the asynchronous discovery of a random string value."""
    await asyncio.sleep(random.uniform(0.05, 0.1))
    return random.choice(ALL_VALUES)


async def discover_slow() -> str:
    """Simulates the asynchronous discovery of a random string value."""
    await asyncio.sleep(random.uniform(0.2, 0.3))
    return random.choice(ALL_VALUES)


async def discover_coro(
    id: int,
    func: Callable,
    missing_values: Set[str],
    discovered_counts: dict[str, int],
    lock: asyncio.Lock,
    exit_event: asyncio.Event,
    min_time: float,
) -> None:
    print(f"Discover coro: {id} started.")
    t0 = time.time()
    elapsed = 0.0

    while not (exit_event.is_set() and elapsed > min_time):
        async with lock:
            if len(missing_values) == 0:
                exit_event.set()

        item = await func()

        async with lock:
            discovered_counts[item] = discovered_counts.get(item, 0) + 1

            if item in missing_values:
                missing_values.remove(item)
                print(
                    f"Task: {id} discovered: '{item}'. Remaining: {missing_values} ({len(missing_values)})"
                )
                if len(missing_values) == 0:
                    remaining = min_time - elapsed
                    print(
                        f"All values discovered, continuing discovery for: {remaining:.2f}"
                    )
            else:
                print(f"Task: {id} discovered: '{item}', but already removed.")

        elapsed = time.time() - t0

    print(f"Discoverer {id}: All values discovered. Exiting.")


async def main():
    values_to_discover: Set[str] = set(ALL_VALUES[:])
    print(f"Initial values to discover: {values_to_discover}")

    discovery_counts: dict[str, int] = {}

    lock = asyncio.Lock()
    exit_event = asyncio.Event()
    min_time = 5.0  # seconds
    max_time = 10.0  # seconds

    kwargs = dict(
        missing_values=values_to_discover,
        discovered_counts=discovery_counts,
        lock=lock,
        exit_event=exit_event,
        min_time=min_time,
    )
    coros = [
        discover_coro(id=1, func=discover_fast, **kwargs),
        discover_coro(id=2, func=discover_slow, **kwargs),
    ]
    tasks = [asyncio.create_task(coro) for coro in coros]

    try:
        await asyncio.wait_for(asyncio.gather(*tasks), timeout=max_time)
        print("\n✅ All tasks finished within the time limit.")
    except asyncio.TimeoutError:
        print(f"\n❌ Process timed out after {max_time}s.")
        print("Cancelling running tasks...")
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
    print(f"\nDone. Final values to discover: {values_to_discover}")
    print(f"Discovery event counts: {discovery_counts}")


if __name__ == "__main__":
    asyncio.run(main())
