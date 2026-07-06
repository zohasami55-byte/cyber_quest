# ==========================================================
#  CYBER QUEST: BREAKOUT  🕹️
#  A real-time 2D arcade game (HTML5 Canvas + JavaScript)
#  wrapped inside a Streamlit page.
#
#  HOW TO RUN (use Python 3.12):
#     py -3.12 -m streamlit run cyber_quest.py
#  Then click the game once and use the LEFT / RIGHT arrow keys.
# ==========================================================

import streamlit as st
import streamlit.components.v1 as components

# ---------- STREAMLIT PAGE FRAME ----------
st.set_page_config(page_title="Cyber Quest: Breakout", page_icon="🕹️", layout="centered")

# A dark background so the whole page matches the cyberpunk game.
st.markdown(
    """
    <style>
    .stApp { background-color: #05060a; }
    h1, p { color: #00f6ff !important; text-align: center;
            text-shadow: 0 0 10px #00f6ff; font-family: monospace; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🕹️ CYBER QUEST: BREAKOUT")
st.markdown(
    "<p>Bounce the laser packet with your neon paddle. "
    "Destroy every Glitch Block to purge the malware!<br>"
    "Click the game, then use ← and → arrow keys. Press SPACE to start / restart.</p>",
    unsafe_allow_html=True,
)

# ==========================================================
#  THE GAME ENGINE  —  pure HTML5 Canvas + JavaScript
#  Everything below lives in the browser and runs at 60 FPS.
# ==========================================================
GAME_HTML = r"""
<div style="display:flex; justify-content:center;">
  <canvas id="game" width="760" height="520"
          style="background:#05060a; border:2px solid #00f6ff;
                 border-radius:10px; box-shadow:0 0 25px #00f6ff;
                 outline:none;" tabindex="0"></canvas>
</div>

<script>
const canvas = document.getElementById("game");
const ctx    = canvas.getContext("2d");
const W = canvas.width, H = canvas.height;

// Make sure the arrow keys go to the game (not the page scroll).
canvas.focus();
canvas.addEventListener("click", () => canvas.focus());

// ---------- GAME STATE ----------
let state = "start";          // "start" | "playing" | "over" | "win" | "levelclear"
let score = 0;
let lives = 3;
let level = 1;                 // current level (1, 2, or 3)

// Each level's ball speed gets faster. Level 1 = base speed.
const speedByLevel = { 1: 1.0, 2: 1.3, 3: 1.6 };

// ---------- PADDLE (the neon bar you control) ----------
const paddle = { w: 110, h: 14, x: W/2 - 55, y: H - 40, speed: 8 };

// ---------- BALL (the glowing laser packet) ----------
let ball = { x: W/2, y: H - 60, r: 8, dx: 4, dy: -4 };

// ---------- GLITCH BLOCKS (the malware to destroy) ----------
// Each block has a hidden tech "reward" name shown when broken.
const rewards = ["CPU Hacked!", "Firewall Secured!", "RAM Cleared!",
                 "Virus Deleted!", "Router Fixed!", "AI Rebooted!",
                 "Cache Purged!", "Bug Squashed!"];
const neon = ["#ff003c", "#00f6ff", "#faff00", "#b400ff", "#00ff85"];

let blocks = [];

// A helper that adds one block at grid position (row r, column c).
const cols = 8;
const bw = 80, bh = 26, padX = 8, padY = 10, offX = 30, offY = 50;
function addBlock(r, c) {
  blocks.push({
    x: offX + c * (bw + padX),
    y: offY + r * (bh + padY),
    w: bw, h: bh, alive: true,
    color: neon[(r + c) % neon.length],
    reward: rewards[(r * cols + c) % rewards.length]
  });
}

// Build a different block layout for each level.
function buildBlocks() {
  blocks = [];
  if (level === 1) {
    // LEVEL 1: a solid 4-row wall.
    for (let r = 0; r < 4; r++)
      for (let c = 0; c < cols; c++) addBlock(r, c);

  } else if (level === 2) {
    // LEVEL 2: a full DOUBLE row of blocks (6 packed rows).
    for (let r = 0; r < 6; r++)
      for (let c = 0; c < cols; c++) addBlock(r, c);

  } else {
    // LEVEL 3: a hard ZIGZAG pattern (staircase of blocks).
    for (let r = 0; r < 6; r++) {
      for (let c = 0; c < cols; c++) {
        // Only place a block where the row+column makes a zigzag stripe.
        if ((r + c) % 2 === 0) addBlock(r, c);
      }
    }
  }
}
buildBlocks();

// ---------- POPUP (the 1-second "CPU Hacked!" message) ----------
let popup = { text: "", x: 0, y: 0, until: 0 };
function showPopup(text, x, y) {
  popup.text = text; popup.x = x; popup.y = y;
  popup.until = performance.now() + 1000;   // visible for 1 second
}

// ---------- KEYBOARD CONTROLS ----------
let leftDown = false, rightDown = false;
document.addEventListener("keydown", (e) => {
  if (e.key === "ArrowLeft")  { leftDown = true;  e.preventDefault(); }
  if (e.key === "ArrowRight") { rightDown = true; e.preventDefault(); }
  if (e.code === "Space") {
    e.preventDefault();
    if (state === "levelclear") nextLevel();               // go to next level
    else if (state === "start" || state === "over" || state === "win") resetGame();
  }
});
document.addEventListener("keyup", (e) => {
  if (e.key === "ArrowLeft")  leftDown = false;
  if (e.key === "ArrowRight") rightDown = false;
});

// ---------- RESET / START A FRESH GAME (from Level 1) ----------
function resetGame() {
  score = 0; lives = 3; level = 1;
  paddle.x = W/2 - paddle.w/2;
  buildBlocks();
  launchBall();
  state = "playing";
}

// ---------- ADVANCE TO THE NEXT LEVEL ----------
function nextLevel() {
  level++;
  paddle.x = W/2 - paddle.w/2;
  buildBlocks();
  launchBall();
  state = "playing";
}

// Launch the ball at a speed that depends on the current level.
function launchBall() {
  const s = speedByLevel[level];      // 1.0, 1.3, or 1.6
  ball.x = W/2; ball.y = H - 60;
  ball.dx = 4 * s * (Math.random() < .5 ? 1 : -1);
  ball.dy = -4 * s;
}

// ---------- DRAWING HELPERS ----------
function glowRect(x, y, w, h, color) {
  ctx.save();
  ctx.shadowColor = color; ctx.shadowBlur = 15;
  ctx.fillStyle = color; ctx.fillRect(x, y, w, h);
  ctx.restore();
}
function glowText(text, x, y, size, color) {
  ctx.save();
  ctx.shadowColor = color; ctx.shadowBlur = 12;
  ctx.fillStyle = color; ctx.font = size + "px monospace";
  ctx.textAlign = "center"; ctx.fillText(text, x, y);
  ctx.restore();
}

// ---------- THE MAIN GAME LOOP (runs ~60 times a second) ----------
function loop() {
  // 1. Clear the screen with a faint grid for the "terminal" look.
  ctx.fillStyle = "#05060a";
  ctx.fillRect(0, 0, W, H);
  ctx.strokeStyle = "rgba(0,246,255,0.06)";
  for (let gx = 0; gx < W; gx += 38) { ctx.beginPath(); ctx.moveTo(gx,0); ctx.lineTo(gx,H); ctx.stroke(); }
  for (let gy = 0; gy < H; gy += 38) { ctx.beginPath(); ctx.moveTo(0,gy); ctx.lineTo(W,gy); ctx.stroke(); }

  if (state === "playing") {
    // 2. Move the paddle from key presses.
    if (leftDown)  paddle.x -= paddle.speed;
    if (rightDown) paddle.x += paddle.speed;
    if (paddle.x < 0) paddle.x = 0;
    if (paddle.x + paddle.w > W) paddle.x = W - paddle.w;

    // 3. Move the ball.
    ball.x += ball.dx; ball.y += ball.dy;

    // 4. Bounce off the side and top walls.
    if (ball.x - ball.r < 0 || ball.x + ball.r > W) ball.dx *= -1;
    if (ball.y - ball.r < 0) ball.dy *= -1;

    // 5. Bounce off the paddle.
    if (ball.y + ball.r >= paddle.y &&
        ball.x >= paddle.x && ball.x <= paddle.x + paddle.w &&
        ball.dy > 0) {
      ball.dy *= -1;
      // Angle the bounce based on where it hit the paddle
      // (faster levels swing the ball wider).
      let hit = (ball.x - (paddle.x + paddle.w/2)) / (paddle.w/2);
      ball.dx = hit * 5 * speedByLevel[level];
    }

    // 6. Fell below the paddle -> lose a life.
    if (ball.y - ball.r > H) {
      lives--;
      if (lives <= 0) { state = "over"; }
      else { launchBall(); }
    }

    // 7. Ball hits a glitch block -> destroy it, score, show popup.
    for (const b of blocks) {
      if (b.alive &&
          ball.x > b.x && ball.x < b.x + b.w &&
          ball.y - ball.r < b.y + b.h && ball.y + ball.r > b.y) {
        b.alive = false;
        ball.dy *= -1;
        score += 10;
        showPopup(b.reward, b.x + b.w/2, b.y);
        break;
      }
    }

    // 8. All blocks gone -> next level, or final VICTORY on Level 3.
    if (blocks.every(b => !b.alive)) {
      if (level >= 3) state = "win";
      else state = "levelclear";
    }
  }

  // ---------- DRAW EVERYTHING ----------
  // Glitch blocks
  for (const b of blocks) {
    if (b.alive) {
      glowRect(b.x, b.y, b.w, b.h, b.color);
      ctx.fillStyle = "#05060a";
      ctx.font = "11px monospace"; ctx.textAlign = "center";
      ctx.fillText("</>", b.x + b.w/2, b.y + b.h/2 + 4);
    }
  }
  // Paddle + ball
  glowRect(paddle.x, paddle.y, paddle.w, paddle.h, "#00ff85");
  ctx.save();
  ctx.shadowColor = "#faff00"; ctx.shadowBlur = 20;
  ctx.fillStyle = "#faff00";
  ctx.beginPath(); ctx.arc(ball.x, ball.y, ball.r, 0, Math.PI*2); ctx.fill();
  ctx.restore();

  // Score + level + lives bar
  glowText("SCORE: " + score, 80, 28, 18, "#00f6ff");
  glowText("LEVEL: " + level, W/2, 28, 18, "#faff00");
  glowText("LIVES: " + "❤".repeat(Math.max(lives,0)), W - 110, 28, 18, "#ff003c");

  // The 1-second reward popup
  if (popup.text && performance.now() < popup.until) {
    glowText(popup.text, popup.x, popup.y, 20, "#ffffff");
  }

  // ---------- OVERLAY SCREENS ----------
  if (state === "start") {
    glowText("CYBER BREAKOUT", W/2, H/2 - 30, 42, "#00f6ff");
    glowText("Press SPACE to start", W/2, H/2 + 20, 22, "#faff00");
    glowText("Move with  ←   →  arrow keys", W/2, H/2 + 55, 18, "#00ff85");
  }
  if (state === "levelclear") {
    glowText("LEVEL " + level + " COMPLETE!", W/2, H/2 - 10, 44, "#00ff85");
    glowText("Press SPACE for Level " + (level + 1), W/2, H/2 + 35, 24, "#faff00");
  }
  if (state === "over") {
    glowText("GAME OVER", W/2, H/2 - 10, 52, "#ff003c");
    glowText("Final Score: " + score, W/2, H/2 + 35, 24, "#00f6ff");
    glowText("Press SPACE to retry", W/2, H/2 + 70, 18, "#faff00");
  }
  if (state === "win") {
    glowText("★ VICTORY ★", W/2, H/2 - 10, 52, "#00ff85");
    glowText("ADA is safe! Score: " + score, W/2, H/2 + 35, 24, "#00f6ff");
    glowText("Press SPACE to play again", W/2, H/2 + 70, 18, "#faff00");
  }

  requestAnimationFrame(loop);   // keep the loop running forever
}

loop();   // start the engine
</script>
"""

# Embed the game. Height must fit the canvas + a little margin.
components.html(GAME_HTML, height=560)

st.caption("Tip: if the arrow keys don't work, click once on the game area to focus it.")
