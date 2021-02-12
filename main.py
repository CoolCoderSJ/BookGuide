from flask import Flask, render_template, request, redirect, flash
import os #Import os commands
import sqlite3
from werkzeug.utils import secure_filename
from threading import Thread
from flaskwebgui import FlaskUI
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
from threading import Timer
import sys

app = Flask(__name__)
ui = FlaskUI(app, fullscreen=True)
app.secret_key = '36b4610b69d1acc500fcc8557a3070846f1241c08c37e0d81b33abdf0afb2f0f'

@app.route('/')
def index(): #Define what happens when Homepagw is visited.
    conn = sqlite3.connect("collaboreadflask.db")
    db = conn.cursor()
    db.execute("SELECT * from books") #Get all books from database
    books = db.fetchall()
    db.close()
    db = conn.cursor()
    db.execute("SELECT * from reviews") #Get all reviews from database
    reviews = db.fetchall()
    db.close()
    avgrevs = {}

    for book in books:
        db = conn.cursor()
        db.execute("SELECT * FROM books JOIN reviews ON books.id = reviews.book_id")
        review_list = db.fetchall()
        db.close()
        avg1 = 0
        avg2 = 0
        for i in review_list:
            if i[8]:
                if int(i[8]) == int(book[0]) and i[-1] != 0:
                    avg1 = avg1 + i[-1]
                    avg2 = avg2 + 1
        if avg2 == 0:
            avg = 0
        else:
            avg = avg1/avg2
            print(avg)
        avgrevs[book[0]] = float(avg)
    print(avgrevs)
    print("\n\n\n\n\n"+str(review_list)+"\n\n\n\n\n")

    db = conn.cursor()
    genre_list = db.execute("SELECT * FROM books JOIN genres ON books.genre_id = genres.id").fetchall()
    db.close()
    genres = {}
    for genre in genre_list:
        collection = [genre[-2], genre[-1]]
        genres[genre[0]] = collection
    return render_template("index.html", books=books, reviews=reviews, avgrevs=avgrevs, genres=genres) #Show index.html file, pass the books, reviews, and db (used for database operations) to the html file.

@app.route('/add', methods=["POST"])
def add(): #Define what happens when a book is added
    conn = sqlite3.connect("collaboreadflask.db")
    db = conn.cursor()
    if request.method == 'POST':
        i = request.form
        print(i)
        qr = db.execute("SELECT * from books").fetchall()
        for book in qr:
            if book[1].lower() == i['title'].lower():
                flash("This book already exists.")
                return redirect("/new")
        if i['title'] == "":
            flash("Book Title is a required field.")
            return redirect("/new")
        if i['grade'] == "":
            flash("Appropriate Grade is a required field.")
        if i['genre-subcategory-fic'] == '' and i['genre-subcategory-nonfic'] == '':
            flash("Please select a genre.")
            return redirect("/new")
        if i['genre-subcategory-fic'] != "" and i['genre-subcategory-nonfic'] != "":
            flash("Please select a genre from only one category.")
            return redirect("/new")
        filedir = 'static/images/books' #Directory where book images are stored
        file = request.files['myfile']
        if file.filename == None or file.filename == "": #If no book image is submitted, make the placeholder image the default image.
            myfilepath = 'static/images/books/placeholder.png'
        else: #If an image is submitted, do the following:
            fileext = secure_filename(file.filename.split(".")[-1])
            myfilepath = filedir + '/' + request.form['title'] + "." + fileext #Define the filepath. This is the directory + the book name + file extension
            file.save(myfilepath)
        #Insert the book title, author, grade, genre, and image file path in the database
        if request.form['genre-category'] == "fiction":
            sub = request.form['genre-subcategory-fic']
        elif request.form['genre-category'] == "nonfiction":
            sub = request.form['genre-subcategory-nonfic']
        db.execute(f"INSERT into books (book_title, author, grade, image, genre_id) VALUES ('{request.form['title']}', '{request.form['author']}', {request.form['grade']}, '{myfilepath}', '{sub}')")
        conn.commit()
        # If user wants to go to the indivdual page:
        if "revnext" in request.form:
            book = db.execute("SELECT * from books") #Get all books from database
            bookTitle = request.form["title"] #Get the submitted book title
            bookDesc = "" #set the description empty, since the book was just added and has no description.
            bookAuthor = request.form["author"] #Get submitted author
            qr = db.execute('SELECT * from books WHERE book_title == \''+bookTitle+"'").fetchall() #Using the submitted title, get the book info from database
            #results = list(qr) #Convert the request to a list so that we can do operations with it
            bookId = int(qr[0][0]) #Get the book ID from the database response
            bookGrade = int(qr[0][-1]) #Get the book grade from the database response
            reviews = db.execute('SELECT * from reviews WHERE book_id == '+str(bookId)).fetchall() #Get all reviews that were submitted for this book
            #reviews = list(qr2) #Convert to list for operations
            avg_rating1 = 0 #The total star rating. This value will be updated later
            avg_rating2 = 0 #Number of reviews that have stars
            avg = 0 #Average star rating
            for review in reviews: #For each review in the given reviews, do the following -
                if review['rating'] != None: #If there is a star rating submitted, do the following -
                    avg_rating1 += review['rating'] #Add the star to the total stars
                    avg_rating2 += 1 #Add one to the total number of reviews that have stars
            if avg_rating2 == 0: #If there were no reviews with stars, set the average to 0.
                avg = 0
            else: #If there were star ratings, do the following -
                avg = avg_rating1/avg_rating2 #Divide total by num of reviews with stars
            print(avg)
            bookIdstr =str(bookId) #Convert BookID to string for later use
            #Show the individual page with all of the collected values
            return redirect("/book_details/"+str(bookId))
        else: #If user does not want to go to the home page then -
            return redirect('/', code=302) #redirect to home page

