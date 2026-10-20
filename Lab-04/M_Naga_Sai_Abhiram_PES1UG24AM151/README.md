# Lab 4 - Vibe Coding: Bubble Bobble

## Objective
Fix the existing Python-based Bubble Bobble game and implement the features specified in the assignment README using a vibe-coding tool.

## Changes Implemented

### 1. Fixed Bubble-Enemy Collision Detection
Corrected the squared-distance comparison in `trap_enemies()` by using the squared collision radius (`24 ** 2`). This makes the collision check mathematically consistent.

### 2. Added Dynamic Bubble Colors
Implemented `bubble_tint(bubble)` to change the color of trapped-enemy bubbles according to their remaining lifetime. Empty bubbles retain their default appearance.

### 3. Added Fruit Collection Counter
Implemented `on_fruit_collected(fruit)` to count collected fruits and display the count in the game HUD. Each fruit is counted only once.

### 4. Added Bonus-Life Threshold
Implemented `bonus_life_threshold()` with a threshold of 5000 points. The existing score-milestone logic awards an extra life when a new threshold is crossed.

## Technologies Used
- Python
- Pygame
- Git and GitHub
- LLM

## How to Run

1. Install Python 3.10 or later.
2. Install Pygame:

   ```bash
   python -m pip install pygame
   ```

3. Run the game:

   ```bash
   python game.py
   ```

## Controls
- Left Arrow: Move left
- Right Arrow: Move right
- Up Arrow: Jump
- Space: Shoot bubbles
- R: Reset the game


## Submission Contents
- Before-change gameplay video
- After-change gameplay video
- Updated Python source code
- Exported vibe-coding chat history in PDF format

