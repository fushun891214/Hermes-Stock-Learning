<script setup>
defineProps({
  isLesson: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['go-home'])
</script>

<template>
  <header class="site-header">
    <div class="wrap topbar">
      <a class="brand brand-text-only" href="/" @click.prevent="emit('go-home')">
        <span class="brand-copy">
          <strong>台股新手投資入門</strong>
          <small>給剛開始投資的人看的基礎課</small>
        </span>
      </a>

      <nav class="site-nav" aria-label="主選單">
        <a href="/" :class="{ 'is-current': !isLesson }" @click.prevent="emit('go-home')">首頁</a>
        <a href="/#roadmap" @click.prevent="emit('go-home', '#roadmap')">課表</a>
      </nav>
    </div>
  </header>
</template>
