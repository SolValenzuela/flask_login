from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Usuario:
    db_name = 'registro' #almacena en una variable el nombre de la base de datos
    def __init__(self,data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.email=data['email']
        self.password=data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data): #agrega datos y devuelve row
        query="INSERT INTO usuarios (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        results=connectToMySQL(cls.db_name).query_db(query,data)
        return results

    @classmethod
    def get_all(cls):#muestra todos los usuarios
        query="SELECT *FROM usuarios"
        results=connectToMySQL(cls.db_name).query_db(query)
        usuarios=[]
        for u in results:
            usuarios.append(cls(u))
        return usuarios
    
    @classmethod
    def get_one(cls,data):
        query="SELECT FROM usuarios WHERE usuarios.id=%(id)s"
        results=connectToMySQL(cls.db_name).query_db(query,data)
        return cls (results[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return False
        return Usuario(results[0])
    
    @staticmethod
    def validate_usuario(usuario):
        is_valid = True 
        if len(usuario['first_name']) < 3:
            flash("Firts name must be at least 3 characters","register")
            is_valid = False
        if len(usuario['last_name']) < 3:
            flash("Last name must be at least 3 characters","register")
            is_valid = False
        if not EMAIL_REGEX.match(usuario['email']):
            is_valid = False
            flash("Invalid Email Address.","register")
        if len(usuario['password']) < 6:
            flash("Password must be at least 6 characters.")
        if usuario['password'] != usuario['confirm_password']:
            is_valid = False
            flash("Passwords do not match!","register")

        return is_valid




