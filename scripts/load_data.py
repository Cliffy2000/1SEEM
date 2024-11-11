import psycopg2
import requests
import re

from jupyter_core.version import pattern
from psycopg2 import sql

# Define connection parameters
db_config = {
    "dbname": "postgres",
    "user": "ct2004admin",
    "password": "60zTCK~oKSurAWl",
    "host": "ntu-ct2004-psql.postgres.database.azure.com",
    "port": "5432"
}

def connect_to_db():
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        return connection, cursor
    except Exception as e:
        print("Error while connecting to PostgreSQL:", e)
        raise e

def retrieve_school_general_info():

    dataset_id = "d_688b934f82c1059ed0a6993d2a829089"
    url = "https://data.gov.sg/api/action/datastore_search?resource_id=" + dataset_id

    response = requests.get(url)
    print(response.json())
    res = response.json().get('result')
    records = res.get('records')
    return records

def clean_data(data_ls, type='tel'):
    new_data = []
    if type == 'tel' or type == 'fax':
        pattern = "\d{8}|\d{4}\s\d{4}"
    else:
        # Not supported type
        return ""
    for data in data_ls:
        if data is None or data == "na":
            continue
        match = re.search(pattern, data)
        if match:
            new_data.append(match.group())
        else:
            continue
    data_str = '|'.join(new_data)
    return data_str


def get_mrt_stations(data):
    from config import mrt_stations
    mrt_ls = []
    new_data = data.upper()
    for mrt in mrt_stations:
        if mrt in new_data:
            mrt_ls.append(mrt)
            new_data = new_data.replace(mrt, "")
    mrt_str = "|".join(mrt_ls)
    return mrt_str


def get_bus_no(data):
    bus_ls = []
    patterns = ["\d{2,3}[A-Za-z]", "\d{2,3}"]

    for pattern in patterns:
        match = re.findall(pattern, data)
        if match:
            bus_ls = bus_ls + match
    bus_str = "|".join(bus_ls)
    return bus_str


def construct_school_info(records):
    data = []
    for record in records:
        tel_lst = [record.get('telephone_no'), record.get('telephone_no_2')]
        fax_lst = [record.get('fax_no'), record.get('fax_no_2')]
        data.append(
            {
                "name": record.get('school_name'),
                "url_address": record.get('url_address'),
                "address": record.get('address'),
                "postal": record.get('postal_code'),
                "tel_no": clean_data(tel_lst, type='tel'),
                "fax_no": clean_data(fax_lst, type='fax'),
                "email": record.get('email_address').upper(),
                "mrt_stations": get_mrt_stations(record.get('mrt_desc')),
                "bus_numbers": get_bus_no(record.get('bus_desc')),
                "principal_name": record.get('principal_name'),
                "district": record.get('dgp_code'),
                "zone": record.get('zone_code'),
                "type": record.get('type_code'),
                "nature": record.get('nature_code'),
                "main_level": record.get('mainlevel_code'),
                "mother_tongues": '|'.join([record.get('mothertongue1_code'),
                                            record.get('mothertongue2_code'),
                                            record.get('mothertongue3_code')]),
                "moe_programmes": ""
            }
        )
    return data


def import_school_info():
    data = retrieve_school_general_info()

    db_data = construct_school_info(data)
    columns = db_data[0].keys()
    column_names = ', '.join(columns)
    placeholders = ', '.join(['%s'] * len(columns))
    insert_query = f"INSERT INTO t_school_info ({column_names}) VALUES ({placeholders})"

    # Prepare data for insertion
    values = [tuple(data[col] for col in columns) for data in db_data]
    print(values)
    try:
        connection, cursor = connect_to_db()
        cursor.executemany(insert_query, values)

        connection.commit()
        print("Data inserted successfully.")
        cursor.close()
        connection.close()

    except Exception as error:
        print("Error while inserting data:", error)
    return True



if __name__ == '__main__':
    import_school_info()