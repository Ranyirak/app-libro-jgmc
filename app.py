##################################################################################################
from flask import Flask, render_template, request, redirect
from flask.templating import render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://gbfqhjpwdaxekz:672f77b4a4a451769c1dd9aedd4ef0e457c6ce8d1025a709713c274e30d2ebf9@ec2-3-211-228-251.compute-1.amazonaws.com:5432/d11s3e4i12k8gc"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

##################################################################################################
#Creacion de las tablas para la base de datos

#Tabla de Usuarios
class Usuarios(db.Model):
    __tablename__ = "usuarios"
    id_usuario = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(255))

    def __init__(self, email, password):
        self.email = email
        self.password = password

#Tabla de Editorial
class Editorial(db.Model):
    __tablename__ = "editorial"
    id_editorial = db.Column(db.Integer, primary_key=True)
    nombre_editorial = db.Column(db.String(80))

    def __init__(self, nombre_editorial):
        self.nombre_editorial = nombre_editorial

#Tabla de Autores
class Autor(db.Model):
    __tablename__ = "autor"
    id_autor = db.Column(db.Integer, primary_key=True)
    nombre_autor = db.Column(db.String(80))
    fecha_nac = db.Column(db.Date)
    nacionalidad = db.Column(db.String(80))

    def __init__(self, nombre_autor, fecha_nac, nacionalidad):
        self.nombre_autor = nombre_autor
        self.fecha_nac = fecha_nac
        self.nacionalidad = nacionalidad

#Tabla de genero
class Genero(db.Model):
    __tablename__ = "genero"
    id_genero = db.Column(db.Integer, primary_key=True)
    nombre_genero = db.Column(db.String(80))

    def __init__(self, nombre_genero):
        self.nombre_genero = nombre_genero

#Tabla de Libros
class Libro(db.Model):
    __tablename__ = "libro"
    id_libro = db.Column(db.Integer, primary_key=True)
    titulo_libro = db.Column(db.String(80))
    fecha_publicacion = db.Column(db.Date)
    numero_paginas = db.Column(db.Integer)
    formato = db.Column(db.String(30))
    volumen = db.Column(db.Integer)

    id_editorial = db.Column(db.Integer, db.ForeignKey("editorial.id_editorial"))
    id_autor = db.Column(db.Integer, db.ForeignKey("autor.id_autor"))
    id_genero = db.Column(db.Integer, db.ForeignKey("genero.id_genero"))

    def __init__(self, titulo_libro, fecha_publicacion, numero_paginas, formato, volumen, id_editorial, id_autor, id_genero):
        self.titulo_libro = titulo_libro
        self.fecha_publicacion = fecha_publicacion
        self.numero_paginas = numero_paginas
        self.formato = formato
        self.volumen = volumen
        self.id_editorial = id_editorial
        self.id_autor = id_autor
        self.id_genero = id_genero

#Tabla de mis favoritos
class MisFavoritos(db.Model):
    __tablename__ = "misfavoritos"
    id_lista_favoritos = db.Column(db.Integer, primary_key=True)
    id_libro = db.Column(db.Integer, db.ForeignKey("libro.id_libro"))
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuarios.id_usuario"))

    def __init__(self, id_libro, id_usuario):
        self.id_libro = id_libro
        self.id_usuario = id_usuario

##################################################################################################
@app.route('/menu')
def menu():
    return render_template ("menu.html")

##################################################################################################
#Metodo para ir a la pagina de inicio de sesion
@app.route('/')
def index():
    return render_template ("index.html")

#Metodo para iniciar sesion
@app.route('/login', methods=['POST'])
def login():
    email = request.form["email"]
    password = request.form["password"]
    #password_cifrado = bcrypt.generate_password_hash(password)
    consulta_usuario = Usuarios.query.filter_by(email = email).first()
    print(consulta_usuario)
    bcrypt.check_password_hash(consulta_usuario.password, password)
    return redirect('/menu')

###################################################################################################
#Metodo para ir a la pagina de registro para el usuario
@app.route('/register')
def register():
    return render_template("registro.html")

