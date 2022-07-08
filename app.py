from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL


mysql=MySQL()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('proveedores/index.html')

if __name__=='__main__':
 app.run(debug=True)
