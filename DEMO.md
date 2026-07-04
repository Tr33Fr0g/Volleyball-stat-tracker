# Demo

A real terminal session of `volleyball-tracker` (installed via pipx) — recording two players, viewing their analytics, comparing them head-to-head, and saving the stat sheet.

```
========================================
  Volleyball Stat Tracker
========================================
1. Record player stats
2. View analytics
3. Save stats
4. Load stats
5. Look up pro team
6. Compare two player stats
7. Exit

Select an option: 1
Enter player name: Alex
Recording stats for Alex:
  kills: 20
  errors: 5
  attempts: 40
  aces: 3
  digs: 10
  blocks: 2
  sets_played: 3
Stats recorded for Alex.

Select an option: 1
Enter player name: Jordan
Recording stats for Jordan:
  kills: 15
  errors: 8
  attempts: 35
  aces: 1
  digs: 14
  blocks: 4
  sets_played: 3
Stats recorded for Jordan.

Select an option: 2
Recorded players
  1. Alex
  2. Jordan
Select a player_number: 1

========================================
  Stats for Alex
========================================
  Kills:        20
  Errors:       5
Attempts:       40
Aces:           3
Digs:           10
Blocks:         2
Sets Played:    3
----------------------------------------
Hitting %: 0.375
Kill Efficiency: 0.500
Aces/Set: 1.000
Digs/Set: 3.333
Blocks/Set: 0.667
Hitter Rating: Amazing
========================================

Select an option: 2
Recorded players
  1. Alex
  2. Jordan
Select a player_number: 2

========================================
  Stats for Jordan
========================================
  Kills:        15
  Errors:       8
Attempts:       35
Aces:           1
Digs:           14
Blocks:         4
Sets Played:    3
----------------------------------------
Hitting %: 0.200
Kill Efficiency: 0.429
Aces/Set: 0.333
Digs/Set: 4.667
Blocks/Set: 1.333
Hitter Rating: Good
========================================

Select an option: 6
Enter the names of the two players to compare.
Players can be from the current session or from saved files.

Enter first player name: Alex
Enter second player name: Jordan

============================================================
  Alex  vs  Jordan
============================================================
  kills                  20 <-- 15
  errors                  5 <-- 8
  attempts               40 <-- 35
  aces                    3 <-- 1
  digs                   10 --> 14
  blocks                  2 --> 4
  sets_played             3  =  3
------------------------------------------------------------
  Hitting %           0.375 <-- 0.200
  Kill Efficiency     0.500 <-- 0.429
  Aces/Set            1.000 <-- 0.333
  Digs/Set            3.333 --> 4.667
  Blocks/Set          0.667 --> 1.333
------------------------------------------------------------
  Rating             Amazing   Good
============================================================
  <-- = Alex leads  :  --> = Jordan leads

Select an option: 3
Enter filename (default: match_1) 
Stats saved to stats/match_1.json

Select an option: 7
Goodbye!
```
