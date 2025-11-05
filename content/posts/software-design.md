---
title: "Software Design"
date: 2025-01-03T15:49:02+01:00
last_modified: .Lastmod
draft: true
---

> every piece of software should be a black box with a pin-hole for input and an even smaller pin-hole for output

---

from https://www.tedinski.com/2018/12/05/types-as-design-tool.html:

> A function is the quintessential abstraction boundary.
> It’s one of the few cases where we should be able to ignore the details.
> (Performance still matters, of course, but even that’s something we can understand in a black-box fashion.)
> We can write better and worse quality functions, but the internal details aren’t really relevant to the software’s overall design.
> It should be isolated.
>
> I think design is about everything that’s leftover after we remove all the function bodies.
> It worth taking a moment to think about what that looks like.

Developer philosophy: https://qntm.org/devphilo

On project scoping and objectives:

> positioning your project as an alternative implementation of something is a losing proposition

> don't go trying to create a subset of Python [...] Do your own thing. That way, you can evolve your system at your own pace and in your own direction, without being chained by expectations that your language should have to match the performance, feature set, or library ecosystem of another implementation.

https://pointersgonewild.com/2024/04/20/the-alternative-implementation-problem/