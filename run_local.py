#!/usr/bin/env python3
"""
Yerli test üçün bot başlatma scripti
"""

import os
import sys
from dotenv import load_dotenv

def check_requirements():
    """Tələbləri yoxlayır"""
    print("🔍 Tələbləri yoxlayır...")
    
    # .env faylını yoxlayır
    if not os.path.exists('.env'):
        print("❌ .env faylı tapılmadı!")
        print("📝 .env faylı yaradın və BOT_TOKEN əlavə edin:")
        print("BOT_TOKEN=your_bot_token_here")
        return False
    
    # Şəkilləri yoxlayır
    required_images = ['start.jpeg', '1.jpeg', '2.jpeg', '3.jpeg']
    missing_images = []
    
    for image in required_images:
        if not os.path.exists(image):
            missing_images.append(image)
    
    if missing_images:
        print(f"❌ Bu şəkillər tapılmadı: {', '.join(missing_images)}")
        print("📁 Şəkilləri layihə qovluğuna yükləyin")
        return False
    
    print("✅ Bütün tələblər qarşılanır!")
    return True

def main():
    """Əsas funksiya"""
    print("🤖 Telegram Avtovoronka Bot - Yerli Test")
    print("=" * 50)
    
    # Tələbləri yoxlayır
    if not check_requirements():
        print("\n❌ Quraşdırma tamamlanmayıb!")
        sys.exit(1)
    
    # Environment dəyişənlərini yükləyir
    load_dotenv()
    
    # Bot tokenini yoxlayır
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token or bot_token == 'your_bot_token_here':
        print("❌ BOT_TOKEN düzgün təyin edilməyib!")
        print("📝 .env faylında düzgün token yazın")
        sys.exit(1)
    
    print("✅ Bot tokeni tapıldı!")
    print("\n🚀 Botu başladırır...")
    print("📱 Telegram-da botunuzu tapın və /start yazın")
    print("⏹️  Dayandırmaq üçün Ctrl+C basın")
    
    try:
        # Botu başladır
        from bot import main as run_bot
        run_bot()
    except KeyboardInterrupt:
        print("\n👋 Bot dayandırıldı!")
    except Exception as e:
        print(f"\n❌ Xəta: {e}")
        print("🔧 Konfiqurasiyanı yoxlayın")

if __name__ == '__main__':
    main()
