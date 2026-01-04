from fastapi import FastAPI, Body , HTTPException
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI()


class Book(BaseModel):
    id : Optional[int] = Field(None,gt=0,description="ID is not needed on create but has to be more thsn 0 is entered")
    genre : str = Field(min_length=4)
    title : str = Field(min_length=4)
    author : str = Field(min_length=2)
    rating : int = Field(gt=0 , le=5)
    description : str = Field(max_length=100)

##prepopulate post values => model_config => json_schema_extra => example => {}
    model_config = {
        "json_schema_extra": {
            "example" : {
            "genre" : "suspense",
            "title" : "a new book",
            "author" : "janjay",
            "rating" : 5,
            "description" : "new book description"
        }
        }
    }

    # def __init__(self , id : int , genre : str , title : str, author : str, rating : str, description: str ):
    #     self.id = id
    #     self.genre = genre
    #     self.title = title
    #     self.author = author
    #     self.rating = rating
    #     self.description = description

BOOKS = [
    Book(id=1,genre="action",title="title one",author="janjay",rating="5",description="random 5 star book"),
    Book(id=2,genre="action",title="title two",author="janjay",rating="4",description="random 4 star book"),
    Book(id=3,genre="action",title="title three",author="janjay",rating="3",description="random 3 star book")

]


@app.get('/books')
async def get_all_books():
    return BOOKS

@app.get('/books/{id}')
async def get_book_by_id(id : int):
    for book in BOOKS:
        if book.id == id :
            return book

@app.post('/books/create_book')
async def create_new_book(new_book : Book ):
    for book in BOOKS:
        if int(book.id) == int(new_book.id):
            raise HTTPException(status_code=400, detail="Book with this id already exists")

    if len(BOOKS)>0:
        new_book.id = BOOKS[-1].id+1
    else :
        new_book.id = 1

    BOOKS.append(new_book)
    return {"message":"book added", "book_id":new_book.id}

@app.delete('/books/delete_book')
async def delete_book(book_name : str):
    for i,book in enumerate(BOOKS):
        if book.title.casefold() == book_name.casefold():
            BOOKS.pop(i)

    return {"message":"book removed"}