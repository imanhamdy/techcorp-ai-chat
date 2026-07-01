[🇫🇷 Français](rapport_devweb.fr.md) · 🇬🇧 English

---

# DEV WEB Report - TechCorp AI Challenge
**Track:** DEV WEB · **Date:** 2026-06-30
**Public URL:** https://4ride.online
**Repo:** github.com/HACKATON-2526-GroupeB/techcorp-ai-chat

---

## 1. Technical stack

| Component | Technology | Version |
|---|---|---|
| UI framework | Vue.js 3 (Composition API) | 3.5 |
| Build tool | Vite | 6.4 |
| CSS | Tailwind CSS + @tailwindcss/typography | 3.4 |
| Markdown | marked.js | 15.x |
| Icons | Material Symbols (Google Fonts CDN) | - |
| Fonts | Geist / Inter (Google Fonts CDN) | - |
| Static server | Caddy v2.9.1 (serves `devweb/dist/`) | 2.9.1 |

---

## 2. Component architecture

```
App.vue ← root: global state, routing between views
 components/layout/
 Sidebar.vue ← conversation history, nav, profile
 TopBar.vue ← logo, model selector, theme, settings
 InputArea.vue ← auto-resize textarea, voice, stop, send
 components/chat/
 ChatViewport.vue ← welcome screen + message feed
 MessageUser.vue ← user bubble (translucent purple)
 MessageAI.vue ← AI response: markdown, copy, timestamp
 components/settings/
 SettingsPanel.vue ← side panel: model, temperature, tokens
 components/ui/
 ShaderCanvas.vue ← animated CSS background (radial-gradient blobs)
 composables/
 useChat.js ← core logic: send, stop, streaming
 useModels.js ← fetch /api/tags → list of models
 useSettings.js ← Ollama URL, temperature, voice language
 useSpeech.js ← Web Speech API (voice recognition)
 useConversations.js ← multi-conversation localStorage history
 useTheme.js ← dark/light mode toggle
```

---

## 3. Implemented features

### Chat & streaming
- **Token-by-token streaming** via `fetch()` + `ReadableStream` to `/api/chat` (Ollama)
- **AbortController**: Stop button interrupts ongoing generation (keeps the partial output)
- **Markdown rendering** in AI responses via `marked.parse()` + Tailwind prose
- **Blinking cursor** during generation (CSS `blink` animation)
- **Typing dots** animated during initial loading

### Interface
- **Welcome screen** with 4 clickable category cards (Financial analysis, Data & markets, Quick summaries, Advice & explanations)
- **Suggestion pills** for quick starts
- **Auto scroll-to-bottom** + floating button if scrolled up
- **Animations**: message entry (`msg-in`), staggered cards (`card-stagger`), background blobs (`drift`)

### Settings
- Model selector (list dynamically loaded from Ollama)
- Temperature (0–1) and max tokens (256–4096) sliders
- Auto-save toggle
- Ollama URL (hidden in the "Advanced" section)
- Voice recognition language (6 languages)

### Mobile
- Sidebar as a **drawer** (off-screen translate-x, backdrop overlay)
- Hamburger button in the TopBar (hidden on desktop)
- Adapted message bubbles (`max-w-[85%]` mobile / `max-w-[72%]` desktop)
- Simplified input toolbar on mobile (voice hidden)

### Theme
- **Dark/light toggle** (/ icon) via `useTheme.js`
- Preference persisted in `localStorage`
- Implementation: `filter: invert(1) hue-rotate(180deg)` on `<html>`

### History
- Multiple conversations stored in **localStorage**
- Create, select, delete conversations from the sidebar
- Configurable auto-save

---

## 4. Connection with Ollama

```
Browser HTTPS Caddy :8443 /api/* Ollama :11434
```

The frontend calls exclusively `https://4ride.online/api/...` - Caddy proxies to Ollama over local HTTP.

### Endpoints used

| Endpoint | Usage |
|---|---|
| `GET /api/tags` | List of available models |
| `POST /api/chat` | Streaming inference (message format) |

---

## 5. Local startup (development)

```bash
# Requirement: Node.js ≥ 18
cd devweb/
npm install
npm run dev # dev server at http://localhost:5173

# Production build
npm run build # → dist/ (served by Caddy)
```

### Important variables in `useSettings.js`

```js
const DEFAULT_URL = 'https://4ride.online' // Ollama URL (via Caddy proxy)
```

To develop locally with a local Ollama instance, change the URL in settings to `http://localhost:11434`.

---

## 6. Production deployment

```bash
export PATH="$HOME/bin/node/bin:$HOME/bin/bin:$HOME/bin:$PATH"

# Build
cd devweb && npm run build

# Caddy serves dist/ automatically (process already active)
# Force config reload if needed:
caddy reload --config /home/ia/techcorp-ai-chat/Caddyfile
```

---

## 7. Feature screenshots

| Feature | Description |
|---|---|
| Welcome screen | Category cards + question suggestions |
| Active chat | Streamed messages + blinking cursor |
| Settings panel | Model selector + temperature/token sliders |
| Mobile drawer | Sidebar accessible via hamburger |
| Stop in progress | Red button interrupts generation |
