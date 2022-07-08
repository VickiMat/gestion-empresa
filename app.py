
from flask import Flask
from flask import render_template,request,redirect,url_for,flash
from flask import send_from_directory
from flaskext.mysql import MySQL
from datetime import datetime
import os


mysql=MySQL()
app = Flask(__name__)
app.secret_key="ClaveSecreta"
#CONEXION DB
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='gestion_empresa'
mysql.init_app(app)

CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)

#MOSTRAR
@app.route('/')
def index():
    sql = "SELECT * FROM `gestion_empresa`.`proveedores`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    proveedores=cursor.fetchall()
    print(proveedores)
    conn.commit()

    return render_template('proveedores/index.html', proveedores=proveedores)

#ELIMINAR
@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT foto FROM `gestion_empresa`.`proveedores` WHERE id=%s",
id)
    
    fila= cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))

    cursor.execute("DELETE FROM `gestion_empresa`.`proveedores` WHERE id=%s", (id))
    conn.commit()

    return redirect('/')

#EDITAR
@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `gestion_empresa`.`proveedores` WHERE id=%s", (id))
    proveedores=cursor.fetchall()
    conn.commit()

    return render_template('proveedores/edit.html', proveedores=proveedores)

@app.route('/update', methods=['POST'])
def update():
    _nombre=request.form['txtNombre']
    _descripcion=request.form['txtDescripcion']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    id=request.form['txtID']

    sql = "UPDATE `gestion_empresa`.`proveedores` SET `nombre`=%s, `descripcion`=%s, `correo`=%s WHERE id=%s;"
    datos=(_nombre,_descripcion,_correo,id)
    conn = mysql.connect()
    cursor = conn.cursor()

    now= datetime.now()
    tiempo= now.strftime("%Y%H%M%S")
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)
        cursor.execute("SELECT foto FROM `gestion_empresa`.`proveedores` WHERE id=%s", id)
        fila= cursor.fetchall()
        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE `gestion_empresa`.`proveedores` SET foto=%s WHERE id=%s", (nuevoNombreFoto, id))
        conn.commit()

    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')

#CREAR
@app.route('/create')
def create():
 return render_template('proveedores/create.html')


@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _descripcion=request.form['txtDescripcion']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
    if _nombre == '' or _descripcion == '' or _correo == '' or _foto =='':
        flash('Recuerda llenar los datos de los campos')
        return redirect(url_for('create'))

    now= datetime.now()
    tiempo= now.strftime("%Y%H%M%S")
    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)


    sql = "INSERT INTO `gestion_empresa`.`proveedores` (`id`, `nombre`,`descripcion`,`correo`, `foto`) VALUES (NULL, %s, %s, %s, %s);"
    datos=(_nombre,_descripcion,_correo,nuevoNombreFoto)
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')



if __name__=='__main__':
 app.run(debug=True)