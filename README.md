# VoicePay 🎙️💸

> **Voice-first payment app** — designed for blind and visually impaired users.  
> Always listening. Always here.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/voicepay)

---

## ✨ Features

- 🎙️ **Always-on voice recognition** — say "pay saran 500" to start a payment instantly
- ✏️ **Draw PIN** — Android-style 3×3 pattern lock for secure authentication  
- 🔢 **Classic PIN** — traditional numpad fallback
- 📱 **Mobile-friendly** — works on phone browsers with touch support
- ♿ **Accessibility-first** — full TTS feedback, ARIA labels, screen-reader support
- 💜 **Premium dark UI** — glassmorphism design with smooth animations

---

## 🚀 Quick Start

### Open locally
Just open `index.html` in **Google Chrome** — allow microphone when prompted.

### Voice commands
| Say | Action |
|-----|--------|
| `"pay saran 500"` | Go straight to PIN with contact + amount set |
| `"pay 200 to priya"` | Same, different format |
| `"check balance"` | Reads your balance aloud |
| `"open history"` | Navigate to transaction history |
| `"go back"` | Navigate back |
| `"reset"` *(on PIN screen)* | Clear draw pattern |

### Draw PIN
Draw through all 9 dots in your secret pattern. Lift finger/mouse to confirm.

### Classic PIN
Switch to 🔢 Classic tab and type `1221`.

---

## 🌐 Deploy

### Vercel (recommended)
1. Push this repo to GitHub
2. Go to [vercel.com](https://vercel.com) → **New Project** → Import your repo
3. Click **Deploy** — done! 🎉

### GitHub Pages
1. Go to repo **Settings** → **Pages**
2. Set source to **main branch / root**
3. Your app is live at `https://YOUR_USERNAME.github.io/voicepay`

---

## 🔒 Security Note

The draw PIN pattern is stored in the client-side JavaScript.  
This is a **demo app** — for production use, implement server-side authentication.

---

## 🛠️ Tech Stack

- **Vanilla HTML + CSS + JavaScript** — zero dependencies, zero build step
- **Web Speech API** — voice recognition + TTS
- **Canvas API** — pattern lock drawing

---

## 📁 Project Structure

```
voicepay/
├── index.html              ← Main app (everything in one file)
├── vercel.json             ← Vercel deployment config
├── README.md               ← This file
├── .gitignore              ← Git ignore rules
├── START VoicePay.bat      ← Local dev server launcher (Windows)
└── start-voicepay-server.ps1 ← PowerShell HTTP server script
```

---

Made with 💜 for accessibility
