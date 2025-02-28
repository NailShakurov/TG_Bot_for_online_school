import pytest
from datetime import datetime

from models.user import User
from models.lesson import Lesson, UserLesson

class TestUserModel:
    """Тесты для модели пользователя"""
    
    def test_user_create(self, mock_db_connection):
        """Тест создания нового пользователя"""
        # Создаем нового пользователя
        user = User(
            user_id=987654321,
            username="newuser",
            full_name="New User"
        )
        
        # Сохраняем в БД
        assert user.save() is True
        
        # Извлекаем и проверяем
        loaded_user = User.find_by_id(987654321)
        assert loaded_user is not None
        assert loaded_user.user_id == 987654321
        assert loaded_user.username == "newuser"
        assert loaded_user.full_name == "New User"
    
    def test_user_register(self, mock_db_connection):
        """Тест метода регистрации пользователя"""
        # Регистрируем нового пользователя
        user = User.register