@app.route('/new', methods=["GET"])
def new(): #Define what happens when user clicks the "Add a book" button
    conn = sqlite3.connect("collaboreadflask.db")
    db = conn.cursor()
    if request.method == 'GET':
        book = db.execute("SELECT * from books").fetchall() #Get all books from database (Used to make sure book doesn't already exist)
        fics = db.execute("SELECT * from genres WHERE type = 'fiction'").fetchall()
        nonfics = db.execute("SELECT * from genres WHERE type = 'nonfiction'").fetchall()
        return render_template("new.html", book=book, fics=fics, nonfics=nonfics) #Pass the books, db object for operations, and string object for operations to the new book form and show form.


@app.route('/book_details/<id>')
def book_details(id): #Define what happens when user wants to see individual page
    conn = sqlite3.connect("collaboreadflask.db")
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
        print(qr)
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
            if review[-1] != None: #If there is a star rating submitted, do the following -
                avg_rating1 += review[-1] #Add the star to the total stars
                avg_rating2 += 1 #Add one to the total number of reviews that have stars
        if avg_rating2 == 0: #If there were no reviews with stars, set the average to 0.
            avg = 0
        else: #If there were star ratings, do the following -
            avg = avg_rating1/avg_rating2 #Divide total by num of reviews with stars
        bookIdstr =str(bookId) #Convert BookID to string for later use
        #Show the individual page with all of the collected values
        image = "http://localhost:5000/"+qr[0][3]
        db = conn.cursor()
        genre_list = db.execute("SELECT * FROM books JOIN genres ON books.genre_id = genres.id").fetchall()
        db.close()
        print("\n\nGENRES: "+str(genre_list))
        genres = {}
        for genre in genre_list:
            collection = [genre[-2], genre[-1]]
            genres[genre[0]] = collection
        bookGenre = genres[bookId][0]
        return render_template("book_details.html", book=book, bookId=bookId, bookTitle=bookTitle, bookDesc=bookDesc, bookAuthor=bookAuthor, bookGrade=bookGrade, reviews=reviews, avg=avg, db=db, bookIdstr=bookIdstr, image=image, bookGenre=bookGenre)

@app.route('/review', methods=["POST"])
def review(): #Define what happens when a review is submitted
    conn = sqlite3.connect("collaboreadflask.db")
    db = conn.cursor()
    if request.method == 'POST':
        book = db.execute("SELECT * from books").fetchall() #Get all books from database from database
        db.close()
        i = request.form #Get user input
        print(i)
        if i['review'] == "" and i['stars'] == '0':
            flash("Please enter either a text description or fill in the stars.")
            return redirect('/book_details/'+i['bookId'], code=303)
        else:
            bookId = int(i['bookId']) #Get bookId (Hidden input)
            Desc = i['review'] #Get text review
            name = i['name'] #Get reviewer name

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

def ui(location):
    qt_app = QApplication(sys.argv)
    web = QWebEngineView()
    web.setWindowTitle("Collaboread")
    web.resize(900, 800)
    scriptDir = os.path.dirname(os.path.realpath(__file__))
    web.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'static/books/ffff.png'))
    web.setZoomFactor(1.5)
    web.load(QUrl(location))
    web.show()
    sys.exit(qt_app.exec_())

print("\n\n\nAPP RUNNING ON PORT 5000\n\n\n")
if __name__ == "__main__":
    #ui.run()
    Timer(1,lambda: ui("http://127.0.0.1:5000/")).start()
    app.run()

#PYINSTALLER SCRIPT
#pyinstaller -n Collaboread -w --add-data="static;static" --add-data="templates;templates" --add-data="collaboreadflask.db;." main.py
