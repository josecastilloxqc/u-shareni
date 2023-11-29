from flask import Flask, render_template, redirect, request
app = Flask(__name__)

@app.route("/")
def index():
    """Website home"""
    if request.method == "GET":
        return render_template("login.html")
    


@app.route("/home")
def home():
    """Website home"""
    return render_template("home.html")

@app.route("/logout")
def logout():
    """Log user out"""
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
<<<<<<< HEAD

    return render_template("register.html")
=======
    if request.method == "GET":
        return render_template("/register.html")
    
    nombre = request.form.get("name")
    contraseña = request.form.get("password")
    confirmacion = request.form.get("confirmation")
    correo = request.form.get("correo")
>>>>>>> 16c92f30f3b00e66aa13496fd193fa960c06ad5c

    redirect ("/login.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Upload file"""
    if request.method == "GET":
        return render_template("/upload.html")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
 