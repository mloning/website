---
title: "Command test run modes"
date: 2026-02-01T21:59:00+01:00
draft: true
---

Executing an application in some development mode without actually changing any state or making any changes

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

- polutes code base, often complicates code as you now have to handle the dry-run condition in every code path

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
```

- also related to dev or staging environments where the stage changes is applied by the entire environment is used for testing
- once everything looks good in the staging environment, the actual state change is applied in the production environment
- requires setting up a full dev environment but not too hard to do with infrastructure-as-code (e.g. terraform)

Related links:

- https://www.gresearch.com/news/in-praise-of-dry-run/
- https://news.ycombinator.com/item?id=27263136
- https://news.ycombinator.com/item?id=46840612
