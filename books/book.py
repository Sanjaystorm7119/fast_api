from fastapi import FastAPI , Body
from typing import Optional

app = FastAPI()

BOOKS = [
    {"title" : "one" , "author" : "san", "category" : "action"},
    {"title" : "two" , "author" : "jay","category" : "action"},
    {"title" : "three" , "author" : "san","category" : "thriller"}
    ]

"""
GET cannot have a BODY**
"""

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
async def get_books_by_title(book_title : str):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            return book

"""
query parameter : /? , for filtering data 
"""
@app.get('/books/')
async def get_books_by_category(category : Optional[str] = 'action'):
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
async def get_books_by_author(book_author : str, category :  Optional[str] = None):
    books_to_return = []
    for book in BOOKS:
        if book['author'].casefold() == book_author.casefold() :
            if category is None or book["category"].casefold() == category.casefold():
                books_to_return.append(book)
            
    return books_to_return



"""
POST => create
"""

"""
do not use this style for post , looks like get 
POST requests should not rely on query params for data
No validation
Easy to send bad or missing data
Not scalable when fields grow
"""
@app.post('/books/create_book')
async def create_book(title : str , author : str , category : str):
    if any(book['title'] == title and book['author']== author for book in BOOKS) :
        return {"message":"book already exists"}
    BOOKS.append({"title" : title , "author": author , "category" : category})
    return {"message" : "book added"}


"""
recommended way , along with pydantic

"""

@app.post('/books/create_new_book')
async def create_new_book(new_book = Body()):
    BOOKS.append(new_book)



"""
PUT => update
has body()
"""
@app.put('/books/update_book')
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].casefold() == updated_book['title'].casefold():
            BOOKS[i] = updated_book

"""
DELETE => delete
"""
@app.delete('/books/delete_book/{book_title}')
async def update_book(book_title : str):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
    return {"message":"deleted"}


#test
@app.get('/books/{author}')
async def get_books_by_author(author : str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return