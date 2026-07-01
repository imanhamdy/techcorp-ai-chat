<script setup>
defineProps({ message: Object })
function fmt(ts) { return new Date(ts).toLocaleTimeString('fr-FR',{hour:'2-digit',minute:'2-digit'}) }
</script>
<template>
  <div class="flex justify-end mb-5 px-3 sm:px-4">
    <div class="max-w-[85%] sm:max-w-[72%]">
      <div class="px-3.5 sm:px-4 py-2.5 sm:py-3 rounded-2xl rounded-tr-sm text-sm text-white leading-relaxed whitespace-pre-wrap" style="background:linear-gradient(135deg,rgba(124,92,252,0.25),rgba(90,79,207,0.2));border:1px solid rgba(124,92,252,0.2)">
        {{ message.content }}
      </div>
      <p class="text-[10px] text-white/20 mt-1 text-right">{{ fmt(message.ts) }}</p>
    </div>
  </div>
</template>
