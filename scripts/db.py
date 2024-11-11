import psycopg2
from psycopg2.extras import RealDictCursor
from scripts.config import db_config

def connect_to_db():
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        return connection, cursor
    except Exception as e:
        print("Error while connecting to PostgreSQL:", e)
        raise e


def select_school_info(filter=None):
    connection, cursor = connect_to_db()
    sql_query = """SELECT * FROM t_school_info"""
    conditions = []
    
    if 'school' in filter:
        school = filter['school']
        conditions.append(f"name = '{school}'")

    if 'district' in filter:
        district = filter['district']
        conditions.append(f"name = '{district}'")

    if 'type' in filter:
        type_cd = filter['type']
        conditions.append(f"name = '{type_cd}'")

    if 'level' in filter:
        level = filter['level']
        conditions.append(f"name = '{level}'")

    if 'bus_no' in filter:
        bus_no = filter['bus_no']
        conditions.append(f"name = '{bus_no}'")
    
    if 'mrt' in filter:
        mrt = filter['mrt']
        conditions.append(f"name = '{mrt}'")

    if conditions:
        sql_query += " WHERE " + " AND ".join(conditions)

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



