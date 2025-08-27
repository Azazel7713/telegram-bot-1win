# Telegram Bot Quraşdırma Scripti
Write-Host "🤖 Telegram Avtovoronka Bot Quraşdırması" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Python yoxlayır
Write-Host "🔍 Python yoxlanılır..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ $pythonVersion tapıldı" -ForegroundColor Green
} catch {
    Write-Host "❌ Python tapılmadı!" -ForegroundColor Red
    Write-Host "📥 Python-u yükləyin: https://python.org" -ForegroundColor Yellow
    exit 1
}

# Pip yoxlayır
Write-Host "🔍 Pip yoxlanılır..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version
    Write-Host "✅ $pipVersion tapıldı" -ForegroundColor Green
} catch {
    Write-Host "❌ Pip tapılmadı!" -ForegroundColor Red
    exit 1
}

# Tələbləri yükləyir
Write-Host "📦 Tələblər yüklənir..." -ForegroundColor Yellow
try {
    pip install -r requirements.txt
    Write-Host "✅ Tələblər yükləndi" -ForegroundColor Green
} catch {
    Write-Host "❌ Tələblər yüklənə bilmədi!" -ForegroundColor Red
    exit 1
}

# .env faylını yoxlayır
Write-Host "🔍 .env faylı yoxlanılır..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ .env faylı mövcuddur" -ForegroundColor Green
} else {
    Write-Host "📝 .env faylı yaradılır..." -ForegroundColor Yellow
    "BOT_TOKEN=your_bot_token_here" | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ .env faylı yaradıldı" -ForegroundColor Green
    Write-Host "⚠️  Zəhmət olmasa .env faylında BOT_TOKEN-i düzəldin" -ForegroundColor Yellow
}

# Şəkilləri yoxlayır
Write-Host "🔍 Şəkillər yoxlanılır..." -ForegroundColor Yellow
$requiredImages = @("start.jpeg", "1.jpeg", "2.jpeg", "3.jpeg")
$missingImages = @()

foreach ($image in $requiredImages) {
    if (Test-Path $image) {
        Write-Host "✅ $image tapıldı" -ForegroundColor Green
    } else {
        Write-Host "❌ $image tapılmadı" -ForegroundColor Red
        $missingImages += $image
    }
}

if ($missingImages.Count -gt 0) {
    Write-Host "⚠️  Bu şəkillər yüklənməli: $($missingImages -join ', ')" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 Quraşdırma tamamlandı!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Növbəti addımlar:" -ForegroundColor Cyan
Write-Host "1. @BotFather-dən bot tokenini alın" -ForegroundColor White
Write-Host "2. .env faylında BOT_TOKEN-i düzəldin" -ForegroundColor White
Write-Host "3. Şəkilləri yükləyin (əgər yoxdursa)" -ForegroundColor White
Write-Host "4. python run_local.py əmrini işə salın" -ForegroundColor White
Write-Host ""
Write-Host "🚀 Botu başlatmaq üçün: python run_local.py" -ForegroundColor Green
