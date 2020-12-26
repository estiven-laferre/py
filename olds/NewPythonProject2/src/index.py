from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flaskext.mysql import MySQL
app = Flask (__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'userr'

app.config['MYSQL_DATABASE_DB'] = 'contactoss'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)
app.secret_key='mysece'
@app.route('/')
def home():
       
        return render_template('newhtml.html')

@app.route('/about')
def about ():
        cur = mysql.connect()
        curssor=cur.cursor()
        curssor.execute('SELECT * FROM conta')
       
        data=curssor.fetchall()
        
        return render_template('about.html',conta = data)
@app.route('/reg', methods=['POST'])
def reg ():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        
        
        cur = mysql.connect()
        cursor=cur.cursor()
        cursor.execute('INSERT INTO conta (fullname, phone, email) VALUES (%s,%s,%s)',
        (fullname, phone, email))
        cursor.execute('commit work;')
        flash('contanto agragado')
        
        return  redirect(url_for('about'))
@app.route('/borrar/<string:id>')
def borrar (id):
        cur = mysql.connect()
        cursor=cur.cursor()
        cursor.execute('DELETE FROM conta WHERE id = {0}'. format(id))
        cursor.execute('commit work;')
        flash('contanto elemenadoi')
        
        return  redirect(url_for('about'))
        
@app.route('/editar/<id>')
def editar(id):
        cur = mysql.connect()
        curssor=cur.cursor()
        curssor.execute('SELECT * FROM conta WHERE id = %s ',(id))
       
        data=curssor.fetchall()
        
        return render_template('editar.html',conta = data[0])
@app.route('/actu/<id>',methods=['POST'])
def actu(id):
     if request.method == 'POST':
        fullname= request.form['fullname']
        phone= request.form['phone']
        email= request.form['email']
        cur = mysql.connect()
        curssor=cur.cursor()
        curssor.execute(""" 
        UPDATE conta
        SET fullname=%s,
        phone = %s,
        email = %s 
        WHERE  id = %s 
        """, (fullname,phone,email,id))
        curssor.execute('commit work;')
        flash('actualizado')
        return  redirect(url_for('about'))
@app.route('/texto')
def homer():
       
        return render_template('texto.html')

app.run(debug=True)
    