#Metodo para registrar el nuevo usuario
@app.route('/register_user', methods=['POST'])
def register_user():
    email = request.form["email"]
    password = request.form["password"]
    print(email)
    print(password)

    password_cifrado = bcrypt.generate_password_hash(password).decode('utf-8')
    print(password_cifrado)

    usuario = Usuarios(email = email, password = password_cifrado)
    db.session.add(usuario)
    db.session.commit()
    return redirect('/register')

#Metodo para regresar a la pagina de inicio de sesion
@app.route('/sign_in')
def sign_in():
    return redirect('/')

##################################################################################################
#Metodo para ir a la pagina de registro para el editorial
@app.route('/editorial')
def editorial():
    return render_template("editorial.html")

#Metodo para registrar el nuevo editoral
@app.route('/register_editorial', methods=['POST'])
def register_editorial():
    nombre_editorial = request.form["nombre_editorial"]
    print(nombre_editorial)

    editorial_nuevo = Editorial(nombre_editorial = nombre_editorial)
    db.session.add(editorial_nuevo)
    db.session.commit()
    return redirect('/cat_editoriales')

#Metodo para mostrar el catalogo de generos
@app.route("/cat_editoriales")
def cateditoriales():
    consulta_editoriales = Editorial.query.all()
    print(consulta_editoriales)
    for editorial in consulta_editoriales:
        nombre = editorial.nombre_editorial;
        print(nombre)
    return render_template("cat_editoriales.html", consulta = consulta_editoriales)

#Metodo para mandar el query e ir a la pagina para editar el editorial
@app.route('/editareditorial/<id>')
def editareditorial(id):
    editorial = Editorial.query.filter_by(id_editorial = int(id)).first()
    print(editorial)
    return render_template("modificarEdi.html", editorial = editorial)

#Metodo para editar el editorial
@app.route('/modificaredi', methods=['POST'])
def modificaredi():
    id_editorial = request.form["id_editorial"]
    nuevo_nombre = request.form["nombre_editorial"]
    editorial = Editorial.query.filter_by(id_editorial = int(id_editorial)).first()
    editorial.nombre_editorial = nuevo_nombre
    db.session.commit()
    return redirect('/cat_editoriales')

#Metodo para eliminar un editorial del catalogo
@app.route('/eliminaredi/<id>')
def eliminaredi(id):
    editorial = Editorial.query.filter_by(id_editorial = int(id)).delete()
    print(editorial)
    db.session.commit()
    return redirect('/cat_editoriales')

###################################################################################################
#Metodo para ir a la pagina de registro para el autor
@app.route('/autor')
def autor():
    return render_template("autor.html")

#Metodo para registrar el nuevo autor
@app.route('/register_autor', methods=['POST'])
def register_autor():
    nombre_autor = request.form["nombre_autor"]
    fecha_nac = request.form["fecha_nac"]
    nacionalidad = request.form["nacionalidad"]
    print(nombre_autor)
    print(fecha_nac)
    print(nacionalidad)

    autor_nuevo = Autor(nombre_autor = nombre_autor, fecha_nac = fecha_nac, nacionalidad = nacionalidad)
    db.session.add(autor_nuevo)
    db.session.commit()
    return redirect('/cat_autores')

#Metodo para mostrar el catalogo de autores
@app.route("/cat_autores")
def catautores():
    consulta_autores = Autor.query.all()
    print(consulta_autores)
    for autor in consulta_autores:
        nombre = autor.nombre_autor;
        fecha_nacimiento = autor.fecha_nac;
        nacionalidad = autor.nacionalidad;
        print(nombre)
        print(fecha_nacimiento)
        print(nacionalidad)

    return render_template("cat_autores.html", consulta = consulta_autores)

#Metodo para mandar el query e ir a la pagina para editar el autor
@app.route('/editarautor/<id>')
def editarautor(id):
    autor = Autor.query.filter_by(id_autor = int(id)).first()
    print(autor)
    return render_template("modificarAutor.html", autor = autor)

