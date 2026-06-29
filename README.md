# Attack-Protection-services-for-donguCTF
Написанные мной сервисы для проведения A/D для donguCTF


#Пояснение к serv4 (к другим сервисам как их запустить пояснение не нужно): 
## Настройка Google Sheets
### 1. Создай сервисный аккаунт в Google Cloud:
- Перейди в [Google Cloud Console](https://console.cloud.google.com/)
- Создай новый проект или выбери существующий
- Включи **Google Sheets API**
- Перейди в **IAM & Admin → Service Accounts**
- Создай новый сервисный аккаунт
- Скачай JSON-ключ

### 2. Заполни config.php:
Открой скачанный JSON-файл и скопируй данные:
- `client_email` → в `SERVICE_ACCOUNT_EMAIL`
- `private_key` → в `$private_key` (весь ключ целиком!)
- ID таблицы → в `SPREADSHEET_ID` (из URL таблицы)

### 3. Дай доступ сервисному аккаунту:
- Открой Google Sheets таблицу
- Нажми "Поделиться"
- Добавь email сервисного аккаунта (client_email)
- Дай права "Редактор"

### 4. Если данные не заполнены:
Скрипт автоматически переключится в локальный режим и будет сохранять данные в папку `data/`
