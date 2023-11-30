from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE")

if not DATABASE_URL:
    raise Exception("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL, echo=True)
db = scoped_session(sessionmaker(bind=engine))

def createtable():
    usuario = text("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            password TEXT NOT NULL
        );

    """ )
    db.execute(usuario) 

    publicacion = text("""
    CREATE TABLE publi (
        id_usuarios INT, 
        titulo TEXT NOT NULL,
        archivo TEXT NOT NULL,
        materia TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        interaccion INT NOT NULL,
        FOREIGN KEY (id_usuarios) REFERENCES users (id)
    )
""")


    db.execute(publicacion) 
    db.commit()

def main():
    print("creando db")
    createtable()

if __name__ == "__main__":
    main()
    print("listo")


    