import sys
#Prevent creation of cache
sys.dont_write_bytecode = True

from flask import Flask, render_template, request, redirect, flash, current_app #Import flask and its necesary components
import os #Import os commands
import sqlite3 #Database import
from werkzeug.utils import secure_filename #A module used for naming files

# Imports used to create the window
from threading import Thread
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from threading import Timer

#Import used for sending emails from flask
from flask_mail import Mail, Message
import re

import logging
from logging import DEBUG, INFO, ERROR
from logging.handlers import TimedRotatingFileHandler




# Define flask app
app = Flask(__name__)
#Secret Key for signing cookies
app.secret_key = '36b4610b69d1acc500fcc8557a3070846f1241c08c37e0d81b33abdf0afb2f0f'
#Define App Configuration
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'prachijain.test@gmail.com'
app.config['MAIL_PASSWORD'] = 'shuchir123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config["ERROR_LOG_PATH"] = "logs/errors.log"
#Define mail app
mail = Mail(app)

# Only set up a file handler if we know where to put the logs
if app.config.get("ERROR_LOG_PATH"):

	# Create one file for each day. Delete logs over 7 days old.
	file_handler = TimedRotatingFileHandler(app.config["ERROR_LOG_PATH"], when="D", backupCount=7)
	#Set level of logger to filter messages that are lower than the currently set level
	app.logger.setLevel(level=logging.DEBUG)
	# Use a multi-line format for this logger, for easier scanning
	file_formatter = logging.Formatter('''
	Time: %(asctime)s
	Level: %(levelname)s
	%(message)s
''')

	file_handler.setFormatter(file_formatter)
	app.logger.addHandler(file_handler)

#Before any request is made
@app.before_request
def log_entry():
	#Context of request
	context = {
		'url': request.path,
		'method': request.method,
		'ip': request.environ.get("REMOTE_ADDR")
	}
	#Log an info message to the log file
	app.logger.info("""Handling Request:
	Method: %(method)s
	Local IP: %(ip)s
	URL: %(url)s
	---------------------""", context)

#Show messages and a link to go home for http errors
@app.errorhandler(400)
def key_error(e):
	return """
	<h1>HTTP Error 400</h1>
	<h3>Bad Request</h3>
	<p>The app encountered an error. Click <a href="/">here</a> to go Home.</p>
	""", 400


@app.errorhandler(Exception)
def unhandled_exception(e):
	return """
	<h1>HTTP Error</h1>
	<h3>Internal Server Error</h3>
	<p>The app encountered an error. Click <a href="/">here</a> to go Home.</p>
	""", 500


