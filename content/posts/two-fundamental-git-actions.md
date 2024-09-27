---
title: "Two Fundamental Git Actions"
date: 2023-12-29T23:20:08+01:00
last_modified: .Lastmod
draft: true
---

I recently read a [blog post] by [graphite] about rebase vs merge commits which made me re-think my usual git worklow.

[graphite]: https://graphite.dev/
[blog post]: https://graphite.dev/blog/why-ban-merge-commits

In the common trunk-based development context with a remote repository, I believe there are two fundamental git actions.

## Submit

The submit action is used whenever you make a change.

It combines: git switch + git commit + gh pr create

usage: `git submit [-m, --message ..., -a, --all] [FILES]`

- if on default branch (e.g. `main`), switch to new branch using message as branch name (`git switch -c ...`)
- `git commit` all or selected files with message as commit message
- if remote branch does not exist, create remote branch
- push to remote branch
- if PR does not exist, create PR using `gh pr create` pointing to default branch

## Sync

The sync action is used whenever someone else made a change and you want to sync your work with theirs.

It combines: git pull + git merge/rebase main + git push

usage: `git sync`

- `git pull` default branch
- `git merge` or `git rebase` from up-to-date default branch
- `git pull` and `git push` to sync with remote branch

These two commands would cover most of my daily git worklow

## Advanced usage: stacked PRs

[graphite]'s CLI additionally supports stacked PRs, where one PR depends on another PR
in the above commands, we assume everything is based on the default branch, i.e. main
we could add a `--stack` option to `git submit`, this would create a new branch off the current branch instead of main but still point to main
for stacked PRs, `git sync` would then recursively sync all PRs, starting with the PR which has main as its parent branch

## Other interesting actions

To address review comments in a clean way, mostly useful when not squash-merging and commit on branch should be clean: https://github.com/tummychow/git-absorb
