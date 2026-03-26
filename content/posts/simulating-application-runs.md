---
title: "Simulating application runs"
date: 2026-03-26T20:59:00+01:00
draft: false
---

## Dry runs

Before running a program for real, we sometimes first want to simulate the outcome, a dry run without actually changing anything, to better understand the consequences of running the application.
This is particularly useful when the program involves state changes that are difficult to revert.
For example, writing to a database, deleting files, or provisioning cloud resources.

Dry runs allow us both to:

- Understand what will happen if we run run the program,
- Test the program – at least partly, by skipping the state-changing operations while running everything else.

A common CLI pattern for dry runs is to allow for a `--dry-run` option.
Sometimes it's safer to make the dry run the default.
You then require an explicit flag like `--no-dry-run` or `--yes` to actually trigger the state changes.

The main issue with dry runs is that they often lead to imperfect simulations.
If the dry-run path in your code isn't representative of the critical execution path, it won't reveal much.
You can also run into race conditions: the state might change between the time you ran the dry run and the time you applied the actual change.
The simulation is only valid if the environment does not change.

Adding a dry run path to your program also tends to pollute the codebase.
You often end up with `if dry_run:` conditionals scattered throughout your code.

## Planning vs. execution

An interesting alternative is to separate the planning and the execution step.
Immediate execution simply becomes `execute(plan())`.
This is, for example, the approach taken tools like [Terraform](https://developer.hashicorp.com/terraform) (`terraform plan` followed by `terraform apply`).

By separating the two, you avoid handling dry-run logic throughout your code.

As an example, suppose we want to write a program that deletes files.
Here's what this would look like in Python:

```python
from pathlib import Path

def plan(dir: Path, pattern: str) -> list[Path]:
    # Read state
    files = list(dir.glob(pattern))
    return files

def execute(files: list[Path]) -> None:
    # Change state
    for file in files:
        file.unlink()

# usage
files = plan(dir=Path("./tmp"), pattern="*.txt")
print(f"Plan to remove: {files}")
if not is_dry_run:
    execute(files)
```

## Fast dev runs

A related idea are fast development runs.
Some programs take a long time to run.
But during development, we still want to iterate quickly, while at the same time simulating the full program execution.

For example, in machine learning, because training a model tends to be slow, tools like [Lightning] provide a `--fast-dev-run` option, which run the program much faster than it would usually take, by just running a few steps of the training loop to ensure the code works but without waiting for convergence.

[Lightning]: https://lightning.ai/

## Staging environments

Another way to simulate programs is to set up a completely separate staging environment.
The staging environment recreates the entire state of our application (e.g. the database), so that we can run our program exactly as in production but without actually changing the production environment.
Once everything works as expected in the staging environment, we can deploy the application into production.

Again, the simulation is valid only if the staging and production environments are identical.
This approach also requires managing multiple environments, however this has become much simpler with infrastructure-as-code tools.

## Related links

A lot of the ideas above were discussed in the [In Praise of --dry-run](https://www.gresearch.com/news/in-praise-of-dry-run/) blog post and the related [HackerNews thread](https://news.ycombinator.com/item?id=27263136) (May 2021) and [HackerNews thread](https://news.ycombinator.com/item?id=46840612) (January 2026).

On dark launching and shadow testing, to simulate new features in production, but without exposing the outcome to the users:

- [Dark Launching](https://martinfowler.com/bliki/DarkLaunching.html) (Martin Fowler)
- [Feature Toggles aka Feature Flags](https://martinfowler.com/articles/feature-toggles.html) (Martin Fowler)
- [The only guide to dark launching you’ll ever need](https://launchdarkly.com/blog/guide-to-dark-launching/)
- [Shadow Testing](https://microsoft.github.io/code-with-engineering-playbook/automated-testing/shadow-testing/) (Microsoft blog post)
