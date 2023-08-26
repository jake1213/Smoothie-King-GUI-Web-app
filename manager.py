from flask import Flask, render_template, redirect, url_for, json
from datetime import datetime
import psycopg2, customer
from datetime import date

app = Flask(__name__)
def db_connection():
   """
   Connects the web application to our SQL database. If unable the function prints and error message.

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    N/A
   """
   try:
      conn = psycopg2.connect(host="csce-315-db.engr.tamu.edu", database="csce315331_xi",
                              user = "csce315331_xi_master", password="ritcheys",)
   except:
      print ("unable to connect to manager")
      
   return conn

def get_ingredient_names():
   """
   Querys the inventory database to find all ingredients names

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   N/A

   Returns:
   List of tuples containing sql query output
   """

   # Select all products from the table
   conn = db_connection()
   cur = conn.cursor()
   cur.execute("SELECT name FROM inventory")

   # Fetch the data
   data = cur.fetchall()

   # close the cursor and connection
   cur.close()
   conn.close()
   
   return data

def get_inventory():
   """
   Querys the inventory database to find all ingredients used in each smoothie

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   N/A

   Returns:
   List of tuples containing sql query output 
   """
   # Select all products from the table
   conn = db_connection()
   cur = conn.cursor()
   cur.execute("SELECT * FROM inventory")

   # Fetch the data
   data = cur.fetchall()

   # close the cursor and connection
   cur.close()
   conn.close()
   
   return render_template('inventory.html', data = data)

def save_inventory(data):
   """
   Querys table with new inventory changes and makes edits in the database tables containing that smoothie

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   data

   Returns:
   Empty string
   """
   if (data):
      # open conn
      conn = db_connection()
      cur = conn.cursor()
      
      for item in data:
         query = "UPDATE inventory SET quantity = '" + data[item]
         query += "' WHERE name = '" + item + "'"
         cur.execute(query)
         conn.commit()
      
      cur.close()
      conn.close()
   else:
      print("no stuff to save")
   
   return ""

def editSmoothie(data):
   """
   Queries the database for the smoothies with the parameter smoothie name and returns that list

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   smoothie name

   Returns:
   list of smoothies that contains the name searched
   """
   conn = db_connection()
   cur = conn.cursor()
   
   query = "SELECT * FROM menu_items WHERE name = '" + data + "'"
   cur.execute(query)
   result = cur.fetchone()
   
   cur.close()
   conn.close()
   
   smoothie = {}
   column_names = [desc[0] for desc in cur.description]
   smoothie = dict(zip(column_names, result))
   
   return smoothie

def save_menu(data):
    """
    Allows for new menu items to be added and saved into the database with queries to the menu_items table

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    data

    Returns:
    Empty string
    """    
    if (data): 
        name = data['name']
        print("Saving updates to " + name)
        # open conn
        conn = db_connection()
        cur = conn.cursor()
        
        for item in data:
            if (item != "name"):
                query = "UPDATE menu_items SET " + item + " = '" + data[item]
                query += "' WHERE name = '" + name + "'"

                cur.execute(query)
                conn.commit()
        
        cur.close()
        conn.close()
    else:
        print("no stuff to save")
    return ""

def get_inventory_data():
   """
   Querys the database to find the current quantity of each ingredient in our inventory table

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   N/A

   Returns:
   List of tuples containing sql query output 
   """
   conn = db_connection()
   cur = conn.cursor()
   cur.execute("SELECT * FROM inventory")

   # Fetch the data
   ingredients = cur.fetchall()

   # close the cursor and connection
   cur.close()
   conn.close()
   
   return {row[0]: row[1] for row in ingredients}

def get_smoothie(name):
   """
   Querys the inventory database to find all ingredients used in one specific smoothie

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   String containing name of a smoothie

   Returns:
   List containing sql query output 
   """
   conn = db_connection()
   cur = conn.cursor()

   # stored as ingredient, quantity
   smoothie_ingredients = {} 
   inventory_list = get_inventory_data()
   
   for item in inventory_list.keys():
      # grabs the inventory item that has not empty thing
      cur.execute("SELECT " + item + " FROM menu_items WHERE name='" + name + "'")
      smoothies_result = cur.fetchall()
      if (smoothies_result[0][0] > 0):
         smoothie_ingredients[item] = smoothies_result

   cur.close()
   conn.close()
      
   return smoothie_ingredients

