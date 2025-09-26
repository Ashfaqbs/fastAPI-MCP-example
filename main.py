from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from fastapi_mcp import FastApiMCP
from bson.objectid import ObjectId
from typing import List
from models import Book  # Import the Pydantic model
import uvicorn


# Initialization 
app = FastAPI()


# Connect to MongoDB
client = MongoClient("mongodb://admin:admin123@localhost:27017/?authSource=admin")
db = client["dev"]
collection = db["books"]


@app.post("/books", response_model=Book)
def create_book(book: Book):
    book_dict = book.dict()
    collection.insert_one(book_dict)
    return book


@app.get("/books", response_model=List[Book],operation_id="get books")
def get_books():
    books = []
    for doc in collection.find():
        books.append(Book(**doc))
    return books


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: str):
    book_doc = collection.find_one({"_id": ObjectId(book_id)})
    if book_doc is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return Book(**book_doc)


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: str, book: Book):
    result = collection.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": book.model_dump()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: str):
    result = collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

mcp = FastApiMCP(app,include_operations=[
        "get books"
    ])
mcp.mount_http()
    
if __name__ == "__main__":

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
# python main.py
# or
# uvicorn main:app --reload
