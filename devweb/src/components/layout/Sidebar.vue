<script setup>
import { ref, computed } from 'vue'
import { useHistory } from '../../composables/useHistory'
import { useChat }    from '../../composables/useChat'

const emit = defineEmits(['clear-chat', 'toggle-settings', 'close'])
const { recentSessions, archivedSessions, deleteSession, relativeTime } = useHistory()
const { loadSession, currentSessionId } = useChat()

const search   = ref('')
const openMenu = ref(null)

const filtered = computed(() =>
  search.value
    ? recentSessions.value.filter(s => s.title.toLowerCase().includes(search.value.toLowerCase()))
    : recentSessions.value
)

function toggleMenu(id, e) { e.stopPropagation(); openMenu.value = openMenu.value === id ? null : id }
function closeMenu() { openMenu.value = null }
function del(id) { deleteSession(id); openMenu.value = null }
function select(s) { loadSession(s); emit('close') }
</script>

<template>
  <aside
    class="w-[280px] h-full flex flex-col border-r border-white/5"
    style="background:#101018"
    @click="closeMenu"
  >
    <!-- Logo + close (mobile) -->
    <div class="px-4 pt-4 pb-3 flex items-center gap-2.5">
      <div class="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0" style="background:linear-gradient(135deg,#7C5CFC,#5A4FCF)">
        <span class="material-symbols-outlined text-white text-[18px]">auto_awesome</span>
      </div>
      <span class="font-bold text-white text-[15px] tracking-tight flex-1">TechCorp <span style="color:#7C5CFC">AI</span></span>
      <!-- Close button on mobile -->
      <button class="md:hidden p-1.5 rounded-lg hover:bg-white/10 text-white/40 hover:text-white transition" @click="emit('close')">
        <span class="material-symbols-outlined text-[20px]">close</span>
      </button>
    </div>

    <!-- New Chat -->
    <div class="px-3 mb-3">
      <button
        class="w-full flex items-center gap-2 justify-center py-2.5 rounded-xl text-sm font-semibold text-white transition hover:opacity-90 active:scale-[0.98]"
        style="background:linear-gradient(135deg,#7C5CFC,#5A4FCF)"
        @click="() => { emit('clear-chat'); emit('close') }"
      >
        <span class="material-symbols-outlined text-[18px]">add</span>
        Nouveau chat
      </button>
    </div>

    <!-- Search -->
    <div class="px-3 mb-3">
      <div class="flex items-center gap-2 px-3 py-2 rounded-xl border border-white/8" style="background:#1e1e2e">
        <span class="material-symbols-outlined text-white/30 text-[16px]">search</span>
        <input v-model="search" type="text" placeholder="Rechercher…" class="flex-1 bg-transparent text-xs text-white placeholder-white/30 outline-none" />
      </div>
    </div>

    <!-- History -->
    <div class="flex-1 overflow-y-auto px-3 pb-3">
      <p v-if="filtered.length" class="text-[10px] font-semibold uppercase tracking-widest text-white/30 px-2 mb-2">Récent</p>

      <div
        v-for="s in filtered"
        :key="s.id"
        class="group flex items-center gap-2 px-3 py-2.5 rounded-xl mb-1 cursor-pointer transition relative"
        :class="s.id === currentSessionId ? 'border border-[#7C5CFC]/30' : 'hover:bg-white/5'"
        :style="s.id === currentSessionId ? 'background:rgba(124,92,252,0.12)' : ''"
        @click="select(s)"
      >
        <span class="material-symbols-outlined text-[15px] flex-shrink-0" :class="s.id === currentSessionId ? 'text-[#7C5CFC]' : 'text-white/25'">chat_bubble_outline</span>
        <div class="flex-1 min-w-0">
          <p class="text-xs font-medium truncate" :class="s.id === currentSessionId ? 'text-white' : 'text-white/60'">{{ s.title }}</p>
          <p class="text-[10px] text-white/25 mt-0.5">{{ relativeTime(s.ts) }}</p>
        </div>
        <button
          class="opacity-0 group-hover:opacity-100 p-1 rounded-lg hover:bg-white/10 text-white/35 hover:text-white transition flex-shrink-0"
          @click.stop="toggleMenu(s.id, $event)"
        >
          <span class="material-symbols-outlined text-[15px]">more_horiz</span>
        </button>
        <Transition name="slide-up">
          <div
            v-if="openMenu === s.id"
            class="absolute right-2 top-full mt-1 z-50 rounded-xl overflow-hidden shadow-2xl border border-white/10 py-1 min-w-[140px]"
            style="background:#1e1e2e"
            @click.stop
          >
            <button class="w-full flex items-center gap-2 px-3 py-2 text-xs text-red-400 hover:bg-red-900/20 transition" @click="del(s.id)">
              <span class="material-symbols-outlined text-[14px]">delete</span> Supprimer
            </button>
          </div>
        </Transition>
      </div>

      <div v-if="!filtered.length && !search" class="flex flex-col items-center justify-center h-24 text-white/20 gap-2">
        <span class="material-symbols-outlined text-[28px]">chat_bubble_outline</span>
        <p class="text-xs">Aucune conversation</p>
      </div>
      <p v-else-if="!filtered.length && search" class="text-xs text-white/25 text-center py-4">Aucun résultat</p>
    </div>

    <!-- Pro card -->
    <div class="mx-3 mb-3 p-3 rounded-xl border border-[#7C5CFC]/20" style="background:linear-gradient(135deg,rgba(124,92,252,0.12),rgba(90,79,207,0.08))">
      <div class="flex items-center gap-2 mb-1.5">
        <span class="material-symbols-outlined text-[#7C5CFC] text-[18px]">star</span>
        <p class="text-xs font-semibold text-white">Passez à Pro</p>
      </div>
      <p class="text-[11px] text-white/40 mb-2.5">Accédez à des modèles avancés, plus rapides et plus performants.</p>
      <button class="w-full text-xs font-semibold text-[#7C5CFC] hover:text-white transition py-1.5 rounded-lg border border-[#7C5CFC]/30 hover:bg-[#7C5CFC]/20">
        Découvrir Pro →
      </button>
    </div>

    <!-- Profile -->
    <div class="px-3 pb-4 border-t border-white/5 pt-3">
      <div class="flex items-center gap-2.5 px-2 py-2 rounded-xl hover:bg-white/5 cursor-pointer transition">
        <div class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold text-white flex-shrink-0" style="background:linear-gradient(135deg,#7C5CFC,#4F8DFF)">TC</div>
        <div class="flex-1 min-w-0">
          <p class="text-xs font-medium text-white truncate">TechCorp AI</p>
          <p class="text-[10px] text-white/35 truncate">phi3-financial</p>
        </div>
        <span class="material-symbols-outlined text-white/30 text-[16px]">expand_more</span>
      </div>
    </div>
  </aside>
</template>
