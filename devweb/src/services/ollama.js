// Crée une erreur structurée avec code HTTP pour errorService.resolveErrorType
function httpError(status, body = '') {
  const err = new Error(`Ollama HTTP ${status}`)
  err.status = status
  err.body   = body
  return err
}

export async function checkOllama(baseUrl) {
  try {
    const res = await fetch(`${baseUrl}/api/tags`, { signal: AbortSignal.timeout(5000) })
    return res.ok
  } catch {
    return false
  }
}

export async function listModels(baseUrl) {
  const res = await fetch(`${baseUrl}/api/tags`, { signal: AbortSignal.timeout(5000) })
  if (!res.ok) throw httpError(res.status, await res.text().catch(() => ''))
  let data
  try {
    data = await res.json()
  } catch {
    // Server responded with non-JSON (HTML error page, wrong URL, etc.)
    const err = new Error('La réponse n\'est pas du JSON — l\'URL ne pointe pas vers Ollama.')
    err.status = 0
    throw err
  }
  return (data.models ?? []).map(m => m.name)
}

export async function* streamChat(messages, model, baseUrl, { temperature = 0.7, maxTokens = 2048, signal } = {}) {
  const res = await fetch(`${baseUrl}/api/chat`, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    signal,
    body: JSON.stringify({
      model,
      messages,
      stream: true,
      options: {
        temperature,
        num_predict: maxTokens,
      },
    }),
  })

  if (!res.ok) {
    const body = await res.text().catch(() => '')
    throw httpError(res.status, body)
  }

  const reader  = res.body.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const lines = decoder.decode(value).split('\n').filter(Boolean)
    for (const line of lines) {
      let json
      try { json = JSON.parse(line) }
      catch (e) {
        const parseErr = new Error(`Stream parse error: ${line.slice(0, 80)}`)
        parseErr.code = 'STREAM_PARSE'
        throw parseErr
      }
      if (json.message?.content) yield json.message.content
    }
  }
}
