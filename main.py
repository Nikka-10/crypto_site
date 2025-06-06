from flask import Flask, request, jsonify

app = Flask(__name__)
DATA_FILE = "users.txt"


def save_user(data):
    with open(DATA_FILE, "a") as file:
        file.write(f"{data['email']}|{data['password']}\n")


@app.route("/process_signup", methods=["POST"])
def process_signup():
    data = request.json
    save_user(data)
    return jsonify({"message": "Signup successful!"})


@app.route("/process_login", methods=["POST"])
def process_login():
    data = request.json
    with open(DATA_FILE, "r") as file:
        for line in file:
            email, password = line.strip().split("|")
            if email == data["email"] and password == data["password"]:
                return jsonify({"message": "Login successful!"})

    return jsonify({"message": "Invalid email or password"}), 401


if __name__ == "__main__":
    app.run(debug=True, port=5001)