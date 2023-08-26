from flask import Flask, render_template,redirect,url_for, request,abort,session,request,jsonify, send_from_directory
import psycopg2
import os
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import customer,server
import orderview
import manager

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = "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" 

app.debug = True

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # to allow Http traffic for local dev

GOOGLE_CLIENT_ID = "539813039862-bhgtehjudmpatod2c7u74se5tctk5o07.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

@app.route('/static/<path:filename>')
def serve_static(filename):
    """
    routes to staic folder

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    String filename

    Returns:
    A function that connects the filename to the root directory
    """
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    # redirect_uri="http://127.0.0.1:5000/callback1"
    redirect_uri={"http://127.0.0.1:5000/callback1","http://127.0.0.1:5000/callback2","https://render-app-wpy0.onrender.com/callback1","https://render-app-wpy0.onrender.com/callback2"}
)

def login_is_required(function):
    """
    Runs the wrapper function recursively

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    function

    Returns:
    wrapper()
    """
    def wrapper(*args, **kwargs):
        """
        if login is wrong, the functions aborts. Otherwise function() is passed back to login_is_required

        Authors:
        Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

        Parameters:
        args and kwargs

        Returns:
        function()
        """

        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper

@app.route("/serverlogin")
def serverlogin():
    """
    Server login page

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Redirects the authorization
    """
    # flow.redirect_uri = "http://127.0.0.1:5000/callback1"
    flow.redirect_uri = "https://render-app-wpy0.onrender.com/callback1"
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/managerlogin")
def managerlogin():
    """
    Manager login page

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Redirects the authorization
    """
    # flow.redirect_uri = "http://127.0.0.1:5000/callback2"
    flow.redirect_uri = "https://render-app-wpy0.onrender.com/callback2"
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback1")
def callback1():
    """
    Callback function that confirms the authentification and if correct redirects to server

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Redirects to server page
    """
    flow.fetch_token(authorization_response=request.url)
    # print("hi")
    # print(session["state"])
    # print(request.args["state"])

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds = 10
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/server")

@app.route("/callback2")
def callback2():
    """
    Callback function that confirms the authentification and if correct redirects to manager

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Redirects to manager page
    """
    flow.fetch_token(authorization_response=request.url)
    # print("hi")
    # print(session["state"])
    # print(request.args["state"])

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds = 10
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/manager")

@app.route("/logout")
def logout():
    """
    logout function that clears the session and redirects 

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Redirects to previous page
    """
    session.clear()
    return redirect("/")

@app.route("/")     
def home():
    """
    Redirects to Home when called

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Redirects to Home
    """
    return render_template('index.html')    

@app.route('/customer')
def customerPage():
    """
    Redirects to customer when called

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Redirects to customer
    """
    return customer.get_menu_items()

@app.route('/manager')
def managerPage():
    """
    Redirects to manager when called

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Redirects to manager and returns data
    """
    data = ""
    return render_template('manager.html', data = data)

@app.route('/server')
def serverPage():
    """
    calls get_menu_items

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    calls get_menu_items in server
    """
    return server.get_menu_items()

@app.route('/orderviewcustomer', methods=['POST'])
def placeOrder():
    """
    reads the values from the user input using the post method and loops through these values and pushes them to the function that updates temp orders

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls get_orders_customer in overview
    """
    values = {}
    menu_items = customer.get_menu_item_names()
    for item in menu_items:
        if (request.form[item] != ''):
            values[item] = request.form[item]
        else:
            continue

    customer.place_order(values)
    return orderview.get_orders_customer()

@app.route('/processOrderCustomer')
def process_order_c():
   """
   app route for the order view customer, if the customer clicks submit order, updates the inventory based on the order, goes back to the customer view

   Authors:
   Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

   Parameters:
   N/A

   Returns:
   Calls process_order_customer
   """
   print("processing order")
   return orderview.process_order_customer()

@app.route('/cancelOrderCustomer')
def cancel_order_c():
    """
    Cancels order

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls cancel_order_customer in overview
    """
    print("cancelling order\n")
    return orderview.cancel_order_customer()

@app.route('/orderviewserver', methods=['POST'])
def serverPlaceOrder():
    """
    Takes input from the orderview page and calls get_orders_server woth that data

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls get_orders_server in overview
    """
    values = {}
    menu_items = server.get_menu_item_names()
    for item in menu_items:
        if (request.form[item] != ''):
            values[item] = request.form[item]
        else:
            continue

    server.place_order_server(values)
    return orderview.get_orders_server()

@app.route('/processOrderServer')
def process_order_s():
    """
    Calls proccess_order_server in overview

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls proccess_order_server in overview
    """
    print("processing order")
    return orderview.process_order_server()

