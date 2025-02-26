import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def add_phone(client_id, phone_number):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO phones (client_id, phone)
        VALUES (%s, %s);
    """, (client_id, phone_number))

    conn.commit()
    cur.close()
    conn.close()

    print(f"Телефон {phone_number} добавлен клиенту с ID {client_id}")

# Пример вызова
add_phone(3, "123-456-7890")

