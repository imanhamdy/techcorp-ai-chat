import { ref, watch } from 'vue'

const dark = ref(localStorage.getItem('theme') !== 'light')

watch(dark, (v) => {
  localStorage.setItem('theme', v ? 'dark' : 'light')
  document.documentElement.classList.toggle('light-mode', !v)
})

// Apply on load
if (!dark.value) document.documentElement.classList.add('light-mode')

export function useTheme() {
  function toggle() { dark.value = !dark.value }
  return { dark, toggle }
}
