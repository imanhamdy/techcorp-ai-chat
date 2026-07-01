<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Sidebar       from './components/layout/Sidebar.vue'
import TopBar        from './components/layout/TopBar.vue'
import InputArea     from './components/layout/InputArea.vue'
import ChatViewport  from './components/chat/ChatViewport.vue'
import SettingsPanel from './components/settings/SettingsPanel.vue'
import ShaderCanvas  from './components/ui/ShaderCanvas.vue'
import { useChat }   from './composables/useChat'
import { useModels } from './composables/useModels'

const { messages, loading, ollamaOnline, send, stop, clearChat, checkStatus } = useChat()
const { fetchModels } = useModels()

const showSettings = ref(false)
const showSidebar  = ref(false)
let interval

onMounted(async () => {
  await checkStatus()
  await fetchModels()
  interval = setInterval(async () => {
    await checkStatus()
    if (ollamaOnline.value) fetchModels()
  }, 30_000)
})
onUnmounted(() => clearInterval(interval))
</script>

<template>
  <div class="flex h-screen overflow-hidden" style="background:#09090B">

    <!-- Mobile backdrop -->
    <Transition name="fade">
      <div
        v-if="showSidebar"
        class="fixed inset-0 bg-black/60 z-30 md:hidden backdrop-blur-sm"
        @click="showSidebar = false"
      />
    </Transition>

    <!-- Sidebar: fixed drawer on mobile, static on desktop -->
    <div
      class="fixed top-0 left-0 h-full z-40 transition-transform duration-300 md:translate-x-0 md:relative md:z-auto md:flex-shrink-0"
      :class="showSidebar ? 'translate-x-0' : '-translate-x-full'"
    >
      <Sidebar
        @clear-chat="() => { clearChat(); showSidebar = false }"
        @toggle-settings="showSettings = !showSettings"
        @close="showSidebar = false"
      />
    </div>

    <!-- Main -->
    <main class="flex-1 flex flex-col relative overflow-hidden min-w-0">
      <ShaderCanvas class="absolute inset-0 pointer-events-none z-0" />
      <div class="relative z-10 flex flex-col h-full">
        <TopBar
          :ollama-online="ollamaOnline"
          @toggle-settings="showSettings = !showSettings"
          @toggle-sidebar="showSidebar = !showSidebar"
        />
        <ChatViewport :messages="messages" :loading="loading" @suggest="send" />
        <InputArea :loading="loading" @send="send" @stop="stop" />
      </div>
    </main>

    <SettingsPanel :show="showSettings" @close="showSettings = false" />
  </div>
</template>