#Metodo para editar el autor
@app.route('/modificarautor', methods=['POST'])
def modificarautor():
    id_autor = request.form["id_autor"]
    nuevo_nombre = request.form["nombre_autor"]
    nueva_fecha = request.form["fecha_nac"]
    nueva_nacionalidad = request.form["nacionalidad"]
    autor = Autor.query.filter_by(id_autor = int(id_autor)).first()
    autor.nombre_autor = nuevo_nombre
    autor.fecha_nac = nueva_fecha
    autor.nacionalidad = nueva_nacionalidad
    db.session.commit()
    return redirect('/cat_autores')

#Metodo para eliminar un autor del catalogo
@app.route('/eliminarautor/<id>')
def eliminarautor(id):
    autor = Autor.query.filter_by(id_autor = int(id)).delete()
    print(autor)
    db.session.commit()
    return redirect('/cat_autores')

###################################################################################################
#Metodo para ir a la pagina de registro para el genero
@app.route('/genero')
def genero():
    return render_template("genero.html")

#Metodo para registrar el nuevo genero
@app.route('/register_genero', methods=['POST'])
def register_genero():
    nombre_genero = request.form["nombre_genero"]
    print(nombre_genero)

    genero_nuevo = Genero(nombre_genero = nombre_genero)
    db.session.add(genero_nuevo)
    db.session.commit()
    return redirect('/cat_generos')

#Metodo para mostrar el catalogo de generos
@app.route("/cat_generos")
def catgeneros():
    consulta_generos = Genero.query.all()
    print(consulta_generos)
    for genero in consulta_generos:
        nombre = genero.nombre_genero;
        print(nombre)
    return render_template("cat_generos.html", consulta = consulta_generos)

#Metodo para mandar el query e ir a la pagina para editar el genero
@app.route('/editargenero/<id>')
def editargenero(id):
    genero = Genero.query.filter_by(id_genero = int(id)).first()
    print(genero)
    return render_template("modificarGen.html", genero = genero)

#Metodo para editar el genero
@app.route('/modificargenero', methods=['POST'])
def modificargenero():
    id_genero = request.form["id_genero"]
    nuevo_nombre = request.form["nombre_genero"]
    genero = Genero.query.filter_by(id_genero = int(id_genero)).first()
    genero.nombre_genero = nuevo_nombre
    db.session.commit()
    return redirect('/cat_generos')

#Metodo para eliminar un genero del catalogo
@app.route('/eliminargenero/<id>')
def eliminargenero(id):
    genero = Genero.query.filter_by(id_genero = int(id)).delete()
    print(genero)
    db.session.commit()
    return redirect('/cat_generos')

###################################################################################################
#Metodo para ir a la pagina de registro para el libro
@app.route('/libro')
def libro():
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    consulta_autor = Autor.query.all()
    print(consulta_autor)
    consulta_genero = Genero.query.all()
    print(consulta_genero)
    return render_template ("libro.html", consulta_editorial = consulta_editorial, consulta_autor = consulta_autor, consulta_genero = consulta_genero)

#Metodo para registrar el nuevo libro
@app.route('/registrar_libro', methods=['POST'])
def registrar_libro():
    titulo_libro = request.form["titulo_libro"]
    fecha_publicacion = request.form["fecha_publicacion"]
    numero_paginas = request.form["numero_paginas"]
    formato = request.form["formato"]
    volumen = request.form["volumen"]
    id_editorial = request.form["editorial"]
    id_autor = request.form["autor"]
    id_genero = request.form["genero"]

    libro_nuevo = Libro(titulo_libro = titulo_libro, fecha_publicacion = fecha_publicacion, numero_paginas = numero_paginas, formato = formato, volumen = volumen, id_editorial = id_editorial, id_autor = id_autor, id_genero = id_genero)
    db.session.add(libro_nuevo)
    db.session.commit()
    return redirect('/cat_libros')

