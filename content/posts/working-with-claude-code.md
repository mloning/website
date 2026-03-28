---
title: "Working with Claude Code"
date: 2026-03-07T14:58:15+01:00
draft: false
---

Notes and links about Claude Code and agentic engineering.

## How Claude Code work

It's not hard to understand the basic workings of coding agents like Claude Code:

- [How Coding Agents Work](https://simonwillison.net/guides/agentic-engineering-patterns/how-coding-agents-work/) (LLM + system prompts + tools in a loop)
- "[ultrathink](https://simonwillison.net/2025/Apr/19/claude-code-best-practices/)" internal keyword
- Claude Code's [system prompts](https://gist.github.com/wong2/e0f34aac66caf890a332f7b6f9e2ba8f#task-management)

Recreating a minimal coding agent is also informative:

- [How to Build an Agent](https://ampcode.com/notes/how-to-build-an-agent)
- [The Emperor Has No Clothes](https://www.mihaileric.com/The-Emperor-Has-No-Clothes/) ([HN thread](https://news.ycombinator.com/item?id=46545620))

## How to get the best out of Claude Code

Some tips on how to get the best out of Claude Code:

- [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/)
- [Getting Good Results from Claude Code](https://www.dzombak.com/blog/2025/08/getting-good-results-from-claude-code/)
- [Anatomy of the Claude folder](https://blog.dailydoseofds.com/p/anatomy-of-the-claude-folder) (user/project settings; rules, skills, commands)

I try to capture as much as possible the things that work for me in my [settings](https://github.com/mloning/dotfiles/tree/main/claude/).

## Reviews of Claude Code

Some reviews of using Claude Code:

- [The Magic of Claude Code](https://www.alephic.com/writing/the-magic-of-claude-code) ([HN thread](https://news.ycombinator.com/item?id=45437893))
- [Six Weeks of Claude Code](https://blog.puzzmo.com/posts/2025/07/30/six-weeks-of-claude-code/) ([HN thread](https://news.ycombinator.com/item?id=44746621))
- [First Attempt Will Be 95% Garbage](https://www.sanity.io/blog/first-attempt-will-be-95-garbage) ([HN thread](https://news.ycombinator.com/item?id=45107962))

Generally, at this stage, it seems like coding agents are:

- Not very good at writing code on their own unless it's simple; generated code often needs to be reviewed and edited for correctness, design and style
- Very good at debugging
- Good at brainstorming

Junior engineers will struggle with reviewing and editing the code, while senior engineers will mostly benefit from coding agents, but sometimes waste their time by using an agent instead of writing the code themselves.

## Risks of using Claude Code

With the increased speed of writing code, our cognitive debt in understanding the code base may also increase:

- [How Generative and Agentic AI Shift Concern from Technical Debt to Cognitive Debt](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/)
- [Cognitive Debt: When Velocity Exceeds Comprehension](https://www.rockoder.com/beyondthecode/cognitive-debt-when-velocity-exceeds-comprehension/)
- [Simon Willison on Cognitive Debt](https://simonwillison.net/2026/Feb/15/cognitive-debt/)
- [Martin Folwer on Cognitive Debt](https://martinfowler.com/fragments/2026-02-13.html)

A similar idea is [Verification Debt](https://fazy.medium.com/agentic-coding-ais-adolescence-b0d13452f981), where we struggle to keep up with verifying and testing the generate code.
