import os
from psycopg2 import *
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, flash, redirect, render_template, request, session, url_for,jsonify, send_from_directory
from dotenv import load_dotenv  
from random import sample
from werkzeug.utils import secure_filename 
from werkzeug.exceptions import RequestEntityTooLarge


app = Flask(__name__)
load_dotenv(override=True)

engine = create_engine(os.getenv("DATABASE"))
db = scoped_session(sessionmaker(bind=engine))

# Configuración de la sesión
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.urandom(24)

#index
@app.route("/")
def index():
    session.clear()
    """Website home"""
    print(session)
    if request.method == "GET":
        return render_template("login.html")
    
#--------------------------------------------------------------------

#login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    if request.method == "POST":
        correo = request.form.get("correo")
        password = request.form.get("password")

        try:
            if correo and password:
                query = text("SELECT * FROM users WHERE correo = :correo")
                result = db.execute(query, {"correo": correo})
                datos = result.fetchall()
                print(datos[0][3])
                if password == datos[0][3]:
                    session['user_id'] = datos[0][0]
                    return redirect(url_for("home"))
                    #-----------------------------------------------
                    
            else:
                flash("Por favor, introduce tu correo y contraseña")
        except:
            return render_template("login.html")
        
    return render_template("login.html")
    
    
#--------------------------------------------------------------------

@app.route("/home")
def home():
    try:
        if "user_id" in session:
             #CONSULTA A LA BASE DE DATOS PARA RELLENAR LAS CARDS DE PUBLICACIONES
            query = text("select * from publi")
            result = db.execute(query)
            elementos = []
            print("RUTA HOME")
            for i in result:
                print(i)
                elementos.append(i)
            return render_template("home.html", cards = elementos)  
        else:
            return render_template("login.html")
    except Exception as e:
        print(f"Error en la función 'home': {str(e)}")
        return render_template("login.html")
#--------------------------------------------------------------------

    
@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return render_template("login.html")
    
#--------------------------------------------------------------------

@app.route("/upload")
def upload():
    """Upload file"""
    try:
        if "user_id" in session:
            return render_template("upload.html")
        else:
            return render_template("login.html")
    except Exception as e:
        print(f"Error en la función 'upload': {str(e)}")
        return render_template("login.html")
#--------------------------------------------------------------------

    
# AQUI SE AGREGAN LOS USUARIOS DESDE REGISTER.HTML
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    #revisamos que el metodo recibido es POST, sino solo carga la plantilla register
    if request.method == "POST":
        nombre = request.form.get("name")
        contraseña = request.form.get("password")
        correo = request.form.get("correo")
        
        #consultamos todas las personas registradas
        resultados = list(db.execute(text("SELECT nombre FROM users")))
        usuarios = [resultado[0] for resultado in resultados]
        print(usuarios)
        print(nombre)
        # comprobamos que la persona nueva no exista en las registradas
        if nombre not in usuarios:
            if nombre and contraseña and correo:
                query = text("INSERT INTO users (nombre, password, correo) VALUES (:nombre, :password, :correo)")
                db.execute(query, {'nombre': nombre, 'password': contraseña, 'correo': correo})
                db.commit()
                flash("Registro exitoso")
                return redirect(url_for("login"))
        else:
            flash("El usuario ya existe")
            return redirect(url_for("register"))
        
    return render_template("register.html") 

#--------------------------------------------------------------------

def stringAleatorio():
    #Generando string aleatorio
    string_aleatorio = "0123456789abcdefghijklmnopqrstuvwxyz_"
    longitud         = 20
    secuencia        = string_aleatorio.upper()
    resultado_aleatorio  = sample(secuencia, longitud)
    string_aleatorio     = "".join(resultado_aleatorio)
    return string_aleatorio


#--------------------------------------------------------------------

@app.route("/postear", methods=["POST"])
def postear():
    if "user_id" not in session:
        return render_template("login.html", flash("NO ESTES DE ALUCIN"))
    try:
        if request.method == "POST":
        #Recibiendo los datos del formulario
            titulo = request.form.get("titulo_archivo")
            descripcion = request.form.get("descripcion_archivo")
            file = request.files['archivo_pdf']
            materia = request.form.get("materia")
            print(titulo)
            print(descripcion)
            print(file)

            basepath = os.path.dirname (__file__)
            filename = secure_filename(file.filename)
            extension           = os.path.splitext(filename)[1]
            nuevoNombreFile     = stringAleatorio() + extension
        
            upload_path = os.path.join (basepath, 'static/archivos', nuevoNombreFile) 
            file.save(upload_path)  
            
            query = text("INSERT INTO publi (id_usuarios, titulo, archivo, materia, descripcion, interaccion) VALUES (:id, :titulo, :archivo, :materia, :descripcion, :interaccion)")
            
            db.execute(query,  {'id': session['user_id'],
                                'titulo': titulo,
                                'archivo': nuevoNombreFile,
                                'materia': materia,
                                'descripcion': descripcion,
                                'interaccion': 0})
            db.commit()
            
            
            return render_template('upload.html'), flash("Archivo subido exitosamente")
        
    except RequestEntityTooLarge as e:
            print(f"Error de carga de archivo: {e}")
            return render_template('upload.html', error="El archivo es demasiado grande.")
    except Exception as e:
        print(f"Error desconocido: {e}")
        return render_template('upload.html', error="Se produjo un error al procesar la solicitud.")

#--------------------------------------------------------------------

@app.route('/descargar/<nombre_archivo>')
def descargar_archivo(nombre_archivo):
    try:
        if "user_id" in session:
            return send_from_directory('static/archivos', nombre_archivo, as_attachment=True)
    except:
        return render_template("login.html", flash("NO ESTES DE ALUCIN"))
    

#--------------------------------------------------------------------

@app.route("/buscarPublicacion")
def buscarPublicacion():
    contenido = request.args.get("contenido")
    contenido_lower = contenido.lower()
    query = (text("SELECT * FROM publi WHERE LOWER(materia) LIKE :contenido OR LOWER(descripcion) LIKE :contenido"))
    result = db.execute(query, {"contenido": "%" + contenido_lower + "%"})
    cards = result.fetchall()
    return render_template("home.html", cards=cards)
# #--------------------------------------------------------------------


@app.route("/perfil")
def perfil():
    try:
        if "user_id" in session:
            return render_template("perfil.html")
    except:
        return render_template("login.html", flash("NO ESTES DE ALUCIN"))
    
# #--------------------------------------------------------------------

@app.route("/cambiarDatos", methods=["POST"])
def cambiarDatos():
    try:
        control = 0
        nombre = request.form.get("nombreUsuario")
        password = request.form.get("contraUsuario")
        correo = request.form.get("correoUsuario")

        if nombre:
            query = text("UPDATE users SET nombre = :nombre WHERE id = :id")
            db.execute(query, {"id": session['user_id'], "nombre": nombre})
            control += 1

        if password:
            query = text("UPDATE users SET password = :password WHERE id = :id")
            db.execute(query, {"id": session['user_id'], "password": password})
            control += 1

        if correo:
            query = text("UPDATE users SET correo = :correo WHERE id = :id")
            db.execute(query, {"id": session['user_id'], "correo": correo})
            control += 1

        if control != 0:
            db.commit()
            flash("DATOS ACTUALIZADOS")
            return render_template('login.html')

    except Exception as e:
        print(f"Error en la función 'cambiar_datos': {str(e)}")
        flash("Hubo un error al actualizar los datos.")
        return render_template('login.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
 