---
title: EuroRust 2025
date: 2025-10-11T11:58:15+02:00
last_modified: .Lastmod
draft: false
---

I attended my first Rust conference, [EuroRust 2025](https://eurorust.eu/2025/) in Paris.

- clippy settings recommendations, including `pedantic` or `undocumented_unsafe_blocks` (structured safety documentation) for unsafe code
- best practices for Rust development by jhpratt ([slides](https://jhpratt.dev/talks/#exemplary-by-design-building-and-maintaining-rust-at-scale), also see his related talk on [compiler-driven development](https://jhpratt.dev/talks/#compiler-driven-development-making-rust-work-for-you))
- inner workings of the Rust compiler, compiler settings and their trade-offs including inlining, [monomorphization](https://en.wikipedia.org/wiki/Monomorphization) link-time optimizations (LTO) by noratrieb ([slides](https://noratrieb.dev/slides/2025-10-10-how-rust-compiles/), [Rust performance book](https://nnethercote.github.io/perf-book/))
- best practices for error handling: for anticipated errors, prefer `thiserror` for libraries to expose concrete and structured errors, and `Result` type and `anyhow` for application code, for unanticipated errors use `panic!` (programmer mistake)
- `criterion` and flamegraphs for profiling
- inner working of atomic types for concurrency and [memory ordering](https://en.wikipedia.org/wiki/Memory_ordering)
- prefer concrete types (e.g. enums) over generics and traits, for speed due to monomorphization and readability, especially in application code
- [presenterm](https://mfontanini.github.io/presenterm/) for making presentations in your terminal
- `embassy` for embedded systems
- `bevy` game engine
- the concept of run-time [reflection](https://en.wikipedia.org/wiki/Reflective_programming) and and Rust's compile-time solutions based on procedural macros like `serde`'s `derive`, e.g. when you add `#[derive(Serialize, Deserialize)]` to a struct, you are using a procedural macro that runs when you compile your code; the macro inspects the definition of your struct (e.g., the field names and types), and based on this inspection automatically generates the implementation of the core `Serialize` and `Deserialize` traits for your specific type
- triemap, a tree-based data structures primarily used for efficient storage and retrieval of associative data where the keys are strings or sequences, e.g. for fast prefix-based lookup
- foreign function interfaces (FFI) in Rust for using functions from other programming languages, particularly C (e.g. using `extern`)
- [Valgrind](https://valgrind.org/) for profiling and memory debugging
- data engineering
  - OLAP (analytical)
    - batch operations involving complex queries, aggregations and scans across many rows but few columns
    - primarily columnar data format, e.g. Parquet/Arrow
    - data warehouse solutions like Delta Lake and Snowflake
  - OLTP (operational)
    - frequent inserts, updates, deletes, and fetching full records (e.g. banking transactions, user profiles)
    - row-based format (e.g. PostgreSQL)
    - document-based/NoSQL databases (e.g. MongoDB), better for complex entities to avoid complicated SQL joins
    

Videos will be available at: https://www.youtube.com/@eurorust.