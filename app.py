import os
import json
#descargando dotenv
from dotenv import load_dotenv
from flask import Flask, session,request, render_template,redirect,jsonify
from flask_session import Session
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, session_activate
load_dotenv()
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"),pool_size=10, max_overflow=20)
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["GET"])
@login_required
def index():
    return "peito"
    
@app.route("/login", methods=["GET"])
@session_activate
def login():
    if request.method == "GET":
        return render_template("login.html")
    
'''@app.route("/index", methods=["POST"])
def indice():
    return jsonify({"message": session["user_id"]})

@app.route("/register", methods=["GET"])
@session_activate
def register():
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/libros", methods=["POST"])
def libros():
    respuesta = request.get_json()
    a = respuesta['value']
    lista = ["elo", "1", 4]
    info = []
    info_json = []
    if(respuesta['option'] == "Por su isbn"):
        info = db.execute(f"SELECT * FROM books WHERE isbn iLIKE '%{respuesta['value']}%' LIMIT 10").fetchall()
        #volvemos los datos una lista de diccionarios para luego convertirlo a json
        info=[dict(row) for row in info]
        #info_json = json.dumps(info, indent=2)
    elif(respuesta['option'] == "Por titulo"):
        info = db.execute(f"SELECT * FROM books WHERE titulo iLIKE '%{respuesta['value']}%' LIMIT 10").fetchall()
        #volvemos los datos una lista de diccionarios para luego convertirlo a json
        info=[dict(row) for row in info]
    elif(respuesta['option'] == "Por autor"):
        info = db.execute(f"SELECT * FROM books WHERE autor iLIKE '%{respuesta['value']}%' LIMIT 10").fetchall()
        #volvemos los datos una lista de diccionarios para luego convertirlo a json
        info=[dict(row) for row in info]
    return jsonify(info)

@app.route("/registerDatosInput", methods=["POST"])
def registerA():
    rq = request.get_json() #espera un json como datos de entrada
    username = rq["username"]
    password =  generate_password_hash(rq["password"])
    confirmacion_usuario = db.execute("SELECT username FROM clients WHERE username=:username", {"username": username}).fetchall()
    if(len(confirmacion_usuario) > 0):  #ya existe el user en la db
        return jsonify({"message":"El nombre de usuario " + username + " ya esta en uso, por favor escoge otro", "redirect": "/register"})
    else:
        oki = db.execute("INSERT INTO clients (name, password, username) VALUES(:name, :password, :username)", {"name": rq["name"], "password": password, "username":username})
        db.commit()
        session["user_id"] = username
        return jsonify({"message": "Registro exitoso ✅", "redirect": "/"})

@app.route("/login", methods=["GET"])
@session_activate
def login():
    if request.method == "GET":
        return render_template("login.html")

@app.route("/welcomeDatos", methods=["POST"])
def welcomeDatos():
    resultados = request.get_json()
    num = resultados['numero']
    lista = []
    for i in range(10):
        r = db.execute("SELECT titulo,isbn FROM books WHERE id_books=:id", {"id": num}).fetchall()
        info=[dict(row) for row in r]
        lista.append(info[0])
        num+=1
    return jsonify(lista)

@app.route("/loginDatos", methods=["POST"])
def loginDatos():
    resultados = request.get_json()
    username = resultados["username"]
    usuario = db.execute("SELECT username FROM clients WHERE username=:username", {"username":username}).fetchall()
    #usuario no existe
    if(len(usuario) !=1):
        return jsonify({"message":"El usuario no existe por favor registrate para continuar", "redirect":"/register", "bool": "false"})
    #usuario existente
    else:
        password = resultados["password"]
        password_confirmation = db.execute("SELECT password FROM clients WHERE username=:username", {"username": username}).fetchone()
        p = check_password_hash(password_confirmation[0], password)
        if p == True:
            session["user_id"] = username
            return jsonify({"message": "contraseñas coinciden 💖", "redirect":"/", "bool": "true"})
        else:
            return jsonify({"message": "contraseñas no coinciden :(", "redirect":"/login", "bool":"false"})

@app.route("/<string:isbn>", methods = ["GET", "POST"])
def hola(isbn):
    if request.method == "GET":
        response = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:"+isbn).json()
        requestDB = db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn": isbn}).fetchall()
        if response['totalItems'] == 0:
            return render_template("libro.html", nombre = requestDB[0]['titulo'], a=isbn, autor=requestDB[0]['autor'])
        
        #obtenemos los comentarios del libro
        comentarios = db.execute("SELECT * from reviews JOIN clients ON reviews.id_usuario=clients.id_clients where isbn=:isbn", {"isbn": isbn}).fetchall()
        respuesta = response['items'][0]['volumeInfo']['title']
        autor = response['items'][0]['volumeInfo']['authors'][0]
        parrafo = response['items'][0]['volumeInfo']['description']
        category = response['items'][0]['volumeInfo']['categories'][0]
        pages = response['items'][0]['volumeInfo']['pageCount']
        try:
            rating = response['items'][0]['volumeInfo']['averageRating']
        except KeyError:
            rating=0

        # if not response['items'][0]['volumeInfo']['averageRating']:
        # else:
        #     rating = response['items'][0]['volumeInfo']['averageRating']
        fecha =  response['items'][0]['volumeInfo']['publishedDate']
        isbn=  response['items'][0]['volumeInfo']['industryIdentifiers'][0]['identifier']
        img = ''
        if rating == 0:
            img = "Parece que no hay ratings :("
        elif rating >= 1 and rating < 2:
            img = "one-star.png"
        elif rating >= 2 and rating < 3:
            img = "two-stars.png"
        elif rating >= 3 and rating < 4:
            img = "three-stars.png"
        elif rating >= 4 and rating < 5:
            img = "four-stars.png"
        else:
            img = "rating.png"
        if(len(comentarios) == 0):
            return render_template("libro.html", nombre = respuesta,  a=isbn, autor=autor, parrafo=parrafo, category=category, pages=pages, rating = rating, img = img, fecha = fecha, isbn=isbn, texto="Parece que nadie ha dejado un comentado :(")
        else:
            comments = []
            for i in comentarios: 
                dicci = {"user": i[8], "review": i[2], "stars": i[4]}
                comments.append(dicci)
            return render_template("libro.html", nombre = respuesta,  a=isbn, autor=autor, parrafo=parrafo, category=category, pages=pages, rating = rating, img = img, fecha = fecha, isbn=isbn, comments= comments)
    else:
        a = request.get_json()
        entrada = a["input"]
        select = a["selectedOption"]
        stars = 0
        if(select == "one"):
            stars = 1
        elif(select == "two"):
            stars = 2
        elif(select == "three"):
             stars = 3
        elif(select == "four"):
             stars = 4
        elif(select == "five"):
             stars = 5
        a = db.execute("SELECT id_clients from clients where username=:name", {"name": session["user_id"]}).fetchall()
        id_clients = a[0][0]
        result = db.execute("SELECT id_usuario from reviews WHERE id_usuario=:id_usuario and isbn=:isbn", {"id_usuario": id_clients, "isbn":isbn}).fetchall()
        if(len(result) == 1):
             return jsonify({"mensaje": "Solo puedes subir un comentario por libro"})
        else:
             db.execute("INSERT INTO reviews(review, stars, id_usuario, ISBN) VALUES(:review, :stars, :id_usuario,:ISBN)", {"review":entrada, "stars": stars, "id_usuario": id_clients, "ISBN": isbn})
             db.commit()
             return jsonify({"mensaje":"subido" })'''