@app.route('/')
def index(): #Define what happens when Homepage is visited.
	conn = sqlite3.connect("database.db")
	db = conn.cursor()
	books = db.execute("SELECT * from books").fetchall() #Get all books from database
	db.close()
	books.reverse() #Reverse order of books so that the default sort option is Newest to Oldest
	db = conn.cursor()
	reviews = db.execute("SELECT * from reviews").fetchall() #Get all reviews from database
	db.close()
	books2 = []
	for book in books:
		booklist = []
		for item in book:
			if book.index(item) == 1:
				booklist.append(item.title())
			else:
				booklist.append(item)
		books2.append(booklist)
	books = books2
	print("A")
	i = request.args #Get URL parameters
	if i.get("genre"): #If genre sort option is enabled
		genre = f"genres.name = '{i.get('genre')}'" #Create query for sort
	else:
		genre = "" #Keep query blank otherwise

	if i.get("grade"): #If grade sort option is enabled
		grade = "books.grade >= "+i.get("grade") #Create query for sort
	else:
		grade = "" #Keep query blank otherwise

	if i.get("ficsearch"): #If fic vs nonfic sort option is enabled
		ficsearch = f"genres.type = '{i.get('ficsearch')}'" #Create query for sort
	else:
		ficsearch = "" #Keep query blank otherwise

	if i.get("star"): #If star rating sort option is enabled
		star = "reviews.rating >= "+i.get("star") #Create query for sort
	else:
		star = "" #Keep query blank otherwise
	print("B")
	# Add filter queries to a list to analyze
	filts = [genre, grade, ficsearch, star]
	#Remove blank queries
	print(filts)
	filts2 = []
	for x in filts:
		if x == '':
			print("Blank query")
			filts2.append(x)
	print(filts2)
	for x in filts2:
		filts.remove(x)
	print(filts)
	# Build the query
	filter_query = ""
	#If more than one sort option selected, join them with keyword AND to prevent sort override
	if len(filts) > 1:
		filter_query += " AND ".join(filts)

	#If not, build the query with the only existing option
	else:
		filter_query += "".join(filts)
	print(filter_query)
	if filter_query:
		print("AA")
	#If query is not blank (If sort options are selected)
	print("C")
	if filter_query:
		db = conn.cursor()
		#Join all of the tables to search all of them at once
		query = db.execute(f"SELECT * from books LEFT OUTER JOIN reviews ON books.id = reviews.book_id JOIN genres ON books.genre_id = genres.id WHERE {filter_query}").fetchall()
		db.close()
		# The join yields multiple book entries since all of the reviews are also added. The following is done to remove the duplicates
		bookids = [] #List of book ids
		books2 = [] #Temporary list of books
		for result in query:
			if result[0] not in bookids: #If the book has not already been added to the new list
				bookids.append(result[0]) #Add the bookid to the list of bookids to prevent adding it again
				books2.append(result) #Add book to new list

		books2.reverse() # Reverse new query result to match New to Old sort
		books = books2 #Destroy temp list and match books list with the temp list
		#Create filters dictionary for all filters for evaluation
		filters = [{"name": "Grade", "val": i.get("grade")}, {"name": "Genre", "val": i.get("genre")}, {"name": "Fic vs. Nonfic", "val": i.get("ficsearch")}, {"name": "Star Rating", "val": i.get("star")}]
		#Create another list. This will hold items that are empty that need to be deleted
		filters2 = []
		#If item is empty, delete it
		for item in filters:
			if item['val'] == "":
				filters2.append(item)
		for item in filters2:
			filters.remove(item)
		#If more than one filter is selected, join the filter breadcrumb contents with '/'
		if len(filters) > 1:
			x = " / "
		else:
			x = ""
		#The breadcrumb text
		breadcrumb = ""
		#Display a bookcount to show user how many books match the query
		bookcount = "Books Found: "+str(len(books))
		#Display a clear filters button instead of a filter button since filter options have already been selected
		filtertext = "Clear Filters"
		#Make the breadcrumb text
		for filter in filters:
			breadcrumb += filter['name'] + ": " + filter['val'] + x
	#if no filters are selected
	else:
		filters = [] #Display no filters
		#set breadcrumb text as all books since no filters are selected
		breadcrumb = "Showing all books"
		#Do not display bookcount since all books are shown
		bookcount = ""
		#Show filter button instead clear filter button since there are no filters
		filtertext = "Filter"
	print("D")
	#Make a dictionary that holds the average number of reviews for each book
	avgrevs = {}

	for book in books:
		db = conn.cursor()
		#Make a JOIN query to get all of a book's reviews next to each book's details
		review_list = db.execute("SELECT * FROM books JOIN reviews ON books.id = reviews.book_id").fetchall()
		db.close()
		stars_total = 0
		num_of_stars = 0
		#Loop through each star to add them and calculate the average
		for i in review_list:
			if i[12]: #If there is a star review
				#If the book_id value of the currently iterating review matches the id of the currently iterating book, and the review is not 0
				if int(i[8]) == int(book[0]) and i[12] != 0:
					print(i[12])
					stars_total = stars_total + i[12] #Add the value of the star to the total
					num_of_stars = num_of_stars + 1 #Add one to the number of stars that have a valid star rating
		if num_of_stars == 0: #If no valid star ratings were found
			avg = 0 #Set the average as 0
		else:
			#else, divide the total by num of stars to get avg
			avg = stars_total/num_of_stars
		#add an entry to the dictionary. The key is the book id and the value is a list that has the exact average as well as the rounded average
		avgrevs[book[0]] = [float(avg), round(float(avg))]

	print(avgrevs)
	db = conn.cursor()
	# Get all of the genres matched with each book
	genre_list = db.execute("SELECT * FROM books JOIN genres ON books.genre_id = genres.id").fetchall()
	db.close()
	#Make a list that will hold the genre for each book
	genres = {}
	for genre in genre_list:
		#Add an entry to the dictionary. The key is the book id, and the value is a list with the genre type and the genre.
		genres[genre[0]] = [genre[-2], genre[-1]]
	db = conn.cursor()
	# Make a list of all genres. This will be iterated over in `index.html`
	genre2 = db.execute("SELECT * FROM genres").fetchall()
	db.close()
	i = request.args #Get URL parameters
	#if url has a sort parameter
	if i.get("sort"):
		#The list of books is reversed to make a New to Old sort by default. if the option selected is old, reverse the list
		if i.get("sort") == "old":
			books.reverse()
		#If sort by alphanumeric is selected
		elif i.get("sort") == "abc":
			#Make a list with book titles. this will be changed to match the abc format later.
			book_titles = []
			#Add all of the titles to the list
			for book in books:
				book_titles.append(book[1].lower())
			#Sort list alphanumerically
			book_titles.sort()
			print(book_titles)
			#Temp list for books
			books2 = []
			#Add all of the book metadata to the temp list by matching on title from the book_titles list.
			for title in book_titles:
				for book in books:
					if book[1].lower() == title:
						booklist = []
						for item in book:
							if book.index(item) == 1:
								booklist.append(item.title())
							else:
								booklist.append(item)
						books2.append(booklist)
			books = books2 #Set books list to the temp
	#Render the home page with all of the important variables created above.
	print("E")
	return render_template("index.html", books=books, reviews=reviews, avgrevs=avgrevs, genres=genres, genre2=genre2, filters=filters, bookcount=bookcount, breadcrumb=breadcrumb, filtertext=filtertext) #Show index.html file, pass the books, reviews, and db (used for database operations) to the html file.

