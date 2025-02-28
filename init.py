from aiohttp import web
from aiogram import Bot, Dispatcher

from config.settings import TELEGRAM_BOT_TOKEN
from services.bot_service import dp, bot, setup_handlers
from services.database import init_database
from controllers.payment_controller import setup_webhook_handler

def create_app() -> web.Application:
    """
    Создает и настраивает экземпляр приложения
    
    Returns:
        Application: Экземпляр приложения aiohttp
    """
    # Создаем экземпляр приложения
    app = web.Application()
    
    # Инициализируем базу данных
    init_database()
    
    # Настраиваем обработчики
    setup_handlers()
    
    # Сохраняем экземпляры бота и диспетчера в приложении
    app['bot'] = bot
    app['dp'] = dp
    
    # Настраиваем маршруты для webhooks
    setup_webhook_routes(app)
    
    return app

def setup_webhook_routes(app: web.Application) -> None:
    """
    Настраивает маршруты для webhook-ов
    
    Args:
        app: Экземпляр приложения
    """
    # Маршрут для webhook Telegram
    app.router.add_post(f'/webhook/{TELEGRAM_BOT_TOKEN}', lambda request: process_telegram_update(request, dp))
    
    # Маршрут для webhook Kaspi Pay
    app.router.add_post('/webhook/kaspi', setup_webhook_handler())

async def process_telegram_update(request: web.Request, dp: Dispatcher) -> web.Response:
    """
    Обрабатывает обновления от Telegram
    
    Args:
        request: Запрос от Telegram
        dp: Диспетчер бота
        
    Returns:
        Response: Ответ сервера
    """
    # Получаем данные из запроса
    data = await request.json()
    
    # Обрабатываем обновление через aiogram
    await dp.process_update(data)
    
    # Возвращаем успешный ответ
    return web.Response(text='OK')