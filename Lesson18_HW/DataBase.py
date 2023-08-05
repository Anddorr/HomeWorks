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


# Print id of products
def get_pr_name_id():
    products = sql.execute('SELECT pr_name FROM products;').fetchall()
    return products


def get_pr_id():
    products = sql.execute('SELECT pr_name, pr_id, pr_amount, pr_price FROM products;').fetchall()
    sorted_prods = [i for i in products if i[2] > 0]
    return sorted_prods


## Methods of cart
# Add products to cart
def add_to_cart(user_id, pr_name, pr_quantity, total=0):
    sql.execute('INSERT INTO cart(user_id, user_pr, pr_quantity, total)'
                'VALUES(?, ?, ?, ?);', (user_id, pr_name, pr_quantity, total))
    amount = sql.execute('SELECT pr_amount FROM products WHERE pr_name=?;', (pr_name,)).fetchone()
    sql.execute(f'UPDATE products SET pr_amount={amount[0] - pr_quantity} WHERE pr_name=?;', (pr_name,))
    connection.commit()


# Clear cart
def clear_cart(id):
    if sql.execute('SELECT * FROM cart WHERE user_id=?;', (id,)).fetchone() is None:
        return 'None'
    else:
        pr_name = sql.execute('SELECT user_pr FROM cart WHERE user_id=?;', (id,)).fetchone()
        amount = sql.execute('SELECT pr_amount FROM products WHERE pr_name=?;', (pr_name[0],)).fetchone()
        pr_quantity = sql.execute('SELECT pr_quantity FROM cart WHERE user_id=?;', (id,)).fetchone()
        sql.execute(f'UPDATE products SET pr_amount={amount[0] + pr_quantity[0]} WHERE pr_name = ?;', (pr_name[0],))
        sql.execute('DELETE FROM cart WHERE user_id=?;', (id,))
        connection.commit()


def send_cart(id):
    if sql.execute('SELECT * FROM cart WHERE user_id=?;', (id,)).fetchone() is None:
        return 'None'
    else:
        return 'Not None'


# Print cart
def show_cart(id):
    cart = sql.execute('SELECT pr_name, pr_quantity, total FROM cart WHERE user_id=?;', (id,)).fetchone()
    return cart


def return_price(name):
    price = sql.execute('SELECT pr_price FROM products WHERE pr_name=?;', (name,)).fetchone()
    return price[0]


def return_name(id):
    name = sql.execute('SELECT * FROM users WHERE id=?', (id,)).fetchone()
    return name


def unite_pr(money):
    text = ''.join(reversed(str(money)))
    split_money_3 = [text[i:i + 3] for i in range(0, len(text), 3)]
    split_money_3.reverse()
    split_money = []
    for i in split_money_3:
        split_money.append(''.join(reversed(i)))
    return ' '.join(split_money)


def print_cart(id):
    order = sql.execute('SELECT * FROM cart WHERE user_id=?;', (id,)).fetchall()
    total_sum = 0
    pr_order = 'Cart:\n'
    for i in order:
        pr_order += f'{i[1]} x{i[2]} - {unite_pr(int(i[3]))}sum\n'
        total_sum += i[3]
    pr_order += f"\nTotal - {unite_pr(int(total_sum))}sum\n\n"
    return pr_order


# sql.execute('INSERT INTO products(pr_name, pr_amount, pr_price, pr_des, pr_photo) '
#             'VALUES(?, ?, ?, ?, ?);', ('Burger', '5000', '31000', "smth",
#                                        "https://i.postimg.cc/YS0vpnt5/image.png"))
# sql.execute('INSERT INTO products(pr_name, pr_amount, pr_price, pr_des, pr_photo) '
#             'VALUES(?, ?, ?, ?, ?);', ('Lavash', '5000', '26000', "smth",
#                                        "https://i.postimg.cc/NfYRd6Fk/da9581ee81134ea59740836aaf9e4a57-e1580887902436.jpg"))
# connection.commit()