---
title: "Installing Fish With Starship"
date: 2026-01-10T20:45:23+01:00
draft: true
---

Installing Fish and Starship is straighforward on macOS:

```bash
brew install fish starship
chsh
```

Next, we add Fish as an allowed non-standard shell on macOS, and set it as the default:

```bash
echo /usr/local/bin/fish | sudo tee -a /etc/shells
chsh -s /usr/local/bin/fish
```

I'm using Alacritty and for Alacritty to pick up the new shell, I had to restart my laptop (or at least log out).

My migration from oh-my-zsh with powerlevel10k was easy.
Most features were supported out of the box or easy to configure:

- Starship provides many of the command line features that oh-my-zsh and powerlevel10k provide
- Added a custom key binding for my tmux sessionizer
- Added `zoxide init fish` to initialize zoxide (`z` command replacement for `cd`)
- Added `fzf --fish` to initialize `fzf` for reverse history search; alternatively there is https://github.com/PatrickF1/fzf.fish for Fisher plugin manager

I wanted to migrate my Zsh command history, here are some options:

- `pip install zsh-history-to-fish` and `zsh-history-to-fish`
- https://github.com/atuinsh/atuin (SQLite database that works across Zsh and Fish)

Compared with Zsh, Fish provides:

- built-in auto-suggestions based on history
- built-in, real-time syntax highlighting
- better built-in tab completion

## Links

- TODO my macOS setup (update post)
- TODO my dotfiles
- https://github.com/nc7s/fish
- https://starship.rs/
