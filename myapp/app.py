from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL
from slackclient import SlackClient

token ="add your token"
sc = SlackClient(token)

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'todolist'
app.config['MYSQL_HOST'] = '35.189.87.238'
mysql.init_app(app)

@app.route('/')
@app.route('/<name>')
def hello(name=None):
	return render_template('index.html', name=name)

@app.route("/list")
def list():
	cur = mysql.connection.cursor()
	cur.execute('''SELECT * FROM task''')
	rv = cur.fetchall()
	return render_template('index.html', name=str(rv))

@app.route("/add/<string:task>")
def add(task=None):
	cur= mysql.connection.cursor()
	cur.execute('''INSERT INTO task (taskName) VALUES (%s)''',(task,))
	mysql.connection.commit()
	sc.api_call("chat.postMessage",channel="#todo",text="Task has been added. :tada:", username='raulbot', icon_emoji=':robot_face:')
	return render_template('index.html', name="New Task has been added to the to do list!")

@app.route("/delete/<no>")
def delete(no=None):
	cur=mysql.connection.cursor()
	delstatmt = "DELETE FROM task WHERE taskID = ' {} ' ".format(no)
	cur.execute(delstatmt)
	mysql.connection.commit()
	return render_template('index.html', name="Task has been deleted!")

@app.route("/update/<task>/<no>")
def update(task=None, no=None):
	cur=mysql.connection.cursor()
	update_stmt = ("UPDATE task SET taskName = %s WHERE taskID = %s")
	data=(task,no)
	cur.execute(update_stmt, data)
	mysql.connection.commit()
	return render_template('index.html', name="Task has been updated!")


if __name__ == "__main__":
	app.run(host='0.0.0.0', port='5000')
