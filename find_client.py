import os
import psycopg2
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def find_client_by_id(client_id):
    """Функция ищет клиента по ID и выводит его данные вместе с телефонами."""
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()
    
    # Поиск клиента по ID
    cur.execute("""
    SELECT first_name, last_name, email
    FROM clients
    WHERE client_id = %s;
    """, (client_id,))
    
    client = cur.fetchone()
    if client:
        print(f"Клиент найден: {client[0]} {client[1]} - {client[2]}")
        
        # Получение телефонов клиента
        cur.execute("""
        SELECT phone
        FROM phones
        WHERE client_id = %s;
        """, (client_id,))
        
        phones = cur.fetchall()
        if phones:
            print(f"Телефоны клиента: {', '.join([phone[0] for phone in phones])}")
        else:
            print("У клиента нет телефонов.")
    else:
        print(f"Клиент с ID {client_id} не найден.")
    
    # Закрытие соединений
    cur.close()
    conn.close()

# Пример вызова функции
if __name__ == "__main__":
    client_id = int(input("Введите ID клиента: "))
    find_client_by_id(client_id)
