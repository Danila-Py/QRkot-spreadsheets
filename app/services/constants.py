# Аутентификация и пользователи
TOKEN_LIFETIME = 3600
MIN_PASSWORD_LENGTH = 3

# Проекты
MAX_PROJECT_NAME_LENGTH = 100
MIN_PROJECT_NAME_LENGTH = 1
MIN_DESCRIPTION_LENGTH = 1
MIN_INVESTED_AMOUNT = 0
DEFAULT_INVESTED_AMOUNT = 0

# Google Sheets
SPREADSHEET_HEADERS = [
    'Название проекта',
    'Время сбора',
    'Описание',
    'Собрано средств',
    'Дата закрытия'
]
SPREADSHEET_COLUMN_COUNT = 4
SPREADSHEET_HEADER_RANGE = 'A1:E1'
SPREADSHEET_HEADER_BACKGROUND = {
    'red': 0.9,
    'green': 0.9,
    'blue': 0.9
}
BASE_SCOPE = 'https://www.googleapis.com/auth/'

# Форматирование времени
SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60