from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session

from books.services.books_service import get_books
from core.database import get_db
from books.schemas.books import BookCreate, Book
from books.models.books import Book as BookModel, Author


book_router = APIRouter()


@book_router.post("/books", response_model=Book)
def book_post(
    book: BookCreate,
    db:Session = Depends(get_db),
):
    # move to service method
    authors = db.query(Author).filter(Author.uid.in_(book.authors)).all()

    if set(book.authors) != set([a.uid for a in authors]):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Some of authors not found")

    try:
        db_book = BookModel(
            title=book.title,
            publication_year=book.publication_year,
            pages=book.pages,
            genre=book.genre,
            authors=authors,
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    except IntegrityError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Book with this title already exists")

    return Book.model_validate({
        'uid': db_book.uid,
        'title': db_book.title,
        'publication_year': db_book.publication_year,
        'pages':  db_book.pages,
        'genre': db_book.genre,
        'authors': [a.uid for a in db_book.authors],
    })


# filter: author, genre
# *add pagination
@book_router.get("/books", response_model=list[Book])
def book_list(
    db: Session = Depends(get_db),
    author_uid: str = Query(None, description='Filter books by author UID'),
    genre: str = Query(None, description='Filter books by genre')
):
    db_books = get_books(db, author_uid, genre)
    return db_books
