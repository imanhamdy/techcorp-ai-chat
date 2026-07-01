# 03 - Design system (Tailwind config)

> Palette **figée** : ne jamais modifier ces couleurs. Coller tel quel dans `tailwind.config.js`.

```js
export default {
 darkMode: 'class',
 content: ['./index.html', './src/**/*.{vue,js}'],
 theme: {
 extend: {
 colors: {
 'primary': '#adc6ff',
 'on-primary': '#002e69',
 'primary-container': '#4d8efe',
 'secondary': '#dab9ff',
 'secondary-container': '#5a3287',
 'on-secondary-container': '#cda2ff',
 'tertiary': '#ffb2b6',
 'tertiary-container': '#e26c77',
 'error': '#ffb4ab',
 'background': '#11131a',
 'surface': '#11131a',
 'surface-dim': '#11131a',
 'surface-bright': '#373941',
 'surface-container-lowest': '#0c0e15',
 'surface-container-low': '#191b23',
 'surface-container': '#1d1f27',
 'surface-container-high': '#282a31',
 'surface-container-highest': '#33343c',
 'on-surface': '#e2e2ec',
 'on-surface-variant': '#c2c6d5',
 'outline': '#8c909f',
 'outline-variant': '#424753',
 'inverse-surface': '#e2e2ec',
 'inverse-on-surface': '#2e3038',
 'surface-variant': '#33343c',
 },
 fontFamily: {
 'body': ['Geist', 'sans-serif'],
 'code': ['"JetBrains Mono"', 'monospace'],
 'display': ['Geist', 'sans-serif'],
 },
 fontSize: {
 'display-lg': ['48px', { lineHeight: '56px', letterSpacing: '-0.02em', fontWeight: '600' }],
 'headline-md': ['24px', { lineHeight: '32px', letterSpacing: '-0.01em', fontWeight: '500' }],
 'body-lg': ['18px', { lineHeight: '28px', fontWeight: '400' }],
 'body-md': ['16px', { lineHeight: '24px', fontWeight: '400' }],
 'label-md': ['14px', { lineHeight: '20px', letterSpacing: '0.02em', fontWeight: '500' }],
 'code-sm': ['13px', { lineHeight: '20px', fontWeight: '400' }],
 },
 borderRadius: {
 DEFAULT: '0.25rem',
 lg: '0.5rem',
 xl: '0.75rem',
 full: '9999px',
 },
 },
 },
}
```

## Classes CSS custom (dans `assets/main.css`)

- `.glass-input` : `background: rgba(255,255,255,0.03)` + `backdrop-filter: blur(32px)` + bordure `rgba(255,255,255,0.1)`, transition `0.4s cubic-bezier(0.4,0,0.2,1)`.
 - `:focus-within` → bordure transparente, `box-shadow: 0 0 0 1px rgba(173,198,255,0.1)`, fond `rgba(255,255,255,0.05)`.
- `.ai-message-border` : `border-left: 1px solid transparent` + `border-image: linear-gradient(to bottom, #adc6ff, transparent) 1`.
- `.spark-gradient` : `radial-gradient(circle at center, #adc6ff, #5a3287)` + `blur(4px)` + animation `pulse-glow 3s infinite alternate`.
- `.custom-scrollbar` : largeur `4px`, thumb `rgba(255,255,255,0.1)` radius `10px`, track transparent.
- `.ambient-bg` : `radial-gradient(circle at 50% 50%, rgba(90,50,135,0.15) 0%, transparent 70%)`.

Rendu cible complet → [reference.html](reference.html).
