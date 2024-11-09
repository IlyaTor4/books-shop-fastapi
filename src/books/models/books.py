import uuid
from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, UUID, Table, Column, ForeignKey
from core.database import Base


author_book_association = Table(
    'author_book',
    Base.metadata,
    Column('author_uid', UUID, ForeignKey('author.uid'), primary_key=True),
    Column('book_uid', UUID, ForeignKey('book.uid'), primary_key=True)
)

class Author(Base):
    __tablename__ = 'author'

    uid: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    books: Mapped[List["Book"]] = relationship(
        "Book",
        secondary=author_book_association,
        back_populates="authors"
    )



class Book(Base):
    __tablename__ = 'book'

    uid: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    publication_year: Mapped[int] = mapped_column(Integer, nullable=False)
    pages: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str] = mapped_column(String(64), nullable=False)
    authors: Mapped[List["Author"]] = relationship(
        "Author",
        secondary=author_book_association,
        back_populates="books"
    )
