from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title" : "one" , "author" : "jay", "category" : "action"},
    {"title" : "two" , "author" : "san","category" : "action"},
    {"title" : "three" , "author" : "ron","category" : "thriller"}
    ]


@app.get('/books')
async def get_all_books():
    return BOOKS

@app.get('/books/mybook')
async def get_books():
    return {'my_book' : "my fav book"}


"""
path parameters
"""
@app.get('/books/{book_title}')
async def get_books(book_title : str):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            return book

"""
query parameter : /? , for filtering data 
"""
@app.get('/books/')
async def get_books_by_category(category : str):
    books_to_return = []
    for book in BOOKS:
        if book['category'].casefold() == category.casefold():
            books_to_return.append(book)
            # return book
    return books_to_return

"""
path param + query param
"""
@app.get('/books/{book_author}/')
async def get_books(book_author : str, category : str):
    books_to_return = []
    for book in BOOKS:
        if book['author'].casefold() == book_author.casefold() and book['category'].casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


