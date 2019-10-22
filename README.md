# Mental Poker

Mental Poker is the common name for a set of cryptographic problems that concerns playing a fair game over distance without the need for a trusted third party [read more](https://en.wikipedia.org/wiki/Mental_poker)

This is a cryptographic toolbox for the basic building blocks of mental card games written in python. The main operations underlying many card games are:

1. shuffling (randomizing the order of cards)
2. dealing (locking a shared order to unknown cards)
3. reavealing (opening unknown cards to one or all parties)

This toolbox is the cryptographic basis for a set of parties at a distance to compute these "deck" operations in a provably fair way. 

*(how the parties communicate with each other, and the logic of any specific card game are outside the scope of this package)*

## Install

`pip install mentalpoker`

python >=3.6

