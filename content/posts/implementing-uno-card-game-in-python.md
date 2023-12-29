---
title: "Implementing the Uno card game in Python"
date: 2023-12-20T19:16:09+01:00
last_modified: .Lastmod
draft: false
---

A friend of mine recently implemented the card game [Uno] as a programming exercise in Python and asked me for feedback. I thought it's a good idea to try it myself and then compare notes. 

You can find my implementation [here].

I largely followed an object-oriented approach, with the following classes to handle the different pieces of the game state:

* a playing card to represent the different cards of the game,
* a player to represent each player, their possible actions (play or draw a card) and their state (their hand), 
* a player's strategy to select which card to play, 
* a collection of players to handle turns, player cycles and any changes to it (e.g. "reverse" and "skip"),
* a dealer to interact with the card deck and discard pile.

To run everything, I have written a function that orchestrates the game.
After initializing the deck, discard pile, dealer and players, it cycles over the collection of players, calling each player to play a card if possible and otherwise draw a new card.
If an action card is played (e.g. "draw 2" or "skip"), the action is executed for the next player before resuming the player cycle.

For now, I have implemented two simple strategies, one always selects a random card, the other passes on input from a human player.

The main challenge was managing the game state, especially the settable color of "wild" cards and player cycle changes. 

Next steps would be to add more features, including smarter strategies (e.g. reinforcement learning) and commonly played rule extensions like being able to stack penalties from action cards. 

I'd also like to re-write it in another programming language, perhaps Rust or C#, and try out a less object-oriented approach.

[Uno]: https://en.wikipedia.org/wiki/Uno_(card_game)
[here]: https://github.com/mloning/uno-py
