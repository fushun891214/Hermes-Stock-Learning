<script setup>
defineProps({
  lessons: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['go-home', 'go-lesson'])
</script>

<template>
  <section class="home-hero panel">
    <div class="hero-layout">
      <div class="hero-copy hero-copy-main">
        <span class="badge-pill">台股新手投資入門</span>
        <h1>先建立觀念，再開始做投資決定</h1>
        <p class="hero-lead">用白話整理股票、ETF、投入節奏與常見判斷情境，幫你把第一步走穩，而不是急著追熱門標的。</p>
        <div class="hero-actions">
          <a class="btn primary" :href="lessons[0].href" @click.prevent="emit('go-lesson', lessons[0].slug)">從 Day 1 開始</a>
          <a class="btn secondary" href="#roadmap" @click.prevent="emit('go-home', '#roadmap')">查看全部課程</a>
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
        <a class="btn row-btn" :href="lesson.href" @click.prevent="emit('go-lesson', lesson.slug)">開始這一天</a>
      </article>
    </div>
  </section>
</template>
