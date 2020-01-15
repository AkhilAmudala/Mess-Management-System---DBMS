from flask import Flask, render_template,request,url_for,redirect,abort
import MySQLdb

app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2106'
app.config['MYSQL_DB'] = 'Hostel_mess_management'
app.config['MYSQL_HOST'] = 'localhost'
mysql = MySQL(app)


table_name = ""
operation = ""


@app.route('/')
def index():
	return render_template("homepage.html")

@app.route('/get_op_table',methods=['GET','POST'])
def get_op_table():
	if request.method == 'POST':
		data = request.form
		global table_name
		global operation
		table_name = request.form["table"]
		operation = request.form["operation"]
		if table_name == "student" and operation == "insert":
			return render_template("student.html")
		elif operation == "read":
			return read()
		elif operation == "update":
			return render_template("update.html")
		elif operation == "search":
			return render_template("search.html")
	else:
		return abort(405)
			

@app.route('/insert',methods = ['GET','POST'])
def insert():
	if request.method == 'POST':
		cur = mysql.connection.cursor()
		global table_name
		global operation
		st_id = str(request.form["st_id"])
		name = request.form["name"]
		block = (request.form["block"])
		roomno = request.form["roomno"]
		if table_name == "student" and operation == "insert":
			sql = '''insert into user (st_id,name,block,roomno) values('%s','%s','%d','%d')''' %(st_id,name,block,roomno)				
			cur.execute(sql)
			mysql.connection.commit()
			return render_template("insert_success.html")
	else:
		return abort(405)

def read():
	global table_name
	cur = mysql.connection.cursor()
	sql = '''select * from %s ''' %(table_name)
	cur.execute(sql)
	result = cur.fetchall()
	result = list(result)
	k=len(result)
	l=len(result[0])
	return render_template("display.html",result=result,l=l,k=k)

@app.route("/update",methods = ["GET","POST"])
def update():
	if request.method == "POST":
		col = request.form["column_name"]
		old = request.form["old_value"]
		new = request.form["new_value"]
		global table_name
		cur = mysql.connection.cursor()
		sql = ''' update %s set %s = '%s' where %s='%s' ''' %(table_name,col,new,col,old)
		cur.execute(sql)
		mysql.connection.commit()
		return render_template("update_success.html")
	else:
		return abort(405)

if __name__ == "__main__":
	app.run(debug=True)

