import psycopg2

# 1. Функция, создающая структуру БД (таблицы).
def create_table(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS Client(
        id SERIAL PRIMARY KEY,
        name VARCHAR(40) NOT NULL,
        surname VARCHAR(40) NOT NULL,
        email VARCHAR(40) NOT NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS Phone(
        id SERIAL PRIMARY KEY,
        client_id INTEGER REFERENCES Client(id) ON DELETE CASCADE,
        phone CHAR(12)
    );
    """)
    return "Succesfully created"

# 2. Функция, позволяющая добавить нового клиента.
def add_client(cur, name, surname, email):
    cur.execute("""
    INSERT INTO Client(name, surname, email) VALUES(%s, %s, %s);
    """, (name, surname, email))
    if cur.rowcount > 0:
       return f"Client {name} {surname} is exists now"
    return "New client not added"

# 3. Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(cur, client_id, phone_number):
    cur.execute("""
    INSERT INTO Phone(client_id, phone) VALUES(%s, %s);
    """, (client_id, phone_number))
    if cur.rowcount > 0:
       return f"Phone {phone_number} is exists now"
    return "New phone not added"

# 4. Функция, позволяющая изменить данные о клиенте.
def update_client(cur, client_id, name=None, surname=None, email=None):
    if name:
        cur.execute("""
            UPDATE Client SET name=%s WHERE id=%s;
            """, (name, client_id))
    if surname:
        cur.execute("""
            UPDATE Client SET surname=%s WHERE id=%s;
            """, (surname, client_id))
    if email:
        cur.execute("""
            UPDATE Client SET email=%s WHERE id=%s;
            """, (email, client_id))
    return cur.rowcount

# 5. Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone(cur, phone_id):
    cur.execute("""
        DELETE FROM Phone WHERE id=%s;
        """, (phone_id, ))
    return cur.rowcount

# 6. Функция, позволяющая удалить существующего клиента.
def delete_client(cur, client_id):
    cur.execute("""
        DELETE FROM Client WHERE id=%s;
        """, (client_id, ))
    return cur.rowcount

# 7. Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def search_client(cur, name=None, surname=None, email=None, phone=None):
    if name and surname and email:
        cur.execute("""
            SELECT id FROM Client WHERE name=%s AND surname=%s AND email=%s;
            """, (name, surname, email))
    elif phone:
        cur.execute("""
            SELECT client_id FROM Phone WHERE phone=%s;
            """, (phone, ))
    if cur.rowcount > 0:
        print('Client is found')
    else:
        print('Client not found')
    client = cur.fetchall()
    print(f'Found a client with id: {client[0][0]}')

if __name__  == '__main__':
    with psycopg2.connect(database="SQL_HW_5", user="postgres", password="1") as conn:
        with conn.cursor() as cur:
            create_table(cur)
            name = input("Input name: ")
            surname = input("Input surname: ")
            email = input("Input email: ")
            add_client(cur, name, surname, email)
            client_id = int(input("Input client_id: "))
            phone_number = int(input("Input phone_number: "))
            add_phone(cur, client_id, phone_number)
            update_client(cur, client_id)
            phone_id = int(input("Input phone_id: "))
            delete_phone(cur, phone_id)
            client_id = int(input("Input client_id: "))
            delete_client(cur, client_id)
            name = input('Please insert name for search: ')
            surname = input('Please insert surname for search: ')
            email = input('Please insert email for search: ')
            phone = input('Please insert phone for search: ')
            search_client(cur, name, surname, email, phone)