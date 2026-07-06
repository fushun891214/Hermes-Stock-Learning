<script setup>
import { computed } from 'vue'

const props = defineProps({
  lesson: {
    type: Object,
    required: true,
  },
  lessons: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['go-home', 'go-lesson'])

const previousLesson = computed(() => props.lessons.find((lesson) => lesson.slug === props.lesson.prevSlug))
const nextLesson = computed(() => props.lessons.find((lesson) => lesson.slug === props.lesson.nextSlug))
</script>

<template>
  <article class="lesson-shell">
    <section class="lesson-top panel">
      <div class="lesson-top-meta">
        <span class="badge-pill">Day {{ lesson.day }}</span>
        <span class="lesson-top-note">{{ lesson.minutes }}・{{ lesson.tag }}</span>
      </div>
      <div class="lesson-top-copy">
        <h1>{{ lesson.title }}</h1>
        <p class="lesson-intro">這一課會用白話方式整理重點，先看懂觀念，再決定下一步。</p>
      </div>
      <div class="progress-track" aria-label="課程進度">
        <span :style="{ width: `${lesson.progress}%` }"></span>
      </div>
    </section>

    <section class="lesson-card panel lesson-body" v-html="lesson.bodyHtml"></section>

    <nav class="lesson-bottom-nav panel" aria-label="課程導覽">
      <div class="lesson-nav-overview">
        <a class="lesson-nav-card lesson-nav-card-home" href="/" @click.prevent="emit('go-home', '#roadmap')">
          <span class="lesson-nav-label">回到課表</span>
          <strong>查看所有課程</strong>
          <span class="lesson-nav-copy">回到首頁課程列表，選擇下一個想看的主題。</span>
        </a>
      </div>
      <div class="lesson-nav">
        <a v-if="previousLesson" class="lesson-nav-card lesson-nav-card-prev" :href="previousLesson.href" @click.prevent="emit('go-lesson', previousLesson.slug)">
          <span class="lesson-nav-label">上一課</span>
          <strong>← Day {{ previousLesson.day }}</strong>
          <span class="lesson-nav-copy">{{ previousLesson.title }}</span>
        </a>
        <a v-if="nextLesson" class="lesson-nav-card lesson-nav-card-next" :href="nextLesson.href" @click.prevent="emit('go-lesson', nextLesson.slug)">
          <span class="lesson-nav-label">下一課</span>
          <strong>Day {{ nextLesson.day }} →</strong>
          <span class="lesson-nav-copy">{{ nextLesson.title }}</span>
        </a>
      </div>
    </nav>
  </article>
</template>
