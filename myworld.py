from flask import Flask, render_template, json, request, redirect, session, abort, flash, url_for
from flask.ext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.secret_key = '101'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'CDMA1xafri'
app.config['MYSQL_DATABASE_DB'] = 'web101'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()

app.config['USERNAME'] = 'test'
app.config['PASSWORD'] = 'test'


@app.route('/')
def show_entries():
    sql = 'select id ,title, post from entries order by id desc'
    cursor.execute(sql)
    conn.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], title=row[1], post=row[2]) for row in data]
    return render_template('show_entries.html', entries=entries)


@app.route('/show_entry/<int:id>')
def show_entry(id):
    id = str(id)
    sql = 'select * from entries WHERE id=' + id
    cursor.execute(sql)
    conn.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], title=row[1], post=row[2]) for row in data]
    return render_template('show_entries.html', entries=entries)
    conn.close


@app.route('/edit_entry/<int:id>')
def edit_entry(id):
    id = str(id)
    sql = 'select * from entries WHERE id=' + id
    cursor.execute(sql)
    conn.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], title=row[1], post=row[2]) for row in data]
    # entries = [{"title": row[0], "text": row[1], "id": row[2]} for row in data]
    return render_template('edit_entry.html', entries=entries)
    conn.close


@app.route('/update_entry/<int:id>', methods=['GET', 'POST'])
def update_entry(id):
    id = str(id)
    title = request.form['title']
    post = request.form['post']
    data = (title, post)
    sql = 'UPDATE entries SET title =%s,post=%s  WHERE id=' + id
    cursor.execute(sql, data)
    conn.commit()
    conn.close
    flash('Entry was successfully updated')
    return redirect(url_for('show_entries'))


@app.route('/delete_entry/<int:id>')
def delete_entry(id):
    id = str(id)
    sql = 'delete from entries WHERE id=' + id
    cursor.execute(sql)
    conn.commit()
    sql = 'select id ,title, post from entries order by id desc'
    cursor.execute(sql)
    conn.commit()
    data = cursor.fetchall()
    entries = [dict(id=row[0], title=row[1], post=row[2]) for row in data]
    # entries = [{"title": row[0], "text": row[1], "id": row[2]} for row in data]
    return render_template('show_entries.html', entries=entries)
    conn.close


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    sql = 'insert into entries (title, post) values (%s,%s)'
    cursor.execute(sql, [request.form['title'], request.form['text']])
    conn.commit()
    conn.close
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You are now logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are now logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run(debug=True)
    # app.debug = True
