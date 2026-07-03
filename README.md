# VoicePay 🎙️💸

> **Voice-first payment app** — designed for blind and visually impaired users.  
> Always listening. Always here.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/YOUR_USERNAME/voicepay)

---

## ✨ Features

- 🎙️ **Always-on voice recognition** — say "pay saran 500" to start a payment instantly
- ✏️ **Handwritten ML PIN** — write digits (0–9) directly on the screen; validated in real-time by a local TensorFlow.js CNN model (default demo PIN: `1-2-2-1`)
- 📸 **UPI QR Code Scanner** — scan standard UPI payment codes using the camera or voice activation ("open qr"), with dynamic routing and transaction simulation
- 👤 **Voice-Activated Contacts** — say "add Adam" and state their number/UPI ID to add contacts hands-free
- 🔢 **Classic PIN** — traditional numpad fallback
- 📱 **Mobile-friendly** — works on phone and tablet browsers
- ♿ **Accessibility-first** — full Text-To-Speech (TTS) feedback, ARIA labels, and screen-reader support
- 💜 **Premium dark UI** — glassmorphism design with smooth layouts and glow effects

---

## 🚀 Quick Start

### Open locally
Just open `index.html` in **Google Chrome** — allow microphone when prompted. Or launch the local server using `START VoicePay.bat`.

### Voice commands
| Say | Action |
|-----|--------|
| `"pay saran 500"` | Go straight to PIN with contact + amount set |
| `"pay 200 to priya"` | Same, different format |
| `"check balance"` | Reads your balance aloud |
| `"open qr"` | Launch camera scanner overlay |
| `"simulate scan"` *(inside scanner)* | Simulate scanning a mock UPI code |
| `"add Adam"` | Start adding contact named Adam |
| `"open history"` | Navigate to transaction history |
| `"go back"` | Navigate back |
| `"reset"` *(on PIN screen)* | Clear drawn canvas digit |

### Handwriting PIN
Draw each digit of the PIN one-by-one. Lift finger/mouse to trigger recognition.

### Classic PIN
Switch to 🔢 Classic tab and type `1221`.

---

## 🌐 Deploy

### Vercel (recommended)
1. Push this repo to GitHub
2. Go to [vercel.com](https://vercel.com) → **New Project** → Import your repo
3. Click **Deploy** — done! 🎉

---

## 🔒 Security Note

The handwritten PIN recognition is performed entirely locally on the client-side using WebGL/CPU acceleration in TensorFlow.js. This is a **demo app** — for production use, implement server-side authentication.

---

## 🛠️ Tech Stack

- **Vanilla HTML + CSS + JavaScript** — zero framework dependencies
- **TensorFlow.js (local)** — offline convolutional neural network (CNN) digit inference
- **html5-qrcode (local)** — HTML5 camera scanner
- **Web Speech API** — voice recognition + TTS

---

## 📁 Project Structure

```
voicepay/
├── index.html              ← Main app (everything in one file)
├── tf.min.js               ← TensorFlow.js core script
├── html5-qrcode.min.js     ← HTML5 QR code scanning engine
├── vercel.json             ← Vercel deployment config
├── README.md               ← This file
├── .gitignore              ← Git ignore rules
├── digit_model/            ← Trained CNN model files
│   ├── model.json          ← Model topology
│   └── group1-shard1of1.bin ← Model weights
├── START VoicePay.bat      ← Local dev server launcher (Windows)
└── start-voicepay-server.ps1 ← PowerShell HTTP server script
```

---

Made with 💜 for accessibility

