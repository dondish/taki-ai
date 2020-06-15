# Taki AI
This is an experiment of teaching an AI to play [Taki](https://www.takigame.com/).

This project uses Keras and Tensorflow for Neural Networks.

The game does not use the 3+, 3+ breaker cards and the king card (new Taki cards).

# Algorithm
Uses DQN with experience replay.

## Card Vector
Cards are a vector with dimension of the number of cards, with one at the respective index.

A deck is a vector sum of card vectors.

## Action Space
The action space takes the card scalar if it's the play card action, or draw card scalar, or close taki scalar for other instances.

## State Space
A concatenation of the following vectors / scalars:
* The hand of the player
* The discard pile
* The state
* The amount of 2+ stacked
* The card shown on the table 

# Using the project
`train.py` trains the AI.

`main.py` let's you play against opponents with a random policy.

`game.py` defines all the classes needed to run the game.

`agents` a folder that includes playable agents.

`agents/dqn.py` the DQN agent.

`agents/human.py` the human agent.

`agents/random.py` an agent with a random policy.

`models` a folder that includes precomputed models. 

# License

```
Copyright (c) 2020 Oded "Dondish" Shapira

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```