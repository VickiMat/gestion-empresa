
from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL


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
    sql = ""
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    return render_template('proveedores/index.html')

@app.route('/create')
def create():
 return render_template('proveedores/create.html')

if __name__=='__main__':
 app.run(debug=True)