def get_menu_items():
   """
   Querys the inventory database to find all menu items

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   N/A

   Returns:
   List of tuples containing sql query output 
   """
   # Select all products from the table
   conn = db_connection()
   cur = conn.cursor()
   cur.execute("SELECT name FROM menu_items")

   # Fetch the data
   data = cur.fetchall()

   # close the cursor and connection
   cur.close()
   conn.close()
   
   return render_template('menu_items.html', smoothies = data)

def generate_new_ingredient():
   """
   Adds a new ingredient 

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   N/A

   Returns:
   Empty string into the add inventory page 
   """
   data = ""
   return render_template('add_inventory.html', data = data)

def generate_new_smoothie():
   """
   Calls get_ingredient_names() in order to add a new smoothie to the menu

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   N/A

   Returns:
   List of strings containing all of the smoothie names
   """
   # todo implement a page to allow user to input new smoothie needs
   # button in view should call add_new_smoothie()
   data = get_ingredient_names()
   return render_template('add_menu_item.html', data = data)

def add_new_ingredient(data):
   """
   Querys the inventory table in the database to add a new ingredient and acossiated quantity

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   List of smoothie specifications

   Returns:
   Empty String
   """
   name = data["name"]
   quantity = data["quantity"]

   query = "INSERT INTO inventory VALUES ('" + name + "', " + quantity + ")"
   
   print(query)

   conn = db_connection()
   cur = conn.cursor()
   cur.execute(query)
   conn.commit()
   # close the cursor and connection
   cur.close()
   conn.close()
   
   query2 = "ALTER TABLE menu_items ADD " + name + " VARCHAR(50)"
   print(query2)
   
   conn = db_connection()
   cur = conn.cursor()
   cur.execute(query2)
   conn.commit()
   # close the cursor and connection
   cur.close()
   conn.close()
   
   return ""

def add_new_smoothie(data):
   """
   Querys the menu_items table in the database to add a new smoothie and acossiated ingredients

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   List of smoothie specifications

   Returns:
   Empty String
   """
   print("save smoothie")
   
   # data holds all of the ingredient names and quantities 
   print(data)
   
   # todo loop through each ingredient
   last_id = ""
   conn = db_connection()
   cur = conn.cursor()
   cur.execute("SELECT MAX(item_id) FROM menu_items")
   
   last_id = cur.fetchall()
   
   # close the cursor and connection
   cur.close()
   conn.close()
   item_id = last_id[0][0][1] + "1"
   print(item_id)
   
   name = data["name"]
   cost = data["cost"]
   ingredients = ""
   
   ingredient_names = get_ingredient_names()
   num_ingredients = len(ingredient_names)
   count = 1
         
   for ingredient_name in ingredient_names:
      curr = str(ingredient_name[0])
      ingredients += data[curr]
      if (count != num_ingredients):
         ingredients += ", "
      count += 1
   
   
   query = "INSERT INTO menu_items VALUES ('" + item_id + "', '" + name + "', " + cost + ", " 
   query += ingredients + ")"
   
   print(query)
   
   # todo test if this query works
   conn = db_connection()
   cur = conn.cursor()
   cur.execute(query)
   conn.commit()

   # close the cursor and connection
   cur.close()
   conn.close()
   
   return ""

def restock_all():
   """
   When called, this functions restocks all of the inventory items to our default value of 500

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   N/A

   Returns:
   Empty String
   """
   # todo connect to database to restock everything
   print("restock all")
   
   query = "UPDATE inventory SET quantity = 500.0"
   
   conn = db_connection()
   cur = conn.cursor()
   cur.execute(query)
   conn.commit()

   # close the cursor and connection
   cur.close()
   conn.close()
   
   return ""


