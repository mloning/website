---
title: "Using tmux"
date: 2026-04-14T22:39:48+02:00
draft: true
---

Command as tmux prefix key on macOS

> Tmux becomes more awesome when you use something like Alacritty or Kitty [EDIT: scratch Kitty, this mainly applies to Alacritty] and map your system's key (Apple's command key or... whatever it would be on Linux or Windows) and use that as your "tmux key". That way you can make single-chord bindings for all things tmux and life becomes better. If you use Vim, adding VimTmuxNavigator[0] improves things so much. For example, to seamlessly switch between panes, be they tmux panes or vim panes, I use `cmd-h`, `cmh-j`, `cmd-k`, `cmd-l`.
> It's possible to achieve "command as tmux key" with iTerm which I did do for years but I don't recommend it. It's very hacky.
> [0] https://github.com/christoomey/vim-tmux-navigator

https://news.ycombinator.com/item?id=33943537

Shift+Enter issue in Claude Code

> In case anyone is looking for it, the fix is "bind-key -T root S-Enter send-keys C-j" borrowed from https://github.com/anthropics/claude-code/issues/6072

https://news.ycombinator.com/item?id=47752819

## Resources

- https://hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/
- https://hamvocke.com/blog/a-guide-to-customizing-your-tmux-conf/
- http://danielallendeutsch.com/blog/16-using-tmux-properly.html (https://news.ycombinator.com/item?id=21055468)
- https://leimao.github.io/blog/Tmux-Tutorial/
- https://smartbear.com/blog/tmux-and-vim/ (https://news.ycombinator.com/item?id=14155761)
- https://zserge.com/posts/tmux/ (https://news.ycombinator.com/item?id=23003603)
- https://ittavern.com/getting-started-with-tmux/
