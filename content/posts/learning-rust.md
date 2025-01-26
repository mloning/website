---
title: "Learning Rust"
date: 2025-01-11T12:08:32+01:00
last_modified: .Lastmod
draft: true
---

## Projects

- https://github.com/mloning/first-steps-in-rust (based on free book)
- https://github.com/mloning/uno-rs
- https://github.com/mloning/rocket-rs

## Project ideas

- https://github.com/kyclark/command-line-rust (book)
- https://github.com/lukemathwalker/zero-to-production (book, [free sample](https://www.zero2prod.com/assets/sample_zero2prod.pdf))
- https://en.wikipedia.org/wiki/Dining_philosophers_problem
- Gossip Gloomers Distributed Systems Challenge
- Implement signal processing filters in Rust

## Debugging

### Using lldb

- [lldb], included with Xcode on macOS
- [lldb tutorial]
- Configure custom settings and command aliases in `~/.lldbinit`

[lldb]: https://lldb.llvm.org/index.html
[lldb tutorial]: https://lldb.llvm.org/use/tutorial.html

Useful commands:

- `cargo build` to build the program
- `lldb <program>` where `<program>` is the built binary, e.g. in my [uno] project: `lldb ./target/debug/uno`
- `help` to see available commands
- `apropros ...` to find help specific to a search term, e.g. `apropros breakpoint`
- `breakpoint set ...` (or `b`), e.g. `breakpoint set main`
- `breakpoint list`
- `breakpoint delete` to delete a specific or all breakpoints
- `breakpoint command add` to add a command to run when the breakpoint is hit (e.g. printing a variable value)
- `breakpoint disable` to disable the breakpoint without deleting it
- `breakpoint enable`
- `run` (or `r`) to run the program
- `next` (or `n`) to run next line
- `list` (or `l`) to list source code
- `step` (or `s`) to step into a function
- `continue` (or `c`) to continue execution, until next breakpoint if set
- `thread until <line-no>` run until line number, like setting and continuing until a one-off breakpoint, useful for stepping out of a loop or function, similar to `tbreak`
- `print` (or `p`) for printing a variable
- `frame variable [<variable-name>]` to print a specific or all variables
- `watchpoint` for managing watchpoints for watching and stopping based on specific conditions for state of variables

[uno]: https://github.com/mloning/uno-rs

### Using Neovim with AstroNvim and nvim-dap

- Install [AstroNvim] and [community Rust language pack], AstroNvim includes [nvim-dap], see [key mappings](https://docs.astronvim.com/mappings/#debugger-mappings)
- Launch debugger using key mappings, e.g. `<leader>db` for setting a breakpoint and `<leader>dc` for launching the program
- To use `lldb` commands from above, navigate to `dap-repl` window in the nvim-dap UI and switch to insert mode using `i`

[AstroNvim]: https://astronvim.com/
[community Rust language pack]: https://github.com/AstroNvim/astrocommunity/tree/main/lua/astrocommunity/pack/rust
[nvim-dap]: https://github.com/mfussenegger/nvim-dap
