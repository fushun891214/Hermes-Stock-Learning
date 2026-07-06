<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { lessonSources, TOTAL_DAYS } from './data/lessons'

const route = ref(getRoute())

function getRoute() {
  const path = window.location.pathname
  const hash = window.location.hash.replace(/^#/, '')
  const lessonMatch = path.match(/\/lessons\/(day-\d+)\.html$/) || hash.match(/^\/lessons\/(day-\d+)/)
  return lessonMatch ? { name: 'lesson', slug: lessonMatch[1] } : { name: 'home' }
}

function goHome(anchor = '') {
  history.pushState({}, '', `/${anchor}`)
  route.value = getRoute()
  if (anchor) requestAnimationFrame(() => document.querySelector(anchor)?.scrollIntoView({ behavior: 'smooth' }))
  else window.scrollTo({ top: 0, behavior: 'smooth' })
}

function goLesson(slug) {
  history.pushState({}, '', `/lessons/${slug}.html`)
  route.value = getRoute()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function onPopState() {
  route.value = getRoute()
}

onMounted(() => window.addEventListener('popstate', onPopState))
onUnmounted(() => window.removeEventListener('popstate', onPopState))

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

function markdownToHtml(markdown) {
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
      const normalizedSrc = src.replace(/^\.\.\//, '/')
      const normalizedDesktopSrc = desktopSrc.replace(/^\.\.\//, '/')
      out.push('<figure class="lesson-graphic">')
      if (desktopSrc) {
        out.push('<picture>')
        out.push(`<source media="(min-width: 981px)" srcset="${escapeHtml(normalizedDesktopSrc)}">`)
        out.push(`<img src="${escapeHtml(normalizedSrc)}" alt="${escapeHtml(alt)}" loading="lazy">`)
        out.push('</picture>')
      } else {
        out.push(`<img src="${escapeHtml(normalizedSrc)}" alt="${escapeHtml(alt)}" loading="lazy">`)
      }
      if (caption) out.push(`<figcaption>${escapeHtml(caption)}</figcaption>`)
      out.push('</figure>')
      return
    }

    if (line.startsWith('# ')) {
      closeList(); out.push(`<h1>${escapeHtml(line.slice(2))}</h1>`)
    } else if (line.startsWith('## ')) {
      closeList(); out.push(`<h2>${escapeHtml(line.slice(3))}</h2>`)
    } else if (line.startsWith('### ')) {
      closeList(); out.push(`<h3>${escapeHtml(line.slice(4))}</h3>`)
    } else if (line.startsWith('- ')) {
      if (!inList) { out.push('<ul>'); inList = true }
      out.push(`<li>${inlineFormat(line.slice(2))}</li>`)
    } else if (/^\d+\.\s+/.test(line)) {
      closeList(); out.push(`<p>${inlineFormat(line.replace(/^\d+\.\s+/, ''))}</p>`)
    } else {
      closeList(); out.push(`<p>${inlineFormat(line)}</p>`)
    }
  })
  closeList()
  return out.join('\n')
}

const lessons = lessonSources.map((lesson, index, all) => {
  const title = lesson.raw.split(/\r?\n/)[0].replace(/^#\s*/, '').trim()
  const bodyMarkdown = lesson.raw.split(/\r?\n/).slice(1).join('\n').trim()
  return {
    ...lesson,
    title,
    href: `/lessons/${lesson.slug}.html`,
    bodyHtml: markdownToHtml(bodyMarkdown),
    progress: Math.max(0, Math.min(100, (lesson.day / TOTAL_DAYS) * 100)),
    prevSlug: all[index - 1]?.slug,
    nextSlug: all[index + 1]?.slug,
  }
})

const currentLesson = computed(() => lessons.find((lesson) => lesson.slug === route.value.slug) || lessons[0])
const isLesson = computed(() => route.value.name === 'lesson')
</script>

<template>
  <div class="site-bg site-bg-a"></div>
  <div class="site-bg site-bg-b"></div>

  <header class="site-header">
    <div class="wrap topbar">
      <a class="brand brand-text-only" href="/" @click.prevent="goHome()">
        <span class="brand-copy">
          <strong>台股新手投資入門</strong>
          <small>給剛開始投資的人看的基礎課</small>
        </span>
      </a>

      <nav class="site-nav" aria-label="主選單">
        <a href="/" :class="{ 'is-current': !isLesson }" @click.prevent="goHome()">首頁</a>
        <a href="/#roadmap" @click.prevent="goHome('#roadmap')">課表</a>
      </nav>
    </div>
  </header>

  <main class="wrap page-shell">
    <template v-if="!isLesson">
      <section class="home-hero panel">
        <div class="hero-layout">
          <div class="hero-copy hero-copy-main">
            <span class="badge-pill">台股新手投資入門</span>
            <h1>先建立觀念，再開始做投資決定</h1>
            <p class="hero-lead">用白話整理股票、ETF、投入節奏與常見判斷情境，幫你把第一步走穩，而不是急著追熱門標的。</p>
            <div class="hero-actions">
              <a class="btn primary" :href="lessons[0].href" @click.prevent="goLesson(lessons[0].slug)">從 Day 1 開始</a>
              <a class="btn secondary" href="#roadmap" @click.prevent="goHome('#roadmap')">查看全部課程</a>
            </div>
          </div>

          <aside class="hero-summary" aria-label="學習路線摘要">
            <span class="section-kicker">先照這個順序走</span>
            <ol class="journey-list">
              <li><strong>理解基本盤</strong><span>先釐清股票、ETF、風險與自己的目的。</span></li>
              <li><strong>建立開始方法</strong><span>準備資金、選商品、安排投入節奏。</span></li>
              <li><strong>練習判斷訊號</strong><span>面對熱門、配息、績效與費用時，不被單一理由帶著走。</span></li>
            </ol>
          </aside>
        </div>
      </section>

      <section class="panel lesson-table-panel" id="roadmap">
        <div class="section-heading lesson-table-heading">
          <div>
            <span class="section-kicker">課程列表</span>
            <h2>目前已開放的課程</h2>
            <p class="section-lead">每一課都可以直接閱讀。第一次接觸投資時，建議從 Day 1 照順序往下看。</p>
          </div>
        </div>

        <div class="roadmap-pills" aria-label="課程階段">
          <span>Day 1–5 基礎與起步</span>
          <span>Day 6–11 持有與檢查</span>
          <span>Day 12 起 判讀常見訊號</span>
        </div>

        <div class="lesson-list">
          <article v-for="lesson in lessons" :key="lesson.slug" class="lesson-row-card">
            <div class="lesson-row-main">
              <span class="day-label">Day {{ lesson.day }}</span>
              <h3>{{ lesson.title }}</h3>
              <div class="lesson-row-meta">
                <span>{{ lesson.minutes }}</span>
                <span class="table-tag">{{ lesson.tag }}</span>
              </div>
            </div>
            <a class="btn row-btn" :href="lesson.href" @click.prevent="goLesson(lesson.slug)">開始這一天</a>
          </article>
        </div>
      </section>
    </template>

    <template v-else>
      <article class="lesson-shell">
        <section class="lesson-top panel">
          <div class="lesson-top-meta">
            <span class="badge-pill">Day {{ currentLesson.day }}</span>
            <span class="lesson-top-note">{{ currentLesson.minutes }}・{{ currentLesson.tag }}</span>
          </div>
          <div class="lesson-top-copy">
            <h1>{{ currentLesson.title }}</h1>
            <p class="lesson-intro">這一課會用白話方式整理重點，先看懂觀念，再決定下一步。</p>
          </div>
          <div class="progress-track" aria-label="課程進度">
            <span :style="{ width: `${currentLesson.progress}%` }"></span>
          </div>
        </section>

        <section class="lesson-card panel lesson-body" v-html="currentLesson.bodyHtml"></section>

        <nav class="lesson-bottom-nav panel" aria-label="課程導覽">
          <div class="lesson-nav-overview">
            <a class="lesson-nav-card lesson-nav-card-home" href="/" @click.prevent="goHome('#roadmap')">
              <span class="lesson-nav-label">回到課表</span>
              <strong>查看所有課程</strong>
              <span class="lesson-nav-copy">回到首頁課程列表，選擇下一個想看的主題。</span>
            </a>
          </div>
          <div class="lesson-nav">
            <a v-if="currentLesson.prevSlug" class="lesson-nav-card lesson-nav-card-prev" :href="`/lessons/${currentLesson.prevSlug}.html`" @click.prevent="goLesson(currentLesson.prevSlug)">
              <span class="lesson-nav-label">上一課</span>
              <strong>← Day {{ lessons.find(l => l.slug === currentLesson.prevSlug)?.day }}</strong>
              <span class="lesson-nav-copy">{{ lessons.find(l => l.slug === currentLesson.prevSlug)?.title }}</span>
            </a>
            <a v-if="currentLesson.nextSlug" class="lesson-nav-card lesson-nav-card-next" :href="`/lessons/${currentLesson.nextSlug}.html`" @click.prevent="goLesson(currentLesson.nextSlug)">
              <span class="lesson-nav-label">下一課</span>
              <strong>Day {{ lessons.find(l => l.slug === currentLesson.nextSlug)?.day }} →</strong>
              <span class="lesson-nav-copy">{{ lessons.find(l => l.slug === currentLesson.nextSlug)?.title }}</span>
            </a>
          </div>
        </nav>
      </article>
    </template>
  </main>

  <footer class="site-footer wrap">
    <div class="footer-card footer-simple">
      <p class="footer-title">台股新手投資入門</p>
      <p class="footer-copy">給剛開始接觸投資的人看的基礎內容。</p>
      <p class="footer-note">本站內容僅供學習整理，不構成投資建議。</p>
    </div>
  </footer>
</template>
