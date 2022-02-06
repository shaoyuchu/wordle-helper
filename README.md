# WordleHelper

![](https://i.imgur.com/cVKJ1uK.png)

### Introduction

WordleHelper suggests words to helps players better enjoy the hit game [Wordle](https://www.powerlanguage.co.uk/wordle/).

WordleHelper hits the corrrect word with an average of 3.53 trials. 91% of words can be guessed in the first 4 tiles.

### Usage

#### How to run WordleHelper?

```
pip3 install -r requirements.txt
python3 solver.py
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
