<script setup>
import { useModels } from '../../composables/useModels'
import { useChat }   from '../../composables/useChat'
import { useTheme }  from '../../composables/useTheme'

defineProps({ ollamaOnline: Boolean })
defineEmits(['toggle-settings', 'toggle-sidebar'])

const { availableModels } = useModels()
const { activeModel }     = useChat()
const { dark, toggle: toggleTheme } = useTheme()
</script>

<template>
  <header class="flex items-center gap-3 px-4 py-3 border-b border-white/5 flex-shrink-0" style="background:rgba(9,9,11,0.8);backdrop-filter:blur(20px)">
    <!-- Hamburger (mobile) -->
    <button
      class="md:hidden p-2 rounded-lg hover:bg-white/8 text-white/50 hover:text-white transition flex-shrink-0"
      @click="$emit('toggle-sidebar')"
    >
      <span class="material-symbols-outlined text-[22px]">menu</span>
    </button>

    <!-- Logo + status -->
    <div class="flex items-center gap-2 flex-shrink-0">
      <div class="w-7 h-7 rounded-lg flex items-center justify-center" style="background:linear-gradient(135deg,#7C5CFC,#5A4FCF)">
        <span class="material-symbols-outlined text-white text-[15px]">auto_awesome</span>
      </div>
      <span class="text-sm font-semibold text-white hidden sm:inline">TechCorp AI</span>
      <span
        class="w-2 h-2 rounded-full flex-shrink-0"
        :class="ollamaOnline ? 'bg-[#22C55E]' : 'bg-red-500'"
        :style="ollamaOnline ? 'box-shadow:0 0 6px #22C55E' : ''"
      />
    </div>

    <!-- Model selector -->
    <div v-if="availableModels.length" class="flex-1 flex justify-center">
      <div class="relative">
        <select
          v-model="activeModel"
          class="appearance-none pl-3 pr-7 py-1.5 rounded-lg text-xs text-white/80 font-medium outline-none cursor-pointer border border-white/10 transition hover:border-[#7C5CFC]/40 max-w-[160px] sm:max-w-none"
          style="background:#181825"
        >
          <option v-for="m in availableModels" :key="m" :value="m">{{ m.replace(':latest','') }}</option>
        </select>
        <span class="material-symbols-outlined text-white/40 text-[14px] absolute right-1.5 top-1/2 -translate-y-1/2 pointer-events-none">expand_more</span>
      </div>
    </div>

    <!-- Icons -->
    <div class="flex items-center gap-1 flex-shrink-0">
      <!-- Theme toggle - actually works now -->
      <button
        class="p-2 rounded-lg hover:bg-white/8 text-white/40 hover:text-white transition hidden sm:flex"
        :title="dark ? 'Mode clair' : 'Mode sombre'"
        @click="toggleTheme"
      >
        <span class="material-symbols-outlined text-[18px]">{{ dark ? 'light_mode' : 'dark_mode' }}</span>
      </button>
      <button
        class="p-2 rounded-lg hover:bg-white/8 text-white/40 hover:text-white transition"
        title="Paramètres"
        @click="$emit('toggle-settings')"
      >
        <span class="material-symbols-outlined text-[18px]">settings</span>
      </button>
    </div>
  </header>
</template>
