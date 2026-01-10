---
title: "Installing Fish With Starship"
date: 2026-01-10T20:45:23+01:00
draft: true
---

Installing Fish and Starship is straighforward on macOS:

```bash
brew install fish starship
```

- Added a custom key binding for my tmux sessionizer
- `zoxide init fish` initializes zoxide (`z` command replacement for `cd`)
- `fzf --fish` initializes `fzf` for reverse history search; alternatively there is https://github.com/PatrickF1/fzf.fish for Fisher plugin manager
- Starship provides many of the command line features that oh-my-zsh and powerlevel10k provide

Compared with zsh, Fish provides:

- built-in auto-suggestions based on history
- built-in, real-time syntax highlighting
- better built-in tab completion

## Links

- TODO my macOS setup (update post)
- TODO my dotfiles
- https://github.com/nc7s/fish
- https://starship.rs/
