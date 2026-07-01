<script setup>
defineProps({ title: String })
</script>
<template>
  <div class="mb-4">
    <p v-if="title" class="text-[10px] font-semibold uppercase tracking-widest text-white/30 px-3 mb-1">{{ title }}</p>
    <slot />
  </div>
</template>
