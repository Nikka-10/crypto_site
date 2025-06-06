from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates")

@app.route("/")
def home():
    return """
    <h1>Welcome to 30 quliani project!</h1>
    <p>Server is running successfully.</p>
    <p><a href='/signup'>Sign Up Here</a></p>
    <p><a href='/login'>Login Here</a></p>
    """

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        data = request.json
        return {"message": "Signup successful!", "data": data}

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        data = request.json
        return {"message": "Login successful!", "data": data}


@app.route("/process_signup", methods=["POST"])
def process_signup():
    data = request.json
    if not data or "email" not in data or "password" not in data:
        return jsonify({"message": "Invalid input"}), 400


    with open("users.txt", "a") as file:
        file.write(f"{data['email']}|{data['password']}|{data.get('fname', '')}|{data.get('lname', '')}\n")

    return jsonify({"message": "Signup successful!"})

if __name__ == "__main__":
    app.run(debug=True)