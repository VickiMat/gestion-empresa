
from flask import Flask
from flask import render_template,request
from flaskext.mysql import MySQL
from datetime import datetime


mysql=MySQL()

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_BD']='gestion_empresa'
mysql.init_app(app)

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


@app.route('/create')
def create():
 return render_template('proveedores/create.html')


@app.route('/store', methods=['POST'])
def storage():
    _nombre=request.form['txtNombre']
    _descripcion=request.form['txtDescripcion']
    _correo=request.form['txtCorreo']
    _foto=request.files['txtFoto']
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

    return render_template('proveedores/index.html')



if __name__=='__main__':
 app.run(debug=True)