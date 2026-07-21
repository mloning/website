---
title: "Agentic engineering and skills"
date: 2026-06-05T14:23:23+01:00
draft: false
tags: ["ai", "engineering"]
---

AI agents like Claude Code or Codex are non-deterministic tools, which can be modified, tweaked and used in many different ways.
Using them effectively requires mastering them and making them your own to some degree, even when agents and the LLMs they rely on are still evolving.

Skill are one way to reuse prompts (besides, for example, defining custom agents or `AGENTS.md` files).
I started writing my own skills, partly based on popular skill libraries like [obra/superpowers](https://github.com/obra/superpowers), mainly because I wanted to:

- have more tailored skills for my common workflows,
- learn more about prompt engineering,
- reflect upon and adjust how I work and how I use agents.

For now, I ended up with the following skills (see on [GitHub](https://github.com/mloning/dotfiles/tree/main/skills)), one for each of my repetitive workflows:

- Review repo (architecture review, refactor to decrease coupling, simplify interfaces, consistent naming, identifying opportunities to reduce tech debt, improve test coverage, clean up stale comments/docs, improve readability)
- Review local changes (change set against `main`)
- Submit PR (MCP or `gh pr create` with PR description, link Jira issue)
- Review PR (change set + PR description/comments and linked resources like Jira tickets, from with different perspectives)
- Reply to PR review (verify and address review comments)
- Brainstorm (pre-planning, scoping, conceptual ideation, web search, pros/cons of alternatives, outputs a precise spec)
- Plan (based on spec, implementation plan in the context of the existing code base, further questioning)
- Review plan (critique plan, review against spec)
- Research (scientific literature review)
- Write docs (e.g. prefer verbs, avoid weasel words)
- Debug (systematic debugging, root cause analysis, analyse available info, state hypotheses, instrument, test hypotheses, iteratively rule out possible causes)
- Implement (best practices; principles, naming)
- Develop (autonomous brainstorming/critique -> planning/critique -> execution/review cycles, PR submission; ask only when really stuck; using max effort level, cross-agent Claude/Codex review, verification via build/tests/linting)
- Explain (be concise; describe data flow; describe sequence of function calls; walk through simple example; give minimal, reproducible example)
- Write skill (a skill to write other skills, ensuring instructions make sense and work reliably)

Skills let me easily change how agents operate, including:

- Autonomy (review every step vs autonomously implement a full feature; may require different permissions modes and sandboxing)
- Parallelization using independent sub-agents
- Control of work depth and speed/cost (e.g. sometimes I want a quick fix, sometimes a fully cross-checked plan-based implementation)
- Cross-agent collaboration (e.g. agent teams or [dynamic workflows](https://code.claude.com/docs/en/workflows))

There a few things to keep in mind when writing skills:

- Reusable for different agents like Claude Code and Codex
- Implicit vs explicit (vs auto) invocation rules (e.g. I don't always want agents to use certain skills, mainly to have more control over depth of work vs speed)
- Composable (e.g. a skill to autonomously develop something may first invoke a skill to plan the change)

Related resources:

- https://www.saturnci.com/my-agent-skill-for-test-driven-development.html
- https://www.thoughtfultechnologist.com/p/automating-myself-out-of-development
- https://github.com/mattpocock/skills
- https://github.com/vercel-labs/skills (npx skills CLI)
- https://www.skills.sh/
- https://skillsmp.com/
- https://github.com/affaan-m/ECC
- https://github.com/obra/superpowers
- https://github.com/openclaw/openclaw/tree/main/.agents/skills
- https://github.com/hesreallyhim/awesome-claude-code
- https://github.com/DanMcInerney/architect-loop (research)
- [Steps of AI Adoption by Boris Cherny](https://claude.ai/code/artifact/bfdfaef9-bc62-4dfe-ba9e-c58a26c9accf)
