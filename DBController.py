import sqlite3
from datetime  import datetime



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
        identifier text,
        description text,
        photo text
    )""")
    db.commit()
    c.execute("""CREATE TABLE IF NOT EXISTS process (
        id  integer PRIMARY KEY AUTOINCREMENT,
        witness_username text,
        debtor_username text,
        start_date date,
        end_date date,
        key_material_asset integer,
        counter_days integer,
        state_acceptance text,
        FOREIGN KEY (witness_username) REFERENCES users(username),
        FOREIGN KEY (debtor_username) REFERENCES users(username),
        FOREIGN KEY (key_material_asset) REFERENCES material_assets(key)
    )""")

    db.commit()
    c.execute("SELECT * FROM access_status")
    if (len(c.fetchall()) == 0):
        c.execute("INSERT INTO access_status (name) VALUES ('common_user')")
        c.execute("INSERT INTO access_status (name) VALUES ('witness')")
        c.execute("INSERT INTO access_status (name) VALUES ('admin')")
        db.commit()


    db.close()



def add_new_process(witness_username, debtor_username, descrp, end_date):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    end_date = datetime.strptime(end_date, "%d.%m.%y").date()
    count_day = end_date - datetime.today().date()
    c.execute("INSERT INTO process (witness_username, debtor_username,  key_material_asset, start_date, end_date, counter_days, state_acceptance) VALUES ('{witness}', '@{debtor}','{descrption}','{start_date}', '{end}', {days}, '{accept}')".
                format(  
                    witness = witness_username,
                    debtor = debtor_username,
                    descrption = descrp, 
                    start_date = str(datetime.today().date()),
                    end = str(end_date),
                    days = count_day.days,
                    accept = "Обрабатывается"
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


def add_new_item(indef, descr, photo):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("INSERT INTO material_assets (identifier, description, photo) VALUES ('{}', '{}', '{}')".format( indef, descr, photo ))
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


def check_user_reg_by_user_id(user_id ): 
    db = sqlite3.connect("database.db")
    c = db.cursor()

    c.execute("SELECT COUNT (*) FROM users WHERE user_id = {}".format(str(user_id)))
 
    if (c.fetchall()[0][0] == 0):
        db.close()
        return False
    db.close()
    return True

def check_user_reg_by_username(username ): 
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

def get_process_string(id):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT * FROM process WHERE id = {}".format(id))
    result = "Вам прислали заявление на заимствование "
    lst = c.fetchone()
    result = "Id сделки - {}\n".format(str(lst[0]))
    result += "Заявитель - {}\n".format(lst[2])
    result += "Дата начала - {}\nДата конца - {}".format(str(lst[3]), str(lst[4]))
    c.execute("Select photo FROM material_assets WHERE key = '{}'".format(lst[5]))
    lst = list(c.fetchone())
    db.close()
    return result, lst[0]
    


def get_witness():
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT username FROM users WHERE access_status = 2 OR access_status = 3")
    lists = c.fetchall()
    min_processes = 10000000
    min_name = ""
    for lst in lists:
        name = lst[0]
        c.execute("SELECT COUNT (*) FROM process WHERE witness_username = '{}'".format(name))
        counter = list(c.fetchone())
        if (counter[0] < min_processes):
            min_name = name
            min_processes = counter[0]
    db.close()
    return min_name


def get_id_by_username(username):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT user_id FROM users WHERE username = '{}'".format(username))
    user_id = list(c.fetchone())[0]
    db.close()
    return user_id



def count_all_process():
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT COUNT (*) FROM process ")
    lst = list(c.fetchone())
    db.close()
    return lst[0]


def update_accept_state(new_state, id):
    db = sqlite3.connect("database.db")
    print(id)
    c = db.cursor()
    c.execute("UPDATE process SET state_acceptance = '{}' WHERE id = '{}'".format(new_state, id))
    db.commit()
    db.close()


def get_debtor_username_by_process_id(id):
    db = sqlite3.connect("database.db")
    c = db.cursor()
    c.execute("SELECT debtor_username FROM process WHERE id = {}".format(id))

    lst = list(c.fetchone())
    db.close()
    return lst[0]