import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def find_client_by_info(value):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()

    query = """
        SELECT c.client_id, c.first_name, c.last_name, c.email, p.phone
        FROM clients c
        LEFT JOIN phones p ON c.client_id = p.client_id
        WHERE c.first_name = %s OR c.last_name = %s OR c.email = %s OR p.phone = %s
    """

    cur.execute(query, (value, value, value, value))
    results = cur.fetchall()

    if results:
        for row in results:
            client_id, first_name, last_name, email, phone = row
            print(f"Клиент найден: {first_name} {last_name} - {email}")
            if phone:
                print(f"Телефон: {phone}")
            else:
                print("Телефона нет.")
    else:
        print("Клиент не найден.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    search_value = input("Введите имя, фамилию, email или телефон клиента: ")
    find_client_by_info(search_value)
