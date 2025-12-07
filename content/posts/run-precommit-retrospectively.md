---
title: Run pre-commit retrospectively on all changed files in a PR
date: 2020-10-02T16:10:57+02:00
draft: false
---
When I was developing [sktime], we had set up automated checks for printing and formatting only after some time. Rather than fixing our entire code base in one go, we decided to roll out the changes slowly, and only enforce them  for the changed files on a PR.

New contributors would sometimes forget to set up [pre-commit] and open a PR without following the linting and formatting rules.

In cases like this, you cannot run pre-commit on all the files in the repo.
Instead, you need to run pre-commit retrospectively only on the changed files in the PR from a `<feature-branch>` into `main`. 
For this, first make sure that `main` is up-to-date, so that your local git state reflects the PR on the remote repository.
If you are working with a fork, take a look at GitHub's guide on [how to sync a fork].

Then run the following:

```bash
git checkout <feature-branch>
pre-commit run --files $(git diff --name-only HEAD main)
```

[sktime]: https://github.com/sktime/sktime
[pre-commit]: https://pre-commit.com/
[how to sync a fork]: https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/syncing-a-fork
[Gist]: https://gist.github.com/mloning/6f4b8d412743968af6b2da8b4eaaf2bf

