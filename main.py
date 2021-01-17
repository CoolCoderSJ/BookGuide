import web #Import the web.py python framework
import os #Import os commands
render = web.template.render('templates/') #Define where the HTML pages are stored

#Define database connection
db = web.database(
    dbn='postgres',
    host='127.0.0.1',
    port=5432,
    user='postgres',
    pw='postgres',
    db='webpy_test',
)

#Define all of the possible URLs that can be shown, as well as what method to call when each URL is visited.
urls = (
    '/', 'index', #Home page
    '/new', 'new', #Add the book (NOT THE FORM)
    '/add', 'add', #Adding a book form
    '/book_details/(.+)', 'book_details', #GET method for getting book details. Not reccomended, and used in only one place.
    '/book_details', 'book_details', #POST method for getting book details, more secure/accurate way to get the details.
    '/review', 'review' #Submit a review method
    )


class index: #Define what happens when Homepagw is visited.
    def GET(self):
        global db
        books = db.select('books') #Get all books from database
        reviews = db.select('reviews') #Get all reviews from database
        return render.index(books, reviews, db) #Show index.html file, pass the books, reviews, and db (used for database operations) to the html file.


class add: #Define what happens when a book is added
    def POST(self):
        i = web.input(myfile={}) # Get user input, make sure image file is a dictionary object so that it is saved properly.
        filedir = 'static/images/books' #Directory where book images are stored
        if i.myfile.filename == None or i.myfile.filename == "": #If no book image is submitted, make the placeholder image the default image.
            myfilepath = 'static/images/books/placeholder.png'
        else: #If an image is submitted, do the following:
            fileext = i.myfile.filename.split('.')[1] #Get the file extension
            myfilepath = filedir + '/' + i.title + "." + fileext #Define the filepath. This is the directory + the book name + file extension
            fout = open(myfilepath, "wb") #Create an empty image object in the directory.
            fout.write(i.myfile.file.read()) #Write the image contents to the server
            fout.close() #Safely close the file operation.
        #Insert the book title, author, grade, genre, and image file path in the database
        n = db.insert('books', book_title=i.title, author=i.author, grade=i.grade, image=myfilepath)
        # If user wants to go to the indivdual page:
        if "revnext" in i:
            book = db.select('books') #Get all books
            i = web.input()
            bookTitle = i.title #Get the submitted book title
            bookDesc = "" #set the description empty, since the book was just added and has no description.
            bookAuthor = i.author #Get submitted author
            qr = db.select('books', where="book_title=$bookTitle", vars=locals()) #Using the submitted title, get the book info from database
            results = list(qr) #Convert the request to a list so that we can do operations with it
            bookId = int(results[0]['id']) #Get the book ID from the database response
            bookGrade = int(results[0]['grade']) #Get the book grade from the database response
            qr2 = db.select('reviews', where="book_id=$bookId", vars=locals()) #Get all reviews that were submitted for this book
            reviews = list(qr2) #Convert to list for operations
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
            bookIdstr =str(bookId) #Convert BookID to string for later use
            #Show the individual page with all of the collected values
            return render.book_details(book, bookId, bookTitle, bookDesc, bookAuthor, bookGrade, reviews, avg, db, bookIdstr)
        else: #If user does not want to go to the home page then -
            raise web.seeother('/') #redirect to home page

class new: #Define what happens when user clicks the "Add a book" button
    def GET(self):
        global db #Get the database
        book = db.select('books') #Get all books (Used to make sure book doesn't already exist)
        return render.new(book, db, str) #Pass the books, db object for operations, and string object for operations to the new book form and show form.

class book_details: #Define what happens when user wants to see individual page
    def POST(self): #POST method - all data is passed through headers, to reduce spam and show accurate results.
        book = db.select('books') #Get all books from database
        i = web.input() #Get "hidden" user input.
        bookId = int(i.bookId) #Get the book ID. This value is a hidden input value on each card that holds the book id.
        qr = db.select('books', where="id=$bookId", vars=locals()) #Get book details from database using the ID to get more details.
        results = list(qr) #Convert to list for further operations.
        bookTitle = results[0]['book_title'] #Get the book title from the list
        bookDesc = results[0]['book_description'] #Get the book description from the list
        bookAuthor = results[0]['author'] #Get the book author from the list
        bookGrade = results[0]['grade'] #Get the book grade from the list.
        qr2 = db.select('reviews', where="book_id=$bookId", vars=locals()) #Get all reviews for the selected book.
        reviews = list(qr2) #Convert to list for further operations
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
        bookIdstr =str(bookId) #Convert BookID to string for later use
        #Show the individual page with all of the collected values
        return render.book_details(book, bookId, bookTitle, bookDesc, bookAuthor, bookGrade, reviews, avg, db, bookIdstr)

    def GET(self):
        book = db.select('books')
        i = web.input(bookId=None)
        bookId = int(i.bookId)
        qr = db.select('books', where="id=$bookId", vars=locals())
        results = list(qr)
        bookTitle = results[0]['book_title']
        bookDesc = results[0]['book_description']
        bookAuthor = results[0]['author']
        bookGrade = results[0]['grade']
        qr2 = db.select('reviews', where="book_id=$bookId", vars=locals())
        reviews = list(qr2)
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
        bookIdstr =str(bookId) #Convert BookID to string for later use
        #Show the individual page with all of the collected values
        return render.book_details(book, bookId, bookTitle, bookDesc, bookAuthor, bookGrade, reviews, avg, db, bookIdstr)

class review:
    def POST(self):
        book = db.select('books')
        i = web.input()
        bookId = int(i.bookId)
        Desc = i.review
        name = i.name
        qr = db.select('books', where="id=$bookId", vars=locals())
        results = list(qr)
        bookTitle = results[0]['book_title']
        bookDesc = results[0]['book_description']
        bookGrade = int(results[0]['grade'])
        bookAuthor = results[0]['author']
        stars = i.stars
        db.insert('reviews', book_id=i.bookId, name=i.name, description=i.review, rating = i.stars)
        qr2 = db.select('reviews', where="book_id=$bookId", vars=locals())
        reviews = list(qr2)
        bookId2 = str(bookId)
        raise web.seeother('/book_details?bookId='+bookId2)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
