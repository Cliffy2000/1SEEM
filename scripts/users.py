from datetime import datetime
from db import connect_to_db

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


if __name__ == '__main__':
    #create_user('test', 'test1234', 'test@gmail.com', 'user')
    delete_user('test')