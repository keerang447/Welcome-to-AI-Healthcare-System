from flask import Flask, render_template, request, redirect, session
import sqlite3
import pickle

app = Flask(__name__)
app.secret_key = "secretkey"

model = pickle.load(open("health_model.pkl", "rb"))

# Database connection
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create tables
conn = get_db()
conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, username TEXT, age INT, bp INT, sugar INT, result TEXT)")
conn.commit()
conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        conn.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
        conn.commit()
        conn.close()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password)).fetchone()
        conn.close()
        if user:
            session["username"] = username
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html")
    return redirect("/login")

@app.route("/predict", methods=["POST"])
def predict():
    age = int(request.form["age"])
    bp = int(request.form["bp"])
    sugar = int(request.form["sugar"])

    prediction = model.predict([[age,bp,sugar]])

    if prediction[0] == 1:
        result = "High Risk"
    else:
        result = "Low Risk"

    conn = get_db()
    conn.execute("INSERT INTO history (username,age,bp,sugar,result) VALUES (?,?,?,?,?)",
                 (session["username"],age,bp,sugar,result))
    conn.commit()
    conn.close()

    return render_template("result.html", result=result)

@app.route("/history")
def history():
    conn = get_db()
    records = conn.execute("SELECT * FROM history WHERE username=?",(session["username"],)).fetchall()
    conn.close()
    return render_template("history.html", records=records)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)