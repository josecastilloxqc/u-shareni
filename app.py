from flask import Flask, render_template,redirect

app = Flask(__name__)

@app.route("/")
def home():
    """Website home"""
    return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    return render_template("register.html")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
 