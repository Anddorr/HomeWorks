import sqlite3

# Connected to DataBase
connection = sqlite3.connect('Lesson16_DB.db', check_same_thread=False)

# Translator from sql to python
sql = connection.cursor()

# Create a table of users
sql.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER, name TEXT, number TEXT, location TEXT);')

# Create a table of products
sql.execute('CREATE TABLE IF NOT EXISTS products(pr_id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'pr_name TEXT,  pr_amount INTEGER, pr_price REAL, pr_des TEXT, pr_photo TEXT);')

# Create a table of purchases
sql.execute('CREATE TABLE IF NOT EXISTS cart(user_id INTEGER, user_pr TEXT, pr_quantity INTEGER, total REAL);')


## Methods for users
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


## Methods for products
# Add product to database
def add_product(pr_name, pr_amount, pr_price, pr_des, pr_photo):
    sql.execute('INSERT INTO products(pr_name, pr_amount, pr_price, pr_des, pr_photo) '
                'VALUES(?, ?, ?, ?, ?);', (pr_name, pr_amount, pr_price, pr_des, pr_photo))
    connection.commit()


# Print info about product
def show_info(id):
    info = sql.execute('SELECT pr_name, pr_amount, pr_price, pr_des, pr_photo FROM product WHERE pr_id=?;', (id,)).fetchone()
    return info


# Print info about all products
def show_all():
    all_products = sql.execute('SELECT * FROM products;')
    return all_products.fetchall()


# Print id of products
def get_pr_name_id():
    products = sql.execute('SELECT pr_id, pr_name, pr_amount FROM products;')
    return products.fetchall()


def get_pr_id():
    products = sql.execute('SELECT pr_name, pr_id, pr_amount FROM products;').fetchall()
    sorted_prods = [i for i in products if i[2] > 0]
    return sorted_prods


## Methods of cart
# Add products to cart
def add_to_cart(user_id, pr_name, pr_quantity, total=0):
    sql.execute('INSERT INTO cart(user_id, pr_name, pr_quantity, total)'
                'VALUES(?, ?, ?, ?);', (user_id, pr_name, pr_quantity, total))
    amount = sql.execute('SELECT pr_amount WHERE pr_name=?;', (pr_name,)).fetchone()
    sql.execute(f'UPDATE products SET pr_amount={amount[0] - pr_quantity} WHERE pr_name=?;', (pr_name,))
    connection.commit()


# Clear cart
def clean_cart(id):
    pr_name = sql.execute('SELECT pr_name FROM cart WHERE user_id=?', (id,)).fetchone()
    amount = sql.execute('SELECT pr_amount FROM products WHERE pr_name=?', (pr_name,)).fetchone()
    pr_quantity = sql.execute('SELECT pr_quantity FROM cart WHERE user_id=?', (id,)).fetchone()
    sql.execute(f'UPDATE products SET pr.amount={amount(0) + pr_quantity} WHERE pr_name = ?;', (pr_name,))
    sql.execute('DELETE FROM cart WHERE id=?;', (id,))
    connection.commit()


# Print cart
def show_cart(id):
    cart = sql.execute('SELECT pr_name, pr_quantity, total FROM cart WHERE user_id=?', (id,)).fetchone()
    return cart


# sql.execute('INSERT INTO products(pr_name, pr_amount, pr_price, pr_des, pr_photo) VALUES(?, ?, ?, ?, ?);', ('Burger', '5000', '25990', "smth",
#                                        "https://i.postimg.cc/YS0vpnt5/image.png"))
# sql.execute('INSERT INTO products(pr_name, pr_amount, pr_price, pr_des, pr_photo) VALUES(?, ?, ?, ?, ?);', ('Pita', '5000', '32990', "smth",
#                                        "https://i.postimg.cc/sD488n1Z/da9581ee81134ea59740836aaf9e4a57-e1580887902436.jpg"))
# connection.commit()