@app.route('/add', methods=["POST"])
def add(): #Define what happens when a book is added
	conn = sqlite3.connect("database.db")
	db = conn.cursor()
	if request.method == 'POST':
		#Get the form data
		i = request.form
		#Get all books
		books = db.execute("SELECT * from books").fetchall()
		try:
			for book in books:
				#If book title is found in database, flash a message to the user and prevent database insert
				if book[1].lower() == i['title'].lower():
					flash("This book already exists.")
					return redirect("/new")
			#If a genre is not selected, flash a message to the user and prevent database insert
			if i['genre-subcategory-fic'] == '' and i['genre-subcategory-nonfic'] == '':
				flash("Please select a genre.")
				return redirect("/new")
			#If user selects genre from fic and nonfic dropdowns, flash a message to the user and prevent database insert
			if i['genre-subcategory-fic'] != "" and i['genre-subcategory-nonfic'] != "":
				flash("Please select a genre from only one category.")
				return redirect("/new")
		except Exception as err:
			app.logger.error(f"Error encountered while flashing messages to user - {err}")

		try:
			filedir = 'static/images/books' #Directory where book images are stored
			file = request.files['myfile'] #Get uploaded file
			if file.filename == None or file.filename == "": #If no book image is submitted, make the placeholder image the default image.
				myfilepath = 'static/images/books/placeholder.png'
			else: #If an image is submitted, do the following:
				fileext = secure_filename(file.filename.split(".")[-1])
				title = request.form['title']
				title = re.sub('[^A-Za-z0-9 ]+', '', title)
				myfilepath = filedir + '/' + title + "." + fileext #Define the filepath. This is the directory + the book name + file extension
				file.save(myfilepath) #Save the image
		except Exception as err:
			app.logger.error(f"Error encountered while saving images - {err}")
		try:
			#Insert the book title, author, grade, genre, and image file path in the database
			if request.form['genre-category'] == "fiction":
				sub = request.form['genre-subcategory-fic']
			elif request.form['genre-category'] == "nonfiction":
				sub = request.form['genre-subcategory-nonfic']
			db.execute(f"INSERT into books (book_title, book_description, author, grade, image, genre_id) VALUES ('{request.form['title']}', '{request.form['desc']}', '{request.form['author']}', {request.form['grade']}, '{myfilepath}', '{sub}')")
			conn.commit()
		except Exception as err:
			app.logger.error(f"Error encountered while adding info to database - {err}")
		# If user wants to go to the indivdual page:
		try:
			if "revnext" in request.form:
				book = db.execute("SELECT * from books") #Get all books from database
				bookTitle = request.form["title"] #Get the submitted book title
				bookDesc = "" #set the description empty, since the book was just added and has no description.
				bookAuthor = request.form["author"] #Get submitted author
				qr = db.execute('SELECT * from books WHERE book_title == \''+bookTitle+"'").fetchall() #Using the submitted title, get the book info from database
				#results = list(qr) #Convert the request to a list so that we can do operations with it
				bookId = int(qr[0][0]) #Get the book ID from the database response
				# bookGrade = int(qr[0][-1]) #Get the book grade from the database response
				# reviews = db.execute('SELECT * from reviews WHERE book_id == '+str(bookId)).fetchall() #Get all reviews that were submitted for this book
				# #reviews = list(qr2) #Convert to list for operations
				# avg_rating1 = 0 #The total star rating. This value will be updated later
				# avg_rating2 = 0 #Number of reviews that have stars
				# avg = 0 #Average star rating
				# for review in reviews: #For each review in the given reviews, do the following -
				# 	if review['rating'] != None: #If there is a star rating submitted, do the following -
				# 		avg_rating1 += review['rating'] #Add the star to the total stars
				# 		avg_rating2 += 1 #Add one to the total number of reviews that have stars
				# if avg_rating2 == 0: #If there were no reviews with stars, set the average to 0.
				# 	avg = 0
				# else: #If there were star ratings, do the following -
				# 	avg = avg_rating1/avg_rating2 #Divide total by num of reviews with stars
				# bookIdstr =str(bookId) #Convert BookID to string for later use
				# #Show the individual page with all of the collected values
				return redirect("/book_details/"+str(bookId))
			else: #If user does not want to go to the home page then -
				return redirect('/', code=302) #redirect to home page
		except Exception as err:
			app.logger.error(f"Error encountered while redirecting user because they wanted to add a review next - {err}")

