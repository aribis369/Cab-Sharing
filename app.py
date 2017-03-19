from flask import Flask, render_template, url_for, request, session, redirect
from flask_session import Session
import MySQLdb
from datetime import datetime
app = Flask(__name__)
sess = Session()

cursor = None
db = None
def connect_database():
	global cursor,db
	# Open database connection
	db = MySQLdb.connect("127.0.0.1", "me", "123", "cab")
	# prepare a cursor object using cursor() method
	cursor = db.cursor()

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/post-cab", methods=["POST"])
def postCab():
	if cursor == None or db == None :
		connect_database()
	# else :
		# return render_template("index.html") #return with error ******
	form_dict = request.form.to_dict()
	date = form_dict["date"]
	time = form_dict["time"]
	dateTime = date + time 
	threshold = form_dict["threshold"]
	print ("{} - {}".format(type(date),date))
	print ("{} - {}".format(type(time),time))
	# dateTime = datetime.strptime(form_dict["datetime"], '%Y-%m-%dT%H:%M:%S.%fZ')
	query = "INSERT INTO cabdetails (name,emailid,number,availSeats,source,dest,date,time,threshold) values ('%s','%s','%s','%s','%s','%s', '%s','%s','%s')" % (form_dict["name"],form_dict["emailid"],form_dict["number"],form_dict["availSeats"],form_dict["source"],form_dict["dest"],date,time,threshold)
	try :
		cursor.execute(query)
		db.commit()
	except Exception as e :
		print e
		#Reder teml with error
	for key in form_dict.keys() :
		print ("{} - {}\n".format(key,form_dict[key]))
	flag = True
	msg = "Your ride data has been successfully submitted"
	msgcode = "RidePost"
	return render_template('index.html' , flag=flag, msg=msg,msgcode=msgcode)

@app.route("/search-cab",methods=["POST"])
def searchCab() :
	if cursor == None or db == None :
		connect_database()
	# else :
		# return render_template("index.html") #return with error ******
	query = "SELECT * FROM cabdetails"
	try :
		cursor.execute(query)
		cabsList = list()
		for row in cursor.fetchall():
			cabsList.append(dict(name= row[0],
								email=row[1],
								number=row[2],
								availSeats=row[3],
								dest=row[5],
								threshold=row[6],
								datetime=row[7]
								))
		return render_template('cabsSearchResult.html' , cabsList=cabsList)
	except Exception as e :
		print e 
		#Reder teml with error

app.secret_key = 'kwoc'
app.config['SESSION_TYPE'] = 'filesystem'

sess.init_app(app)
app.debug = True

if __name__ == "__main__" :
	app.run(debug=True)