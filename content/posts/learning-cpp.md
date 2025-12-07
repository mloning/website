---
title: Learning C++
date: 2025-05-14T08:47:02+02:00
draft: false
---
## Learning resources
For discussions, see: https://news.ycombinator.com/item?id=16535886, https://www.reddit.com/r/cpp_questions/comments/rxx0z5/best_resources_to_learn_c/

- Book "Effective Modern C++" by Scott Meyers
- Comprehensive tutorials:
  - https://www.learncpp.com/cpp-tutorial/
  - https://www.studyplan.dev/cpp
- Basic tutorials:
  - Back to basics videos from CppCon: https://www.youtube.com/user/CppCon/search?query=back%20to%20basics
  - https://www.youtube.com/playlist?list=PLlrATfBNZ98dudnM48yfGUldqGD0S4FFb
  - https://cplusplus.com/
- Cheat sheet: https://hackingcpp.com/cpp/cheat_sheets.html; discussion: https://news.ycombinator.com/item?id=30579884
- Short overview: https://learnxinyminutes.com/c++/

## Other resources
- C++ build process: https://github.com/green7ea/blog/blob/master/cpp-build-process/README.md; discussion: https://news.ycombinator.com/item?id=18454140
  - linking process: https://youtu.be/dOfucXtyEsU?si=shOVX7xs0KzOYWQA
- Working with legacy C++ code base: https://news.ycombinator.com/item?id=39549486
  - ignoring large formatting changes in git blame using https://git-scm.com/docs/git-blame#Documentation/git-blame.txt---ignore-revltrevgt (see [blog](https://medium.com/@ramunarasinga/git-blame-ignore-revs-to-ignore-bulk-formatting-changes-f20ac23e6155)
- Low-latency C++ patterns: https://news.ycombinator.com/item?id=40908273
- Videos from CppCon: https://www.youtube.com/@CppCon/videos
- C++ to Rust book: https://cel.cs.brown.edu/crp/

## Discussions on C++, its problems and future
- https://news.ycombinator.com/item?id=32905885; original post: https://x.com/markrussinovich/status/1571995117233504257
- https://www.babaei.net/blog/rust-devs-think-we-are-hopeless-lets-prove-them-wrong-with-cpp-memory-leaks/
- https://m.youtube.com/watch?v=7DCO-IISBnc
- Comparing with Rust: "In my experience, C++ is a much more complicated language. The 8 ways to initialize something, the 5 types of values (xvalues etc.), inconsistent formatting conventions, inconsistent naming conventions, the rule of 5, exceptions, always remembering to check `this != other` when doing a move assignment operator, perfect forwarding, SFINAE, workarounds for not having a great equivalent to traits, etc. Part of knowing the language is also knowing the conventions on top that are necessary in order to write it more safely and faster (if your move constructor is not noexcept it'll cause copies to occur when growing a vector of that object), and learning the many non-ideal competing ways that people do things, like error handling." https://news.ycombinator.com/item?id=45606560
- In C/C++, making almost every variable const at initialization is good practice. I wish it was the default, and mutable was a keyword. (John Carmack on X, https://x.com/ID_AA_Carmack/status/1983593511703474196)