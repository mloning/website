---
title: "Installing fish shell with Starship"
date: 2026-01-10T20:45:23+01:00
---

I had heard good things about [fish] and after using [oh-my-zsh] for a long time, I wanted to give it a try with [Starship].

[oh-my-zsh]: https://ohmyz.sh/
[fish]: https://fishshell.com/
[Starship]: https://starship.rs/
[powerlevel10k]: https://github.com/romkatv/powerlevel10k

Installing fish and Starship is straightforward on macOS:

```bash
brew install fish starship
```

Next, we add fish as an allowed non-standard shell on macOS, and set it as the default:

```bash
echo /usr/local/bin/fish | sudo tee -a /etc/shells
chsh -s /usr/local/bin/fish
```

I was using [Alacritty] and for Alacritty to pick up the new shell, I had to restart my laptop (or at least log out and back in).

[Alacritty]: https://alacritty.org/

My migration from [oh-my-zsh] with [powerlevel10k] was easy.
Most features were supported out of the box or easy to configure:

- `starship init fish | source` to initialize Starship, with many of the command line features that oh-my-zsh and powerlevel10k provide
- A custom key binding for my tmux sessionizer
- `zoxide init fish` to initialize zoxide (`z` command replacement for `cd`)
- `fzf --fish` to initialize `fzf` for reverse history search; alternatively there is [fzf.fish](https://github.com/PatrickF1/fzf.fish), a fish plugin using the [fisher] plugin manager

You can find my full configuration in [my dotfiles repository](https://github.com/mloning/dotfiles).

[fisher]: https://github.com/jorgebucaran/fisher

Compared with Zsh, fish provides:

- Built-in auto-suggestions based on history
- Built-in, real-time syntax highlighting
- Better built-in tab completion

I also wanted to migrate my Zsh command history, here are some options, but haven't tried them yet:

- `pip install zsh-history-to-fish` and then run: `zsh-history-to-fish`
- https://github.com/atuinsh/atuin (SQLite database that works across Zsh and fish)

## Links

- https://github.com/mloning/dotfiles (my dotfiles)
- https://github.com/nc7s/fish (interesting fish config)
