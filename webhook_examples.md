# 🔗 Webhook API для автоматической проверки

## 📋 **Описание**

Бот теперь поддерживает автоматическую проверку регистрации и депозита через webhook POST запросы. Это позволяет интегрировать проверку с внешними системами.

## 🔐 **Безопасность**

- **Токен**: `topwinbot_secure_2024`
- **Обязательный заголовок**: `Content-Type: application/json`
- **Все запросы должны содержать токен**

## 📡 **Endpoints**

### **1. Проверка регистрации**

**URL**: `POST /`  
**Назначение**: Автоматическое подтверждение регистрации пользователя

**Пример запроса:**
```json
{
  "token": "topwinbot_secure_2024",
  "type": "registration",
  "user_id": 123456789,
  "account_id": "ACC123456"
}
```

**Ответ:**
```json
{
  "status": "processing",
  "type": "registration"
}
```

### **2. Проверка депозита**

**URL**: `POST /`  
**Назначение**: Автоматическое подтверждение депозита пользователя

**Пример запроса:**
```json
{
  "token": "topwinbot_secure_2024",
  "type": "deposit",
  "user_id": 123456789,
  "account_id": "ACC123456"
}
```

**Ответ:**
```json
{
  "status": "processing",
  "type": "deposit"
}
```

### **3. Проверка состояния**

**URL**: `GET /`  
**Назначение**: Проверка работоспособности сервера

**Ответ**: `Bot is running!`

## 🚀 **Как использовать**

### **cURL примеры:**

#### **Проверка регистрации:**
```bash
curl -X POST https://your-bot-url.onrender.com/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "topwinbot_secure_2024",
    "type": "registration",
    "user_id": 123456789,
    "account_id": "ACC123456"
  }'
```

#### **Проверка депозита:**
```bash
curl -X POST https://your-bot-url.onrender.com/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "topwinbot_secure_2024",
    "type": "deposit",
    "user_id": 123456789,
    "account_id": "ACC123456"
  }'
```

### **Python примеры:**

#### **Проверка регистрации:**
```python
import requests
import json

url = "https://your-bot-url.onrender.com/"
data = {
    "token": "topwinbot_secure_2024",
    "type": "registration",
    "user_id": 123456789,
    "account_id": "ACC123456"
}

response = requests.post(url, json=data)
print(response.json())
```

#### **Проверка депозита:**
```python
import requests
import json

url = "https://your-bot-url.onrender.com/"
data = {
    "token": "topwinbot_secure_2024",
    "type": "deposit",
    "user_id": 123456789,
    "account_id": "ACC123456"
}

response = requests.post(url, json=data)
print(response.json())
```

## ⚠️ **Важные моменты**

1. **user_id** - это Telegram ID пользователя (число)
2. **account_id** - это ID аккаунта на сайте 1win
3. **type** - тип проверки: `registration` или `deposit`
4. **token** - обязательный токен безопасности

## 🔄 **Автоматические действия**

### **При подтверждении регистрации:**
- ✅ Пользователь автоматически переходит к Шагу 2
- ✅ Отправляется сообщение с `2.jpeg` и текстом депозита
- ✅ Статус обновляется в системе

### **При подтверждении депозита:**
- ✅ Пользователь получает финальное сообщение успеха
- ✅ Отправляется сообщение с `3.jpeg` и текстом успеха
- ✅ Процесс завершается автоматически

## 🛡️ **Обработка ошибок**

- **401 Unauthorized** - неверный токен
- **400 Bad Request** - неверный формат данных
- **200 OK** - запрос обработан успешно

## 📱 **Интеграция с сайтом**

Теперь ваш сайт 1win может автоматически отправлять webhook запросы при:
- ✅ Успешной регистрации пользователя
- ✅ Успешном депозите пользователя

Это полностью автоматизирует процесс проверки! 🚀
