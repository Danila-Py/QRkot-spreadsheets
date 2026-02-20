# Кошачий благотворительный фонд
Сервис для поддержки котиков! Благотворительная платформа, позволяющая пользователям делать пожертвования на поддержание кошачьей преступности.

## Функциональность

- Аутентификация и авторизация пользователей (JWT)

- Разделение прав доступа (обычные пользователи и суперпользователи)

- Создание и управление благотворительными проектами (для администратора)

- Возможность делать пожертвования

- Автоматическое распределение средств между проектами

- **Формирование отчетов в Google Таблицах** (для администратора)

## Установка

Клонируйте репозиторий:

```
git clone
```

Создайте файл .env в корневой директории со следующим содержимым:

```
# Настройки Google Cloud (данные из json сервисного аккаунта)
TYPE=service_account
PROJECT_ID=your-project-id
PRIVATE_KEY_ID=your-private-key-id
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nМНОГО_СИМВОЛОВ\n-----END PRIVATE KEY-----\n"
CLIENT_EMAIL=your-service-account@project.iam.gserviceaccount.com
CLIENT_ID=your-client-id
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40project.iam.gserviceaccount.com
EMAIL=your-personal-email@gmail.com

# ID предварительно созданной Google таблицы
SPREADSHEET_ID=your_google_sheets_id
```

Создайте виртуальное окружение и активируйте его:

```
python -m venv .venv
source venv/Scripts/activate # Windows
```

Установите зависимости:

```
pip install -r requirements.txt
```

Примените миграции:

```
alembic upgrade heads
```

Запустите приложение:

```
uvicorn app.main:app --reload
```