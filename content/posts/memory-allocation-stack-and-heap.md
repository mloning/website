---
title: "Stack and Heap"
date: 2025-11-13T22:11:10+01:00
draft: true
---

The stack and the heap are two separate areas of memory used during program execution.
They differ in how memory is managed, how fast it's to access, and the lifetime of the data stored.

## Stack

The stack is used for static memory allocation.

It operates on a Last-In, First-Out (LIFO) principle.

Stack allocation and deallocation is extremely fast because it only involves moving a single pointer (the stack pointer) and the memory is contiguous.

Memory is automatically allocated when a function is called and automatically freed when the function returns (when its stack frame is "popped" off).

Data must have a known, fixed size at compile time.
This usually includes function local variables, basic primitive types, and return addresses.

## Heap

The heap is used for dynamic memory allocation.

It is a large pool of memory that is less organized than the stack.
Memory is allocated and deallocated in a less predictable order, which can lead to memory fragmentation.

Allocation is slower than the stack because the system must search for an empty block of memory large enough for the request.
Accessing data is also slower because you have to follow a pointer from the stack to the heap.

Data can live longer than the function that created it.
Management requires either manual deallocation (like in C/C++), automatic cleanup via a garbage collector, or a smart pointers/ownership system.

Used for data whose size is unknown at compile time or that needs to persist across function calls, such as large objects, dynamic arrays and custom classes.

## Python

Almost everything is an object stored on the heap, including all Python objects (e.g. lists, dictionaries, custom class instances, strings, most integers and floats).
Python manages this memory automatically using a private heap, a reference counting system for quick deallocation, and a cyclic garbage collector for breaking circular references.

The stack primarily stores reference variables (pointers) to objects, function call frames, and primitive local values.

When a function is called, a new stack frame is created.

## Rust

Rust, as a systems programming language, gives you explicit control over stack versus heap allocation, which is managed through its ownership and borrowing system.
By default, data is stored on the stack where possible.

Data types with a known size at compile time are allocated on the stack (e.g. `array: [i32; 4]`).

Dynamically sized data is stored on the heap, with a type that manages heap data allocation and a pointer on the stack to the data on the heap.
The pointer to the data is stored on the stack, while the actual data lives on the heap.

For example, `String` is a dynamic, growable type.
When defining a `String`, e.g. `let s = String::from("hello")`, the `s` variable itself is on the stack (pointer, length, capacity).
The actual string data ("hello") is stored on the heap.

## Pointer

### Raw pointer

A (raw) pointer is the most basic type of pointer in programming languages like C, C++, and Rust, where they are called unsafe pointers.

It is a variable that stores the memory address of some data.

A raw pointer holds a number, which is the address in the computer's RAM where the data is stored.

Unlike smart pointers, raw pointers provide no automatic memory management or safety features.

- They don't indicate who is responsible for cleaning up the memory they point to.
- They don't automatically deallocate the memory on the heap when they go out of scope.

The programmer is responsible for correctly allocating and deallocating the memory block pointed to.
If they fail to do so, it leads to:

- Memory leaks: the memory is never freed, reducing available RAM.
- Dangling pointers: the memory is freed, but the pointer still holds the address, pointing to invalid or reused data; dereferencing a dangling pointer causes undefined behavior (e.g. crashes or security vulnerabilities).

### Smart pointer

A smart pointer is an abstract data type that mimics the behavior of a traditional raw pointer but adds extra features, most commonly automatic memory management and resource cleanup.

It's essentially a structure that owns a pointer and a block of memory on the heap.
When the smart pointer itself goes out of scope on the stack, it automatically executes cleanup code (usually by calling its `Drop` implementation in Rust or its destructor in C++) to deallocate the memory it points to on the heap.
This prevents memory leaks.

In C++, the general rule is to use a smart pointer (`std::unique_ptr` or `std::shared_ptr`) unless you have a specific, low-level requirement for a raw pointer.

#### Smart pointers in Rust

| Smart Pointer    | Purpose                                 | Description                                                                                                                                                                    |
| :--------------- | :-------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`Box<T>`**     | **Single Ownership**                    | Stores data on the **heap**. Used when you need to store large or unknown-sized data and want **one owner**. Cleans up memory automatically when it goes out of scope.         |
| **`Rc<T>`**      | **Multiple Ownership (Immutable)**      | **Reference Counting**. Allows **multiple parts** of code to share ownership of the same data (which is immutable). Data is freed only when the reference count drops to zero. |
| **`Arc<T>`**     | **Thread-Safe Multiple Ownership**      | **Atomic Reference Counting**. Similar to `Rc<T>` but uses atomic operations, making it safe to share ownership **across different threads**.                                  |
| **`RefCell<T>`** | **Interior Mutability (Single Thread)** | Allows mutation of data inside an otherwise **immutable** structure. The borrowing check happens at **runtime** and is often used with `Rc<T>`.                                |
| **`Weak<T>`**    | **Non-Owning Reference**                | Used with `Rc<T>` to create a reference that **doesn't contribute to the reference count**. Essential for breaking **reference cycles** to prevent memory leaks.               |

### Fat pointer

A fat (or wide) pointer is a pointer that is twice the size of a normal (or thin) pointer because it stores the memory address along with metadata about the data being pointed to.

For example, Rust makes heavy use of fat pointers for Dynamically Sized Types (DSTs), which are types whose size isn't fixed until runtime.

- A simple reference to an integer (`&i32`) is a thin pointer.
- A reference to a slice (`&[i32]`) is a fat pointer.
