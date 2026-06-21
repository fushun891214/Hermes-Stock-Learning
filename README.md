# Hermes Stock Learning

台股新手學習網站專案。

## 目標
- 以 30 天課程方式學習台股基礎
- 使用 GitHub Actions 自動建置靜態網站
- 使用 GitHub Pages 發佈
- 後續可接上 `stock.fushun181.com`

## 專案結構
- `content/`：原始課程內容（Markdown）
- `templates/`：HTML 模板
- `assets/`：CSS、JS、圖片等靜態資源
- `scripts/`：建置腳本
- `site/`：建置輸出（由腳本產生）
- `.github/workflows/`：GitHub Actions

## 本地建置
```bash
python3 scripts/build.py
```

建置完成後可查看：
- `site/index.html`
- `site/lessons/day-01.html`

## 自動發布單一課程
如果你剛寫完或改完某一天的課程，可以直接執行：
```bash
python3 scripts/publish_day.py 1
```

它會自動：
1. rebuild 網站
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
- 補齊 Day 3 ~ Day 30
- 加入 glossary / 進度追蹤
- 接上每日自動更新流程
