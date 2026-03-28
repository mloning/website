---
title: Learning C++
date: 2025-05-14T08:47:02+02:00
draft: false
---

## Build process

For an introduction to the build process, see [The C++ Build Process Explained](https://github.com/green7ea/blog/blob/master/cpp-build-process/README.md) and the related [HackerNews thread](https://news.ycombinator.com/item?id=18454140).
For a deeper explanation, see [The Bits Between the Bits: How We Get to main()](https://www.youtube.com/watch?v=dOfucXtyEsU).
For a real-time visualisation of the build process, see [this post](https://danielchasehooper.com/posts/syscall-build-snooping/).

Best practices:

- Use a package manager (e.g. `conan`)
- Use [CMake](https://cmake.org/) with Ninja (for CMake best practices, see [Professional CMake](https://crascit.com/professional-cmake/) or [Pragmatic CMake](https://www.youtube.com/watch?v=NDfTwOvWIao))
- Strict compiler settings: at least `-Wall -Wextra -Werror`, preferably also `-Wpedantic -Wcast-align -Wno-unused -Wshadow -Woverloaded-virtual`, and ideally with `-Wconversion -Wsign-conversion -Wnull-dereference -Wdouble-promotion`
- Static analysis: linters, formatters (e.g. `clang-tidy` and `clang-format`)
- Dynamic analysis: sanitizers, at least [ASan](https://clang.llvm.org/docs/AddressSanitizer.html) and [UBSan](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) (e.g. `g++ -fsanitize=address,undefined -g -O1`)

## Learning resources

For a discussion on C++ learning resources, see this [HackerNews discussion](https://news.ycombinator.com/item?id=16535886) or [Reddit thread](https://www.reddit.com/r/cpp_questions/comments/rxx0z5/best_resources_to_learn_c/).
Below are some highlights.

### Books

- Book "Effective Modern C++" by Scott Meyers
- [A Tour of C++](https://www.stroustrup.com/Tour.html) by Bjarne Stroustrup (overview of C++ for experienced programmers)
- [Programming: Principles and Practice Using C++](https://www.stroustrup.com/programming.html) by Bjarne Stroustrup (introductory)

### Tutorials

- [Modern C++ Programming Course](https://github.com/federico-busato/Modern-CPP-Programming), [HackerNews thread](https://news.ycombinator.com/item?id=38444834)
- [Learn C++](https://www.learncpp.com/cpp-tutorial/), very comprehensive tutorial for the C++ language itself, but without discussing the wider ecosystem like existing testing frameworks or toolchains
- [C++ Study Plan](https://www.studyplan.dev/cpp)
- [Learn C++ in Y Minutes](https://learnxinyminutes.com/c++/), very concise introduction

### Videos

- [Video tutorials](https://www.youtube.com/playlist?list=PLlrATfBNZ98dudnM48yfGUldqGD0S4FFb) focused on game development
- [Back to Basics](https://www.youtube.com/user/CppCon/search?query=back%20to%20basics) video series from [CppCon](https://cppcon.org/), for example:
  - [Getting Started](https://www.youtube.com/watch?v=NReDubvNjRg)
  - [Unit Testing in C++](https://www.youtube.com/watch?v=MwoAM3sznS0) (2024) or [Testing in C++](https://www.youtube.com/watch?v=7_H4qzhWbnQ) (2023)
  - [Debugging](https://www.youtube.com/watch?v=qgszy9GquRs)
  - [C++ Coding with Neovim](https://www.youtube.com/watch?v=nzRnWUjGJl8)
- [It's Complicated](https://www.youtube.com/watch?v=tTexD26jIN4) (Kate Gregory, Meeting C++ 2017 Keynote)
- [10 Core Guidelines You Need to Start Using Now](https://www.youtube.com/watch?v=XkDEzfpdcSg) (Kate Gregory, CppCon 2017)
- [Undefined Behavior in C++: What Every Programmer Should Know and Fear](https://www.youtube.com/watch?v=k9N8OrhrSZw) (Fedor Pikus, CppCon 2023)

### Other resources

- [Cheat sheet](https://hackingcpp.com/cpp/cheat_sheets.html) with [HackerNews thread](https://news.ycombinator.com/item?id=30579884)
- Well-written C++ repos: [nlohmann/json](https://github.com/nlohmann/json)

## Other resources

- Example best-practices repository [bemanproject/exemplar](https://github.com/bemanproject/exemplar)
- [You've just inherited a legacy C++ codebase, now what?](https://gaultier.github.io/blog/you_inherited_a_legacy_cpp_codebase_now_what.html), great blog post on working with a legacy C++ code base, but most tips apply to any language; also see the related [HackerNews thread](https://news.ycombinator.com/item?id=39549486) and the [blog post](https://medium.com/@ramunarasinga/git-blame-ignore-revs-to-ignore-bulk-formatting-changes-f20ac23e6155) on how to ignore large formatting changes using [.git-blame-ignore-revs](https://git-scm.com/docs/git-blame#Documentation/git-blame.txt---ignore-revltrevgt)
- [cplusplus.com](https://cplusplus.com/), community tutorials, forum and blog posts
- [cppreference.com](https://en.cppreference.com/), language reference
- [C++ Insights](https://cppinsights.io/) and [Compiler Explorer](https://compiler-explorer.com/) to better understand the compiled code and how the compiler works
- [ISO C++ User Groups](https://isocpp.org/wiki/faq/user-groups-worldwide) to find user groups around the world
- [Low-latency C++ patterns](https://news.ycombinator.com/item?id=40908273)
- [C++ to Rust Phrasebook](https://cel.cs.brown.edu/crp/)

## C++ shortcomings and its future

- [Why I don't spend time with Modern C++ anymore](https://news.ycombinator.com/item?id=11720659)
- [Linus Torvalds on C++](https://harmful.cat-v.org/software/c++/linus)
- [C++ is an absolute blast](https://news.ycombinator.com/item?id=42495135)
- [Modern C++ Won't Save Us](https://news.ycombinator.com/item?id=19723066)
- ["Modern" C++ Lamentations](https://news.ycombinator.com/item?id=18777735)
- [All C++20 core language features with examples](https://news.ycombinator.com/item?id=26723851)
- [The two factions of C++](https://herecomesthemoon.net/2024/11/two-factions-of-cpp/), [HackerNews thread](https://news.ycombinator.com/item?id=42231489)
- [Matt Godbolt sold me on Rust by showing me C++](https://news.ycombinator.com/item?id=43907820)
- [It's time to halt starting any new projects in C/C++](https://news.ycombinator.com/item?id=32905885), discussion based on the [original tweet](https://x.com/markrussinovich/status/1571995117233504257)
- [Rust Devs Think We’re Hopeless; Let’s Prove Them Wrong (with C++ Memory Leaks)!](https://www.babaei.net/blog/rust-devs-think-we-are-hopeless-lets-prove-them-wrong-with-cpp-memory-leaks/)
- [Lessons Learnt from a Rust Rewrite](https://gaultier.github.io/blog/lessons_learned_from_a_successful_rust_rewrite.html)
- Comparing with Rust: "In my experience, C++ is a much more complicated language. The 8 ways to initialize something, the 5 types of values (xvalues etc.), inconsistent formatting conventions, inconsistent naming conventions, the rule of 5, exceptions, always remembering to check `this != other` when doing a move assignment operator, perfect forwarding, SFINAE, workarounds for not having a great equivalent to traits, etc. Part of knowing the language is also knowing the conventions on top that are necessary in order to write it more safely and faster (if your move constructor is not noexcept it'll cause copies to occur when growing a vector of that object), and learning the many non-ideal competing ways that people do things, like error handling." ([HackerNews comment](https://news.ycombinator.com/item?id=45606560))
- "In C/C++, making almost every variable const at initialization is good practice. I wish it was the default, and mutable was a keyword." (John Carmack [tweet](https://x.com/ID_AA_Carmack/status/1983593511703474196))
