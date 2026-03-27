---
title: Learning C++
date: 2025-05-14T08:47:02+02:00
draft: false
---

## Build process

For an introduction to the build process, see [The C++ Build Process Explained](https://github.com/green7ea/blog/blob/master/cpp-build-process/README.md) and the related [HackerNews thread](https://news.ycombinator.com/item?id=18454140).
For a deeper explanation, see [The Bits Between the Bits: How We Get to main()](https://www.youtube.com/watch?v=dOfucXtyEsU).

Best practices:

- Use a package manager (e.g. `conan`)
- Use [CMake](https://cmake.org/) with Ninja (for CMake best practices, see [Professional CMake](https://crascit.com/professional-cmake/) or [Pragmatic CMake](https://www.youtube.com/watch?v=NDfTwOvWIao))
- Strict compiler settings: at least `-Wall -Wextra -Werror`, preferably also `-Wpedantic -Wcast-align -Wno-unused -Wshadow -Woverloaded-virtual`, and ideally with `-Wconversion -Wsign-conversion -Wnull-dereference -Wdouble-promotion`
- Static analysis: linters, formatters (e.g. `clang-tidy` and `clang-format`)
- Dynamic analysis: sanitizers, at least [ASan](https://clang.llvm.org/docs/AddressSanitizer.html) and [UBSan](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html) (e.g. `g++ -fsanitize=address,undefined -g -O1`)

## Learning resources

- Book "Effective Modern C++" by Scott Meyers
- Online tutorials:
  - [Learn C++](https://www.learncpp.com/cpp-tutorial/), very comprehensive tutorial for the C++ language itself, but without discussing the wider ecosystem like existing testing frameworks or toolchains
  - https://www.studyplan.dev/cpp
  - [Video tutorials](https://www.youtube.com/playlist?list=PLlrATfBNZ98dudnM48yfGUldqGD0S4FFb) focused on game development
  - https://learnxinyminutes.com/c++/, very concise introduction
- [Back to Basics](https://www.youtube.com/user/CppCon/search?query=back%20to%20basics) video series from [CppCon](https://cppcon.org/), for example:
  - [Getting Started](https://www.youtube.com/watch?v=NReDubvNjRg)
  - [Unit Testing in C++](https://www.youtube.com/watch?v=MwoAM3sznS0) (2024) or [Testing in C++](https://www.youtube.com/watch?v=7_H4qzhWbnQ) (2023)
  - [Debugging](https://www.youtube.com/watch?v=qgszy9GquRs)
  - [C++ Coding with Neovim](https://www.youtube.com/watch?v=nzRnWUjGJl8)
- [Cheat sheet](https://hackingcpp.com/cpp/cheat_sheets.html) with [HackerNews thread](https://news.ycombinator.com/item?id=30579884)

For a discussion of C++ learning resources, see this [HackerNews discussion](https://news.ycombinator.com/item?id=16535886) or [Reddit thread](https://www.reddit.com/r/cpp_questions/comments/rxx0z5/best_resources_to_learn_c/).

## Other resources

- Example best-practices repository https://github.com/bemanproject/exemplar
- [You've just inherited a legacy C++ codebase, now what?](https://gaultier.github.io/blog/you_inherited_a_legacy_cpp_codebase_now_what.html), great blog post on working with a legacy C++ code base, but most tips apply to any language; also see the related [HackerNews thread](https://news.ycombinator.com/item?id=39549486) and the [blog post](https://medium.com/@ramunarasinga/git-blame-ignore-revs-to-ignore-bulk-formatting-changes-f20ac23e6155) on how to ignore large formatting changes using [.git-blame-ignore-revs](https://git-scm.com/docs/git-blame#Documentation/git-blame.txt---ignore-revltrevgt)
- https://cplusplus.com/, community tutorials, forum and blog posts
- https://en.cppreference.com/, language reference
- https://cppinsights.io/ and https://compiler-explorer.com/ to better understand the compiled code and how the compiler works
- https://isocpp.org/wiki/faq/user-groups-worldwide to find user groups around the world
- Low-latency C++ patterns: https://news.ycombinator.com/item?id=40908273
- C++ to Rust book: https://cel.cs.brown.edu/crp/

## Discussions on C++, its problems and future

- [It's time to halt starting any new projects in C/C++](https://news.ycombinator.com/item?id=32905885), discussion based on the [original tweet](https://x.com/markrussinovich/status/1571995117233504257)
- [Rust Devs Think We’re Hopeless; Let’s Prove Them Wrong (with C++ Memory Leaks)!](https://www.babaei.net/blog/rust-devs-think-we-are-hopeless-lets-prove-them-wrong-with-cpp-memory-leaks/)
- [Lessons Learnt from a Rust Rewrite](https://gaultier.github.io/blog/lessons_learned_from_a_successful_rust_rewrite.html)
- Comparing with Rust: "In my experience, C++ is a much more complicated language. The 8 ways to initialize something, the 5 types of values (xvalues etc.), inconsistent formatting conventions, inconsistent naming conventions, the rule of 5, exceptions, always remembering to check `this != other` when doing a move assignment operator, perfect forwarding, SFINAE, workarounds for not having a great equivalent to traits, etc. Part of knowing the language is also knowing the conventions on top that are necessary in order to write it more safely and faster (if your move constructor is not noexcept it'll cause copies to occur when growing a vector of that object), and learning the many non-ideal competing ways that people do things, like error handling." ([HackerNews comment](https://news.ycombinator.com/item?id=45606560))
- "In C/C++, making almost every variable const at initialization is good practice. I wish it was the default, and mutable was a keyword." (John Carmack [tweet](https://x.com/ID_AA_Carmack/status/1983593511703474196))
