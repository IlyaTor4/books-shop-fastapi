from typing import List

from sqlalchemy.orm import Session

from books.models.books import Book as BookModel, Author
from books.schemas.books import Book



def get_books(db: Session, author_uid: str = None, genre: str = None) -> List[Book]:
    query = db.query(BookModel)

    if author_uid:
        query = query.join(BookModel.authors).filter(Author.uid == author_uid)
    if genre:
        query = query.filter(BookModel.genre == genre)

    books = query.all()

    return [
        Book.model_validate({
            'uid': book.uid,
            'title': book.title,
            'publication_year': book.publication_year,
            'pages': book.pages,
            'genre': book.genre,
            'authors': [author.uid for author in book.authors],
        })
        for book in books
    ]
