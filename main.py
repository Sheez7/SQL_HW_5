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

def add_client(cur):
    name = input("Input name: ")
    surname = input("Input surname: ")
    email = input("Input email: ")
    cur.execute("""
    INSERT INTO Client(name, surname, email) VALUES(%s, %s, %s);
    """, (name, surname, email))
    if cur.rowcount > 0:
       return f"Client {name} {surname} is exists now"
    return "New client not added"

# 3. Функция, позволяющая добавить телефон для существующего клиента.

def add_phone(cur):
    client = int(input("Input client_id: "))
    phone = int(input("Input phone_id: "))
    phone_number = int(input("Input phone_number: "))
    cur.execute("""
    INSERT INTO Phone(client_id, phone) VALUES(%s, %s);
    """, (client, phone_number))
    if cur.rowcount > 0:
       return f"Phone {phone_number} is exists now"
    return "New phone not added"

# 4. Функция, позволяющая изменить данные о клиенте.

def update_client(cur):
    name = input('Name: ')
    surname = input('Surname: ')
    email = input('Email: ')
    phone = int(input('Phone: '))
    id = int(input('Phone_id: '))
    client_id = int(input('Client_id: '))
    cur.execute("""
        UPDATE Client SET name=%s, surname=%s, email=%s WHERE id=%s;
        """, (name, surname, email, id))
    cur.execute("""
            UPDATE Phone SET phone=%s WHERE client_id=%s;
            """, (phone, id, ))
    return cur.rowcount

# 5. Функция, позволяющая удалить телефон для существующего клиента.

def delete_phone(cur):
    id = int(input('For delete please insert phone id: '))
    cur.execute("""
        DELETE FROM Phone WHERE id=%s;
        """, (id, ))
    return cur.rowcount

# 6. Функция, позволяющая удалить существующего клиента.

def delete_client(cur):
    id = int(input('For delete please insert client id: '))
    cur.execute("""
        DELETE FROM Client WHERE id=%s;
        """, (id, ))
    return cur.rowcount

# 7. Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.

def search_client(cur):
    name = input('Please insert name for search: ')
    surname = input('Please insert surname for search: ')
    email = input('Please insert email for search: ')
    phone = input('Please insert phone for search: ')
    cur.execute("""
        SELECT id FROM Client WHERE name=%s AND surname=%s AND email=%s;
        """, (name, surname, email))
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
            add_client(cur)
            add_phone(cur)
            update_client(cur)
            delete_phone(cur)
            delete_client(cur)
            search_client(cur)








