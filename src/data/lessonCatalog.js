import { lessonSources, TOTAL_DAYS } from './lessons'
import { lessonBodyFromMarkdown, lessonTitleFromMarkdown, markdownToHtml } from '../utils/markdown'

export const lessons = lessonSources.map((lesson, index, all) => {
  const title = lessonTitleFromMarkdown(lesson.raw)
  const bodyMarkdown = lessonBodyFromMarkdown(lesson.raw)

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

export function findLesson(slug) {
  return lessons.find((lesson) => lesson.slug === slug) || lessons[0]
}
