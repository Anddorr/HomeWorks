import sqlite3

# Connected to DataBase
connection = sqlite3.connect('MyDB.db', check_same_thread=False)

# Translator from sql to python
sql = connection.cursor()

# Create a table of users
sql.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER, name TEXT, number TEXT, location TEXT);')

# Create a table of products
sql.execute('CREATE TABLE IF NOT EXISTS products(pr_id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'pr_name TEXT,  pr_amount INTEGER, pr_price REAL, pr_des TEXT, pr_photo TEXT);')

# Create a table of purchases
sql.execute('CREATE TABLE IF NOT EXISTS cart(user_id INTEGER, user_pr TEXT, pr_quantity INTEGER, total REAL);')


# Methods for users


# Registration
def registration(id, name, num, loc):
    sql.execute('INSERT INTO users VALUES(?, ?, ?, ?);', (id, name, num, loc))
    # Save
    connection.commit()


# Check is user in database
def checker(id):
    check = sql.execute('SELECT id FROM users WHERE id=?', (id,))
    if check.fetchone():
        return True
    else:
        return False


def return_name(id):
    name = sql.execute('SELECT name FROM users WHERE id=?', (id,)).fetchone()
    return name[0]


def commit_name(new_info, id):
    sql.execute(F'UPDATE users SET name="{new_info}" WHERE id={id};')
    connection.commit()


def commit_num(new_info, id):
    sql.execute(F'UPDATE users SET number="{new_info}" WHERE id={id};')
    connection.commit()


def commit_loc(new_info, id):
    sql.execute(F'UPDATE users SET location="{new_info}" WHERE id={id};')
    connection.commit()

