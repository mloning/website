---
title: "Cleaning Up Storage on Macos"
date: 2024-12-20T16:58:20+01:00
last_modified: .Lastmod
draft: true
---

## Using macOS storage manager

- Go to System Settings, Storage
  – Click on the info circle to further investigate each category and remove applications or files that you no longer need

## Clearing cache from developer tools

- `docker system prune --all`
- remove unused conda environments `conda info --envs`, `conda remove -n <name> --all`
- cargo cache https://blog.rust-lang.org/2023/12/11/cargo-cache-cleaning.html

## Manually searching for large directories and files

- set "Calculate all sizes" in Finder - Show Wiew Options
- run: `defaults write com.apple.finder AppleShowAllFiles yes` to show hidden files

Directories to focus on:

- `/Library/`
- `~/`, particularly `~/Library/ApplicationSupport/` for application cache (e.g. Slack, Zoom, etc)