def get_excess_report(data):
   """
   Querys the orders table between an inputted time frame to find which ingredients are less that 10% of their original inventory

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   List of smoothie specifications

   Returns:
   List of ingredients in excess
   """
   print(data)
   
   timestamp = data["timestamp"] + ".000"
   timeformat = "%Y-%m-%d %H:%M:%S.%f"
   date_obj = datetime.strptime(timestamp, timeformat)
   
   # data will store the info given by the user
   query = "SELECT smoothie_name, quantity FROM orders WHERE (time) >= '{date_str}'".format(date_str=date_obj.strftime('%Y-%m-%d %H:%M:%S'))
   
   print(query)
   conn = db_connection()
   cur = conn.cursor()
   cur.execute(query)
   
   result = cur.fetchall()
   print(result)

   # close the cursor and connection
   cur.close()
   conn.close()
   
   # map of ingredients and amts
   map = {}
   excess = {}
   
   for smoothie in result:
      smoothie_ingredients = get_smoothie(smoothie[0])
      
      for smoothie_part in smoothie_ingredients:
         if (smoothie_part in map):
            map[smoothie_part] += smoothie[1]
         else:
            map[smoothie_part] = smoothie[1]
   
      
   for ingredient in get_inventory_data():
      if (ingredient in map):
         # 500 is the restock value for each ingredient, and we are checking against the last restock
         if (map[ingredient] < .1*(500)):
            excess[ingredient] = map[ingredient]
      else:
         excess[ingredient] = 0
   
   return excess

def get_sales_report(data):
   """
   Querys the orders table between a certain time to find what was sold

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   data

   Returns:
   Map of smoothies sold
   """
   print("sales report")
   print(data)
   
   start_time = data["start_time"]
   end_time = data["end_time"]
   
   # stores key ordernum to access list[time, smoothie name, quantity, price]
   result_map = {}
   
   time_query = "SELECT * FROM orders WHERE time BETWEEN '"
   time_query += start_time + "' AND '" + end_time + "'"
   
   print(time_query)
   conn = db_connection()
   cur = conn.cursor()
   cur.execute(time_query)
   
   results = cur.fetchall()
   print()
   print(results)

   # close the cursor and connection
   cur.close()
   conn.close()
   
   i = 0
   
   for order in results:
      time = str(order[0])
      order_num = order[1]
      smoothie_name = order[2]
      quantity = order[3]
      price = order[4]
      
      details = [time, order_num, smoothie_name, quantity, price]
      
      result_map[i] = details
      i += 1
   
   return result_map

def get_restock_report():
   """
   Query the inventory table to find which ingredients are at less that 1% quantity

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   N/A

   Returns:
   List of ingredients that are in low quantity
   """
   print("restock report")
   
   query = "SELECT * FROM inventory WHERE quantity < 5.0"
   
   conn = db_connection()
   cur = conn.cursor()
   cur.execute(query)
   
   results = cur.fetchall()
   print(results)

   # close the cursor and connection
   cur.close()
   conn.close()
   
   return results

def x_report():
   """
   Querys the x_report table to find everything sold since the last clear (Z report)

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   N/A

   Returns:
   List of tuples from the query output
   """
   data = []
   conn = db_connection()
   cur = conn.cursor()
   cur.execute("SELECT time,order_num,smoothie_name,quantity,price FROM x_report")

   # Fetch the data
   data = cur.fetchall()
      

   # close the cursor and connection
   cur.close()
   conn.close()

   #return
   return render_template('x_report.html', data = data) 

def z_report():
   """
   Querys the z_report table to find everything sold for the current day. Also clears the x_reports table

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   N/A

   Returns:
   List of tuples containing query output
   """
   # Open connection
   conn = db_connection()
   cur = conn.cursor()

   today = date.today()
   query2 = "SELECT * FROM x_report WHERE time = '{date}'".format(date=today.strftime('%Y-%m-%d'))
   cur.execute(query2)

   # Fetch the data
   data = cur.fetchall()

   query1 = "DELETE FROM x_report;"
   cur.execute(query1)
   conn.commit()

   #Close connection
   cur.close()
   conn.close()

   #return
   return render_template('z_report.html', data = data) 

