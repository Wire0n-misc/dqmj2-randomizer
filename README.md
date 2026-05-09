# DQMJ2 Randomizer

---

## Presentation

DQMJ2 Randomizer is a tool made in Python  that allows you to randomize monsters encounter in Dragon Quest Monster Joker 2.This only works for EU (European) versions of the game.

## Requirements

This tool needs Python 3.11.4 at least in order to run!
Also for now it only works with EU versions of DQMJ2.

## Installing the randomizer

1. In a folder of your choice,open a CMD and type:
   
   ```
   git clone https://github.com/Wire0n-misc/dqmj2-randomizer.git
   ```

2. Open DQMJ2_Randomizer.bat

3. Wait for it to open a browser tab or in your browser URL bar type : 127.0.0.1:8080

4. When you're done with the tool just close the tab and the command line interface.

## Features

- Seed : choose the seed used for randomization. If none,then a random one will be choosed.

- Rank filtering : choose which monsters can appear based on selected ranks.

- Family filtering: choose which monsters can appear based on selected families.

- Size filtering: choose which monsters can appear based on selected sizes.

- Challenges:
  
  - No flee : Make it impossible to flee any battle!
  
  - Stronger monsters : Every enemy monster receive a 50% stats raise (HP,MP,ATK,DEF,AGI,WIS)

- Other features coming soon!

## Important notes

1. Ability to flee a battle is directly bind to monsters themselves.So it is possible that you can't escape a fight because of a boss or special monster present in battle.I'll adress this issue soon.

2. In most cases, even if big monsters overlap other slots, it isn't an issue since the game can handle it, despite being a visual mess. But there is a few cases where a specific configuration might be problematic because when you're attacking enemies the game will crash.I noticed that when it happens there is always a giant monster involved. Hopefully I found a turnaround : battling with only one monster will give game enough memory space to not crash.
