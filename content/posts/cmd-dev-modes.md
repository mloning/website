---
title: "Simulating application runs"
date: 2026-02-01T21:59:00+01:00
draft: true
---

Before running some application or command, we often want to first simulate what the application would do, to understand the consequences of the command execution.

This is useful when you want to verify that everything runs as expected before applying a state change.
For example, we may want to understand which files would deleted by a command before actually deleting them.
The simulation in this example is usually called a dry run.
But there are other ways to simulate application runs, for example fast development runs which execute the overall application workflow but may skip or shorten long-running stage.

## Why simulating application runs?

The purpose is usually simple:

- **Understand** what will happen when running an application in a certain situation,
- **Test** an application, at least partly, by skipping or mocking the state-changing "write" operations while running the "read" operations,
- **Test** an application by running key workflows

In deep learning, for example, [Lightning](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.params.fast_dev_run) provides a `fast-dev-run` flag. It runs a few steps of training and validation to ensure the code won't crash after five hours of training due to a silly typo in the logging code.

Common patterns include:

- `--dry-run` for CLI tools.
- `--skip-upload` to avoid updating a database or remote storage.

Sometimes, it is even safer to make the dry run the default. You then require an explicit flag like `--no-dry-run` or `--yes` to actually trigger state changes.

### The downsides

The main issue with dry runs is that they often lead to **imperfect simulations**. If the dry-run path in your code isn't representative of the critical execution path, it won't reveal much. You can also run into race conditions: the state might change between the time you ran the dry run and the time you applied the actual change.

Architecturally, it also "pollutes" the codebase. You often end up with `if dry_run:` conditionals scattered throughout your logic, which complicates the flow.

### Planning vs. Execution

A cleaner alternative is to separate the **planning** and **execution** steps. This is the approach taken by tools like Terraform (`terraform plan` followed by `terraform apply`).

By separating the two, you avoid handling dry-run logic throughout your core functions. Immediate execution simply becomes `execute(plan())`.

````python
from pathlib import Path

def plan(dir: Path, pattern: str) -> list[Path]:
    # Only read state
    files = list(dir.glob(pattern))
    return files

def execute(files: list[Path]) -> None:
    # Only write state
    for file in files:
        file.unlink()

# Usage
files = plan(dir=Path("./tmp"), pattern="*.txt")

if dry_run:
    print(f"Would remove: {files}")
else:
    execute(files)

---

Options for development, debugging or testing everything runs as expected before actually applying some state change.

- `fast-dev-run` to run an application much faster than it would usually take (e.g. in deep learning model training using [Lightning](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.params.fast_dev_run))
- `--dry-run`
- `--skip-upload` to avoid state change in database

- default should sometimes be the dry run instead of the actual run, so often better have a flag that toggles on the actual state changes while no state changes are applied by default (e.g. `--no-dry-run` or `--yes` flag)

purpose

- simulate what would happen
  - understand what will happen
  - test what will happen (test all operations that read state while mocking/skipping those that would write/change the state)
  - debug code

inevitably, imperfect simulation

- important to make the fast-run or dry-run path in the code representative, to test the critical code paths, otherwise it will not reveal much
- can still have a race condition where the external state changes between the situation in which you ran the dry run and the situation where you applied the actual change

downside:

- pollutes code base, often complicates code as you now have to handle the dry-run condition in every code path

- complete separate planning and execution steps (e.g. `terraform plan`, then `terraform apply` on the generated plan)
- avoids race conditions
- avoids handling dry run throughout the code by separating out everything into planning and execution
- immediate execution just becomes `execute(plan())`

```python
def plan(dir: Path, pattern: str) -> list[Path]:
    files = dir.glob(pattern)
    return files

def execute(files: list[Path]) -> None:
    for file in files:
        file.unlink()

files = plan(dir=Path(tmp_dir), pattern="*.txt")
if dry_run:
    print(f"Would remove: {files}")
else:
    execute(files)
````

- also related to dev or staging environments where the stage changes is applied by the entire environment is used for testing
- once everything looks good in the staging environment, the actual state change is applied in the production environment
- requires setting up a full dev environment but not too hard to do with infrastructure-as-code (e.g. terraform)

Related links:

- https://www.gresearch.com/news/in-praise-of-dry-run/
- https://news.ycombinator.com/item?id=27263136
- https://news.ycombinator.com/item?id=46840612
