from flask import Flask
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv(override=True)

DATABASE_URL = os.getenv("DATABASE")

if not DATABASE_URL:
    raise Exception("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

def createtable():
    usuario = """
        CREATE TABLE users(
        id INT PRIMARY KEY, 
        nombre TEXT, 
        correo TEXT, 
        password TEXT
        )
    """

    publicacion = """"
        CREATE TABLE publi (
        id INT FOREIGN KEY, 
        titulo TEXT,
        archivo 

        )
    
    """
    