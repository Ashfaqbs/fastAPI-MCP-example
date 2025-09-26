from pydantic import BaseModel, Field

# A Pydantic model representing a book and its attributes.
class Book(BaseModel):
    title: str                   # Title of the book (required)
    author: str                  # Author name (required)
    description: str | None = None  # Description (optional, can be None)
    published_year: int          # Year the book was published (required)

    class Config:
        schema_extra = {
            "example": {  # Example data to show in docs
                "title": "The Hitchhiker's Guide to the Galaxy",
                "author": "Douglas Adams",
                "description": "A humorous science fiction novel.",
                "published_year": 1979
            }
        }
