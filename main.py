import webpy as web
import os
render = web.template.render('templates/')

db = web.database(
    dbn='postgres',
    host='127.0.0.1',
    port=5432,
    user='postgres',
    pw='postgres',
    db='webpy_test',
)



urls = (
    '/', 'index',
    '/index', 'index',
    '/new', 'new',
    '/add', 'add',
    '/test', 'test',
    '/book_details/(.+)', 'book_details',
    '/book_details', 'book_details',
    '/review', 'review'
    )


class index:
    def GET(self):
        global db
        books = db.select('books')
        reviews = db.select('reviews')
        return render.index(books, reviews, db)

class welcome:
    def GET(self):
        return render.welcome()


class add:
    def POST(self):
        i = web.input(myfile={})
        filedir = 'static/images/books' 
        print("\n\n"+i.myfile.filename+"\n\n")
        if i.myfile.filename == None or i.myfile.filename == "":
            myfilepath = 'static/images/books/placeholder.png'
        else:
            fileext = i.myfile.filename.split('.')[1]
            print(fileext)
            myfilepath = filedir + '/' + i.title + "." + fileext
            fout = open(myfilepath, "wb")
            fout.write(i.myfile.file.read())

            fout.close() 
        n = db.insert('books', book_title=i.title, author=i.author, grade=i.grade, image=myfilepath)
        if "revnext" in i:
            book = db.select('books')
            reviews = db.select('reviews')
            i = web.input()
            bookTitle = i.title
            bookDesc = ""
            bookAuthor = i.author
            qr = db.select('books', where="book_title=$bookTitle", vars=locals())
            results = list(qr)
            bookId = int(results[0]['id'])
            bookGrade = int(results[0]['grade'])
            qr2 = db.select('reviews', where="book_id=$bookId", vars=locals())
            reviews = list(qr2)
            avg_rating1 = 0
            avg_rating2 = 0
            avg = 0
            for review in reviews:
                if review['rating'] != None:
                    avg_rating1 += review['rating']
                    avg_rating2 += 1
            if avg_rating2 == 0:
                avg = 0
            else:
                avg = avg_rating1/avg_rating2
            avgstr = str(avg)
            print("\n\nAVG: "+avgstr+"\n\n")
            bookIdstr =str(bookId)
            return render.book_details(book, bookId, bookTitle, bookDesc, bookAuthor, bookGrade, reviews, avg, db, bookIdstr)
        else:
            raise web.seeother('/')

class new:
    def GET(self):
        book = db.select('books')
        return render.new(book)

class book_details:
    def POST(self):
        book = db.select('books')
        i = web.input()
        bookId = int(i.bookId)
        qr = db.select('books', where="id=$bookId", vars=locals())
        results = list(qr)
        bookTitle = results[0]['book_title']
        bookDesc = results[0]['book_description']
        bookAuthor = results[0]['author']
        bookGrade = results[0]['grade']
        qr2 = db.select('reviews', where="book_id=$bookId", vars=locals())
        reviews = list(qr2)
        avg_rating1 = 0
        avg_rating2 = 0
        avg = 0
        for review in reviews:
            if review['rating'] != None:
                avg_rating1 += review['rating']
                avg_rating2 += 1
        if avg_rating2 == 0:
            avg = 0
        else:
            avg = avg_rating1/avg_rating2        
        avgstr = str(avg)
        print("\n\nAVG: "+avgstr+"\n\n")
        bookIdstr = str(bookId)
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
        avg_rating1 = 0
        avg_rating2 = 0
        avg = 0
        for review in reviews:
            if review['rating'] != None:
                avg_rating1 += review['rating']
                avg_rating2 += 1
        if avg_rating2 == 0:
            avg = 0
        else:
            avg = avg_rating1/avg_rating2
        avgstr = str(avg)
        print("\n\nAVG: "+avgstr+"\n\n")
        bookIdstr = str(bookId)
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
        print("\n\nRating = "+stars+"\n\n")
        db.insert('reviews', book_id=i.bookId, name=i.name, description=i.review, rating = i.stars)
        qr2 = db.select('reviews', where="book_id=$bookId", vars=locals())
        reviews = list(qr2)
        bookId2 = str(bookId)
        raise web.seeother('/book_details?bookId='+bookId2)

class test:
    def GET(self):
        book = db.select('books')
        return render.test(book)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
