import { ref } from 'vue'

// ─── Catalogue des types d'erreur ────────────────────────────────────────────

export const ERROR_TYPES = {
  NETWORK: {
    code:  'NETWORK',
    label: 'Connexion impossible',
    detail: 'Ollama est injoignable. Vérifiez que le serveur tourne.',
    icon:  'wifi_off',
    color: 'text-error',
  },
  MODEL_NOT_FOUND: {
    code:  'MODEL_NOT_FOUND',
    label: 'Modèle introuvable',
    detail: 'Le modèle demandé n\'existe pas sur ce serveur Ollama.',
    icon:  'model_training',
    color: 'text-tertiary',
  },
  SERVER_ERROR: {
    code:  'SERVER_ERROR',
    label: 'Erreur serveur Ollama',
    detail: 'Ollama a retourné une erreur interne (500). Le modèle a peut-être planté ou manqué de mémoire.',
    icon:  'dns',
    color: 'text-error',
  },
  BAD_REQUEST: {
    code:  'BAD_REQUEST',
    label: 'Requête invalide',
    detail: 'Ollama a rejeté la requête (400). Payload malformé ou paramètres invalides.',
    icon:  'data_object',
    color: 'text-tertiary',
  },
  STREAM_PARSE: {
    code:  'STREAM_PARSE',
    label: 'Erreur de parsing stream',
    detail: 'Le flux NDJSON d\'Ollama contient une ligne non parseable.',
    icon:  'broken_image',
    color: 'text-tertiary',
  },
  SPEECH: {
    code:  'SPEECH',
    label: 'Reconnaissance vocale',
    detail: 'Erreur micro ou Speech API non supportée par ce navigateur.',
    icon:  'mic_off',
    color: 'text-on-surface-variant',
  },
  NO_MODELS: {
    code:   'NO_MODELS',
    label:  'Aucun modèle disponible',
    detail: 'Ollama ne contient aucun modèle. Téléchargez-en un : `ollama pull phi3.5`',
    icon:   'model_training',
    color:  'text-tertiary',
  },
  UNKNOWN: {
    code:  'UNKNOWN',
    label: 'Erreur inconnue',
    detail: 'Une erreur inattendue est survenue.',
    icon:  'help',
    color: 'text-on-surface-variant',
  },
}

// ─── Résolution automatique depuis un code HTTP ou une exception ──────────────

export function resolveErrorType(err) {
  if (!err) return ERROR_TYPES.UNKNOWN

  // Network / CORS / connection refused / timeout / non-JSON response
  if (
    err instanceof TypeError ||
    err?.status === 0 ||
    err?.name === 'TimeoutError' ||
    err?.name === 'AbortError'
  ) return ERROR_TYPES.NETWORK

  const status = err?.status
  if (status === 400) return ERROR_TYPES.BAD_REQUEST
  if (status === 404) return ERROR_TYPES.MODEL_NOT_FOUND
  if (status === 500) return ERROR_TYPES.SERVER_ERROR

  if (err?.code === 'SPEECH')      return ERROR_TYPES.SPEECH
  if (err?.code === 'STREAM_PARSE') return ERROR_TYPES.STREAM_PARSE
  if (err?.code === 'NO_MODELS')   return ERROR_TYPES.NO_MODELS

  return ERROR_TYPES.UNKNOWN
}

// ─── Message d'erreur affiché dans la bulle IA ───────────────────────────────

export function chatErrorMessage(type, rawDetail = '') {
  const base = type.detail
  return rawDetail ? `${base}\n\nDétail : ${rawDetail}` : base
}

// ─── Store réactif singleton ─────────────────────────────────────────────────

const errors = ref([])   // [{ id, ts, type, detail, raw }]

export function useErrors() {
  function push(err, rawDetail = '') {
    const type = resolveErrorType(err)
    const entry = {
      id:     crypto.randomUUID(),
      ts:     new Date(),
      type,
      detail: rawDetail || err?.message || err?.body || type.detail,
      raw:    err,
    }
    errors.value.unshift(entry)
    if (errors.value.length > 50) errors.value.length = 50
    return entry
  }

  function dismiss(id) {
    const i = errors.value.findIndex(e => e.id === id)
    if (i !== -1) errors.value.splice(i, 1)
  }

  function clear() { errors.value = [] }

  return { errors, push, dismiss, clear }
}
