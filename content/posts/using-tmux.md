---
title: "Using tmux"
date: 2026-04-14T22:39:48+02:00
draft: false
---

## What's tmux?

tmux is a client-server terminal multiplexer.
It is pretty old, but has remained very popular, regularly features on the Hacker News front page, and is available on most Unix systems.

Traditional terminal emulators (e.g. Alacritty, iTerm2) are tightly coupled to the shell process via a pseudo-terminal (PTY), where the shell is the program that interprets and executes user input.
If we close the terminal emulator, the shell process is closed, too, and with it any running program we may have launched.

tmux, on the other hand, separates the execution environment from the rendering environment.

- Traditional: `Emulator <-> shell/PTY`
- tmux: `Emulator <-> tmux client <-> Unix socket <-> tmux server <-> shell/PTY`

The tmux server runs independently of the client.
So when closing the terminal emulator, the client is closed too but the server and any shell process running on it lives on.

For example, when working on a remote server, our SSH connection may drop or we may accidentally close our terminal window.
With traditional emulators, we would loose our shell session and anything we have been runnng; with tmux our processes live on.

## Core concepts

tmux uses some key concepts, in a hierarchy:

1. Server: The process managing all shell/PTY sessions
2. Session: A collection of windows (e.g. one session for each project)
3. Window: A collection of panes; by default a window has one pane (so no split view) (e.g. one for your editor, one for running your coding agent)
4. Pane: Subdivision of a window (horizontal/vertical split view)

## Commands

tmux uses a prefix (configurable, by default `Ctrl+b`) to distinguish tmux commands from your what you want to send to the shell.

Some useful commands:

| Key            | Action                                                     |
| :------------- | :--------------------------------------------------------- |
| `prefix` + `w` | Interactive tree view (window/session selection + preview) |
| `prefix` + `[` | Enter copy mode (scrollback, search, and yank)             |
| `prefix` + `c` | Create a new window                                        |
| `prefix` + `%` | Split pane vertically (I remapped this to `\|`)            |
| `prefix` + `"` | Split pane horizontally (I remapped this to `-`)           |
| `prefix` + `d` | Detach from the current session                            |

## CLI

In addition to the commands, tmux comes with a CLI.
This allows you to manage the server from the command line and to script helper tools, for example a [tmux sessionizer script](https://github.com/mloning/dotfiles/blob/main/scripts/.local/bin/tmux-sessionizer.sh).

- `tmux ls`: List active sessions.
- `tmux new -s <name>`: Create a new named session.
- `tmux attach -t <name>`: Attach to a specific session (alias: `tmux a -t`).
- `tmux kill-server`: Kill all sessions and the server process.
- `tmux source-file ~/.tmux.conf`: Reload configuration without restarting.

## Configuration

tmux is very configurable.
Configuration lives in `~/.tmux.conf`.
Check out the links below, or my setup [here](https://github.com/mloning/dotfiles/blob/main/tmux/.tmux.conf).

## Advantages

In summary, here are the main reason why I like using tmux:

- Keyboard centric
- State persistence (including process execution, scrollback, cursor position) over unstable remote connections or accidentally closing a window
- Session management and easy switching between projects, each with multiple windows (editor, coding agent, etc)

In addition, tmux allows for pair programming, with multiple clients attaching to the same session but I have not tried that out yet.

## Notes

### macOS: Mapping "Command" as the Prefix

tmux usually requires two-key cord for its prefix.
However, I read that with some terminals like Alacritty, you can map the `Cmd` key on macOS to send hex codes that tmux interprets as commands.
This enables single-key prefix key.

> Tmux becomes more awesome when you use something like Alacritty or Kitty [EDIT: scratch Kitty, this mainly applies to Alacritty] and map your system's key (Apple's command key or... whatever it would be on Linux or Windows) and use that as your "tmux key". That way you can make single-chord bindings for all things tmux and life becomes better. If you use Vim, adding VimTmuxNavigator[0] improves things so much. For example, to seamlessly switch between panes, be they tmux panes or vim panes, I use `cmd-h`, `cmh-j`, `cmd-k`, `cmd-l`.
> It's possible to achieve "command as tmux key" with iTerm which I did do for years but I don't recommend it. It's very hacky.
> [0] https://github.com/christoomey/vim-tmux-navigator

https://news.ycombinator.com/item?id=33943537

### Shift+Enter in Claude Code

For Claude Code inside tmux, you may encounter that `Shift+Enter` does not work (new line for the prompt).
Alternatively, you can use `Ctrl+j`.
Another fix which I have not tried yet is to bind the key in your config:

```bash
bind-key -T root S-Enter send-keys C-j
```

## Resources

- https://zellij.dev/ (alternative to tmux)
- https://hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/
- https://hamvocke.com/blog/a-guide-to-customizing-your-tmux-conf/
- http://danielallendeutsch.com/blog/16-using-tmux-properly.html (https://news.ycombinator.com/item?id=21055468)
- https://leimao.github.io/blog/Tmux-Tutorial/
- https://smartbear.com/blog/tmux-and-vim/ (https://news.ycombinator.com/item?id=14155761)
- https://zserge.com/posts/tmux/ (https://news.ycombinator.com/item?id=23003603)
- https://ittavern.com/getting-started-with-tmux/
