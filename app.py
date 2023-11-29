from flask import Flask, render_template, redirect, request
app = Flask(__name__)

@app.route("/")
def index():
    """Website home"""
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
    if request.method == "GET":
        return render_template("/register.html")
    
    nombre = request.form.get("name")
    contraseña = request.form.get("password")
    confirmacion = request.form.get("confirmation")
    correo = request.form.get("correo")




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
 