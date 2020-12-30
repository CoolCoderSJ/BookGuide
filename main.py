import web
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
    '/book_details', 'book_details'
    )


class index:
    def GET(self):
        book = db.select('books')
        return render.index(book)

class welcome:
    def GET(self):
        return render.welcome()


class add:
    def POST(self):
        i = web.input()
        n = db.insert('books', book_title=i.title, author=i.author, grade=i.grade)
        if "revnext" in i:
            book = db.select('books')
            i = web.input()
            bookTitle = i.title
            bookDesc = ""
            bookAuthor = i.author
            qr = db.select('books', where="book_title=$bookTitle", vars=locals())
            results = list(qr)
            bookId = int(results[0]['id'])
            bookGrade = int(results[0]['grade'])
            return render.book_details(book, bookId, bookTitle, bookDesc, bookAuthor, bookGrade)
        else:
            raise web.seeother('/')

class new:
    def GET(self):
        book = db.select('books')
        return render.new(book)

class book_details:
    def POST(self):
        book = db.select('books')
        reviews = db.select('reviews')
        i = web.input()
        bookId = int(i.bookId)
        bookTitle = i.bookTitle
        bookDesc = i.bookDesc
        bookAuthor = i.bookAuthor
        bookGrade = i.bookGrade
        return render.book_details(book, bookId, bookTitle, bookDesc, bookAuthor, bookGrade, reviews)

class test:
    def GET(self):
        book = db.select('books')
        return render.test(book)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
