import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
#carga las variables de entorno, en donde va incluida la uri a la db
load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
def main():
    #db.execute("CREATE TABLE books(id_books SERIAL PRIMARY KEY, ISBN VARCHAR(255), Titulo VARCHAR(255), Autor VARCHAR(255), Anio_publicacion VARCHAR(255))")
    f = open("books.csv")
    i = 0
    filas = csv.reader(f)
    for isbn, title, author, year in filas:
        if i == 0:
            i+=1
        elif i != 0:
            db.execute("INSERT INTO books (isbn, titulo, autor, anio_publicacion) VALUES (:isbn, :titulo, :autor, :anio)",
                    {"isbn":isbn, "titulo":title, "autor":author, "anio":year})
    db.commit()

if __name__ == "__main__":
    main()
