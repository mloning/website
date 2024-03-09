---
title: "Implementing Uno Card Game in Rust"
date: 2024-03-09T00:06:13+01:00
last_modified: .Lastmod
draft: true
---

After [having implemented](https://www.mloning.com/posts/implementing-uno-card-game-in-python/) [Uno] in Python, I decided to rewrite it in Rust.

[Uno]: https://en.m.wikipedia.org/wiki/Uno_(card_game) 

You can find my Rust implementations [here](https://github.com/mloning/uno-rs/). My Python implementation is [here](https://github.com/mloning/uno-py).

For Uno rules, see [Wikipedia](<https://en.m.wikipedia.org/wiki/Uno_(card_game)>).

## Design

### Core objects

I represent key game concepts in the following objects: 

* a single `Card` struct with a symbol and optional color field, with symbol and color each being represented by an enum; one could further distinguish between multiple types of cards, for example color vs wild cards and action vs non-action cards, and use structs, enums or traits to implement each of them; ultimately, keeping a single card struct and differentiating by card symbol was easy enough and much simpler
* the `Deck` of cards as a deque (or double-ended queue) of cards, to allow for appending at the top and bottom of the deck
* the discard `Pile` as a vector of cards
* a `Player` struct 
* a `RandomStrategy` as a simple strategy to play cards 
* a `Strategy` trait to define a common interface for all strategies with a single method for selecting a card from a set of legally playable cards
* a `Play`, which is either a card if the player can play a card or None
* the `PlayerCycle` handling player turns; when skip or reverse action cards are played, the next player is skipped or the direction of the cycle is reversed

### Handling game state 

State involves the following objects:

* Deck
* Pile, especially the top card
* Player hand
* Player cycle, including current player and cycle direction (forward or reversed)
* Color for wild cards which is set when played and reset when recycled from the pile into the deck
* Player strategy, keeping track of the history of plays by other players

Some observations on state:

* The top card references the pile (shared reference), but the pile changes when a played card is discarded (mutable reference). To avoid the conflict from having a shared and mutable reference at the same time, instead of passing a reference to the top card, I copy it. In theory, there should not be a conflict though, as the reference to the top card is only needed until a card is played. The reference to the top card is no longer needed when the pile changes. So the lifetimes of the references would not overlap, but I'm not sure how to implement that.
* When the deck is empty, the pile is recycled into the deck, including all cards except the top card. The color of wild cards is reset when recycled into the deck.
* A action card must only be executed once, right after it was played, even though the card may stay on top of the pile for various turn, as the next player(s) may not be able to play a card.
* I distinguish between playable cards and legal cards. Playable cards are usually the player's hand, except in the situation when no card was played and a new card is drawn, where the new card will be the only playable cards. On the other hand, legal cards are those cards that, given the top card, can legally be played, following the usual rules of symbol and color matches and wild cards. Legal cards are always a subset of playable cards. The player strategy selects a card from the legal cards. 
* We need to keep track of cards. For example, when playing a card, we first select the legal cards from the player's hand, then select which card we want to play from the legal cards, and finally need to remove the selected card from the player's hand. We could pass a (mutable) reference to the player's hand and pop the selected card from the hand. However, the legal cards are usually a subset of the hand, and the selection algorithm only needs to deal with (unique) legal cards, not all playable cards. When copying cards, we have to compare cards and find an equal card to remove from the player's hand. A complication is that when taking a copy, for wild cards, the selected card has a set color, whereas the card on the player's hand will still be colorless.
* The player cycle starts with the first player and endlessly cycles through the players. It must be reversible so that instead of going to the next player, we go back to the previous player and continue the cycle in reverse direction. So the cycle needs to keep track of the current player (or index) and direction. When the first card is a reverse action card, the cycle starts with the last player and continues in reverse direction. 

### Thoughts on extensibility

Some observations on extensibility:

* new cards, especially action cards; this requires implementing both the new card and its action; we would have to define a interface for handling card state (e.g. resetting state when recycling the pile) and actions (e.g. executing an action may force a player to take cards or change the player cycle)
* new player strategy, especially human-input or AI-driven strategies; the strategy interface should take the legal cards and the top card (or a more complete history of plays by other players), and return the next card to play, selected from the playable cards


## Resources

While implementing Uno, I found these resources on Rust particularly useful:

* [Educational blog for Rust beginners](https://github.com/pretzelhammer/rust-blog/tree/master)
* [SO answer on lifetimes](https://stackoverflow.com/a/70674633/9334962)
* [The Rust Programming Language](https://doc.rust-lang.org/book/title-page.html)
* [Programming Rust: Fast, Safe Systems Development](https://www.goodreads.com/book/show/25550614-programming-rust)
* [Rustlings Coding Exercises](https://github.com/rust-lang/rustlings)

