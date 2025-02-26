import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

# Подключение к БД
conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

# Создание таблицы клиентов
cur.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id SERIAL PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE
    )
""")

# Создание таблицы телефонов (может быть несколько у одного клиента)
cur.execute("""
    CREATE TABLE IF NOT EXISTS phones (
        phone_id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES clients(client_id) ON DELETE CASCADE,
        phone VARCHAR(20)
    )
""")

conn.commit()  # Сохранение изменений
cur.close()
conn.close()  # Закрытие соединения

print("Таблицы созданы успешно.")
