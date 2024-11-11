from db import select_school_info

def get_all_schools_info(filter=None):

    return_data = {"status": 0}

    data = select_school_info(filter)
    if data is None:
        return_data["status"] = 1
    return_data["data"] = data

    return return_data


if __name__ == '__main__':
    sch_info = get_all_schools_info(filter={"school":'XXX'})
    print(sch_info)
