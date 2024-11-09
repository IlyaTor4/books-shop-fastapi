from typing import Any

import pytest
from fastapi.testclient import TestClient
from fastapi import status


@pytest.fixture()
def book_without_authors_payload() -> dict[str, Any]:
    return {
        'title': 'Test Book',
        'publication_year': 2023,
        'pages': 250,
        'genre': 'Fiction',
        'authors': []
    }


@pytest.fixture()
def book_invalid_payload() -> dict[str, Any]:
    return {
        'title': '',
        'publication_year': 5005,
        'pages': 250,
        'genre': 345,
        'authors': []
    }


@pytest.fixture()
def book_invalid_author() -> dict[str, Any]:
    return {
        'title': 'Test Book',
        'publication_year': 2023,
        'pages': 250,
        'genre': 'Fiction',
        'authors': ["b41225b8-966f-409a-a6a0-c671fc686c9a"]
    }




def test_book_post(test_client: TestClient, book_without_authors_payload: dict[str, Any]) -> None:
    response = test_client.post('/api/books', json=book_without_authors_payload)

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data['title'] == book_without_authors_payload['title']
    assert response_data['publication_year'] == book_without_authors_payload['publication_year']
    assert response_data['pages'] == book_without_authors_payload['pages']
    assert response_data['genre'] == book_without_authors_payload['genre']
    assert set(response_data['authors']) == set(book_without_authors_payload['authors'])


def test_book_post__invalid_params(test_client: TestClient, book_invalid_payload: dict[str, Any]) -> None:
    response = test_client.post('/api/books', json=book_invalid_payload)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_book_post__invalid_author(test_client: TestClient, book_invalid_author: dict[str, Any]) -> None:
    response = test_client.post('/api/books', json=book_invalid_author)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Some of authors not found'}
