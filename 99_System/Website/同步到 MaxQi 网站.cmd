@echo off
setlocal
cd /d C:\Users\MaxQ\.codex\.chatgpt-projects\g-p-68ad3b897c4881918fe538a8a5e598c7\maxqi-site
"C:\Program Files\nodejs\node.exe" scripts\sync-obsidian.mjs
echo.
if errorlevel 1 (
  echo 同步没有完成，请把上面的提示发给 Codex。
) else (
  echo 同步完成。现在可以打开 https://maxqi.com/admin/sync 检查并发布。
)
pause
