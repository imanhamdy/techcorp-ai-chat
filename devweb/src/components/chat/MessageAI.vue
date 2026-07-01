<script setup>
import { computed, ref } from 'vue'
import { marked }        from 'marked'
import { ERROR_TYPES }   from '../../services/errorService'

const props  = defineProps({ message: Object, streaming: Boolean })
const copied = ref(false)
const html   = computed(() => props.message.content ? marked.parse(props.message.content,{breaks:true,gfm:true}) : '')

function fmt(ts) { return new Date(ts).toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'}) }
function errMeta(t) { return ERROR_TYPES[t] ?? ERROR_TYPES.NETWORK }
async function copy() {
  await navigator.clipboard.writeText(props.message.content)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}
</script>
<template>
  <div v-if="message.content || message.error" class="flex gap-2.5 sm:gap-3 mb-5 px-3 sm:px-4 group">
    <div class="w-7 h-7 sm:w-8 sm:h-8 rounded-xl flex items-center justify-center flex-shrink-0 mt-0.5" style="background:linear-gradient(135deg,#7C5CFC,#5A4FCF)">
      <span class="material-symbols-outlined text-white text-[13px] sm:text-[15px]">auto_awesome</span>
    </div>
    <div class="flex-1 min-w-0">
      <p class="text-xs font-semibold mb-1.5" style="color:#7C5CFC">TechCorp AI</p>
      <div v-if="message.error" class="px-3.5 py-3 rounded-2xl rounded-tl-sm text-sm" style="background:#1a0a0a;border:1px solid rgba(239,68,68,0.2)">
        <p class="flex items-center gap-2 text-red-400 font-semibold mb-1">
          <span class="material-symbols-outlined text-[15px]">{{ errMeta(message.errorType).icon }}</span>
          {{ errMeta(message.errorType).label }}
        </p>
        <p class="text-red-300/60 text-xs">{{ errMeta(message.errorType).detail }}</p>
        <p class="text-white/25 text-[10px] mt-2 uppercase tracking-widest">CODE : {{ message.errorType }}</p>
      </div>
      <div v-else class="relative">
        <div class="px-3.5 sm:px-4 py-3 rounded-2xl rounded-tl-sm text-sm text-white/90 leading-relaxed" style="background:#181825;border:1px solid rgba(255,255,255,0.06)">
          <div class="prose prose-invert prose-sm max-w-none" v-html="html" />
          <span v-if="streaming" class="inline-block w-0.5 h-4 ml-0.5 align-middle animate-blink" style="background:#7C5CFC" />
        </div>
        <button
          v-if="!streaming && message.content"
          class="absolute -top-1 right-1 p-1.5 rounded-lg opacity-0 group-hover:opacity-100 transition hover:bg-white/10 text-white/30 hover:text-white"
          @click="copy"
        >
          <span class="material-symbols-outlined text-[14px]">{{ copied ? 'check' : 'content_copy' }}</span>
        </button>
      </div>
      <p class="text-[10px] text-white/18 mt-1 pl-0.5">{{ fmt(message.ts) }}</p>
    </div>
  </div>
</template>
