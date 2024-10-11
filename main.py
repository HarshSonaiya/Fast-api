from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
import os
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from .env
load_dotenv()
uri = os.getenv("ATLAS_URI")

# Book model to validate incoming data
class Book(BaseModel):
    name: str
    author: str

@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB when the app starts"""
    app.mongodb_client = MongoClient(uri)
    app.mongodb = app.mongodb_client["test"]  
    app.book_collection = app.mongodb["books"]  
    print("MongoDB connected.")

@app.on_event("shutdown")
async def shutdown_event():
    """Close the MongoDB connection when the app shuts down"""
    app.mongodb_client.close()

@app.post("/add-book/")
async def add_new_book(book: Book):
    """
    Adds a new book if it's not already present and returns success message.
    """
    existing_book = await app.book_collection.find_one({"name": book.name})
    if existing_book:
        raise HTTPException(status_code=400, detail="Book is already present")
    
    new_book = book.dict()
    await app.book_collection.insert_one(new_book)
    return {"message": "Book inserted successfully"}

@app.get("/get-book/{name}")
async def get_book_by_name(name: str):
    """
    Retrieves a book's details by its name.
    """
    book = await app.book_collection.find_one({"name": name})
    if book:
        del book["_id"]  # Remove MongoDB's internal ID from the result
        return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.get("/available-books")
async def get_available_books():
    """
    Retrieves the list of all available books.
    """
    books = await app.book_collection.find().to_list(length=100)
    for book in books:
        del book["_id"]  # Remove MongoDB's internal ID from the result
    return books

@app.put("/update-book/{name}")
async def update_book(name: str, book: Book):
    """
    Updates book details by its name.
    """
    update_result = await app.book_collection.update_one(
        {"name": name},
        {"$set": book.dict()}
    )
    if update_result.modified_count == 1:
        return {"message": "Book updated successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/remove-book/{name}")
async def delete_book(name: str):
    """
    Deletes a book by its name.
    """
    delete_result = await app.book_collection.delete_one({"name": name})
    if delete_result.deleted_count == 1:
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
