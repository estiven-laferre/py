from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flaskext.mysql import MySQL
app = Flask (__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'estiven'

app.config['MYSQL_DATABASE_DB'] = 'tareas'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
app.secret_key='mysece'
@app.route('/')
def home():
       
        return render_template('my page.html')
        
@app.route('/registro')
def regi ():
        cur = mysql.connect()
        curssor=cur.cursor()
       
        curssor.execute('SELECT * FROM users ')
        
        data=curssor.fetchall()
        
        return render_template('registro.html',users = data)
        
@app.route('/reg', methods=['POST'])
def reg ():
       if request.method == 'POST':
        name = request.form['name']
        passw = request.form["passw"]
       
        
        
        cur = mysql.connect()
        curssor=cur.cursor()
        curssor.execute('INSERT INTO users (name , passw) VALUES (%s,%s)',(name,passw))
        curssor.execute('commit work;')
        flash('contanto agragado')

        return  redirect(url_for('regi'))
@app.route('/veri',methods=['POST'])
def veri (name,passw):
       if request.method == 'POST':
        name = request.form['name']
        passw = request.form['passw']

        cur = mysql.connect()
        curssor=cur.cursor()
        
        curssor.execute('SELECT * FROM users WHERE name=%s AND passw=%s',(name,passw) )
        curssor.execute('commit work;')

        data=curssor.fetchall()

       return render_template('registro.html',users = data[0])
app.run(debug=True)