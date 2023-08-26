from flask import Flask, render_template, redirect, url_for
import psycopg2
import datetime

app = Flask(__name__)

# connect to database
def db_connection():

    """
    Summary or Description of the Function 
    # connection to database

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip

    Parameters:
    N/A

    Returns:
    connection
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







def get_menu_items():

    """
    Summary or Description of the Function 
    returns customer.html, displays all menu items, ingredients, price, and gives user a place to enter the quantity they want to order
    1) Select all products from the table
    2) Fetch the data
    3) close the cursor and connection
    4) convert every menu item name into a list
    5) dictionary that contains each ingredient with all the smoothies that use that ingredient
    6) list of all ingredients
    7) loop through all smoothies
        if an ingredient is used in a certain smoothie then display it on customer.html
    

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip

    Parameters:
    N/A

    Returns:
        Returns the rendered template for customer.html
    """
    # Select all products from the table
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, cost FROM menu_items")
  
    # Fetch the data
    data = cur.fetchall()
   
    # close the cursor and connection
    cur.close()
    conn.close()

    # convert every menu item name into a list
    smoothies = []
    for smoothie in data:
        tempItem = ""
        for i in range(0, len(smoothie[0])):
            tempItem += smoothie[0][i]

        tempItem = str(tempItem)
        smoothies.append(tempItem)
    

    # dictionary that contains each ingredient with all the smoothies that use that ingredient
    smoothies_with_ingredient = get_ingredients()
    # list of all ingredients
    inventory_list = get_inventory_items()

    # loop through all smoothies
    # if an ingredient is used in a certain smoothie then display it on customer.html
    newData = []
    for smoothieTuple in data:
        smoothie = list(smoothieTuple)
        recipe = []
        for item in inventory_list:
            if (smoothies_with_ingredient[item].count(smoothie[0]) > 0 and recipe.count(item) == 0):
                recipe.append(item)
        smoothie.append(recipe)
        newTuple = tuple(smoothie)
        newData.append(newTuple)
    return render_template('customer.html', data = newData)






def get_inventory_items():

    """
    Summary or Description of the Function 
    function to return a list of every inventory item
    1) converts the list of tuples into a list of ingredients
    
    

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip

    Parameters:
    N/A

    Returns:
        Returns a list of every inventory item
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM inventory")

    inventory_items = cur.fetchall()

    # converts the list of tuples into a list of ingredients
    inventory_list = []
    for item in inventory_items:
        tempItem = ""
        for i in range(0, len(item[0])):
            tempItem += item[0][i]

        
        tempItem = str(tempItem)
        inventory_list.append(tempItem)

    cur.close()
    conn.close()
    return inventory_list








def get_ingredients():

    """
    Summary or Description of the Function 
    creates a hashmap that has each inventory item and which all smoothies use that item
    1) loop through list of inventory items
    2) select all smoothies in which that specific ingredient quantity is greater than 0

    3) if the ingredient is used in that smoothie, add it to a temp list
    4) assign that temp list (value / list of smoothie names) to the key (ingredient)
    
    

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip

    Parameters:
    N/A

    Returns:
        returns a dictionary that has each inventory item and which all smoothies use that item
    """

    conn = db_connection()
    cur = conn.cursor()

    smoothies_with_ingredient = {}

    inventory_list = get_inventory_items()
    
    # loop through list of inventory items
    # select all smoothies in which that specific ingredient quantity is greater than 0

    # if the ingredient is used in that smoothie, add it to a temp list
    # assign that temp list (value / list of smoothie names) to the key (ingredient)
    for item in inventory_list:
        cur.execute("SELECT name FROM menu_items WHERE " + item + " > 0")
        smoothies_with_ingredient_query = cur.fetchall()

        smoothie_list = []
        for smoothies in smoothies_with_ingredient_query:
            tempItem = ""
            for i in range(0, len(smoothies[0])):
                tempItem += smoothies[0][i]

            tempItem = str(tempItem)
            smoothie_list.append(tempItem)

        smoothies_with_ingredient[item] = smoothie_list

    cur.close()
    conn.close()

    return smoothies_with_ingredient








def get_menu_item_names():

    """
    Summary or Description of the Function 
    function to return a list of all smoothie names
    1) convert the list of tuples to a list of smoothies
  
    
    

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip

    Parameters:
    N/A

    Returns:
        returns a list of all smoothie names
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM menu_items")

    menu_items = cur.fetchall()

    # convert the list of tuples to a list of smoothies
    menu_list = []
    for item in menu_items:
        tempItem = ""
        for i in range(0, len(item[0])):
            tempItem += item[0][i]

        
        tempItem = str(tempItem)
        menu_list.append(tempItem)

    cur.close()
    conn.close()
    return menu_list







def smoothies_with_price():

    """
    Summary or Description of the Function 
    creates a dictionary that contains each menu item as the key and the price as the value
    1) loops through the query and assigns each smoothie name a cost
    
    

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip

    Parameters:
    N/A

    Returns:
        returns a dictionary that contains each menu item as the key and the price as the value
    """
    conn = db_connection()
    cur = conn.cursor()

    smoothie_prices = {}

    cur.execute("SELECT name, cost FROM menu_items")

    costs = cur.fetchall()

    # loops through the query and assigns each smoothie name a cost
    for smoothie in costs:
        tempItem = ""
        tempCost = ""
        for i in range(0, len(smoothie[0])):
            tempItem += smoothie[0][i]

        tempItem = str(tempItem)
        tempCost = smoothie[1]
        smoothie_prices[tempItem] = tempCost
        # print(tempItem, tempCost)

    cur.close()
    conn.close()
    return smoothie_prices







def place_order(data):

    """
    Summary or Description of the Function 
    function to loop through the user input on the customer page and push it into the temp order table
    this gives the user a chance to cancel their order before it updates the inventory
    
    

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip

    Parameters:
    N/A

    Returns:
        Returns the rendered template for orderviewcustomer.html
    """
    # print(data)
    conn = db_connection()
    cur = conn.cursor()

    smoothie_prices = smoothies_with_price()
    now = datetime.datetime.now()
    formatted_date_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    
    for smoothie in data:
        # cur.execute('INSERT INTO mytable (name, age, email) VALUES (%s, %s, %s)', (name, age, email))
        cur.execute("INSERT INTO temp_order (time, order_num, smoothie_name, quantity, price) VALUES (%s, %s, %s, %s, %s)", (formatted_date_time, 1, smoothie, (data[smoothie]), (smoothie_prices[smoothie])))
        # print(smoothie, data[smoothie], smoothie_prices[smoothie])
    conn.commit()

    cur.close()
    conn.close()
    return render_template("orderviewcustomer.html", data = data)