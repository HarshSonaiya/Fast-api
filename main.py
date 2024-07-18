'''
The demo of CRUD Operations:
GET - Read Data
POST - Insert Data
PUT - Update Data
DELETE - Discard Data
'''

from fastapi import FastAPI,Path,HTTPException
from typing import Optional 
from pydantic import BaseModel


app = FastAPI()

books = {
    1:{
        "name": "Harry Potter and the Deathly Hollows",
        "author": "J.K. Rowling"
    },
    2:{
        "name": "Mathematics for ML",
        "author": "Gilbert Stang"
    },
    3:{
        "name": "Mathematics",
        "author": "Gilbert Stang"
    }

}

class Book(BaseModel):
    name: str
    author: str

@app.get("/") 
def root():
    '''
    Return a welcome message
    '''
    return {"message" : "Welcome Page"} 

@app.get("/get-book-details/{book_id}")
def get_book_details(book_id: int = Path(..., description="The ID of the book to fetch",gt=0,lt=3)):
    """
    Retrieves details of a book by its ID.
    Raises a 404 HTTPException if the book is not found.
    """
    try:
        return books[book_id]
    except KeyError:
        raise HTTPException(status_code=404, detail="Book not found")

@app.get("/available-books")
def get_availabel_books():
    '''
    Retrieves list of all available books
    '''
    return list(books.values())

@app.get("/get-by-name")
def get_book(name: Optional[str] = None):
    '''
    Searches for a book by name Return book ID if found 
    otherwise returns a message stating "Book not found"
    '''
    for id_ in books :
        if books[id_]["name"] == name:
            return id_
    return {"message":"Book not found"}
        
@app.post("/add-book/{book_id}")
def add_new_book(book_id: int, book: Book):
    '''
    Adds a new book if it is not already present and returns its Book ID
    otherwise returns a message stating "Book is already present"
    '''
    for key,value in books.items():
        if book.name == value["name"]:
            return {"message":"Book is already present"}
    books[book_id] = book
    return books[book_id]

@app.put("/update-book-details")
def update_book(book: Book):
    '''
    Searches for a book by name and updates book records if found 
    otherwise returns a message stating "Book not found"
    '''
    for key,value in books.items():
        if book.name == value["name"]:
            books[key] = book
            return {"message":"Book Records updated Successfully"}
    return {"message":"Book not found"}

@app.delete("/remove-book-details")
def delete_book(book: Book):
    '''
    Searches for a book by name and deletes book records if found 
    otherwise returns a message stating "Book not found"
    '''
    for key,value in books.items():
        if value["name"] == book.name:
            del books[key]
            return {"message":"Book Records deleted Successfully"}
    return {"message":"Book not found"}