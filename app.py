from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Curso, Alumno, Anecdotario, Anotacion

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///colegio.db'
db.init_app(app)

@app.route('/')
def index():
    # cursos = Curso.query.all()
    # print(cursos)
    #return render_template('index.html', cursos=cursos)
    return render_template('index.html')

@app.route('/anotacion')
def admin_anotacion():
    cursos = Curso.query.all()
    print(cursos)
    return render_template('admin_anotacion.html', cursos=cursos)

@app.route('/curso/<int:id_curso>')
def listar_alumnos(id_curso):
    curso = Curso.query.get_or_404(id_curso)
    alumnos = Alumno.query.filter_by(curso=id_curso).all()
    return render_template('alumnos.html', curso=curso, alumnos=alumnos)

@app.route('/agregar_alumno', methods=['POST'])
def agregar_alumno():
    nombre = request.form.get('nombre')
    nro = request.form.get('nro_lista')
    id_curso = request.form.get('id_curso')
    nuevo = Alumno(nombre=nombre, nro_lista=nro, curso=id_curso)
    db.session.add(nuevo)
    db.session.commit()
    return redirect(url_for('listar_alumnos', id_curso=id_curso))

@app.route('/anotacion/nuevo/<int:id_alumno>')
def vista_agregar_anotacion(id_alumno):
    # Buscamos al alumno para mostrar su nombre en el formulario
    alumno = Alumno.query.get_or_404(id_alumno)
    # Obtenemos los tipos de anécdota disponibles en la BD
    tipos_anecdota = Anecdotario.query.all()
    print(len(tipos_anecdota))
    return render_template('agregar_anotacion.html', alumno=alumno, tipos_anecdota=tipos_anecdota)


@app.route('/anotacion/guardar', methods=['POST'])
def guardar_anotacion():
    # Obtenemos los datos del formulario
    id_alumno = request.form.get('id_alumno')
    id_anecdota = request.form.get('id_anecdota')
    descripcion = request.form.get('descripcion')
    
    # Creamos una nueva instancia del modelo Anotacion
    # La fecha se asignará automáticamente si tu modelo la tiene definida con default=datetime.utcnow
    nueva_anotacion = Anotacion(
        id_alumno=id_alumno,
        id_anecdota=id_anecdota,
        descripcion=descripcion
    )
    
    # Guardamos en la base de datos
    db.session.add(nueva_anotacion)
    db.session.commit()
    
    # Redirigimos al usuario a la lista de alumnos del curso correspondiente
    # Primero buscamos el alumno para saber a qué curso pertenece
    alumno = Alumno.query.get(id_alumno)
    
    return redirect(url_for('listar_alumnos', id_curso=alumno.curso))

# Administración de Cursos ABM de cursos
@app.route('/admin/cursos', methods=['GET', 'POST'])
def admin_cursos():
    if request.method == 'POST':
        nombre = request.form.get('nombre_curso')
        nuevo_curso = Curso(nombre_curso=nombre)
        db.session.add(nuevo_curso)
        db.session.commit()
        return redirect(url_for('admin_cursos'))
    
    cursos = Curso.query.all()
    return render_template('admin_cursos.html', cursos=cursos)

@app.route('/admin/cursos/eliminar/<int:id>')
def eliminar_curso(id):
    curso = Curso.query.get_or_404(id)
    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for('admin_cursos'))

@app.route('/admin/cursos/editar/<int:id>', methods=['GET', 'POST'])
def editar_curso(id):
    curso = Curso.query.get_or_404(id)
    if request.method == 'POST':
        curso.nombre_curso = request.form.get('nombre_curso')
        db.session.commit()
        return redirect(url_for('admin_cursos'))
    return render_template('editar_curso.html', curso=curso)

# Administrar alumnos ABM de Alumnos
@app.route('/admin/alumnos', methods=['GET', 'POST'])
def admin_alumnos():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        nro_lista = request.form.get('nro_lista')
        id_curso = request.form.get('id_curso')
        nuevo_alumno = Alumno(nombre=nombre, nro_lista=nro_lista, curso=id_curso)
        db.session.add(nuevo_alumno)
        db.session.commit()
        return redirect(url_for('admin_alumnos'))
    
    alumnos = Alumno.query.all()
    cursos = Curso.query.all()
    return render_template('admin_alumnos.html', alumnos=alumnos, cursos=cursos)

@app.route('/admin/alumnos/eliminar/<int:id>')
def eliminar_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    db.session.delete(alumno)
    db.session.commit()
    return redirect(url_for('admin_alumnos'))

@app.route('/admin/alumnos/editar/<int:id>', methods=['GET', 'POST'])
def editar_alumno(id):
    alumno = Alumno.query.get_or_404(id)
    if request.method == 'POST':
        alumno.nombre = request.form.get('nombre')
        alumno.nro_lista = request.form.get('nro_lista')
        alumno.curso = request.form.get('id_curso')
        db.session.commit()
        return redirect(url_for('admin_alumnos'))
    cursos = Curso.query.all()
    return render_template('editar_alumno.html', alumno=alumno, cursos=cursos)

# Administracion del anecdotario: Tipos de anecdotas ABM
@app.route('/admin/anecdotas', methods=['GET', 'POST'])
def admin_anecdotas():
    if request.method == 'POST':
        desc = request.form.get('descripcion')
        nueva = Anecdotario(descripcion=desc)
        db.session.add(nueva)
        db.session.commit()
        return redirect(url_for('admin_anecdotas'))
    
    lista = Anecdotario.query.all()
    return render_template('admin_anecdotas.html', tipos=lista)

@app.route('/admin/anecdotas/eliminar/<int:id>')
def eliminar_anecdota(id):
    item = Anecdotario.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('admin_anecdotas'))

@app.route('/admin/anecdotas/editar/<int:id>', methods=['GET', 'POST'])
def editar_anecdota(id):
    item = Anecdotario.query.get_or_404(id)
    if request.method == 'POST':
        item.descripcion = request.form.get('descripcion')
        db.session.commit()
        return redirect(url_for('admin_anecdotas'))
    return render_template('editar_anecdota.html', item=item)


if __name__ == "__main__":
    with app.app_context():
        db.create_all() # Esto crea las tablas si no existen

    app.run(debug=True)