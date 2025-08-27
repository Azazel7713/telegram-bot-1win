import os
from dotenv import load_dotenv

load_dotenv()

# Bot token
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Admin ID
ADMIN_ID = 5649983054

# Registration link
REGISTRATION_LINK = "https://1wksxo.life/?open=register&p=kj0h"

# Promo code
PROMO_CODE = "Topwinbot"

# Languages
LANGUAGES = {
    'az': '🇦🇿 Azərbaycan',
    'tr': '🇹🇷 Türk',
    'ru': '🇷🇺 Русский', 
    'en': '🇺🇸 English',
    'hi': '🇮🇳 हिंदी',
    'ur': '🇵🇰 اردو',
    'pt': '🇧🇷 Português',
    'de': '🇩🇪 Deutsch'
}

# Messages in different languages
MESSAGES = {
    'az': {
        'welcome': '🤖 Bot-a xoş gəlmisiniz!\n\n🚀 Daxili süni intellekt ilə təchiz edilmiş ƏN YAXŞI BOT!\n\n💎 Bu bot hesabınıza xüsusi proqram təqdim edir və 1win saytında sabit gəlir təmin edir.\n\n🧠 Layihə Reationale süni intellekti əsasında qurulub.\n\n💰 Qazanmağa başlayın!',
        'step1_title': '📝 Addım 1 - Qeydiyyatdan keçin',
        'step1_text': '🔗 Hesabınızı botumuzla sinxronlaşdırmaq üçün YENİ hesab qeydiyyatından keçməlisiniz.\n\n🎁 Qeydiyyat zamanı mütləq Topwinbot promokodunu daxil etməlisiniz, əks halda bot işləməyəcək!!!\n\n⚠️ Əgər linkə keçid edib köhnə hesaba düşürsünüzsə, ondan çıxmalı və linkə YENİDƏN keçid etməlisiniz!\n\n✅ Qeydiyyatı bitirdikdən sonra bota qayıdın.',
        'step2_title': '💳 Addım 2 - İlk depozit',
        'step2_text': '💰 İndi bot ilə inteqrasiya üçün istənilən məbləğdə ilk depozit etməlisiniz və yoxlama üçün ID-nizi göndərməlisiniz.\n\n🎯 Minimum məbləğ: 1₽\n\n⚡ Tez və təhlükəsiz!',
        'send_id': '🆔 Yoxlama üçün hesab ID-nizi göndərin\n\n📋 ID-nizi çata yapışdırın və göndərin',
        'registration_check': '✅ Qeydiyyat yoxlaması',
        'deposit_check': '💰 Depozit yoxlaması',
        'not_registered': '❌ Siz qeydiyyatdan keçməmisiniz\n\n🔄 Yenidən cəhd edin',
        'no_deposit': '❌ Siz depozit etməmisiniz\n\n💳 Depozit edib yenidən cəhd edin',
        'success': '🎉 Təbriklər! Siz bot ilə inteqrasiya üçün bütün məqamları keçdiniz!\n\n⏰ 24 saat ərzində menecermiz sizinlə əlaqə saxlayacaq və botunuzu quraşdıracaq.\n\n🚀 Uğurlar!',
        'next': '➡️ Davam et',
        'site_registration': '🌐 Sayt qeydiyyatı',
        'confirm': '✅ Təsdiq et',
        'reject': '❌ Rədd et',
        'id_sent': '✅ ID-niz göndərildi!\n\n⏳ Yoxlama gözləyir...\n\n📱 Tezliklə cavab alacaqsınız!',
        'back': '← Geri qayıt'
    },
    'tr': {
        'welcome': '🤖 Bota hoş geldiniz!\n\n🚀 Yerleşik yapay zeka ile donatılmış EN İYİ BOT!\n\n💎 Bu bot hesabınıza özel yazılım sağlar ve 1win sitesinde istikrarlı gelir sunar.\n\n🧠 Proje Reationale yapay zekası temelinde kurulmuştur.\n\n💰 Kazanmaya başlayın!',
        'step1_title': '📝 Adım 1 - Kayıt olun',
        'step1_text': '🔗 Hesabınızı botumuzla senkronize etmek için YENİ hesap kaydı yapmanız gerekiyor.\n\n🎁 Kayıt sırasında mutlaka Topwinbot promosyon kodunu girmeniz gerekiyor, aksi takdirde bot çalışmayacak!!!\n\n⚠️ Eğer linke geçiş yapıp eski hesaba düşüyorsanız, ondan çıkmalı ve linke YENİDEN geçiş yapmalısınız!\n\n✅ Kayıt tamamlandıktan sonra bota geri dönün.',
        'step2_title': '💳 Adım 2 - İlk depozit',
        'step2_text': '💰 Şimdi bot ile entegrasyon için herhangi bir miktarda ilk depozit yapmanız ve kontrol için ID\'nizi göndermeniz gerekiyor.\n\n🎯 Minimum miktar: 1₺\n\n⚡ Hızlı ve güvenli!',
        'send_id': '🆔 Kontrol için hesap ID\'nizi gönderin\n\n📋 ID\'nizi sohbete yapıştırın ve gönderin',
        'registration_check': '✅ Kayıt kontrolü',
        'deposit_check': '💰 Depozit kontrolü',
        'not_registered': '❌ Kayıt olmadınız\n\n🔄 Tekrar deneyin',
        'no_deposit': '❌ Depozit yapmadınız\n\n💳 Depozit yapıp tekrar deneyin',
        'success': '🎉 Tebrikler! Bot ile entegrasyon için tüm adımları geçtiniz!\n\n⏰ 24 saat içinde menajerimiz sizinle iletişime geçecek ve botunuzu kuracak.\n\n🚀 Başarılar!',
        'next': '➡️ Devam et',
        'site_registration': '🌐 Site kaydı',
        'confirm': '✅ Onayla',
        'reject': '❌ Reddet',
        'id_sent': '✅ ID\'niz gönderildi!\n\n⏳ Kontrol bekleniyor...\n\n📱 Yakında cevap alacaksınız!',
        'back': '← Geri dön'
    },
    'ru': {
        'welcome': '🤖 Добро пожаловать в бот!\n\n🚀 ЛУЧШИЙ БОТ со встроенным искусственным интеллектом!\n\n💎 Вписывает в ваш аккаунт специальный софт и дает стабильный доход на сайте 1win.\n\n🧠 Проект основан на искусственном интеллекте Reationale.\n\n💰 Начинайте зарабатывать!',
        'step1_title': '📝 Шаг 1 - Зарегистрируйся',
        'step1_text': '🔗 Для синхронизации вашего аккаунта с нашим ботом необходимо зарегистрировать НОВЫЙ аккаунт.\n\n🎁 Во время регистрации обязательно нужно ввести промокод Topwinbot иначе бот не заработает!!!\n\n⚠️ Если вы переходите по ссылке и попадаете на старый аккаунт, необходимо выйти из него и ЗАНОВО перейти по ссылке регистрации!\n\n✅ После завершения регистрации вернитесь в бот.',
        'step2_title': '💳 Шаг 2 - Первый депозит',
        'step2_text': '💰 Теперь для интеграции в боте вам нужно сделать первый депозит на любую сумму и отправить свой id для проверки.\n\n🎯 Минимальная сумма: 1₽\n\n⚡ Быстро и безопасно!',
        'send_id': '🆔 Отправьте свой id аккаунта на проверку\n\n📋 Вставьте id в чат и отправьте',
        'registration_check': '✅ Проверка регистрации',
        'deposit_check': '💰 Проверка депозита',
        'not_registered': '❌ Вы не зарегистрировались\n\n🔄 Попробуйте снова',
        'no_deposit': '❌ Вы не сделали депозит\n\n💳 Сделайте депозит и попробуйте снова',
        'success': '🎉 Поздравляем! Вы прошли все пункты для интеграции с ботом!\n\n⏰ В течение 24 часов с вами свяжется наш менеджер и настроит вам бота.\n\n🚀 Удачи!',
        'next': '➡️ Дальше',
        'site_registration': '🌐 Сайт регистрации',
        'confirm': '✅ Подтвердить',
        'reject': '❌ Отказать',
        'id_sent': '✅ Ваш ID отправлен!\n\n⏳ Ожидается проверка...\n\n📱 Скоро получите ответ!',
        'back': '← Назад'
    },
    'en': {
        'welcome': '🤖 Welcome to the bot!\n\n🚀 THE BEST BOT with built-in artificial intelligence!\n\n💎 Integrates special software into your account and provides stable income on the 1win site.\n\n🧠 The project is based on Reationale artificial intelligence.\n\n💰 Start earning!',
        'step1_title': '📝 Step 1 - Register',
        'step1_text': '🔗 To synchronize your account with our bot, you need to register a NEW account.\n\n🎁 During registration, you must enter the Topwinbot promo code, otherwise the bot will not work!!!\n\n⚠️ If you follow the link and end up on an old account, you need to log out and go through the registration link AGAIN!\n\n✅ After completing registration, return to the bot.',
        'step2_title': '💳 Step 2 - First deposit',
        'step2_text': '💰 Now for integration in the bot you need to make a first deposit of any amount and send your id for verification.\n\n🎯 Minimum amount: $1\n\n⚡ Fast and secure!',
        'send_id': '🆔 Send your account id for verification\n\n📋 Paste id in chat and send',
        'registration_check': '✅ Registration check',
        'deposit_check': '💰 Deposit check',
        'not_registered': '❌ You have not registered\n\n🔄 Try again',
        'no_deposit': '❌ You have not made a deposit\n\n💳 Make a deposit and try again',
        'success': '🎉 Congratulations! You have passed all points for integration with the bot!\n\n⏰ Within 24 hours our manager will contact you and set up your bot.\n\n🚀 Good luck!',
        'next': '➡️ Next',
        'site_registration': '🌐 Site registration',
        'confirm': '✅ Confirm',
        'reject': '❌ Reject',
        'id_sent': '✅ Your ID has been sent!\n\n⏳ Verification pending...\n\n📱 You will receive a response soon!',
        'back': '← Back'
    },
    'hi': {
        'welcome': '🤖 बॉट में आपका स्वागत है!\n\n🚀 अंतर्निहित कृत्रिम बुद्धिमत्ता के साथ सर्वश्रेष्ठ बॉट!\n\n💎 आपके खाते में विशेष सॉफ्टवेयर एकीकृत करता है और 1win साइट पर स्थिर आय प्रदान करता है।\n\n🧠 प्रोजेक्ट Reationale कृत्रिम बुद्धिमत्ता पर आधारित है।\n\n💰 कमाई शुरू करें!',
        'step1_title': '📝 चरण 1 - पंजीकरण करें',
        'step1_text': '🔗 अपने खाते को हमारे बॉट के साथ सिंक्रनाइज़ करने के लिए, आपको एक नया खाता पंजीकृत करना होगा।\n\n🎁 पंजीकरण के दौरान, आपको Topwinbot प्रोमो कोड दर्ज करना होगा, अन्यथा बॉट काम नहीं करेगा!!!\n\n⚠️ यदि आप लिंक का अनुसरण करते हैं और पुराने खाते में समाप्त होते हैं, तो आपको लॉग आउट करना होगा और पंजीकरण लिंक से फिर से गुजरना होगा!\n\n✅ पंजीकरण पूरा करने के बाद, बॉट पर वापस लौटें।',
        'step2_title': '💳 चरण 2 - पहला जमा',
        'step2_text': '💰 अब बॉट में एकीकरण के लिए आपको किसी भी राशि का पहला जमा करना होगा और सत्यापन के लिए अपना आईडी भेजना होगा।\n\n🎯 न्यूनतम राशि: ₹1\n\n⚡ तेज और सुरक्षित!',
        'send_id': '🆔 सत्यापन के लिए अपना खाता आईडी भेजें\n\n📋 चैट में आईडी पेस्ट करें और भेजें',
        'registration_check': '✅ पंजीकरण जांच',
        'deposit_check': '💰 जमा जांच',
        'not_registered': '❌ आपने पंजीकरण नहीं किया है\n\n🔄 फिर से कोशिश करें',
        'no_deposit': '❌ आपने जमा नहीं किया है\n\n💳 जमा करके फिर से कोशिश करें',
        'success': '🎉 बधाई हो! आपने बॉट के साथ एकीकरण के लिए सभी बिंदुओं को पार कर लिया है!\n\n⏰ 24 घंटों के भीतर हमारा प्रबंधक आपसे संपर्क करेगा और आपके बॉट को सेट करेगा।\n\n🚀 शुभकामनाएं!',
        'next': '➡️ अगला',
        'site_registration': '🌐 साइट पंजीकरण',
        'confirm': '✅ पुष्टि करें',
        'reject': '❌ अस्वीकार करें',
        'id_sent': '✅ आपका ID भेज दिया गया है!\n\n⏳ सत्यापन लंबित...\n\n📱 आपको जल्द ही जवाब मिलेगा!',
        'back': '← वापस'
    },
    'ur': {
        'welcome': '🤖 بلٹ ان مصنوعی ذہانت کے ساتھ بوٹ میں خوش آمدید!\n\n🚀 آپ کے اکاؤنٹ میں خصوصی سافٹ ویئر کو مربوط کرنے والا بہترین بوٹ!\n\n💎 1win سائٹ پر مستحکم آمدنی فراہم کرتا ہے۔\n\n🧠 پروجیکٹ Reationale مصنوعی ذہانت پر مبنی ہے۔\n\n💰 کمائی شروع کریں!',
        'step1_title': '📝 مرحلہ 1 - رجسٹر کریں',
        'step1_text': '🔗 اپنے اکاؤنٹ کو ہمارے بوٹ کے ساتھ ہم آہنگ کرنے کے لیے، آپ کو ایک نیا اکاؤنٹ رجسٹر کرنا ہوگا۔\n\n🎁 رجسٹریشن کے دوران، آپ کو Topwinbot پرومو کوڈ درج کرنا ہوگا، ورنہ بوٹ کام نہیں کرے گا!!!\n\n⚠️ اگر آپ لنک پر جاتے ہیں اور پرانے اکاؤنٹ میں ختم ہوتے ہیں، تو آپ کو لاگ آؤٹ کرنا ہوگا اور رجسٹریشن لنک سے دوبارہ گزرنا ہوگا!\n\n✅ رجسٹریشن مکمل کرنے کے بعد، بوٹ پر واپس جائیں۔',
        'step2_title': '💳 مرحلہ 2 - پہلی جمع',
        'step2_text': '💰 اب بوٹ میں انضمام کے لیے آپ کو کسی بھی رقم کی پہلی جمع کرنی ہوگی اور تصدیق کے لیے اپنا آئی ڈی بھیجنا ہوگا۔\n\n🎯 کم از کم رقم: ₨1\n\n⚡ تیز اور محفوظ!',
        'send_id': '🆔 تصدیق کے لیے اپنا اکاؤنٹ آئی ڈی بھیجیں\n\n📋 چیٹ میں آئی ڈی پیسٹ کریں اور بھیجیں',
        'registration_check': '✅ رجسٹریشن چیک',
        'deposit_check': '💰 جمع چیک',
        'not_registered': '❌ آپ نے رجسٹر نہیں کیا ہے\n\n🔄 دوبارہ کوشش کریں',
        'no_deposit': '❌ آپ نے جمع نہیں کیا ہے\n\n💳 جمع کر کے دوبارہ کوشش کریں',
        'success': '🎉 مبارک ہو! آپ نے بوٹ کے ساتھ انضمام کے لیے تمام نکات پاس کر لیے ہیں!\n\n⏰ 24 گھنٹوں کے اندر ہمارا مینیجر آپ سے رابطہ کرے گا اور آپ کے بوٹ کو سیٹ کرے گا۔\n\n🚀 نیک خواہشات!',
        'next': '➡️ اگلا',
        'site_registration': '🌐 سائٹ رجسٹریشن',
        'confirm': '✅ تصدیق کریں',
        'reject': '❌ مسترد کریں',
        'id_sent': '✅ آپ کا ID بھیج دیا گیا ہے!\n\n⏳ تصدیق زیر التوا...\n\n📱 آپ کو جلد ہی جواب ملے گا!',
        'back': '← واپس'
    },
    'pt': {
        'welcome': '🤖 Bem-vindo ao bot!\n\n🚀 O MELHOR BOT com inteligência artificial integrada!\n\n💎 Integra software especial em sua conta e fornece renda estável no site 1win.\n\n🧠 O projeto é baseado na inteligência artificial Reationale.\n\n💰 Comece a ganhar!',
        'step1_title': '📝 Passo 1 - Registre-se',
        'step1_text': '🔗 Para sincronizar sua conta com nosso bot, você precisa registrar uma NOVA conta.\n\n🎁 Durante o registro, você deve inserir o código promocional Topwinbot, caso contrário o bot não funcionará!!!\n\n⚠️ Se você seguir o link e acabar em uma conta antiga, você precisa fazer logout e passar pelo link de registro NOVAMENTE!\n\n✅ Após completar o registro, retorne ao bot.',
        'step2_title': '💳 Passo 2 - Primeiro depósito',
        'step2_text': '💰 Agora para integração no bot você precisa fazer um primeiro depósito de qualquer valor e enviar seu id para verificação.\n\n🎯 Valor mínimo: R$1\n\n⚡ Rápido e seguro!',
        'send_id': '🆔 Envie seu id da conta para verificação\n\n📋 Cole o id no chat e envie',
        'registration_check': '✅ Verificação de registro',
        'deposit_check': '💰 Verificação de depósito',
        'not_registered': '❌ Você não se registrou\n\n🔄 Tente novamente',
        'no_deposit': '❌ Você não fez depósito\n\n💳 Faça um depósito e tente novamente',
        'success': '🎉 Parabéns! Você passou por todos os pontos para integração com o bot!\n\n⏰ Dentro de 24 horas nosso gerente entrará em contato com você e configurará seu bot.\n\n🚀 Boa sorte!',
        'next': '➡️ Próximo',
        'site_registration': '🌐 Registro do site',
        'confirm': '✅ Confirmar',
        'reject': '❌ Rejeitar',
        'id_sent': '✅ Seu ID foi enviado!\n\n⏳ Verificação pendente...\n\n📱 Você receberá uma resposta em breve!',
        'back': '← Voltar'
    },
    'de': {
        'welcome': '🤖 Willkommen beim Bot!\n\n🚀 DER BESTE BOT mit integrierter künstlicher Intelligenz!\n\n💎 Integriert spezielle Software in Ihr Konto und bietet stabile Einnahmen auf der 1win-Website.\n\n🧠 Das Projekt basiert auf Reationale künstlicher Intelligenz.\n\n💰 Beginnen Sie zu verdienen!',
        'step1_title': '📝 Schritt 1 - Registrieren',
        'step1_text': '🔗 Um Ihr Konto mit unserem Bot zu synchronisieren, müssen Sie ein NEUES Konto registrieren.\n\n🎁 Während der Registrierung müssen Sie den Topwinbot-Promocode eingeben, sonst funktioniert der Bot nicht!!!\n\n⚠️ Wenn Sie dem Link folgen und auf einem alten Konto landen, müssen Sie sich abmelden und den Registrierungslink ERNEUT durchgehen!\n\n✅ Nach Abschluss der Registrierung kehren Sie zum Bot zurück.',
        'step2_title': '💳 Schritt 2 - Erste Einzahlung',
        'step2_text': '💰 Jetzt für die Integration im Bot müssen Sie eine erste Einzahlung in beliebiger Höhe tätigen und Ihre ID zur Überprüfung senden.\n\n🎯 Mindestbetrag: 1€\n\n⚡ Schnell und sicher!',
        'send_id': '🆔 Senden Sie Ihre Konto-ID zur Überprüfung\n\n📋 Fügen Sie die ID in den Chat ein und senden Sie',
        'registration_check': '✅ Registrierungsprüfung',
        'deposit_check': '💰 Einzahlungsprüfung',
        'not_registered': '❌ Sie haben sich nicht registriert\n\n🔄 Versuchen Sie es erneut',
        'no_deposit': '❌ Sie haben keine Einzahlung getätigt\n\n💳 Tätigen Sie eine Einzahlung und versuchen Sie es erneut',
        'success': '🎉 Glückwunsch! Sie haben alle Punkte für die Integration mit dem Bot bestanden!\n\n⏰ Innerhalb von 24 Stunden wird sich unser Manager bei Ihnen melden und Ihren Bot einrichten.\n\n🚀 Viel Glück!',
        'next': '➡️ Weiter',
        'site_registration': '🌐 Website-Registrierung',
        'confirm': '✅ Bestätigen',
        'reject': '❌ Ablehnen',
        'id_sent': '✅ Ihre ID wurde gesendet!\n\n⏳ Überprüfung ausstehend...\n\n📱 Sie erhalten bald eine Antwort!',
        'back': '← Zurück'
    }
}
