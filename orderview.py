from flask import Flask, render_template, redirect, url_for
import psycopg2, customer, server

app = Flask(__name__)

def db_connection():
    """
    Authors:
        Joshua Wienecke, Jake Rounds, Sneha Dilip, Mugdha Merchant, Bella Woliver

    Returns:
        creates a connection between the Flask app and the PSQL database.
    """
    try:
        conn = psycopg2.connect(host="csce-315-db.engr.tamu.edu",
                            database="csce315331_xi",
                            user = "csce315331_xi_master",
                            password="ritcheys",
                            )
        print("connected")
    except:
        print ("I am unable to connect to the database")
    return conn




def update_database():
    """
    Updates psql tables (orders, x_report, inventory) according to order made
    1. copy data from temp_order into orders and X_report
    2. Create hashmap of items in inventory
    3. Update the hashmap with two loops. loop 1: finds menu_item that matches with item name. 
       loop 2: updates quantity in inventory_map if the menu_item column name matches
    4. update inventory table according to hashmap
    
    Authors:
        Joshua Wienecke, Jake Rounds, Sneha Dilip, Mugdha Merchant, Bella Woliver

    Parameters:
        N/A
    
    Returns:
        no return.
    """
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO orders SELECT * FROM temp_order")    
    cur.execute("INSERT INTO x_report SELECT * FROM temp_order")

    inventory_map = {}
    cur.execute("SELECT name FROM inventory")
    rows = cur.fetchall()
    for row in rows:
        inventory_map[row[0]] = 0

    cur.execute("SELECT smoothie_name, quantity FROM temp_order")
    rows = cur.fetchall()
    for row in rows:
        smoothie_name = row[0]
        quantity = row[1]
        cur.execute("SELECT * FROM menu_items WHERE name = %s", (smoothie_name,))
        menu_item = cur.fetchone()
        if menu_item:
            for i in range(3, len(menu_item)): 
                col_name = cur.description[i].name
                if col_name in inventory_map:
                    inventory_map[col_name] += (menu_item[i] * quantity) 

    for name, qty in inventory_map.items():
        if qty > 0:
            cur.execute("UPDATE inventory SET quantity = quantity - %s WHERE name = %s", (qty, name))

    conn.commit()
    cur.close()
    conn.close()
    print("updated database")
    return


def process_order_customer():
    """
    Updates database, clears the temp_order table and returns to customerview

    Authors:
        Joshua Wienecke, Jake Rounds, Sneha Dilip, Mugdha Merchant, Bella Woliver

    Parameters:
        N/A    

    Returns:
        Returns the rendered template for customer.html
    """
    update_database()
    clear_temp_table()
    return customer.get_menu_items()

def cancel_order_customer():
    """
    Clears the temp_order table and returns to customerview

    Authors:
        Joshua Wienecke, Jake Rounds, Sneha Dilip, Mugdha Merchant, Bella Woliver

    Parameters:
        N/A    
        
    Returns:
        Returns the rendered template for customer.html
    """
    clear_temp_table()
    return customer.get_menu_items()

def process_order_server():
    """
    Updates database, clears the temp_order table and returns to serverview

    Authors:
        Joshua Wienecke, Jake Rounds, Sneha Dilip, Mugdha Merchant, Bella Woliver

    Parameters:
        N/A
        
    Returns:
        Returns the rendered template for server.html
    """
    update_database()
    clear_temp_table()
    return server.get_menu_items()

def cancel_order_server():
    """
    Clears the temp_order table and returns to serverview

    Authors:
        Joshua Wienecke, Jake Rounds, Sneha Dilip, Mugdha Merchant, Bella Woliver

    Parameters:
        N/A
        
    Returns:
        Returns the rendered template for server.html
    """
    clear_temp_table()
    return server.get_menu_items()

def clear_temp_table():
    """
    Clears the temp_order table using PSQL commands

    Authors:
        Joshua Wienecke, Jake Rounds, Sneha Dilip, Mugdha Merchant, Bella Woliver

    Parameters:
        N/A        
        
    Returns:
        no return.
    """
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM temp_order")

    conn.commit()
    cur.close()
    conn.close()
    print("cleared temp orders")
    return 

def get_orders_customer():
    """
    Navigates from server page to orderview page
    Updates the orderview page with the order stored in temp_order
    1. loop through the orders table and store the columns into lists
    2. return rendered template with the lists data

    Authors:
        Joshua Wienecke, Jake Rounds, Sneha Dilip, Mugdha Merchant, Bella Woliver

    Parameters:
        N/A

    Returns:
        Returns the rendered html file for orderview.
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT smoothie_name, quantity, price FROM temp_order")

    smoothie_names = []
    quantities = []
    prices = []
    total_price = 0.0

    for smoothie_name, quantity, price in cur:
        smoothie_names.append(smoothie_name)
        quantities.append(quantity)
        prices.append(price)
        total_price += price * quantity
    price_total = round(total_price, 2)

    cur.close()
    conn.close()

    return render_template("orderviewcustomer.html", smoothie_names=smoothie_names, 
                           quantities=quantities, prices=prices, price_total=price_total)

def get_orders_server():
    """
    Navigates from server page to orderview page
    Updates the orderview page with the order stored in temp_order
    1. loop through the orders table and store the columns into lists
    2. return rendered template with the lists data

    Authors:
        Joshua Wienecke, Jake Rounds, Sneha Dilip, Mugdha Merchant, Bella Woliver

    Parameters:
        N/A

    Returns:
        Returns the rendered html file for orderview.
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT smoothie_name, quantity, price FROM temp_order")

    smoothie_names = []
    quantities = []
    prices = []
    total_price = 0.0

    
    for smoothie_name, quantity, price in cur:
        smoothie_names.append(smoothie_name)
        quantities.append(quantity)
        prices.append(price)
        total_price += price * quantity
    price_total = round(total_price, 2)

    cur.close()
    conn.close()

    return render_template("orderviewserver.html", smoothie_names=smoothie_names, 
                           quantities=quantities, prices=prices, price_total=price_total)

