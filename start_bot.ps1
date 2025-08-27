# PowerShell скрипт для безопасного запуска Telegram бота

Write-Host "🤖 Останавливаем все процессы Python..." -ForegroundColor Yellow

# Останавливаем все процессы Python
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

Write-Host "✅ Все процессы Python остановлены" -ForegroundColor Green

# Ждем немного
Start-Sleep -Seconds 2

Write-Host "🚀 Запускаем бота..." -ForegroundColor Green

# Запускаем бота
python bot.py
