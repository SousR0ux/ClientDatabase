import os
import psycopg2
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def update_client(client_id, new_first_name, new_last_name, new_email):
    """Обновляет данные клиента по client_id."""
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE clients
        SET first_name = %s, last_name = %s, email = %s
        WHERE client_id = %s;
    """, (new_first_name, new_last_name, new_email, client_id))
    
    conn.commit()
    cur.close()
    conn.close()

    print(f"Данные клиента с ID {client_id} успешно обновлены!")

# --- Пример вызова функции ---
update_client(3, "Иван", "Петров", "new.email@example.com")
def delete_phone(phone_id):
    """Удаляет телефон по его ID."""
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    
    cur.execute("DELETE FROM phones WHERE phone_id = %s;", (phone_id,))
    
    conn.commit()
    cur.close()
    conn.close()

    print(f"Телефон с ID {phone_id} успешно удалён!")

# --- Пример вызова функции ---
delete_phone(1)
