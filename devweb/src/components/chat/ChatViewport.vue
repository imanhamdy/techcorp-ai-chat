<script setup>
import { ref, watch, nextTick, computed } from 'vue'
import MessageUser from './MessageUser.vue'
import MessageAI   from './MessageAI.vue'

const props = defineProps({ messages: Array, loading: Boolean })
const emit  = defineEmits(['suggest'])

const viewport      = ref(null)
const showScrollBtn = ref(false)

const CATEGORIES = [
  { icon: 'bar_chart',   color: '#7C5CFC', label: 'Analyse financière',    desc: 'Rapports, ratios et tendances.' },
  { icon: 'trending_up', color: '#4F8DFF', label: 'Données & marchés',     desc: 'Actions, indices et plus.' },
  { icon: 'description', color: '#22C55E', label: 'Résumés rapides',        desc: "Résumés clairs d'informations." },
  { icon: 'lightbulb',   color: '#F59E0B', label: 'Conseils & explications', desc: 'Concepts financiers simplement.' },
]

const SUGGESTIONS = [
  "Qu'est-ce que l'EBITDA ?",
  "Expliquez le ratio CET1 Bâle III",
  "Comment fonctionne MiFID II ?",
  "Différence entre actif et passif ?",
]

const streamingMsg = computed(() => {
  if (!props.loading) return null
  const last = props.messages[props.messages.length - 1]
  return last?.role === 'assistant' ? last : null
})
function isStreaming(msg) { return streamingMsg.value === msg }

async function scrollBottom() {
  await nextTick()
  if (viewport.value) viewport.value.scrollTop = viewport.value.scrollHeight
}
function onScroll() {
  if (!viewport.value) return
  const { scrollTop, scrollHeight, clientHeight } = viewport.value
  showScrollBtn.value = scrollHeight - scrollTop - clientHeight > 100
}
watch(() => props.messages, scrollBottom, { deep: true })
</script>

<template>
  <div class="relative flex-1 overflow-hidden">
    <div ref="viewport" class="h-full overflow-y-auto" @scroll="onScroll">

      <!-- Welcome screen -->
      <div v-if="!messages.length" class="flex flex-col items-center justify-center min-h-full py-8 px-4 sm:px-8">
        <div class="text-center mb-8 animate-float">
          <div class="w-14 h-14 sm:w-16 sm:h-16 rounded-2xl flex items-center justify-center mx-auto mb-4" style="background:linear-gradient(135deg,#7C5CFC,#5A4FCF);box-shadow:0 8px 32px rgba(124,92,252,0.4)">
            <span class="material-symbols-outlined text-white text-[28px] sm:text-[32px]">auto_awesome</span>
          </div>
          <h1 class="text-3xl sm:text-4xl font-bold text-white mb-2" style="letter-spacing:-0.02em">Bonjour !</h1>
          <p class="text-white/45 text-sm sm:text-base">Je suis votre assistant IA. Posez votre première question financière.</p>
        </div>

        <!-- Cards: 1 col on mobile, 2 on tablet+ -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full max-w-2xl mb-6 card-stagger">
          <button
            v-for="c in CATEGORIES"
            :key="c.label"
            class="card text-left p-4 sm:p-5 cursor-pointer group"
            @click="emit('suggest', c.label)"
          >
            <div class="flex items-start gap-3 sm:block">
              <div class="w-9 h-9 sm:w-10 sm:h-10 rounded-xl flex items-center justify-center flex-shrink-0 sm:mb-3 transition group-hover:scale-110" :style="`background:${c.color}22`">
                <span class="material-symbols-outlined text-[18px] sm:text-[20px]" :style="`color:${c.color}`">{{ c.icon }}</span>
              </div>
              <div class="flex-1 sm:flex sm:items-start sm:justify-between">
                <div>
                  <p class="text-sm font-semibold text-white mb-0.5">{{ c.label }}</p>
                  <p class="text-xs text-white/40">{{ c.desc }}</p>
                </div>
                <span class="hidden sm:flex mt-3 w-6 h-6 rounded-full items-center justify-center text-white/25 group-hover:text-white group-hover:bg-white/10 transition flex-shrink-0 ml-2" style="border:1px solid rgba(255,255,255,0.1)">
                  <span class="material-symbols-outlined text-[13px]">arrow_forward</span>
                </span>
              </div>
            </div>
          </button>
        </div>

        <!-- Suggestion pills -->
        <div class="flex flex-wrap gap-2 justify-center max-w-xl">
          <button
            v-for="s in SUGGESTIONS"
            :key="s"
            class="px-3 py-1.5 rounded-full text-xs text-white/50 hover:text-white transition border border-white/8 hover:border-[#7C5CFC]/40 hover:bg-[#7C5CFC]/10"
            style="background:rgba(255,255,255,0.03)"
            @click="emit('suggest', s)"
          >
            {{ s }}
          </button>
        </div>

        <p class="mt-5 text-xs text-white/20 flex items-center gap-1.5">
          <span class="material-symbols-outlined text-[13px]">shield</span>
          Vos données sont sécurisées et confidentielles.
        </p>
      </div>

      <!-- Messages -->
      <div v-else class="py-4 sm:py-6 max-w-3xl mx-auto w-full">
        <TransitionGroup name="msg" tag="div">
          <template v-for="msg in messages" :key="msg.ts">
            <MessageUser v-if="msg.role === 'user'" :message="msg" />
            <MessageAI   v-else :message="msg" :streaming="isStreaming(msg)" />
          </template>
        </TransitionGroup>

        <div v-if="loading && streamingMsg && !streamingMsg.content" class="flex gap-3 px-4 mb-4 items-start">
          <div class="w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0" style="background:linear-gradient(135deg,#7C5CFC,#5A4FCF)">
            <span class="material-symbols-outlined text-white text-[15px]">auto_awesome</span>
          </div>
          <div class="px-4 py-3 rounded-2xl rounded-tl-sm flex items-center gap-1.5" style="background:#181825;border:1px solid rgba(255,255,255,0.06)">
            <span v-for="i in 3" :key="i" class="w-1.5 h-1.5 rounded-full bg-white/40 animate-dot" :style="`animation-delay:${(i-1)*0.15}s`" />
          </div>
        </div>
      </div>
    </div>

    <Transition name="fade">
      <button
        v-if="showScrollBtn"
        class="absolute bottom-4 right-4 w-9 h-9 rounded-full flex items-center justify-center text-white/60 hover:text-white transition shadow-lg border border-white/10"
        style="background:#181825"
        @click="scrollBottom"
      >
        <span class="material-symbols-outlined text-[20px]">keyboard_arrow_down</span>
      </button>
    </Transition>
  </div>
</template>
