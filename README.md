# WordleHelper

![](https://i.imgur.com/cVKJ1uK.png)

### Introduction

WordleHelper suggests words to help players better enjoy the hit game [Wordle](https://www.nytimes.com/games/wordle/index.html). Both the general mode and the hard mode are supported.

WordleHelper hits the corrrect word with an average of **_3.53_** trials. For both game modes, **100%** Wordle words can be guessed within 6 trials, while **over 91%** of the words can be guessed in the first 4 tiles.

### Usage

#### How to run WordleHelper?

```
pip3 install -r requirements.txt
python3 solver.py [--hard]
```

#### How to play Wordle with WordleHelper’s assistance?

1. WordleHelper suggests at most 3 words for every guess. Pick the word you like as your guess.
2. Enter the word you picked, e.g. `soare[Enter]`
3. Enter the guess result, e.g. `g----[Enter]`, where `g`, `y`, `-` represents the green, yellow, and grey block, respectively.
4. Continue, until you hit the word!

#### Example

```
100%|██████████████████████████████████████████████████████████████████| 12972/12972 [00:17<00:00, 721.83it/s]
The suggested words are ['soare', 'roate', 'raise', 'raile', 'reast'] (2315 candidates left).
Enter the word you guessed: soare
Enter the guessing result, e.g. y-yg-: g----
--------------------------------------------------------------------------------------------------------------
100%|█████████████████████████████████████████████████████████████████| 12972/12972 [00:01<00:00, 6511.60it/s]
The suggested words are ['thilk', 'think', 'plink', 'clint', 'glint'] (63 candidates left).
Enter the word you guessed: thilk
Enter the guessing result, e.g. y-yg-: --ggy
--------------------------------------------------------------------------------------------------------------
100%|██████████████████████████████████████████████████████████████████████████| 1/1 [00:00<00:00, 131.63it/s]
The suggested words are ['skill'] (1 candidates left).
Enter the word you guessed: skill
Enter the guessing result, e.g. y-yg-: ggggg
--------------------------------------------------------------------------------------------------------------
Congratulations!!
```
