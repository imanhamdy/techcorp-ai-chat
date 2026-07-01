import { ref, watch } from 'vue'

export const DEFAULT_URL = 'https://4ride.online'

function normalizeUrl(url) {
  const u = (url ?? '').trim().replace(/\/$/, '')
  if (!u) return DEFAULT_URL
  if (!/^https?:\/\//.test(u)) return 'https://' + u
  return u
}

// Migrate old localhost default to new remote URL
function loadUrl() {
  const stored = localStorage.getItem('ollamaUrl')
  // Migrate old defaults (localhost or https with invalid cert) to the working URL
  if (!stored || stored === 'http://localhost:11434' || stored === 'http://4ride.online') {
    return DEFAULT_URL
  }
  return normalizeUrl(stored)
}

function persist(key, ref_) {
  watch(ref_, (v) => localStorage.setItem(key, String(v)))
}

// ─── Singleton module-level ───────────────────────────────────────────────────
const ollamaUrl   = ref(loadUrl())
const temperature = ref(Number(localStorage.getItem('temperature') ?? 0.7))
const maxTokens   = ref(Number(localStorage.getItem('maxTokens')   ?? 2048))
const speechLang  = ref(localStorage.getItem('speechLang')  ?? 'fr-FR')
const autoSave    = ref(localStorage.getItem('autoSave')    !== 'false')

persist('ollamaUrl',   ollamaUrl)
persist('temperature', temperature)
persist('maxTokens',   maxTokens)
persist('speechLang',  speechLang)
persist('autoSave',    autoSave)

export const SPEECH_LANGS = [
  { value: 'fr-FR', label: 'Français (France)' },
  { value: 'en-US', label: 'English (US)' },
  { value: 'en-GB', label: 'English (UK)' },
  { value: 'es-ES', label: 'Español' },
  { value: 'de-DE', label: 'Deutsch' },
  { value: 'ar-SA', label: 'العربية' },
  { value: 'zh-CN', label: '中文 (简体)' },
]

export { normalizeUrl }
export function useSettings() {
  return { ollamaUrl, temperature, maxTokens, speechLang, autoSave, DEFAULT_URL, SPEECH_LANGS }
}