@app.route('/new', methods=["GET"])
def new(): #Define what happens when user clicks the "Add a book" button
	conn = sqlite3.connect("database.db")
	db = conn.cursor()
	if request.method == 'GET':
		book = db.execute("SELECT * from books").fetchall() #Get all books from database (Used to make sure book doesn't already exist)
		fics = db.execute("SELECT * from genres WHERE type = 'fiction'").fetchall()
		nonfics = db.execute("SELECT * from genres WHERE type = 'nonfiction'").fetchall()
		return render_template("new.html", fics=fics, nonfics=nonfics) #Pass the books, db object for operations, and string object for operations to the new book form and show form.


@app.route('/book_details/<id>')
def book_details(id): #Define what happens when user wants to see individual page
	conn = sqlite3.connect("database.db")
	db = conn.cursor()
	if request.method == 'GET':
		db = conn.cursor()
		book = db.execute("SELECT * from books").fetchall() #Get all books from database from the database
		db.close()
		i = request.form #Get URL parameters, set bookId to None by default in case none is given
		bookId = int(id) #Convert bookId to integer
		db = conn.cursor()
		qr = db.execute('SELECT * from books WHERE id == '+str(bookId)).fetchall() #Get book details from database using the ID to get more details.
		db.close()
		bookTitle = qr[0][1] #Get the book title from the list
		bookDesc = qr[0][2] #Get the book description from the list
		bookAuthor = qr[0][4] #Get the book author from the list
		bookGrade = qr[0][5] #Get the book grade from the list.
		db = conn.cursor()
		reviews = db.execute('SELECT * from reviews WHERE book_id == '+str(bookId)).fetchall() #Get all reviews for the selected book.
		#reviews = list(qr2) #Convert to list for later operations
		avg_rating1 = 0 #The total star rating. This value will be updated later
		avg_rating2 = 0 #Number of reviews that have stars
		avg = 0 #Average star rating
		for review in reviews: #For each review in the given reviews, do the following -
			if review[-1] != 0: #If there is a star rating submitted, do the following -
				avg_rating1 += review[-1] #Add the star to the total stars
				avg_rating2 += 1 #Add one to the total number of reviews that have stars
		if avg_rating2 == 0: #If there were no reviews with stars, set the average to 0.
			avg = 0
		else: #If there were star ratings, do the following -
			avg = avg_rating1/avg_rating2 #Divide total by num of reviews with stars
		bookIdstr =str(bookId) #Convert BookID to string for later use
		#Show the individual page with all of the collected values
		#Get image filepath
		image = "http://localhost:5000/"+qr[0][3]
		db = conn.cursor()
		#Make genre list
		genre_list = db.execute("SELECT * FROM books JOIN genres ON books.genre_id = genres.id").fetchall()
		db.close()
		genres = {}
		for genre in genre_list:
			genres[genre[0]] = [genre[-2], genre[-1]]
		bookGenre = genres[bookId][0]
		#Render te book's individual page
		return render_template("book_details.html", book=book, bookId=bookId, bookTitle=bookTitle.title(), bookDesc=bookDesc, bookAuthor=bookAuthor.title(), bookGrade=bookGrade, reviews=reviews, avg=avg, db=db, bookIdstr=bookIdstr, image=image, bookGenre=bookGenre)

