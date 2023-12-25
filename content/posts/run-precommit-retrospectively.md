---
title: "Run pre-commit retrospectively on all changed files in a PR"
date: 2020-10-02T16:10:57+02:00
lastmod: 2023-12-25T16:10:57+02:00
draft: false
---

When I was developing [sktime], we sometimes had new contributors who opened a PR but forgot to set up [pre-commit]. 

This is how you can run pre-commit retrospectively on all changed files in the PR from a `<feature-branch>` into `main`. 
First make sure that `main` is up-to-date, so that your local git state reflects the PR on the remote repository.
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

