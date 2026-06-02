<div align="center">

<img src="https://raw.githubusercontent.com/AMIR-SHAHROKH/faztoumim/main/docs/logo-preview.png" width="90" alt="فازتومیم logo" />

# فازتومیم — Faztoumim

**A real-time multiplayer party game where you act out moods and your friends try to guess them.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![WebSockets](https://img.shields.io/badge/WebSockets-real--time-6366f1?style=flat-square)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)
[![License: MIT](https://img.shields.io/badge/License-MIT-f472b6?style=flat-square)](LICENSE)

[**Live Demo**](#) · [**Report a Bug**](../../issues) · [**Request a Feature**](../../issues)

</div>

---

## What is فازتومیم?

فازتومیم (Faztoumim) is a **Persian party game** inspired by the viral TikTok trend where people say the same sentence in wildly different moods — sarcastic, flirty, villain, drunk, or even in an Isfahani accent.

One player gets a **secret mood** and a **random sentence**. They say it out loud. Everyone else races to guess which mood it was. The clearer your performance, the more points you score — and correct guessers earn points too.

No app download needed. Works on any phone browser. Perfect for gatherings, game nights, and breaking the ice.

---

## Features

- 🎭 **18 moods** — from *Sarcastic* and *Flirty* to *Drunk*, *Villain*, *Diva*, and regional Iranian accents (Isfahani, Shomali, Sabzevari…)
- 📱 **Mobile-first** — designed for phones, no install required
- ⚡ **Real-time** — WebSocket-powered, results appear the instant the last player votes
- 🔄 **Session persistence** — refresh the page and you're right back in the game
- 🔑 **Rejoin by name** — left mid-game? Type your name and room code to rejoin your slot
- 🏆 **Dual scoring** — actor earns points for each correct guess; correct guessers earn a point too
- 🎊 **Confetti + rank card** — personalized medal (🥇🥈🥉) and confetti burst on the results screen
- ⚙️ **Customizable rounds** — host sets how many rounds each player acts (1–10)
- 🚪 **Exit anytime** — dedicated exit button; explicit leave cleans up your slot
- 🌐 **Zero CDN dependencies** — fully self-hosted, works offline on a local network
- 🌙 **Dark glass UI** — purple/pink gradient accents, animated mood cards, voter dots, shimmer effects

---

## Moods

| Mood | Emoji | Mood | Emoji |
|------|-------|------|-------|
| کنایی (Sarcastic) | 🙄 | دیوا (Diva) | 💅 |
| فلرت (Flirty) | 😏 | مست (Drunk) | 🥴 |
| عصبانی (Angry) | 😡 | ترسیده (Terrified) | 😱 |
| غمگین (Sad) | 😢 | اغراق‌آمیز (Overdramatic) | 🎭 |
| هیجان‌زده (Excited) | 🤩 | لهجه هندی (Indian accent) | 🪷 |
| رسمی (Formal) | 🧐 | لهجه روسی (Russian accent) | 🥶 |
| بچگانه (Baby talk) | 🍼 | لهجه عربی (Arabic accent) | 🫡 |
| شرور (Villain) | 😈 | لهجه اصفهانی (Isfahani accent) | 🎶 |
| لهجه شمالی (Northern accent) | 🌊 | لهجه سبزواری (Sabzevari accent) | 🌾 |

---

## How to Play

1. **One player creates a room** — share the 4-letter code with everyone
2. **Everyone joins** on their own phone using the room code
3. **Host starts the game** (and can set how many rounds per player)
4. **Each round:**
   - One player is the **actor** — they see a random sentence + a secret mood
   - They say the sentence out loud in that mood (no recording, just live performance!)
   - Everyone else **guesses** which of the 18 moods it was
5. **Scoring:** actor gets +1 per correct guess · each correct guesser gets +1
6. Rotate through all players, then see the **final leaderboard with confetti** 🎊

---

## Quick Start

### Requirements

- Python 3.10+
- `pip`

### Install & Run

```bash
# Clone the repo
git clone https://github.com/AMIR-SHAHROKH/faztoumim.git
cd faztoumim

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

### Play on your local network

Find your machine's local IP:

```bash
# Linux / macOS
hostname -I | awk '{print $1}'

# Windows
ipconfig
```

Share `http://YOUR_LOCAL_IP:8000` with everyone on the same Wi-Fi. No internet needed.

---

## Project Structure

```
faztoumim/
├── main.py          # FastAPI app — HTTP routes + WebSocket game loop
├── game.py          # Game state machine — rooms, players, scoring, moods, sentences
├── requirements.txt
└── templates/
    └── index.html   # Single-page frontend — all screens, animations, session logic
```

| File | Responsibility |
|------|---------------|
| `main.py` | FastAPI server, WebSocket connections, message dispatch |
| `game.py` | `Room` dataclass with all game logic: `begin_game`, `actor_done`, `submit_guess`, `do_reveal`, `next_round` |
| `templates/index.html` | 100% self-contained frontend: all CSS, JS, and HTML in one file, zero external dependencies |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) |
| Real-time | [WebSockets](https://websockets.readthedocs.io/) (via `websockets` library) |
| Frontend | Vanilla JS + hand-written CSS (no frameworks, no CDN) |
| State | In-memory Python dataclasses (no database) |
| Session | `localStorage` for refresh-safe reconnection |

---

## Game Architecture

```
Browser (Player A)                  FastAPI Server                 Browser (Player B)
        │                                  │                               │
        │──── POST /api/create ───────────>│                               │
        │<─── {room_id, player_id} ────────│                               │
        │                                  │                               │
        │──── WS /ws/{room}/{id} ─────────>│<── WS /ws/{room}/{id} ───────│
        │                                  │                               │
        │──── {action: "start"} ──────────>│                               │
        │                                  │──── broadcast state ─────────>│
        │<─── state + secret_mood ─────────│   (no secret_mood for B)      │
        │                                  │                               │
        │──── {action: "actor_done"} ─────>│──── broadcast "guessing" ────>│
        │                                  │                               │
        │                                  │<─── {action: "guess"} ────────│
        │                                  │  (last guess → auto-reveal)   │
        │<─── reveal state ────────────────│──── reveal state ────────────>│
```

Key design decisions:
- **Secret mood** is only included in the WebSocket message sent to the actor, never broadcast
- **Players are not removed on disconnect** — only on explicit `exit` action — enabling refresh-safe sessions
- **Instant reveal** — `submit_guess()` returns `True` when the last guesser votes, triggering `do_reveal()` immediately in the same message cycle

---

## Contributing

Pull requests are welcome. For major changes, open an issue first.

```bash
# Fork → clone your fork
git clone https://github.com/YOUR_USERNAME/faztoumim.git

# Create a feature branch
git checkout -b feature/your-feature

# Make changes, then push
git push origin feature/your-feature

# Open a pull request on GitHub
```

---

## License

[MIT](LICENSE) — do whatever you want with it.

---

<div align="center">

Built with ❤️ for game nights — no app store, no login, just a link.

</div>
