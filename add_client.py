import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def add_client(first_name, last_name, email):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO clients (first_name, last_name, email)
        VALUES (%s, %s, %s) RETURNING client_id;
    """, (first_name, last_name, email))

    client_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    print(f"Клиент {first_name} {last_name} успешно добавлен с ID {client_id}")

# Пример вызова
add_client("Иван", "Петров", "ivan.petrov@example.com")
