from datetime import datetime
from scripts.db import connect_to_db

def check_user_exists(username):
    connection, cursor = connect_to_db()
    sql_query = f"""SELECT username FROM t_user_info WHERE username = '{username}' 
                                                    AND valid_flag = 1"""
    cursor.execute(sql_query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(data) == 0:
        return False
    return True


def authenticate_user(username, password):
    connection, cursor = connect_to_db()
    sql_query = f"""SELECT * FROM t_user_info WHERE username = '{username}' 
                                                AND password = '{password}' AND valid_flag = 1"""
    cursor.execute(sql_query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    if len(data) == 0:
        return False
    return True

def get_user_type(username):
    connection, cursor = connect_to_db()
    sql_query = f"""SELECT user_type FROM t_user_info WHERE username = %s AND valid_flag = 1"""

    cursor.execute(sql_query, (username,))
    data = cursor.fetchone()

    cursor.close()
    connection.close()
    
    if data is None:
        return None
    return data['user_type']


def get_user_id(username):
    connection, cursor = connect_to_db()
    sql_query = f"""SELECT id FROM t_user_info WHERE username = %s AND valid_flag = 1"""

    cursor.execute(sql_query, (username,))
    data = cursor.fetchone()

    cursor.close()
    connection.close()
    
    if data is None:
        return None
    return data['id']


def get_user_name(user_id):
    connection, cursor = connect_to_db()
    sql_query = """SELECT username FROM t_user_info WHERE id = %s AND valid_flag = 1"""

    cursor.execute(sql_query, (user_id,))
    data = cursor.fetchone()

    cursor.close()
    connection.close()
    
    if data is None:
        return None
    return data['username']


def create_user(username, password, email, user_type):
    connection, cursor = connect_to_db()
    data = {
        'username': username,
        'password': password,
        'email': email,
        'user_type': user_type,
        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'valid_flag': 1
    }
    columns = ', '.join(data.keys())
    placeholders = ', '.join(f"%({key})s" for key in data.keys())
    sql_query = f"INSERT INTO t_user_info ({columns}) VALUES ({placeholders});"

    cursor.execute(sql_query, data)
    connection.commit()

    return True


def delete_user(username):
    connection, cursor = connect_to_db()
    # Check if user exists
    user_exists = check_user_exists(username)
    if user_exists:
        sql_query = f"UPDATE t_user_info SET valid_flag = 2 WHERE username = '{username}'"
        cursor.execute(sql_query)
        connection.commit()
        return True
    else:
        print("User not found in Database")
        return False


def reset_user_table():
    connection, cursor = connect_to_db()
    
    cursor.execute("DELETE FROM t_user_info;")
    
    cursor.execute("""
        DO $$ 
        BEGIN
            IF NOT EXISTS (SELECT * FROM information_schema.columns 
                           WHERE table_name='t_user_info' AND column_name='user_id') THEN
                ALTER TABLE t_user_info
                ADD COLUMN user_id SERIAL PRIMARY KEY;
            END IF;
        END $$;
    """)

    connection.commit()
    cursor.close()
    connection.close()
    
    print("User table reset.")