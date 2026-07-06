# Hermes Stock Learning

台股新手學習網站專案。使用 Vue / Vite 建置，並部署到 GitHub Pages。

## 目標
- 以 30 天課程方式學習台股基礎
- 使用 Vue 元件管理首頁、課程頁與共用版面
- 使用 GitHub Actions 自動建置靜態網站
- 使用 GitHub Pages 發佈
- 後續可接上 `stock.fushun181.com`

## 專案結構
- `src/`：Vue 前端程式
  - `src/App.vue`：簡易路由與頁面切換
  - `src/pages/`：首頁與課程頁
  - `src/components/`：Header / Footer 等共用元件
  - `src/data/`：課程 metadata 與 Markdown 匯入
  - `src/utils/`：Markdown 轉 HTML 工具
- `content/lessons/`：原始課程內容（Markdown）
- `assets/graphics/`：課程教學圖解 SVG
- `scripts/postbuild.mjs`：建置後複製靜態資源與產生 lesson 直連 fallback
- `scripts/publish_day.py`：單日課程更新後自動 build / commit / push
- `site/`：建置輸出（由 Vite 產生，不提交）
- `.github/workflows/`：GitHub Actions 部署流程

## 本地開發
```bash
npm install
npm run dev
```

## 本地建置
```bash
npm run build
```

建置完成後可查看：
- `site/index.html`
- `site/lessons/day-01.html`

> 注意：`/lessons/day-XX.html` 會由 `scripts/postbuild.mjs` 自動複製 Vue app shell，確保舊的課程直連網址仍可在 GitHub Pages 正常開啟。

## 自動發布單一課程
如果你剛寫完或改完某一天的課程，可以直接執行：
```bash
python3 scripts/publish_day.py 1
```

它會自動：
1. `npm run build`
2. `git add -A`
3. 建立 commit
4. push 到 `origin/main`

也可自訂訊息：
```bash
python3 scripts/publish_day.py 1 --message "Update Day 1 lesson"
```

## GitHub Pages
建議在 repo `Settings -> Pages`：
- Source 選 `GitHub Actions`
- Custom domain 之後填 `stock.fushun181.com`

## 下一步
- 補齊 Day 18 ~ Day 30
- 加入 glossary / 進度追蹤
- 接上每日自動更新流程
