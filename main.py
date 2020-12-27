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

"""
urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())


class hello:
    def GET(self, name):
        if not name:
            name = 'Shuchir'
        return 'Hello, ' + name + '!'


if __name__ == "__main__":
    app.run()

"""

urls = (
    '/', 'index',
    '/add', 'add',
    '/test', 'test'
    )


class index:
    def GET(self):
        book = db.select('books')
        return render.index(book)

class add:
    def POST(self):
        i = web.input()
        n = db.insert('books', book_title=i.title)
        raise web.seeother('/')

class test:
    def GET(self):
        return render.test()


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
