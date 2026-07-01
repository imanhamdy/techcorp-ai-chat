import { ref } from 'vue'
import { listModels }  from '../services/ollama'
import { useSettings } from './useSettings'
import { useErrors }   from '../services/errorService'
import { useChat }     from './useChat'

// Singleton module-level
const availableModels = ref([])
const loadingModels   = ref(false)
const initialized     = ref(false)

const PREFERRED_MODEL = 'phi3-financial:latest'

export function useModels() {
  const { ollamaUrl }    = useSettings()
  const { push }         = useErrors()
  const { activeModel }  = useChat()

  async function fetchModels() {
    loadingModels.value = true
    try {
      const models = await listModels(ollamaUrl.value)
      availableModels.value = models

      if (models.length === 0) {
        const err = Object.assign(new Error('No models found'), { code: 'NO_MODELS' })
        push(err, 'Aucun modèle disponible sur ce serveur Ollama.')
      } else {
        // Auto-select preferred model if available, otherwise first in list
        if (models.includes(PREFERRED_MODEL)) {
          activeModel.value = PREFERRED_MODEL
        } else if (!models.includes(activeModel.value)) {
          activeModel.value = models[0]
        }
      }
    } catch (err) {
      push(err)
      availableModels.value = []
    } finally {
      loadingModels.value = false
      initialized.value   = true
    }
  }

  return { availableModels, loadingModels, initialized, fetchModels }
}
