from datetime import datetime
from db import connect_to_db

def submit_report(sender, receiver, content, image=None):
    connection, cursor = connect_to_db()
    data = {
        "sender_id": sender,
        "receiver_id": receiver,
        "content": content,
        "image": image if image is not None else '',
        "created_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    columns = ', '.join(data.keys())
    placeholders = ', '.join(f"%({key})s" for key in data.keys())
    sql_query = f"INSERT INTO t_incident_reports ({columns}) VALUES ({placeholders});"

    cursor.execute(sql_query, data)
    connection.commit()
    cursor.close()
    connection.close()

    return True

def get_report(sender):
    # return the reports by a specific sender
    connection, cursor = connect_to_db()
    sql_query = f"SELECT * FROM t_incident_reports WHERE sender_id = {sender}"

    cursor.execute(sql_query)
    data = cursor.fetchall()
    result = []
    for row in data:
        row_res = {}
        for key in row:
            row_res[key] = row[key]
        result.append(row_res)
    cursor.close()
    connection.close()
    return result