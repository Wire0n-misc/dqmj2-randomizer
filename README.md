# DQMJ2 Randomizer

---

## ℹ️Presentation

DQMJ2 Randomizer is a tool made in Python  that allows you to randomize monsters encounter in Dragon Quest Monster Joker 2.This only works for EU (European) versions of the game.

⚠️**This tool is regulary updated, so check for updates and fixes !**

## 📝Requirements

This tool needs Python 3.11.4 at least in order to run!
Also for now it only works with EU versions of DQMJ2.

## 📥Installing and running the randomizer

1. You can either do this:
   
   In a folder of your choice,open a CMD and type:
   
   ```
   git clone https://github.com/Wire0n-misc/dqmj2-randomizer.git
   ```
   
   Or go to releases page and download the lastest release:
   
   [Release DQMJ2 Randomizer V1.0 · Wire0n-misc/dqmj2-randomizer · GitHub](https://github.com/Wire0n-misc/dqmj2-randomizer/releases/tag/DQMJ2_Randomizer))

2. Open DQMJ2_Randomizer_Windows.bat on Windows. Linux version will come soon.

3. Wait for it to open a browser tab or in your browser URL bar type : 127.0.0.1:8080

4. When you're done with the tool just close the tab and the command line interface.

## ✨Features

- Seed : choose the seed used for randomization. If none,then a random one will be choosed.

- Rank filtering : choose which monsters can appear based on selected ranks.

- Family filtering: choose which monsters can appear based on selected families.

- Size filtering: choose which monsters can appear based on selected sizes.

- Challenges:
  
  - No flee : Make it impossible to flee any battle!
  
  - Stronger monsters : Every enemy monster receive a 50% stats raise (HP,MP,ATK,DEF,AGI,WIS)

- Other features coming soon!

## 🚨Important notes

In most cases, even if big monsters overlap other slots, it isn't an issue since the game can handle it, despite being a visual mess. But there is a few cases where a specific configuration might be problematic because when you're attacking enemies the game will crash.I noticed that when it happens there is always a giant monster involved. Hopefully I found a turnaround : battling with only one monster will give game enough memory space to not crash.

**What to do if you're stuck then even if you pulled this trick and it doesn't work?**

There is a way to rerandomize the game from this point without losing your progress if you play on DeSmuMe (a similar technique could be used on different emulator but i haven't tested it):

1. Save you current game by using savestates (choose a slot to save in)

2. Delete or store the .nds file you're currently using AND take note of the file name(It's very important!).

3. Randomize the game with a different seed.

4. Put the newly randomized .nds rom in the same folder the old one was and rename it EXACTLY like the old one.

5. Start the emulator and load your savestate

6. You can now redo your problematic battle: the monsters will change and it might be possible now without crashing.

If you want to go back to your old rom,then do the same as above and just invert the two roms.