@app.route('/cancelOrderServer')
def cancel_order_s():
    """
    does not update the database if the user cancels the order, goes back to server view

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls proccess_order_server in overview
    """
    print("cancelling order\n")
    return orderview.cancel_order_server()

@app.route('/inventory')
def inventoryPage():
    """
    Manager functions, app route allowing the manager to see the inventory

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls get_inventory in manager
    """
    return manager.get_inventory()

@app.route('/saveInventory', methods=['POST'])
def saveInventory():
    """
    saves inventory

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    String filename

    Returns:
    calls save_inventory in manager
    """
    data = request.get_json()
    return manager.save_inventory(data)
   
@app.route('/menuItems')
def menuItemPage():
    """
    App route allowing the manager to see and edit all the menu items

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls get_menu_items in manager
    """
    return manager.get_menu_items()

@app.route('/saveMenu', methods=['POST'])
def saveMenu():
    """
    saves new smoothie

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    String filename

    Returns:
    calls save_menu in manager
    """
    data = request.get_json()
    return manager.save_menu(data)

@app.route('/editSmoothie', methods=['POST', 'GET'])
def editSmoothie():
    """
    Allows for smoothies to be editted to contain new ingredients

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    String filename

    Returns:
    Opens to new html
    """
    name = request.form['name']
    data = manager.editSmoothie(name)
    ingredients = manager.get_ingredient_names()
    return render_template('edit_menu_item.html', data=data, inventory=ingredients)
    
@app.route('/addNewIngredient')
def newIngredientPage():
    """
    App route allowing the manager to add a new ingredient

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls generate_new_ingredient in manager
    """
    return manager.generate_new_ingredient()

@app.route('/addNewSmoothie')
def newSmoothiePage():
    """
    App route allowing the manager to add a new menu item

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls generate_new_smoothie in manager
    """
    return manager.generate_new_smoothie()

@app.route('/getIngredients', methods=['GET'])
def getIngredients():
    """
    Takes in the user input, allows the user to add a new item to inventory

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls get_ingredient_names in manager
    """
    return manager.get_ingredient_names()

@app.route('/saveIngredient', methods=['POST'])
def saveIngredient():
    """
    Just functions, no new page, saves the new ingredient and adds it to database

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls add_new_ingredient in manager
    """
    data = request.get_json()
    return manager.add_new_ingredient(data)

@app.route('/saveSmoothie', methods=['POST'])
def saveSmoothie():
    """
    Takes in the user input, allows the manager to add a new menu item

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls add_new_smoothie in manager
    """
    data = request.get_json()
    return manager.add_new_smoothie(data)

@app.route('/restockAll', methods=['POST'])
def restock():
    """
    Button allowing the manager to restock all inventory items to 500 units

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls restock_all in manager
    """
    return manager.restock_all()

@app.route('/excessReport')
def excessReportPage():
    """
    App route to display all inventory items that there is an excess of

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Opens excess_report html and corresponding data
    """
    data = {}
    return render_template('excess_report.html', data = data)

@app.route('/generatedExcessReport', methods=['GET','POST'])
def excessReport():
    """
    User can enter a time, excess report is generated for all excess items between last restock and given time

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    empty string or excess_report html and corresponding data
    """
    input_data = request.get_json()
    print("entered excess generate")
    if (input_data):
      data = manager.get_excess_report(input_data)
      print("exited repot")
      return render_template('excess_report.html', data=data)
    else:
      return ""

@app.route('/salesReport')
def salesReportPage():
    """
    App route to display the sales report, allows the user to input a start and end time

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Redirects to sales_report html and return data
    """
   # grab real data here
    print("sales")
    data = {}
    return render_template('sales_report.html', data = data)

@app.route('/generatedSalesReport', methods=['GET','POST'])
def salesReport():
    """
    Displays all orders between the user inputted start and end time, finds this from the orders table

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Opens sales_report html and associated data
    """
    print("entered sales generate")
    # gather actual data here
    input_data = request.get_json()
    data = manager.get_sales_report(input_data)
    return render_template('sales_report.html', data = data)

@app.route('/restockReport')
def restockReport():
    """
    Displays all inventory items that need to be restocked

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Redirects to restock html page with data parameter
    """
    data = manager.get_restock_report()
    print("restock")
    return render_template('restock_report.html', data = data)

@app.route('/x_report')
def manager_to_x():
    """
    manager to x report, app route to display the x report

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls x_report in manager
    """
    return manager.x_report()

@app.route('/z_report')
def manager_to_z():
    """
    manager to z report, app route to display the z report

    Authors:
    Jake Rounds, Bella Woliver, Joshua Wienecke, Mugdha Merchant, Sneha Dilip 

    Parameters:
    N/A

    Returns:
    Calls x_report in manager
    """
    return manager.z_report()

if __name__ == "__main__":
    app.run(debug = True)

