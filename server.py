from flask import Flask, render_template, request, redirect


from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection

app = Flask(__name__)

#HOME
@app.route("/users")
def index():
    mysql = connectToMySQL('users_schema')	        # call the function, passing in the name of our db
    users = mysql.query_db('SELECT * FROM users;')  # call the query_db function, pass in the query as a string
    print(users)
    return render_template("index.html", all_users = users)

#CREATE
@app.route("/users/new")
def create():
    return render_template("index2.html")


@app.route("/create_user", methods=["POST"])
def add_user_to_db():
    mysql = connectToMySQL("users_schema")
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at)" \
    "VALUES (%(fn)s, %(ln)s, %(eml)s, NOW(), NOW());"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "eml": request.form["eml"]
    }
    new_user_id = mysql.query_db(query, data)
    return redirect(f"/users/{new_user_id}")


#Read One
@app.route("/users/<int:user_id>")
def display_user(user_id):
    mysql = connectToMySQL("users_schema")
    query = "SELECT * FROM users WHERE id = %(id)s"
    data = { 
        "id" : user_id 
    }

    user_list = mysql.query_db(query, data)
    print(user_list[0])

    return render_template("index3.html" , user = user_list[0])


#Edit
@app.route("/users/<int:user_id>/edit")
def edit_user_form(user_id):
    mysql = connectToMySQL("users_schema")
    query = "SELECT * FROM users WHERE id = %(id)s"
    data = { 
        "id" : user_id 
    }

    user_list = mysql.query_db(query, data)
    return render_template("index4.html" , user = user_list[0])


@app.route("/users/<int:user_id>/update", methods = ["POST"])
def update_user(user_id):
    mysql = connectToMySQL("users_schema")
    query = "UPDATE users SET first_name = %(fn)s, last_name = %(ln)s, email = %(eml)s, " \
        "updated_at = NOW() WHERE id = %(id)s;"
    data = {
        "fn": request.form['first_name'],
        "ln": request.form['last_name'],
        "eml": request.form['email'],
        "id": user_id
    }

    mysql.query_db(query, data)

    return redirect(f"/users/{ user_id }/edit")


#Delete
@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    mysql = connectToMySQL("users_schema")
    query = "DELETE FROM users WHERE id = %(id)s;"
    data = {
        "id": user_id
    }

    mysql.query_db(query, data)

    return redirect("/users")


if __name__ == "__main__":
    app.run(debug=True)