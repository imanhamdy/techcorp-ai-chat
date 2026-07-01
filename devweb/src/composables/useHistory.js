import { ref, computed, watch } from 'vue'

const STORAGE_KEY = 'techcorp_sessions'

function load() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]') }
  catch { return [] }
}

const sessions = ref(load())

watch(sessions, (s) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(s))
}, { deep: true })

function relativeTime(ts) {
  const diff = Date.now() - ts
  const m = Math.floor(diff / 60000)
  if (m < 1)  return 'just now'
  if (m < 60) return `${m}m`
  const h = Math.floor(m / 60)
  if (h < 24) return `${h}h`
  const d = Math.floor(h / 24)
  if (d < 7)  return `${d}d`
  return `${Math.floor(d / 7)}w`
}

export function useHistory() {
  const recentSessions = computed(() =>
    sessions.value
      .filter(s => !s.archived)
      .sort((a, b) => b.ts - a.ts)
      .slice(0, 20)
  )

  const archivedSessions = computed(() =>
    sessions.value
      .filter(s => s.archived)
      .sort((a, b) => b.ts - a.ts)
  )

  function saveSession(messages, id = null) {
    if (!messages.length) return null
    const firstUser = messages.find(m => m.role === 'user')
    if (!firstUser) return null

    const title = firstUser.content.slice(0, 55) + (firstUser.content.length > 55 ? '…' : '')

    if (id) {
      const existing = sessions.value.find(s => s.id === id)
      if (existing) {
        existing.messages = messages.map(m => ({ ...m, ts: m.ts instanceof Date ? m.ts.toISOString() : m.ts }))
        existing.ts    = Date.now()
        existing.title = title
        return id
      }
    }

    const newId = crypto.randomUUID()
    sessions.value.unshift({
      id:       newId,
      title,
      ts:       Date.now(),
      messages: messages.map(m => ({ ...m, ts: m.ts instanceof Date ? m.ts.toISOString() : m.ts })),
      archived: false,
    })
    return newId
  }

  function archiveSession(id) {
    const s = sessions.value.find(s => s.id === id)
    if (s) s.archived = !s.archived
  }

  function deleteSession(id) {
    const idx = sessions.value.findIndex(s => s.id === id)
    if (idx !== -1) sessions.value.splice(idx, 1)
  }

  return { sessions, recentSessions, archivedSessions, saveSession, archiveSession, deleteSession, relativeTime }
}
