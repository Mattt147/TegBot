import sqlite3
import datetime



db_name = "database.db"


def create_db():
    db = sqlite3.connect("database.db")

    c = db.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS  access_status(
        id  integer PRIMARY KEY AUTOINCREMENT,
        name text
    )""")
    db.commit()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        username  text PRIMARY KEY,
        second_name text,
        first_name text,
        counter_duty integer,
        access_status integer,
        FOREIGN KEY (access_status) REFERENCES access_status(id)
    )""")
    db.commit()
    c.execute("""CREATE TABLE IF NOT EXISTS process (
        id  integer PRIMARY KEY AUTOINCREMENT,
        witness_username text,
        debtor_username text,
        description_item text, 
        start_date date,
        end_date date,
        count_day integer,
        FOREIGN KEY (witness_username) REFERENCES users(username),
        FOREIGN KEY (debtor_username) REFERENCES users(username)
    )""")

    db.commit()

    c.execute("INSERT INTO access_status (name) VALUES ('common_user')")
    c.execute("INSERT INTO access_status (name) VALUES ('witness')")
    c.execute("INSERT INTO access_status (name) VALUES ('admin')")
    db.commit()
    db.close()



def add_new_process(witness_username, debtor_username, descrp, end_date : datetime.date):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    count_day = end_date - datetime.today()
    c.execute("INSERT INTO process (witness_username, debtor_username, description_item, start_date, end_date, count_day) VALUES ({witness}, {debtor},{descrption},{start_date}, {end}, {days}})".
                format(   
                    witness = witness_username,
                    debtor = debtor_username,
                    descrption = descrp, 
                    start_date = datetime.today(),
                    end = end_date,
                    days = count_day.days
                    )
            )
    db.commit()
    db.close()



def change_access(username,new_access):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT id FROM access_status WHERE name = {}".format(new_access))
    new_id = c.fetchall()[0][0]
    c.execute("UPDATE users SET access_status = {} WHERE username = {}".format(new_id, username))
    db.commit()
    db.close()




def add_new_user(username, second_name, first_name, access):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT id FROM access_status WHERE name = {}".format(access))
    id_access = c.fetchall()[0][0]
    c.execute("INSERT INTO users (username, second_name, first_name, counter_duty, access_status) VALUES ({username}, {second_name},{first_name}, {counter_duty}, {access}})".
                format(   
                    username = username,
                    second_name = second_name,
                    first_name = first_name, 
                    counter_duty = "0",
                    access =  str(id_access)
                    )
            )
    db.commit()
    db.close()




def remove_zap (id):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("DELETE FROM process WHERE id = {}".format(str(id)))
    db.commit()
    db.close()



def remove_user(username):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("DELETE FROM users WHERE username = {}".format(username))
    db.commit()
    db.close()




