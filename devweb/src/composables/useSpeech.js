import { ref, watch } from 'vue'
import { useSettings } from './useSettings'
import { useErrors, ERROR_TYPES } from '../services/errorService'

const SR = typeof window !== 'undefined'
  ? (window.SpeechRecognition || window.webkitSpeechRecognition)
  : null

export const speechSupported = !!SR

export function useSpeech({ onResult }) {
  const { speechLang } = useSettings()
  const { push } = useErrors()

  const listening  = ref(false)
  const transcript = ref('')

  if (!SR) return { listening, transcript, supported: false, toggle: () => {
    const err = Object.assign(new Error('Speech API non supportée'), { code: 'SPEECH' })
    push(err, 'Utilisez Chrome, Edge ou Safari pour la reconnaissance vocale.')
  }}

  const rec = new SR()
  rec.continuous      = false
  rec.interimResults  = true
  rec.maxAlternatives = 1

  // Sync langue depuis settings
  watch(speechLang, (l) => { rec.lang = l }, { immediate: true })

  rec.onresult = (e) => {
    const result = Array.from(e.results).map(r => r[0].transcript).join('')
    transcript.value = result
    if (e.results[e.results.length - 1].isFinal) {
      onResult(result)
      transcript.value = ''
      listening.value  = false
    }
  }

  rec.onerror = (e) => {
    const speechErrors = {
      'not-allowed':    'Permission micro refusée par le navigateur.',
      'no-speech':      'Aucune voix détectée.',
      'audio-capture':  'Micro introuvable ou inaccessible.',
      'network':        'Erreur réseau pendant la transcription.',
      'aborted':        'Transcription annulée.',
    }
    const err = Object.assign(new Error(e.error), { code: 'SPEECH' })
    push(err, speechErrors[e.error] ?? `Erreur Speech API : ${e.error}`)
    listening.value = false
  }

  rec.onend = () => { listening.value = false }

  function toggle() {
    if (listening.value) {
      rec.stop()
    } else {
      transcript.value = ''
      try {
        rec.start()
        listening.value = true
      } catch (e) {
        const err = Object.assign(new Error(e.message), { code: 'SPEECH' })
        push(err, 'Impossible de démarrer le micro.')
      }
    }
  }

  return { listening, transcript, supported: true, toggle }
}
