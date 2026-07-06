<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import SiteFooter from './components/SiteFooter.vue'
import SiteHeader from './components/SiteHeader.vue'
import { findLesson, lessons } from './data/lessonCatalog'
import HomePage from './pages/HomePage.vue'
import LessonPage from './pages/LessonPage.vue'

function getRoute() {
  const path = window.location.pathname
  const hash = window.location.hash.replace(/^#/, '')
  const lessonMatch = path.match(/\/lessons\/(day-\d+)\.html$/) || hash.match(/^\/lessons\/(day-\d+)/)
  return lessonMatch ? { name: 'lesson', slug: lessonMatch[1] } : { name: 'home' }
}

const route = ref(getRoute())
const isLesson = computed(() => route.value.name === 'lesson')
const currentLesson = computed(() => findLesson(route.value.slug))

function updateRoute() {
  route.value = getRoute()
}

function goHome(anchor = '') {
  history.pushState({}, '', `/${anchor}`)
  updateRoute()
  if (anchor) requestAnimationFrame(() => document.querySelector(anchor)?.scrollIntoView({ behavior: 'smooth' }))
  else window.scrollTo({ top: 0, behavior: 'smooth' })
}

function goLesson(slug) {
  history.pushState({}, '', `/lessons/${slug}.html`)
  updateRoute()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => window.addEventListener('popstate', updateRoute))
onUnmounted(() => window.removeEventListener('popstate', updateRoute))
</script>

<template>
  <div class="site-bg site-bg-a"></div>
  <div class="site-bg site-bg-b"></div>

  <SiteHeader :is-lesson="isLesson" @go-home="goHome" />

  <main class="wrap page-shell">
    <HomePage v-if="!isLesson" :lessons="lessons" @go-home="goHome" @go-lesson="goLesson" />
    <LessonPage v-else :lesson="currentLesson" :lessons="lessons" @go-home="goHome" @go-lesson="goLesson" />
  </main>

  <SiteFooter />
</template>
