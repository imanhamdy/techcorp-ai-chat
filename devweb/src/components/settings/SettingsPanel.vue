<script setup>
import { ref } from 'vue'
import { useSettings }  from '../../composables/useSettings'
import { useModels }    from '../../composables/useModels'
import { useChat }      from '../../composables/useChat'

defineProps({ show: Boolean })
defineEmits(['close'])

const { temperature, maxTokens, speechLang, autoSave, SPEECH_LANGS } = useSettings()
const { availableModels } = useModels()
const { activeModel }     = useChat()

const showAdvanced = ref(false)
const { ollamaUrl, DEFAULT_URL } = useSettings()
</script>

<template>
  <Teleport to="body">
    <Transition name="panel">
      <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-end">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="$emit('close')" />
        <div class="relative w-full max-w-[360px] h-full border-l border-white/8 flex flex-col shadow-2xl" style="background:#101018">

          <!-- Header -->
          <div class="flex items-center justify-between px-5 py-4 border-b border-white/8 flex-shrink-0">
            <h2 class="text-sm font-semibold text-white">Paramètres</h2>
            <button class="p-1.5 rounded-lg hover:bg-white/10 text-white/40 hover:text-white transition" @click="$emit('close')">
              <span class="material-symbols-outlined text-[18px]">close</span>
            </button>
          </div>

          <div class="flex-1 overflow-y-auto px-5 py-5 space-y-6">

            <!-- Model -->
            <div>
              <label class="text-[10px] font-semibold uppercase tracking-widest text-white/40">Modèle</label>
              <select
                v-model="activeModel"
                class="mt-2 w-full border border-white/10 rounded-xl px-3 py-2.5 text-sm text-white outline-none transition hover:border-[#7C5CFC]/40 cursor-pointer"
                style="background:#181825"
              >
                <option v-for="m in availableModels" :key="m" :value="m">{{ m.replace(':latest','') }}</option>
              </select>
              <p v-if="!availableModels.length" class="text-xs text-white/30 mt-1">Chargement des modèles…</p>
            </div>

            <!-- Temperature -->
            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-[10px] font-semibold uppercase tracking-widest text-white/40">Température</label>
                <span class="text-xs font-mono text-[#7C5CFC]">{{ temperature }}</span>
              </div>
              <input v-model.number="temperature" type="range" min="0" max="1" step="0.05"
                class="w-full h-1.5 rounded-full appearance-none cursor-pointer"
                style="accent-color:#7C5CFC" />
              <div class="flex justify-between text-[10px] text-white/25 mt-1">
                <span>Précis</span><span>Créatif</span>
              </div>
            </div>

            <!-- Max tokens -->
            <div>
              <div class="flex items-center justify-between mb-2">
                <label class="text-[10px] font-semibold uppercase tracking-widest text-white/40">Tokens max</label>
                <span class="text-xs font-mono text-[#7C5CFC]">{{ maxTokens }}</span>
              </div>
              <input v-model.number="maxTokens" type="range" min="256" max="4096" step="256"
                class="w-full h-1.5 rounded-full appearance-none cursor-pointer"
                style="accent-color:#7C5CFC" />
              <div class="flex justify-between text-[10px] text-white/25 mt-1">
                <span>256</span><span>4096</span>
              </div>
            </div>

            <!-- Voice language -->
            <div>
              <label class="text-[10px] font-semibold uppercase tracking-widest text-white/40">Langue vocale</label>
              <select
                v-model="speechLang"
                class="mt-2 w-full border border-white/10 rounded-xl px-3 py-2.5 text-sm text-white outline-none cursor-pointer"
                style="background:#181825"
              >
                <option v-for="l in SPEECH_LANGS" :key="l.value" :value="l.value">{{ l.label }}</option>
              </select>
            </div>

            <!-- Auto-save toggle -->
            <div class="flex items-center justify-between py-1">
              <div>
                <p class="text-sm text-white font-medium">Sauvegarde auto</p>
                <p class="text-xs text-white/35 mt-0.5">Sauvegarder les conversations automatiquement</p>
              </div>
              <button
                class="relative w-11 h-6 rounded-full transition-colors duration-200 flex-shrink-0"
                :style="autoSave ? 'background:#7C5CFC' : 'background:rgba(255,255,255,0.15)'"
                @click="autoSave = !autoSave"
              >
                <span
                  class="absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform duration-200"
                  :class="autoSave ? 'translate-x-5' : 'translate-x-0.5'"
                />
              </button>
            </div>

            <!-- Advanced section -->
            <div class="border-t border-white/8 pt-4">
              <button
                class="flex items-center gap-2 text-xs text-white/35 hover:text-white/60 transition w-full"
                @click="showAdvanced = !showAdvanced"
              >
                <span class="material-symbols-outlined text-[14px]">tune</span>
                Avancé
                <span class="material-symbols-outlined text-[14px] ml-auto transition-transform" :class="showAdvanced ? 'rotate-180' : ''">expand_more</span>
              </button>

              <div v-if="showAdvanced" class="mt-3 space-y-3">
                <div>
                  <label class="text-[10px] font-semibold uppercase tracking-widest text-white/40">URL Ollama</label>
                  <input
                    v-model="ollamaUrl"
                    type="text"
                    class="mt-1.5 w-full border border-white/10 rounded-xl px-3 py-2 text-xs text-white/70 outline-none font-mono focus:border-[#7C5CFC]/40"
                    style="background:#181825"
                  />
                  <p class="text-[10px] text-white/25 mt-1">Défaut : {{ DEFAULT_URL }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Footer -->
          <div class="px-5 py-4 border-t border-white/8 flex-shrink-0">
            <p class="text-[10px] text-white/20 text-center">TechCorp AI · phi3-financial · v1.0</p>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
