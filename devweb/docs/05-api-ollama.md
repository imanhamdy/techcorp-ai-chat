# 05 - API Ollama, services & composables

## Endpoint
```
POST http://localhost:11434/api/chat
```

## Payload
```json
{
 "model": "phi3.5",
 "messages": [{ "role": "user", "content": "..." }],
 "stream": true
}
```

## `services/ollama.js`

### Streaming (NDJSON)
```js
export async function* streamChat(messages, model = 'phi3.5') {
 const res = await fetch('http://localhost:11434/api/chat', {
 method: 'POST',
 headers: { 'Content-Type': 'application/json' },
 body: JSON.stringify({ model, messages, stream: true }),
 })

 const reader = res.body.getReader()
 const decoder = new TextDecoder()

 while (true) {
 const { done, value } = await reader.read()
 if (done) break
 const lines = decoder.decode(value).split('\n').filter(Boolean)
 for (const line of lines) {
 const json = JSON.parse(line)
 if (json.message?.content) yield json.message.content
 }
 }
}
```

### Health check
```js
export async function checkOllama() {
 try {
 const res = await fetch('http://localhost:11434/api/tags')
 return res.ok
 } catch {
 return false
 }
}
```

### Lister les modèles
```js
export async function listModels() {
 const res = await fetch('http://localhost:11434/api/tags')
 const data = await res.json()
 return data.models.map(m => m.name)
}
```

## Composable `useChat.js`
```js
import { ref, reactive } from 'vue'
import { streamChat, checkOllama } from '../services/ollama'

export function useChat() {
 const messages = ref([]) // [{ role: 'user'|'assistant', content, ts: Date }]
 const loading = ref(false)
 const ollamaOnline = ref(false)
 const activeModel = ref('phi3.5')

 async function send(userInput) {
 if (!userInput.trim() || loading.value) return

 messages.value.push({ role: 'user', content: userInput, ts: new Date() })
 loading.value = true

 const aiMsg = reactive({ role: 'assistant', content: '', ts: new Date() })
 messages.value.push(aiMsg)

 const history = messages.value
 .slice(0, -1)
 .map(m => ({ role: m.role, content: m.content }))

 for await (const chunk of streamChat(history, activeModel.value)) {
 aiMsg.content += chunk
 }

 loading.value = false
 }

 function clearChat() {
 messages.value = []
 }

 return { messages, loading, ollamaOnline, activeModel, send, clearChat }
}
```

## CORS - lancer Ollama avec origines autorisées
```bash
OLLAMA_ORIGINS="*" ollama serve
```
PowerShell :
```powershell
$env:OLLAMA_ORIGINS="*"; ollama serve
```
