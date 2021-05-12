from flask import Flask, render_template, request, redirect


from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection

app = Flask(__name__)


@app.route("/")
def index():
    mysql = connectToMySQL('users_schema')	        # call the function, passing in the name of our db
    users = mysql.query_db('SELECT * FROM users;')  # call the query_db function, pass in the query as a string
    print(users)
    return render_template("index.html", all_users = users)


@app.route("/create")
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
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)