#Metodo para mostrar el catalogo de libros
@app.route("/cat_libros")
def catlibros():
    consulta_libros = Libro.query.join(Editorial, Libro.id_editorial == Editorial.id_editorial).join(Autor, Libro.id_autor == Autor.id_autor).join(Genero, Libro.id_genero == Genero.id_genero).add_columns(Libro.titulo_libro, Libro.fecha_publicacion, Libro.numero_paginas, Libro.formato, Libro.volumen, Editorial.nombre_editorial, Autor.nombre_autor, Genero.nombre_genero, Libro.id_libro)
    return render_template("cat_libros.html", consulta = consulta_libros)

#Metodo para mandar el query e ir a la pagina para editar el libro
@app.route('/editarlibro/<id>')
def editarlibro(id):
    libro = Libro.query.filter_by(id_libro = int(id)).first()
    print(libro)
    consulta_editorial = Editorial.query.all()
    print(consulta_editorial)
    consulta_autor = Autor.query.all()
    print(consulta_autor)
    consulta_genero = Genero.query.all()
    print(consulta_autor)
    return render_template("modificarLibro.html", libro = libro, consulta_editorial = consulta_editorial, consulta_autor = consulta_autor, consulta_genero = consulta_genero)

#Metodo para editar el libro
@app.route('/modificarlibro', methods=['POST'])
def modificarlibro():
    id_libro = request.form["id_libro"]
    nuevo_titulo = request.form["titulo_libro"]
    nueva_fecha = request.form["fecha_publicacion"]
    nueva_pagina = request.form["numero_paginas"]
    nuevo_formato = request.form["formato"]
    nueva_volumen = request.form["volumen"]
    nuevo_editorial = request.form["editorial"]
    nuevo_autor = request.form["autor"]
    nuevo_genero = request.form["genero"]

    libro = Libro.query.filter_by(id_libro = int(id_libro)).first()
    libro.titulo_libro = nuevo_titulo
    libro.fecha_publicacion = nueva_fecha
    libro.numero_paginas = nueva_pagina
    libro.formato = nuevo_formato
    libro.volumen = nueva_volumen
    libro.id_editorial = nuevo_editorial
    libro.id_autor = nuevo_autor
    libro.id_genero = nuevo_genero
    db.session.commit()
    return redirect('/cat_libros')

#Metodo para eliminar un genero del libro
@app.route('/eliminarlibro/<id>')
def eliminarlibro(id):
    libro = Libro.query.filter_by(id_libro = int(id)).delete()
    print(libro)
    db.session.commit()
    return redirect('/cat_libros')

#Metodo para agregar un libro a favoritos
@app.route('/agregarfav/<id>')
def agregarlibro(id):
    libro = Libro.query.filter_by(id_libro = int(id)).first()
    favorito = MisFavoritos.query.order_by(MisFavoritos.id_lista_favoritos.desc()).first
    id_libro = libro.id_libro
    id_usuario = int(1)
    id_favorito = favorito.id_lista_favoritos
    nuevo_id_favoritos = id_favorito+1
    nuevo_favorito = MisFavoritos(id_lista_favoritos = nuevo_id_favoritos, id_libro = id_libro, id_usuario = id_usuario)
    db.session.add(nuevo_favorito)
    db.session.commit()
    return redirect('/cat_libros')

###################################################################################################
#Metodo para ir a la pagina de misfavoritos
@app.route('/misfavoritos')
def misfavoritos():
    consulta_fav = MisFavoritos.query.join(Libro, MisFavoritos.id_libro == Libro.id_libro).join(Usuarios, MisFavoritos.id_usuario == Usuarios.id_usuario).add_columns(Libro.titulo_libro, Libro.id_libro)
    return render_template("misfavoritos.html", consulta = consulta_fav)

#Metodo para eliminar un libro de favoritos
@app.route('/eliminarfav/<id>')
def eliminarfav(id):
    favorito = MisFavoritos.query.filter_by(id_libro = int(id)).delete()
    print(favorito)
    db.session.commit()
    return redirect('/misfavoritos')

###################################################################################################
if __name__ == "__main__":
    db.create_all()
    app.run()#debug=True

###################################################################################################