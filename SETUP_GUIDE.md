# Telegram Bot Quraşdırma Təlimatları

## 1. Bot Tokenini Alın

1. Telegram-da @BotFather-a yazın
2. `/newbot` əmrini göndərin
3. Bot adını daxil edin (məsələn: "1win Avtovoronka Bot")
4. Bot username-i daxil edin (məsələn: "onewin_voronka_bot")
5. Tokeni kopyalayın və saxlayın

## 2. Environment Faylı Yaradın

`.env` faylı yaradın və bot tokenini əlavə edin:

```
BOT_TOKEN=your_bot_token_here
```

## 3. Şəkilləri Yükləyin

Layihə qovluğuna bu şəkilləri yükləyin:
- `start.jpeg` - başlanğıc şəkli
- `1.jpeg` - addım 1 şəkli
- `2.jpeg` - addım 2 şəkli
- `3.jpeg` - uğurlu tamamlama şəkli

## 4. GitHub-a Yükləyin

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin your_repo_url
git push -u origin main
```

## 5. Render-də Yerləşdirin

1. render.com-a daxil olun
2. "New Web Service" seçin
3. GitHub repository-nizi birləşdirin
4. Environment variables əlavə edin:
   - Key: `BOT_TOKEN`
   - Value: Bot tokeniniz
5. "Create Web Service" basın

## 6. Botu Test Edin

1. Telegram-da botunuzu tapın
2. `/start` əmrini göndərin
3. Dil seçin və test edin

## Xəta Həlli

Əgər xəta alırsınızsa:
- Bot tokeninin düzgün olduğunu yoxlayın
- Şəkillərin düzgün adlandırıldığını yoxlayın
- Render loglarını yoxlayın