@app.route('/review', methods=["POST"])
def review(): #Define what happens when a review is submitted
	conn = sqlite3.connect("database.db")
	db = conn.cursor()
	if request.method == 'POST':
		book = db.execute("SELECT * from books").fetchall() #Get all books from database from database
		db.close()
		i = request.form #Get user input
		if i['review'] == "" and i['stars'] == '0':
			flash("Please enter either a text description or fill in the stars.")
			return redirect('/book_details/'+i['bookId'], code=303)
		else:
			bookId = int(i['bookId']) #Get bookId (Hidden input)
			Desc = i['review'] #Get text review
			name = i['name'] #Get reviewer name
			try:
				db = conn.cursor()
				qr = db.execute("SELECT * from books WHERE id = '"+str(bookId)+"'").fetchall() #Get book details for specific book from database
				db.close()
				bookTitle = qr[0][1] #Get the book title from the list
				bookDesc = qr[0][2] #Get the book description from the list
				bookAuthor = qr[0][4] #Get the book author from the list
				bookGrade = qr[0][5] #Get the book grade from the list.
				stars = i['stars'] #Get stars value
				db = conn.cursor()
				db.execute(f"INSERT into reviews (book_id, name, description, rating) VALUES ('{i['bookId']}',  '{i['name']}', '{i['review']}', '{i['stars']}')") #Insert text review, reviewer name, bookId, and star rating into datbase
				conn.commit()
				db.close()
				db = conn.cursor()
				reviews = db.execute('SELECT * from reviews WHERE book_id == '+str(bookId)).fetchall() #Get reviews for specific book
				db.close()
				#reviews = list(qr2) #Convert to list for operations
				bookId2 = str(bookId)
				return redirect('/book_details/'+bookId2, code=303) #Reload the individual page/reviews
			except Exception as err:
				app.logger.error(f"Error encountered while adding a review and redirecting - {err}")

@app.route("/about")
def about():
	#If about page is selected, render about page
	return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
	if request.method == "GET":
		#If contact page is selected, render contact page
		return render_template("contact.html")
	elif request.method == "POST":
		#If the form is submitted, email me the contact form boxes
		msg = Message("BookGuide Contact Form Filled", sender="prachijain.test@gmail.com", recipients=['prachijain.test@gmail.com'])
		msg.body = f"SENDER: {request.form['name']}\n\nEMAIL: {request.form['email']}\n\n\nCONTENT:\n{request.form['content']}"
		mail.send(msg)
		#Show user success message and render contact page
		flash("Successfully Submitted!")
		return redirect("/contact", code=303)

#Define the window object
def ui(location):
	#Create window object
	qt_app = QApplication(sys.argv)
	#Load Web Engine to show localhost page
	web = QWebEngineView()
	#Set window title
	web.setWindowTitle("BookGuide")
	#Size the window
	web.resize(900, 800)
	#Set the window icon as the brand logo
	scriptDir = os.path.dirname(os.path.realpath(__file__))
	web.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'static/images/brandlogo.png'))
	#Magnify the window just a bit
	web.setZoomFactor(1.2)
	#Load given URL
	web.load(QUrl(location))
	#Show the window object
	web.show()
	sys.exit(qt_app.exec_())

# if __name__ == "__main__":
	#Show the window with the localhost:5000 url
Timer(1,lambda: ui("http://127.0.0.1:5000/")).start()
#Start the Flask App
app.run('0.0.0.0')

#PYINSTALLER SCRIPT
#pyinstaller -n BookGuide -w --add-data="static;static" --add-data="templates;templates" --add-data="database.db;." -i "static/images/logo.ico" main.py
