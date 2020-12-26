from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import make_response
from flask import session
from flaskext.mysql import MySQL
from flask import jsonify
import i18n
i18n.load_path.append('i18n')

i18n.set('locale', 'es')

print(i18n.t('foo.his'))
print(i18n.t('foo.hi'))

print( i18n.t('foo.mail_number',count=2) # You do not have any mail.
        
)



app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'esti'
app.config['MYSQL_DATABASE_DB'] = 'basses'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
app.secret_key = 'mysece'


@app.route('/')
def home():
      
        return render_template('login.html')

         
#registro de nuevos usuarios
@app.route('/registro')
def registro():
        return render_template('registro.html')

@app.route('/registrar', methods=['POST'])
def registrar():
        if request.method == 'POST':
                name = request.form['nom']
                apell = request.form['apell']
                nickname = request.form['user_name']
                passw = request.form['pass']
                fecha_nacimiento = request.form['nacimiento']

                cur = mysql.connect()
                curssor = cur.cursor()
                curssor.execute('INSERT INTO usersz (nom,apell,user_name,pass,fecha_nacimiento) VALUES(%s , %s , %s , %s , %s)', (
                    name, apell, nickname, passw, fecha_nacimiento))
                curssor.execute('commit work;')
                flash('Usario registrado')

                return redirect(url_for('home'))
 #logueado de usarios
@app.route('/login', methods=['POST'])
def login():
        if request.method == 'POST':
                name = request.form['user']
                passw = request.form['pass']
                try:

                        cur = mysql.connect()
                        curssor = cur.cursor()
                        curssor.execute(
                            'SELECT * FROM usersz WHERE user_name = %s AND pass=%s', (name, passw))
                        data = curssor.fetchall()


                        session['nombre'] = data[0][3]
                        session['id'] = data[0][0]
                        session['admin'] = data[0][6]
                        flash('hola '+data[0][3], "bienvenido")
                        
                        return redirect(url_for('user'))
                except:
                        flash('no sabes como ingresar un usario o que?')

                        return redirect(url_for('home'))

@app.route('/user')
def user():
        #llamando a los productos
                        cur = mysql.connect()
                        curssor = cur.cursor()
                        curssor.execute('SELECT * FROM productos')
                        data_pro = curssor.fetchall()
                        session['last_page'] = url_for('user')
                        
                        return render_template('user.html', products=data_pro , admin=session.get('admin'))
@app.route('/registrar_producto', methods=['POST'])
def registrar_producto():
        #Ingreso de nuevo producto
        if request.method == 'POST':
                pro = request.form['pro']
                pre = request.form['pre']
                cant = request.form['cant']
                nombre_usuario = session.get('nombre')

                cur = mysql.connect()
                curssor = cur.cursor()
                curssor.execute(
                    'INSERT INTO productos (nom,precio,cant,user_name) VALUES(%s , %s , %s ,%s)', (pro, pre, cant, nombre_usuario))
                curssor.execute('commit work;')
                flash('Producto agregado')

                return redirect(url_for('user'))
@app.route('/borrar/<string:id>')
def borrar(id):
        cur = mysql.connect()
        cursor = cur.cursor()
        cursor.execute('DELETE FROM productos WHERE id = {0}'. format(id))
        cursor.execute('commit work;')
        flash('elemento eliminado')

        return redirect(url_for('tab_productos'))
# panel admin

@app.route('/user/admin')
def admin():
        if  session['admin'] == 1:
         cur = mysql.connect()
         curssor = cur.cursor()
         curssor.execute('SELECT * FROM usersz')
         datas = curssor.fetchall()
         url=url_for('admin')
         session['last_page']=url
         return render_template('admin.html', users=datas)
        else:
                return "noquieras hakainos"
# privilegios de ser admin


@app.route('/registrar1', methods=['POST'])
def registrar1():
        if request.method == 'POST':
                name = request.form['nom']
                apell = request.form['apell']
                nickname = request.form['user_name']
                passw = request.form['pass']
                fecha_nacimiento = request.form['nacimiento']

                cur = mysql.connect()
                curssor = cur.cursor()
                curssor.execute('INSERT INTO usersz (nom,apell,user_name,pass,fecha_nacimiento) VALUES(%s , %s , %s , %s , %s)', (
                    name, apell, nickname, passw, fecha_nacimiento))
                curssor.execute('commit work;')
                flash('Usario registrado')

                return redirect(url_for('admin'))
@app.route('/editar_user/<id>')
def editar_Users(id):
        
        cur = mysql.connect()
        curssor=cur.cursor()
        curssor.execute('SELECT * FROM usersz WHERE id = %s ',(id))
       
        data=curssor.fetchall()
        url="/editar_user/"+(id)

        session['last_page']=url

        return render_template('editar.html', user=data[0] )
@app.route('/actu/<string:id>', methods=['POST'])
def actu(id):
 if request.method == 'POST':
        name = request.form['nom']
        apell = request.form['apell']
        nickname = request.form['user_name']
        passw = request.form['pass']
        fecha_nacimiento = request.form['nacimiento']
        try:
                admin=request.form['admina']
        except:
                admin = 0

        cur = mysql.connect()
        curssor=cur.cursor()
        curssor.execute(""" 
        UPDATE usersz
        SET nom=%s ,apell=%s ,user_name=%s ,pass=%s ,fecha_nacimiento=%s , admin=%s
        WHERE  id = %s 
        """, (name, apell, nickname, passw, fecha_nacimiento,admin,id))
        curssor.execute('commit work;')
        flash('actualizado')

        return  redirect(url_for('admin'))
@app.route('/borrar_user/<string:id>')
def borrar_users(id):
        cur = mysql.connect()
        cursor = cur.cursor()
        cursor.execute('DELETE FROM usersz WHERE id = {0}'. format(id))
        cursor.execute('commit work;')
        flash('elemento eliminado')

        return redirect(url_for('admin'))
@app.route('/login/cuenta')
def cuenta():
        flash('', "cuenta")
        
       
        return redirect(session.get('last_page')) 
app.run(debug=True)
