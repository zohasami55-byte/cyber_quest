# 🕹️ Cyber Quest: Breakout

A retro **cyberpunk arcade game** built with **Streamlit** and an **HTML5 Canvas** game engine.
You are a digital detective — bounce the glowing laser packet with your neon paddle to
smash the "Glitch Blocks" (malware) and save **ADA**, a broken AI system!

---

## 🎮 How to Play

1. **Start the game** (see *How to Run* below).
2. **Click once** on the game area so it can hear your keyboard.
3. Press **SPACE** to begin.
4. Move your paddle with the **← Left** and **→ Right** arrow keys.
5. Bounce the packet to destroy every block. Don't let it fall past your paddle!

### Goal
Clear all the blocks in each level to advance. Beat all **3 levels** to win.

# ASSIGNMENT REPORT: AI COLLABORATION SUMMARY
## Project 1: Cyber Quest - Breakout Game

### 1. Initial Requirement & Architecture Shift
* **Objective:** To build an interactive, tech-themed educational game tailored for an 8th-grade student with no prior IT background.
* **Initial Approach:** The project was originally conceptualized as a text-based terminal quiz engine. However, real-time evaluation proved that a standard text question-and-answer format was too static and dry to maintain high engagement.
* **The Pivot:** To maximize gamification, the architecture was completely shifted away from standard text inputs. The game frontend was redesigned around a visual, real-time 2D environment powered by Streamlit and an embedded HTML5 Canvas component.

### 2. Engineering & Feature Iterations
* **UI/UX Overhaul:** Developed a retro, cyberpunk arcade environment named "Cyber Quest: Breakout". Features a dark grid canvas layout with glowing neon elements and code blocks encapsulated in HTML tags (`</>`).
* **Game Loop Implementation:** Integrated native keyboard listener controls (Arrow Keys for paddle navigation, Spacebar for state handling) along with collision boundary physics for the moving laser packet (ball).
* **Dynamic Multi-Level Logic:** Scaled the game engine to manage game states sequentially across 3 levels. Each progressive level programmatically scales up the difficulty matrix by adjusting the block grid complexity and multiplier-based ball speed velocity.

### 3. Tooling & Technologies Utilized
* **Bonsai CLI & Claude:** Leveraged for iterative prompt engineering, state management orchestration, and source code updates.
* **Python & Streamlit:** Used to scaffold the localized app server framework and handle session states.
* **HTML5 Canvas & JavaScript:** Embedded inside `st.components.v1.html` to run smooth, lag-free 60FPS animation rendering loops.
---

## 🏆 Game Features

- **3 Levels** with rising difficulty:
  | Level | Block Layout        | Ball Speed |
  |-------|---------------------|------------|
  | 1     | Solid 4-row wall    | 1.0× (normal) |
  | 2     | Full double wall (6 rows) | 1.3× (faster) |
  | 3     | Hard zigzag pattern | 1.6× (fastest) |
- **Live scoreboard** — SCORE, LEVEL, and LIVES shown at the top of the canvas.
- **3 lives** — lose one each time the packet falls off the bottom.
- **Reward popups** — each block flashes a tech message like `CPU Hacked!` or `Firewall Secured!`.
- **Neon cyberpunk theme** — dark terminal grid with glowing blocks, paddle, and ball.
- **Win / Lose screens** — `LEVEL COMPLETE!`, `GAME OVER`, and `★ VICTORY ★`, all drawn inside the game.

---

## ⌨️ Controls

| Key            | Action                          |
|----------------|---------------------------------|
| **← / →**      | Move the paddle left / right    |
| **SPACE**      | Start game / next level / retry |

---

## 💻 How to Run

> **Important:** This game must be run with **Python 3.12**.
> Python 3.14 is too new and causes Streamlit to crash on this computer.

1. Open a terminal (PowerShell) in this folder: `D:\1st_assignment`
2. Run this command:

   ```
   py -3.12 -m streamlit run cyber_quest.py
   ```

3. The game opens automatically in your web browser.
4. To stop the game, click the terminal and press **Ctrl + C**.

### First-time setup (only if Streamlit is not installed)

```
py -3.12 -m pip install streamlit
```

---

## 🧠 How the Code Works (for learning)

- **Python + Streamlit** builds the web page *once*, then hands control to the browser.
- The whole game engine is **JavaScript inside an HTML5 `<canvas>`**, embedded with
  `st.components.v1.html`.
- The heart of the game is the **`loop()` function**. About 60 times per second it:
  1. Clears the screen and draws the grid,
  2. Moves the paddle and ball,
  3. Checks for collisions (walls, paddle, blocks),
  4. Redraws everything,
  5. Calls `requestAnimationFrame(loop)` to run again.
- A single **`level`** variable controls the block layout and ball speed. When all
  blocks are cleared, the code either loads the next level or shows the victory screen.

---

## 📁 Files

| File            | Description                          |
|-----------------|--------------------------------------|
| `cyber_quest.py`| The complete game (Python + JS).     |
| `README.md`     | This file.                           |

---

## 🛠️ Requirements

- **Python 3.12**
- **Streamlit** (`pip install streamlit`)
- Any modern web browser (Chrome, Edge, Firefox)

---

Made for learning Python, Streamlit, and game programming. Have fun, detective! 🦸💚
