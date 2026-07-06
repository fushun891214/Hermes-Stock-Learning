import { cp, mkdir, writeFile, copyFile, readdir } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import { join } from 'node:path'

const root = process.cwd()
const site = join(root, 'site')

await mkdir(join(site, 'assets'), { recursive: true })
await cp(join(root, 'assets'), join(site, 'assets'), { recursive: true, force: true })
await writeFile(join(site, '.nojekyll'), '')

if (existsSync(join(root, 'CNAME'))) {
  await copyFile(join(root, 'CNAME'), join(site, 'CNAME'))
}

// Keep existing lesson URLs directly loadable on GitHub Pages.
await mkdir(join(site, 'lessons'), { recursive: true })
const lessonFiles = await readdir(join(root, 'content', 'lessons'))
for (const file of lessonFiles.filter((name) => /^day-\d+\.md$/.test(name))) {
  const slug = file.replace(/\.md$/, '.html')
  await copyFile(join(site, 'index.html'), join(site, 'lessons', slug))
}
