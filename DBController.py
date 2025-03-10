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
        user_id integer PRIMARY KEY,
        username  text UNIQUE, 
        last_name text,
        first_name text,
        counter_duty integer,
        access_status integer,
        FOREIGN KEY (access_status) REFERENCES access_status(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS  material_assets(
        key  integer PRIMARY KEY AUTOINCREMENT,
        identifier integer,
        description text,
        photo text
    )""")
    db.commit()
    c.execute("""CREATE TABLE IF NOT EXISTS process (
        id  integer PRIMARY KEY AUTOINCREMENT,
        witness_username text,
        debtor_username text,
        description_item text, 
        start_date date,
        end_date date,
        key_material_assets integer,
        count_day integer,
        FOREIGN KEY (witness_username) REFERENCES users(username),
        FOREIGN KEY (debtor_username) REFERENCES users(username)
        FOREIGN KEY (key_material_assets) REFERENCES material_assets(key)
    )""")

    db.commit()
    c.execute("SELECT * FROM access_status")
    if (len(c.fetchall()) == 0):
        c.execute("INSERT INTO access_status (name) VALUES ('common_user')")
        c.execute("INSERT INTO access_status (name) VALUES ('witness')")
        c.execute("INSERT INTO access_status (name) VALUES ('admin')")
        db.commit()


    db.close()



def add_new_process(witness_username, debtor_username, descrp, end_date : datetime.date):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    count_day = end_date - datetime.today()
    c.execute("INSERT INTO process (witness_username, debtor_username, description_item, start_date, end_date, count_day) VALUES ('{witness}', '{debtor}','{descrption}',{start_date}, {end}, {days}})".
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
    c.execute("SELECT id FROM access_status WHERE name = '{}'".format(new_access))
    new_id = c.fetchall()[0][0]
    c.execute("UPDATE users SET access_status = {} WHERE username = '{}'".format(str(new_id), username))
    db.commit()
    db.close()




def add_new_user(id_user, username, second_name, first_name, access):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT id FROM access_status WHERE name = '{}'".format(access))
    db.commit()
    id_access = c.fetchall()[0][0]
    c.execute("INSERT INTO users (user_id, username, last_name, first_name, counter_duty, access_status) VALUES ({}, '@{}', '{}', '{}', {}, {})".format( str(id_user), username, second_name, first_name, "0", str(id_access)))
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


def check_user_reg_by_user_id(user_id ): #выбирается либо  1 либо другой параметр
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute("SELECT COUNT (*) FROM users WHERE user_id = {}".format(str(user_id)))
 
    if (c.fetchall()[0][0] == 0):
        db.close()
        return False
    db.close()
    return True

def check_user_reg_by_username(username ): #выбирается либо  1 либо другой параметр
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute("SELECT COUNT (*) FROM users WHERE username = '{user}'".format(user = username))   
 
    if (c.fetchall()[0][0] == 0):
        db.close()
        return False
    db.close()
    return True


def  is_admin(user_id):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT access_status FROM users WHERE user_id = {}".format(str(user_id)))
    if (c.fetchall()[0][0] == 3):
        db.close()
        return True
    db.close()
    return False

def getListOfUsers():
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT username, last_name, first_name, counter_duty FROM users")
    result = c.fetchall()
    db.close()
    return result

def get_count_duty(id):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT counter_duty FROM users WHERE user_id = {}".format(str(id)))
    result = c.fetchone()[0]
    db.close()
    return result
