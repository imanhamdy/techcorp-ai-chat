# 01 - Contexte & stack

## Contexte du projet

Interface web de chat connectée à **Ollama** (serveur d'inférence local) pour interagir avec le modèle **Phi-3.5-Financial**. L'UI reproduit fidèlement le design "Synthetic Intelligence" : dark theme, glassmorphism, sidebar fixe, input flottant.

## Stack technique

- **Framework** : Vue 3 (Composition API, `<script setup>`)
- **Build** : Vite
- **CSS** : Tailwind CSS (config étendue → voir [03-design-system.md](03-design-system.md))
- **Icônes** : Material Symbols Outlined (Google Fonts)
- **Polices** : Geist (corps), JetBrains Mono (code)
- **API** : Ollama REST - `http://localhost:11434`
- **Pas de router** : single-page, une seule vue

## Commandes du projet

```bash
npm create vite@latest techcorp-chat -- --template vue
cd techcorp-chat
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm run dev # dev server → http://localhost:5173
npm run build # build production → dist/
```
