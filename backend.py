from flask import Flask,render_template,request,redirect, session,url_for
import sqlite3

slambook = Flask(__name__)
slambook.secret_key='nitt'
con = sqlite3.connect('slambook.db')
con.execute('create table if not exists users(username text, branch text, hostel text, password text)')
con.close()

@slambook.route('/')
def login():
    return render_template('index.html')

@slambook.route('/homepage',methods=['POST','GET'])
def homepage():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        con = sqlite3.connect('slambook.db')
        con.row_factory=sqlite3.Row
        cur = con.cursor()
        cur.execute('select * from users where username=? and password=?',(username,password))
        data = cur.fetchone()

        if data:
            session['username']=data['username']
            session['password']=data['password']
            return redirect('newsfeed')
        else:        
            return redirect(url_for('login'))   

@slambook.route('/newsfeed',methods=['POST','GET'])
def newsfeed():
    return render_template('newsfeed.html')

@slambook.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        try:
            username=request.form['username']
            branch=request.form['branch']
            hostel=request.form['hostel']
            password=request.form['password']
            con=sqlite3.connect("slambook.db")
            cur=con.cursor()
            cur.execute("insert into users(username,branch,hostel,password)values(?,?,?,?)",(username,branch,hostel,password))
            con.commit()
            con.close()
        finally:
            return redirect(url_for("login"))        
    return render_template('register.html')

@slambook.route('/logout',methods=['POST','GET'])
def logout():
    if request.method=='POST':
        return redirect(url_for('login'))

@slambook.route('/searcheduser',methods=['POST','GET'])
def search():
    if request.method=='POST':
        searched_user=request.form['search']
        print(searched_user)
        con = sqlite3.connect('slambook.db')
        cur = con.cursor()
        cur.execute('select * from users where username=?',(searched_user,))
        info = cur.fetchone()
        if info:
            session['searched_user']=info['username']
            print('not found')
            return render_template('otherusers.html')
        else:
            return redirect(url_for('newsfeed'))    

if __name__ == '__main__':
    slambook.run(debug=True)
    