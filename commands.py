from scripts.users import create_user, get_user_type, reset_user_table
from scripts.report import submit_report


if __name__ == "__main__":
    reset_user_table()
    
    create_user("user1", "user", "user1@m.com", "user")
    create_user("user2", "user", "user2@m.com", "user")
    create_user("user3", "user", "user3@m.com", "user")

    create_user("admin1", "admin", "admin1@m.com", "admin")
    
    # submit_report("user1", "admin1", "report 1.1")
    # submit_report("user1", "admin1", "report 1.2")
    # submit_report("user1", "admin1", "report 1.3")
    # submit_report("user2", "admin1", "report 2.1")
    
    pass