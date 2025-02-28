import sqlite3
from typing import Dict, List, Any, Optional, Tuple, Type, TypeVar, Generic
from datetime import datetime

from services.database import get_db_connection

T = TypeVar('T', bound='BaseModel')

class BaseModel:
    """Базовый класс для всех моделей приложения"""
    
    table_name: str = ""
    primary_key: str = "id"
    
    # Схема таблицы в формате {имя_колонки: тип}
    schema: Dict[str, str] = {}
    
    def __init__(self, **kwargs):
        """Инициализация модели с атрибутами"""
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    @classmethod
    def create_table(cls) -> None:
        """Создает таблицу в БД на основе схемы"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        fields = []
        for field_name, field_type in cls.schema.items():
            field_def = f"{field_name} {field_type}"
            if field_name == cls.primary_key:
                field_def += " PRIMARY KEY"
            fields.append(field_def)
        
        query = f"CREATE TABLE IF NOT EXISTS {cls.table_name} ({', '.join(fields)})"
        cursor.execute(query)
        conn.commit()
        conn.close()
    
    @classmethod
    def find_by_id(cls: Type[T], id_value: Any) -> Optional[T]:
        """Поиск записи по первичному ключу"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = f"SELECT * FROM {cls.table_name} WHERE {cls.primary_key} = ?"
        cursor.execute(query, (id_value,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Создаем словарь с именами колонок и их значениями
            columns = [column[0] for column in cursor.description]
            record = {columns[i]: row[i] for i in range(len(columns))}
            return cls(**record)
        return None
    
    @classmethod
    def find_one(cls: Type[T], conditions: Dict[str, Any]) -> Optional[T]:
        """Поиск одной записи по условию"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        where_clauses = []
        values = []
        
        for key, value in conditions.items():
            where_clauses.append(f"{key} = ?")
            values.append(value)
        
        where_str = " AND ".join(where_clauses)
        query = f"SELECT * FROM {cls.table_name} WHERE {where_str} LIMIT 1"
        
        cursor.execute(query, tuple(values))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [column[0] for column in cursor.description]
            record = {columns[i]: row[i] for i in range(len(columns))}
            return cls(**record)
        return None
    
    @classmethod
    def find_all(cls: Type[T], conditions: Optional[Dict[str, Any]] = None, 
                order_by: Optional[str] = None, limit: Optional[int] = None) -> List[T]:
        """Поиск всех записей, удовлетворяющих условию"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = f"SELECT * FROM {cls.table_name}"
        values = []
        
        if conditions:
            where_clauses = []
            for key, value in conditions.items():
                where_clauses.append(f"{key} = ?")
                values.append(value)
            
            where_str = " AND ".join(where_clauses)
            query += f" WHERE {where_str}"
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, tuple(values))
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            columns = [column[0] for column in cursor.description]
            record = {columns[i]: row[i] for i in range(len(columns))}
            results.append(cls(**record))
        
        conn.close()
        return results
    
    def save(self) -> bool:
        """Сохраняет модель в БД (создает или обновляет)"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        attributes = vars(self)
        primary_key_value = attributes.get(self.primary_key)
        
        # Проверяем существование записи
        if primary_key_value and self.find_by_id(primary_key_value):
            # Обновление существующей записи
            update_fields = []
            values = []
            
            for key, value in attributes.items():
                if key != self.primary_key and key in self.schema:
                    update_fields.append(f"{key} = ?")
                    values.append(value)
            
            values.append(primary_key_value)  # Для WHERE условия
            
            query = f"UPDATE {self.table_name} SET {', '.join(update_fields)} WHERE {self.primary_key} = ?"
            cursor.execute(query, tuple(values))
        else:
            # Создание новой записи
            fields = []
            placeholders = []
            values = []
            
            for key, value in attributes.items():
                if key in self.schema:
                    fields.append(key)
                    placeholders.append('?')
                    values.append(value)
            
            query = f"INSERT INTO {self.table_name} ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
            cursor.execute(query, tuple(values))
            
            # Получаем ID новой записи, если это автоинкремент
            if not primary_key_value and self.primary_key == 'id':
                setattr(self, self.primary_key, cursor.lastrowid)
        
        conn.commit()
        conn.close()
        return True
    
    def delete(self) -> bool:
        """Удаляет модель из БД"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        primary_key_value = getattr(self, self.primary_key)
        if not primary_key_value:
            return False
        
        query = f"DELETE FROM {self.table_name} WHERE {self.primary_key} = ?"
        cursor.execute(query, (primary_key_value,))
        
        conn.commit()
        conn.close()
        return True
    
    @classmethod
    def delete_by_id(cls, id_value: Any) -> bool:
        """Удаляет запись по ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = f"DELETE FROM {cls.table_name} WHERE {cls.primary_key} = ?"
        cursor.execute(query, (id_value,))
        
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        return affected_rows > 0
    
    @classmethod
    def count(cls, conditions: Optional[Dict[str, Any]] = None) -> int:
        """Подсчитывает количество записей, удовлетворяющих условию"""
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = f"SELECT COUNT(*) FROM {cls.table_name}"
        values = []
        
        if conditions:
            where_clauses = []
            for key, value in conditions.items():
                where_clauses.append(f"{key} = ?")
                values.append(value)
            
            where_str = " AND ".join(where_clauses)
            query += f" WHERE {where_str}"
        
        cursor.execute(query, tuple(values))
        count = cursor.fetchone()[0]
        
        conn.close()
        return count