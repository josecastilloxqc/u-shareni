import sqlite3
from flask import Flask, render_template, redirect, request
from database import *

app = Flask(__name__)


@app.route("/")
def index():
    """Website home"""
    if request.method == "GET":
        return render_template("login.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    
    if request.method == "GET":
        return render_template("login.html")
    
    # nombre_usuario = request.form.get("name")
    # contraseña = request.form.get("password")

    # if nombre_usuario == "usuario" and contraseña == "contraseña":
    #     Session["logged_in"] = True
    #     return redirect("/home.html")
    # else:
    #     return "Credenciales inválidas"
        
    # return redirect("home.html")
@app.route("/home")
def home():
    """Website home"""
    return render_template("home.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Session.clear()

    # return redirect("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    
    nombre = request.form.get("name")
    contraseña = request.form.get("password")
    confirmacion = request.form.get("confirmation")
    correo = request.form.get("correo")

    # conn = sqlite3.connect("database.py")

    # with conn:

    #     try:
    #         conn.execute("INSERT INTO usuarios (nombre, contraseña, correo) VALUES (?, ?, ?)", (nombre, contraseña, correo))
    #     except:
    #         return render_template("register.html")
        

    return redirect("login.html")

 

@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Upload file"""
    if request.method == "GET":
        return render_template("upload.html")
    
    archivo_pdf = request.form.get("archivo_pdf")
    titulo_archivo = request.form.get("titulo_archivo")
    descripcion_archivo = request.form.get("descripcion_archivo")
   # tipo_archivo = request.form.get("tipo_materia")
    

    ##aqui va la parte de la base de datos

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
 