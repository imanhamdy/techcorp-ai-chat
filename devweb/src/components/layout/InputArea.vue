<script setup>
import { ref } from 'vue'
import { useSpeech } from '../../composables/useSpeech'

const props = defineProps({ loading: Boolean })
const emit  = defineEmits(['send', 'stop'])
const input    = ref('')
const textarea = ref(null)

const { listening, toggle: toggleSpeech, supported: speechSupported } = useSpeech({
  onResult: (t) => { input.value = t }
})

function handleSend() {
  if (!input.value.trim() || props.loading) return
  emit('send', input.value.trim())
  input.value = ''
  if (textarea.value) textarea.value.style.height = 'auto'
}
function handleKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend() }
}
function autoResize(e) {
  e.target.style.height = 'auto'
  e.target.style.height = Math.min(e.target.scrollHeight, 140) + 'px'
}
</script>

<template>
  <div class="px-3 sm:px-4 pb-3 sm:pb-4 pt-2 flex-shrink-0">
    <div class="rounded-xl sm:rounded-2xl border border-white/10 overflow-hidden transition focus-within:border-[#7C5CFC]/40 focus-within:shadow-[0_0_0_1px_rgba(124,92,252,0.15)] max-w-3xl mx-auto" style="background:#181825">
      <div class="flex items-end gap-2 px-3 sm:px-4 py-2.5 sm:py-3">
        <!-- Attachment -->
        <button class="p-1.5 rounded-lg text-white/30 hover:text-white hover:bg-white/8 transition flex-shrink-0 mb-0.5" title="Joindre">
          <span class="material-symbols-outlined text-[20px]">attach_file</span>
        </button>

        <!-- Textarea -->
        <textarea
          ref="textarea"
          v-model="input"
          rows="1"
          placeholder="Posez votre question financière..."
          class="flex-1 bg-transparent text-sm text-white placeholder-white/25 outline-none resize-none py-1 leading-relaxed"
          style="max-height:140px"
          :disabled="loading"
          @keydown="handleKeydown"
          @input="autoResize"
        />

        <!-- Voice (hidden on very small screens) -->
        <button
          v-if="speechSupported"
          class="hidden sm:flex p-1.5 rounded-lg transition flex-shrink-0 mb-0.5"
          :class="listening ? 'text-red-400 bg-red-900/20 animate-pulse' : 'text-white/30 hover:text-white hover:bg-white/8'"
          :disabled="loading"
          @click="toggleSpeech"
        >
          <span class="material-symbols-outlined text-[20px]">{{ listening ? 'mic' : 'mic_none' }}</span>
        </button>

        <!-- Stop / Send -->
        <button
          v-if="loading"
          class="w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 transition"
          style="background:rgba(239,68,68,0.2);border:1px solid rgba(239,68,68,0.3)"
          @click="emit('stop')"
        >
          <span class="material-symbols-outlined text-red-400 text-[17px]">stop</span>
        </button>
        <button
          v-else
          class="w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 transition"
          :class="input.trim() ? 'text-white' : 'text-white/25'"
          :style="input.trim() ? 'background:linear-gradient(135deg,#7C5CFC,#5A4FCF);box-shadow:0 4px 14px rgba(124,92,252,0.35)' : 'background:rgba(255,255,255,0.05)'"
          :disabled="!input.trim()"
          @click="handleSend"
        >
          <span class="material-symbols-outlined text-[18px]">arrow_upward</span>
        </button>
      </div>

      <!-- Bottom bar — hidden on very small screens to save space -->
      <div class="hidden sm:flex items-center gap-3 px-4 py-2 border-t border-white/5">
        <button class="flex items-center gap-1.5 text-xs text-white/30 hover:text-white/60 transition">
          <span class="material-symbols-outlined text-[14px]">attach_file</span>
          Joindre un fichier
        </button>
        <button class="flex items-center gap-1.5 text-xs text-white/30 hover:text-white/60 transition">
          <span class="material-symbols-outlined text-[14px]">lightbulb</span>
          Exemples de questions
        </button>
      </div>
    </div>
    <p class="text-[10px] text-white/12 text-center mt-1.5 hidden sm:block">TechCorp AI peut faire des erreurs. Vérifiez les informations importantes.</p>
  </div>
</template>
