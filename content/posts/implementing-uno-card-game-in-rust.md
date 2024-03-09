---
title: "Implementing the Uno Card Game in Rust"
date: 2024-03-09T00:06:13+01:00
last_modified: .Lastmod
draft: false
---

After having [implemented](https://github.com/mloning/uno-py/) the Uno card game in Python, I decided to [rewrite](https://github.com/mloning/uno-rs) it in Rust. 

Rewriting Uno in Rust has taught me a lot, as Rust forces you define objects and their interactions more clearly, and encourages you to keep them as simple as possible.

For Uno rules, see [Wikipedia](<https://en.m.wikipedia.org/wiki/Uno_(card_game)>).

## Main objects

I represent key game concepts in the following objects: 

* a single `Card` struct with a symbol and optional color field, with symbol and color each being represented by an enum; one could further distinguish between multiple types of cards, for example color vs wild cards and action vs non-action cards, and use structs, enums or traits to implement each of them; ultimately, keeping a single card struct and differentiating by card symbol was easy enough and much simpler
* the `Deck` of cards as a deque (or double-ended queue) of cards, to allow for appending at the top and bottom of the deck
* the discard `Pile` as a vector of cards
* a `Dealer` struct, handling the interactions between the `Deck` and `Pile`
* a `Player` struct, encapsulating the player's hand and strategy and providing methods for playing cards and taking new cards onto the hand
* a `RandomStrategy` as a simple strategy to play cards 
* a `Strategy` trait to define a common interface for different strategies to select which card to play given the set of legally playable cards and potentially the history of previous plays
* a `Play`, which is either a card if the player was able to play a card, otherwise None
* the `PlayerCycle` handling player turns; when "skip" or "reverse" action cards are played, the next player is skipped or the direction of the cycle is reversed, respectively

## Handling state 

State involves the following objects:

* Deck
* Pile
* Player hand
* Player cycle, including current player and cycle direction (forward or reversed)
* Color for wild cards which is set when played and reset when recycled from the pile into the deck
* Player strategy, potentially keeping track of the history of previous plays 

Some observations on state:

* The top card references the pile (shared reference), but the pile changes when a played card is discarded (mutable reference). To avoid the conflict from having a shared and mutable reference at the same time, instead of passing a reference to the top card, I copy it. In theory, there should not be a conflict though, as the reference to the top card is only needed until a card is played. The reference to the top card is no longer needed when the pile changes. So the lifetimes of the references would not overlap, but I'm not sure how to implement that.
* When the deck is empty, the pile is recycled into the deck, including all cards except the top card. The color of wild cards is reset when recycled into the deck. Having a `Dealer` object which encapsulates both makes this easy to handle.
* An action card must only be executed once, right after it was played, even though the card may stay on top of the pile for various turn, as the next player(s) may not be able to play a card. To handle this, I decided to execute actions depending on the `Play` object, and not the current top card. So, when no new card is played, even though the top card remains the same, the `Play` object changes to None. 
* I distinguish between playable cards and legal cards. Playable cards are usually the player's hand, except in the situation when no card was played and a new card is drawn, where the new card will be the only playable card. On the other hand, legal cards are those cards that, given the top card, can legally be played, following the usual rules of symbol and color matches and wild cards. Legal cards are always a subset of playable cards. The player strategy selects a card from the legal cards. 
* We need to keep track of cards. For example, when playing a card, we first select the legal cards from the player's hand, then select which card we want to play from the legal cards, and finally need to remove the selected card from the player's hand. We could pass a (mutable) reference to the player's hand and pop the selected card from the hand. However, the legal cards are usually a subset of the hand, and the selection algorithm only needs to deal with (unique) legal cards, not all playable cards. When copying cards, we have to compare cards and find an equal card to remove from the player's hand. A complication is that when taking a copy, for wild cards, the selected card has a set color, whereas the card on the player's hand will still be colorless.
* The player cycle starts with the first player and endlessly cycles through the players. It must be reversible so that instead of going to the next player, we go back to the previous player, and then continue the cycle in reverse direction. So the cycle needs to keep track of the current player (or index) and direction. When the first card is a reverse action card, the cycle starts with the last player and continues in reverse direction. 

## Thoughts on extensibility

Adding a new player strategy should be straightforward given the `Strategy` trait. For example, adding a strategy using human-input or machine learning could be added. The strategy interface currently only takes the set of legal cards as input, but could be extended to also take a history of previous plays. It returns a `Play`, that is, either the card selected to play or None.

Adding new cards will be more involved, especially for action cards. Currently, action cards are simply defined by a special symbol (e.g. "reverse", "skip" or "draw-2"). They do not define how to execute their actions. Instead, a match expression in the main loop of the game determines which action to execute and defines the corresponding actions for each action symbol. To enhance extensibility, we would have to define an interface for handling actions (e.g. forcing the next player to draw new cards or mutating the player cycle) as well as card state (e.g. resetting state when recycling the pile into the deck) and actions. 

## Resources

While implementing Uno, I found these resources on Rust particularly useful:

* [Educational blog for Rust beginners](https://github.com/pretzelhammer/rust-blog/tree/master)
* [SO answer on lifetimes](https://stackoverflow.com/a/70674633/9334962)
* [The Rust Programming Language](https://doc.rust-lang.org/book/title-page.html)
* [Programming Rust: Fast, Safe Systems Development](https://www.goodreads.com/book/show/25550614-programming-rust)
* [Rustlings Coding Exercises](https://github.com/rust-lang/rustlings)

