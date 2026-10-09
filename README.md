# The Revenge of Farts

A short, atmospheric 2D platformer prototype built entirely from scratch using **Python** and **Pygame**. 

This is my first completed game project, built as a learning journey to understand the core mechanics of 2D game development before moving on to a dedicated game engine like Godot.

## 🎮 Play the Game
You can download the playable Windows `.exe` here:
**[Link to Itch.io page here]**

## 🕹️ Controls
| Action | Key |
| :--- | :--- |
| Move Left/Right | Arrow Keys |
| Jump | Z |
| Attack | X |
| Restart | R |

## ✨ Features
Despite being a prototype, the game includes several custom-built systems:
*   **State Machine:** Tracks player states (IDLE, RUN, JUMP, FALL, ATTACK) to manage movement logic.
*   **Custom Physics:** Implements gravity, acceleration, friction, and variable jump height.
*   **Axis-Separated Collision:** Resolves X and Y collisions independently to prevent "snagging" on platform edges.
*   **Smooth Camera:** Follows the player using linear interpolation (Lerp) and level boundary clamping.
*   **Combat System:** Includes attack hitboxes, cooldown timers, enemy health, and knockback.
*   **Invincibility Frames:** The player flashes green and becomes temporarily invincible after taking damage.

## 🛠️ How to Run the Source Code
If you want to run the raw Python files instead of the `.exe`:

1. Make sure you have Python installed.
2. Clone this repository:
   ```bash
   git clone https://github.com/YourUsername/the-revenge-of-farts.git
