# Telegram Bot с автооплатой через Kaspi Pay

<div align="center">

![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue?logo=telegram)
![Kaspi Pay](https://img.shields.io/badge/Payment-Kaspi%20Pay-red)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

<p align="center">
  <img src="https://via.placeholder.com/600x300?text=Kaspi+Course+Bot" alt="Kaspi Course Bot Demo" width="600">
</p>

## 📋 Обзор

Бот для Telegram с возможностью подключения платежной системы Kaspi Pay, поэтапным открытием уроков и отслеживанием прогресса студентов.

## ✨ Особенности

<div align="center">

| 🔄 | 📚 | 📊 | 🛠️ |
|:---:|:---:|:---:|:---:|
| **Автоматические платежи** через Kaspi Pay | **Поэтапное открытие уроков** после выполнения заданий | **Система отслеживания прогресса** учеников | **MVC архитектура** для удобного расширения |

</div>

## 🛠️ Стек технологий

<table align="center">
  <tr>
    <td align="center"><img src="https://via.placeholder.com/50?text=Python" width="50"/><br>Python 3.8+</td>
    <td align="center"><img src="https://via.placeholder.com/50?text=aiogram" width="50"/><br>aiogram</td>
    <td align="center"><img src="https://via.placeholder.com/50?text=SQLite" width="50"/><br>SQLite</td>
    <td align="center"><img src="https://via.placeholder.com/50?text=aiohttp" width="50"/><br>aiohttp</td>
    <td align="center"><img src="https://via.placeholder.com/50?text=Kaspi" width="50"/><br>Kaspi Pay API</td>
  </tr>
</table>

## 🚀 Установка и запуск

### Предварительные требования

- Python 3.8 или выше
- [Telegram Bot Token](https://core.telegram.org/bots#3-how-do-i-create-a-bot) от @BotFather
- Аккаунт в системе Kaspi Pay и API-ключи (для работы с платежами)

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/yourusername/kaspi-course-bot.git
cd kaspi-course-bot
```

### Шаг 2: Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
# или
venv\Scripts\activate  # Для Windows
```

### Шаг 3: Установка зависимостей

```bash
pip install -r requirements.txt
```

### Шаг 4: Настройка конфигурации

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте файл `.env` и добавьте необходимые параметры:

```ini
TELEGRAM_BOT_TOKEN=ваш_телеграм_токен
KASPI_API_KEY=ваш_ключ_kaspi_api
KASPI_MERCHANT_ID=ваш_id_мерчанта_kaspi
```

### Шаг 5: Запуск бота

```bash
python run.py
```

## 🛠️ Режимы работы

Бот может работать в двух режимах:

<table>
  <tr>
    <th>Режим</th>
    <th>Описание</th>
    <th>Настройка</th>
  </tr>
  <tr>
    <td><strong>polling</strong></td>
    <td>Для разработки</td>
    <td>Указан по умолчанию в <code>.env.example</code></td>
  </tr>
  <tr>
    <td><strong>webhook</strong></td>
    <td>Для продакшн</td>
    <td>Требует SSL-сертификат</td>
  </tr>
</table>

Для запуска в режиме webhook добавьте в `.env` файл:

```ini
DEVELOPMENT_MODE=webhook
WEBHOOK_HOST=example.com
WEBHOOK_PORT=8443
WEBHOOK_SSL_CERT=путь_к_ssl_сертификату
WEBHOOK_SSL_PRIV=путь_к_ssl_ключу
```

## ☁️ Деплой на Heroku

```bash
heroku create
git push heroku main
heroku ps:scale web=1
```

## 📂 Структура проекта

```
kaspi_course_bot/
│
├── init.py                 # Инициализация приложения
├── run.py                  # Точка входа
├── requirements.txt        # Зависимости проекта
├── Procfile                # Инструкции для Heroku
│
├── config/                 # Конфигурации
│   └── settings.py         # Настройки из переменных окружения
│
├── models/                 # Модели для работы с данными
│   ├── base.py             # Базовый класс для моделей
│   ├── lesson.py           # Модель урока
│   ├── payment.py          # Модель платежа
│   └── user.py             # Модель пользователя
│
├── controllers/            # Контроллеры для обработки запросов
│   ├── payment_controller.py
│   ├── lesson_controller.py
│   └── user_controller.py
│
├── views/                  # Представления для взаимодействия с пользователем
│   ├── keyboards.py        # Клавиатуры бота
│   └── messages.py         # Шаблоны сообщений
│
├── services/               # Сервисы для бизнес-логики
│   ├── database.py         # Сервис для работы с БД
│   ├── kaspi_service.py    # Сервис для работы с Kaspi API
│   └── bot_service.py      # Сервис для работы с Telegram API
│
├── tests/                  # Тесты
│   ├── conftest.py         # Фикстуры для тестов
│   ├── test_payment.py     # Тесты платежей
│   ├── test_lessons.py     # Тесты уроков
│   └── test_user.py        # Тесты пользователей
│
└── db/                     # Файлы базы данных и миграции
    ├── migrations/         # SQL-скрипты для миграций
    └── seeds/              # Данные для заполнения БД
```

## 🧪 Запуск тестов

```bash
pytest
```

Для запуска с отчетом о покрытии:

```bash
pytest --cov=.
```

## 🔧 Кастомизация контента

Для изменения учебных материалов отредактируйте тестовые данные в `services/database.py` в функции `seed_test_data()`.

## 💲 Интеграция с Kaspi Pay

<div align="center">

| Шаг | Описание |
|:---:|:---|
| 1️⃣ | Получите API-ключи и ID мерчанта в личном кабинете Kaspi Pay |
| 2️⃣ | Настройте webhook для получения уведомлений о платежах (URL: `/webhook/kaspi`) |
| 3️⃣ | Замените URL перенаправления в `services/kaspi_service.py` на ссылку на вашего бота |

</div>

## 🔒 Безопасность

⚠️ **Важно:** Данный репозиторий является демонстрационным примером. Для использования в продакшн необходимо:

<table>
  <tr>
    <td>🔐</td>
    <td>Дополнительно защитить API-ключи</td>
  </tr>
  <tr>
    <td>✅</td>
    <td>Добавить валидацию платежей на стороне сервера</td>
  </tr>
  <tr>
    <td>🔒</td>
    <td>Настроить SSL для webhook-ов</td>
  </tr>
  <tr>
    <td>💾</td>
    <td>Использовать более безопасную базу данных (PostgreSQL, MySQL)</td>
  </tr>
</table>

## 🤝 Вклад в проект

Вклады приветствуются! Если у вас есть идеи или предложения:

1. Сделайте форк проекта
2. Создайте ветку с вашей фичей (`git checkout -b feature/amazing-feature`)
3. Создайте коммит с изменениями (`git commit -m 'Добавлена новая фича'`)
4. Отправьте изменения в ваш форк (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности в файле [LICENSE](LICENSE).

## 📞 Контакты

<div align="center">
  
  [![GitHub](https://img.shields.io/badge/GitHub-yourusername-181717?logo=github&style=for-the-badge)](https://github.com/yourusername)
  [![Email](https://img.shields.io/badge/Email-email%40example.com-D14836?logo=gmail&style=for-the-badge)](mailto:email@example.com)
  [![Telegram](https://img.shields.io/badge/Telegram-username-2CA5E0?logo=telegram&style=for-the-badge)](https://t.me/username)

</div>

---

<div align="center">
  
  ⭐ Не забудьте поставить звезду, если проект вам понравился! ⭐

</div>
