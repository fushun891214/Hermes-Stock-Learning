function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
}

function inlineFormat(text) {
  return escapeHtml(text).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
}

function normalizeAssetPath(src) {
  return src.replace(/^\.\.\//, '/')
}

export function markdownToHtml(markdown) {
  const lines = markdown.split(/\r?\n/)
  const out = []
  let inList = false

  const closeList = () => {
    if (inList) {
      out.push('</ul>')
      inList = false
    }
  }

  lines.forEach((raw) => {
    const line = raw.trimEnd()
    if (!line.trim()) {
      closeList()
      return
    }

    const image = line.trim().match(/^!\[(.*?)\]\(([^)\s]+)(?:\s+"([^"]+)")?\)$/)
    if (image) {
      closeList()
      const [, alt, src, title] = image
      let desktopSrc = ''
      let caption = title || ''

      if (title?.startsWith('desktop:')) {
        desktopSrc = title.split(':').slice(1).join(':').trim()
        caption = ''
      }

      out.push('<figure class="lesson-graphic">')
      if (desktopSrc) {
        out.push('<picture>')
        out.push(`<source media="(min-width: 981px)" srcset="${escapeHtml(normalizeAssetPath(desktopSrc))}">`)
        out.push(`<img src="${escapeHtml(normalizeAssetPath(src))}" alt="${escapeHtml(alt)}" loading="lazy">`)
        out.push('</picture>')
      } else {
        out.push(`<img src="${escapeHtml(normalizeAssetPath(src))}" alt="${escapeHtml(alt)}" loading="lazy">`)
      }
      if (caption) out.push(`<figcaption>${escapeHtml(caption)}</figcaption>`)
      out.push('</figure>')
      return
    }

    if (line.startsWith('# ')) {
      closeList()
      out.push(`<h1>${escapeHtml(line.slice(2))}</h1>`)
    } else if (line.startsWith('## ')) {
      closeList()
      out.push(`<h2>${escapeHtml(line.slice(3))}</h2>`)
    } else if (line.startsWith('### ')) {
      closeList()
      out.push(`<h3>${escapeHtml(line.slice(4))}</h3>`)
    } else if (line.startsWith('- ')) {
      if (!inList) {
        out.push('<ul>')
        inList = true
      }
      out.push(`<li>${inlineFormat(line.slice(2))}</li>`)
    } else if (/^\d+\.\s+/.test(line)) {
      closeList()
      out.push(`<p>${inlineFormat(line.replace(/^\d+\.\s+/, ''))}</p>`)
    } else {
      closeList()
      out.push(`<p>${inlineFormat(line)}</p>`)
    }
  })

  closeList()
  return out.join('\n')
}

export function lessonTitleFromMarkdown(markdown) {
  return markdown.split(/\r?\n/)[0].replace(/^#\s*/, '').trim()
}

export function lessonBodyFromMarkdown(markdown) {
  return markdown.split(/\r?\n/).slice(1).join('\n').trim()
}
