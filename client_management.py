import os
import psycopg2
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# Функция добавления клиента
def add_client(first_name, last_name, email):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO clients (first_name, last_name, email)
                VALUES (%s, %s, %s) RETURNING client_id;
            """, (first_name, last_name, email))
            client_id = cur.fetchone()[0]
    print(f"Клиент {first_name} {last_name} добавлен с ID {client_id}")

# Функция добавления телефона клиенту
def add_phone(client_id, phone_number):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO phones (client_id, phone)
                VALUES (%s, %s);
            """, (client_id, phone_number))
    print(f"Телефон {phone_number} добавлен клиенту с ID {client_id}")

# Функция поиска клиента по параметрам
def find_client(first_name=None, last_name=None, email=None, phone=None):
    query = """
        SELECT c.client_id, c.first_name, c.last_name, c.email, p.phone
        FROM clients c
        LEFT JOIN phones p ON c.client_id = p.client_id
    """
    conditions = []
    values = []

    if first_name:
        conditions.append("c.first_name = %s")
        values.append(first_name)
    if last_name:
        conditions.append("c.last_name = %s")
        values.append(last_name)
    if email:
        conditions.append("c.email = %s")
        values.append(email)
    if phone:
        conditions.append("p.phone = %s")
        values.append(phone)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            return cur.fetchall()

# Функция обновления данных клиента
def update_client(client_id, first_name=None, last_name=None, email=None):
    if not any([first_name, last_name, email]):
        print("Ошибка: нужно передать хотя бы одно поле для обновления.")
        return

    query = "UPDATE clients SET"
    updates = []
    values = []

    if first_name:
        updates.append(" first_name = %s")
        values.append(first_name)
    if last_name:
        updates.append(" last_name = %s")
        values.append(last_name)
    if email:
        updates.append(" email = %s")
        values.append(email)

    query += ",".join(updates) + " WHERE client_id = %s"
    values.append(client_id)

    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)

    print(f"Данные клиента {client_id} обновлены.")

# Основное меню
if __name__ == "__main__":
    print("Выберите действие:")
    print("1 - Добавить клиента")
    print("2 - Добавить телефон")
    print("3 - Найти клиента")
    print("4 - Обновить данные клиента")
    choice = input("Введите номер действия: ")

    if choice == "1":
        fname = input("Имя: ")
        lname = input("Фамилия: ")
        email = input("Email: ")
        add_client(fname, lname, email)
    elif choice == "2":
        cid = input("ID клиента: ")
        phone = input("Телефон: ")
        add_phone(cid, phone)
    elif choice == "3":
        fname = input("Имя (Enter - пропустить): ") or None
        lname = input("Фамилия (Enter - пропустить): ") or None
        email = input("Email (Enter - пропустить): ") or None
        phone = input("Телефон (Enter - пропустить): ") or None
        results = find_client(fname, lname, email, phone)
        print(results if results else "Клиент не найден.")
    elif choice == "4":
        cid = input("ID клиента: ")
        fname = input("Новое имя (Enter - пропустить): ") or None
        lname = input("Новая фамилия (Enter - пропустить): ") or None
        email = input("Новый email (Enter - пропустить): ") or None
        update_client(cid, fname, lname, email)
