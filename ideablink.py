#modules
import MySQLdb
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import md5
from config import *


#start app
app = Flask(__name__)
app.config.from_object(__name__)


#app functions
@app.before_request
def before_request():
        g.db = MySQLdb.connect(host='localhost',user='root',passwd=DBPWD,db='ideablink')


@app.after_request
def after_request(response):
        g.db.commit()
        g.db.close()
        return response


@app.route('/post')
def post():
        if 'username' in session:
                username = session['username']
                return render_template('addlink.html', username=username)
        return redirect(url_for('login'))


@app.route('/add', methods =['POST'])
def add_entry():
        username = session['username']
        cur = g.db.cursor()
        test_form = request.form['entrylink']
        test_form2 = request.form['entryblurb']
        cur.execute("""INSERT INTO main (entry_link, entry_blurb, username) VALUES (%s, %s, %s)""", (test_form, test_form2, username))
        #cur.execute('INSERT INTO main (entry_link_ values (''test'')')#, (request.form['entrylink']))
        return redirect(url_for('show_entries'))


@app.route('/favorite/<id>')
def make_favorite(id):
        username = session['username']
        cur = g.db.cursor()
        cur.execute("""UPDATE main SET favorite = 1 WHERE id = %s""", (id))
        return redirect(url_for('show_user', username=username))


@app.route('/remfavorite/<id>')
def rem_favorite(id):
        username = session['username']
        cur = g.db.cursor()
        cur.execute("""UPDATE main SET favorite = 0 WHERE id = %s""", (id))
        return redirect(url_for('show_user', username=username))


@app.route('/')
def show_entries():
        cur = g.db.cursor()
        cur.execute('SELECT entry_link, entry_blurb, entry_date, username FROM main ORDER BY id DESC LIMIT 15') #currently limit to 15..should be configurable by user
        entry_fetch = cur.fetchall()
        entries = [dict(entry_link=row[0], entry_blurb=row[1], entry_date=row[2],entry_username=row[3]) for row in entry_fetch]
        return render_template('main.html', entries=entries)


@app.route('/<username>')
def show_user(username):
        cur = g.db.cursor()
        cur.execute('SELECT entry_link, entry_blurb, entry_date, id, favorite FROM main WHERE username=%s ORDER BY id DESC',(username))
        entry_fetch = cur.fetchall()
        entries = [dict(entry_link=row[0], entry_blurb=row[1], entry_date=row[2], entry_id=row[3], entry_favorite=row[4]) for row in entry_fetch]
        return render_template('user.html', entries=entries, user=username)


@app.route('/<username>/favorites')
def show_user_favorites(username):
        cur = g.db.cursor()
        cur.execute('SELECT entry_link, entry_blurb, entry_date, id FROM main WHERE username=%s  AND favorite = 1 ORDER BY id DESC',(username))
        entry_fetch = cur.fetchall()
        entries = [dict(entry_link=row[0], entry_blurb=row[1], entry_date=row[2], entry_id=row[3]) for row in entry_fetch]
        return render_template('user.html', entries=entries, user=username)


@app.route('/login', methods=['GET','POST'])
def login():
        if 'username' in session:
                return redirect(url_for('post'))
        else:
                error = None
                if request.method == 'POST':
                        username_entry = request.form['username']
                        cur = g.db.cursor()
                        cur.execute("""SELECT password FROM users WHERE username=%s""",(username_entry))
                        results = cur.fetchall()
                        password_entry = results[0][0]
                        if md5.new(request.form['password']).hexdigest() != password_entry:
                                error = 'Invalid Password'
                        else:
                                session['logged_in'] = True
                                session['username'] = request.form['username']
                                flash('You were logged in')
                                return redirect(url_for('post'))
        return render_template('login.html', error=error)


@app.route('/logout')
def logout():
        session.pop('logged_in', None)
        session.pop('username', None)
        flash('You were logged out')
        return redirect(url_for('show_entries'))


@app.route('/register')
def register():
        return render_template('register.html')


@app.route('/add_user', methods=['POST'])
def add_user():
        error = False
        cur = g.db.cursor()
        form_username = request.form['username']
        form_email = request.form['email']
        form_password = request.form['password']
        cur.execute("""SELECT COUNT(username) FROM users WHERE username=%s""", (form_username))
        entry_fetch = cur.fetchall()
        for row in entry_fetch:
                entry = row[0]
        #check against list of usernames we want to prevent registering as
        if form_username in ['test','hashsquid','add','register','login','about','faq','ryan','squid',
                             'commons','home']:
                entry = 'bad'
        if len(form_username) < 6:
                entry = 'bad'
        if entry == 0:
                pass
                cur.execute("""INSERT INTO users (username, password) values (%s,%s)""",(form_username, md5.new(form_password).hexdigest()))
        else:
                return render_template('register.html', error='Try again.')
        return '%s, %s, %s, %s' % (form_username, form_email, form_password, entry)


@app.route('/about')
def about():
        return render_template('about.html') 


@app.route('/faqs')
def faqs():
        return render_template('faqs.html')


if __name__ == '__main__':
        app.run(host = HOST, debug=True)
