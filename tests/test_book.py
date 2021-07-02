def test_get_all_books(client):
    response = client.get("/books/")

    assert response.json == [
        {"id": 1, "author": "Brown", "title": "Origin"},
        {"id": 2, "author": "Rowling", "title": "Harry Potter"},
        {"id": 3, "author": "Shevchenko", "title": "Kobzar"},
        {"id": 4, "author": "Brown", "title": "Inferno"},
    ]


def test_get_all_books_by_author(client):
    response = client.get("/books/?author=Brown")

    assert response.json == [
        {"id": 1, "author": "Brown", "title": "Origin"},
        {"id": 4, "author": "Brown", "title": "Inferno"},
    ]


def test_get_all_books_by_wrong_author(client):
    response = client.get("/books/?author=hello")

    assert response.json == []


def test_get_book_by_correct_id(client):
    id = 1

    response = client.get(f"/books/{id}")

    assert response.json == {"id": 1, "author": "Brown", "title": "Origin"}


def test_get_book_by_incorrect_id(client):
    id = "asd"

    response = client.get(f"/books/{id}")

    assert response.status_code == 422


def test_get_book_by_id_not_in_collection(client):
    id = 10

    response = client.get(f"/books/{id}")

    assert response.json == {"error": f"no book with id:{id}"}


def test_create_book_correct_body(client):
    new_book = {"id": 5, "author": "new author", "title": "new title"}

    response = client.post("/books/", json=new_book)

    assert response.json == new_book


def test_create_book_incorrect_body(client):
    new_book = {"id": 5, "title": "new title"}

    response = client.post("/books/", json=new_book)

    assert response.status_code == 422


def test_create_book_with_existing_id(client):
    new_book = {"id": 4, "author": "new author", "title": "new title"}

    response = client.post("/books/", json=new_book)

    assert response.json == {"error": f"book with id:{new_book['id']} already exists"}


def test_update_book_correct_body_and_id(client):
    id = 4
    updated_book = {"author": "new author", "title": "new title"}

    response = client.put(f"/books/{id}", json=updated_book)

    assert response.json == {**updated_book, "id": id}


def test_update_book_correct_body_incorrect_id(client):
    id = "qwe"
    updated_book = {"author": "new author", "title": "new title"}

    response = client.put(f"/books/{id}", json=updated_book)

    assert response.status_code == 422


def test_update_book_incorrect_body_correct_id(client):
    id = 4
    updated_book = {"author": "new author"}

    response = client.put(f"/books/{id}", json=updated_book)

    assert response.status_code == 422


def test_update_book_id_not_in_collection(client):
    id = 100
    updated_book = {"author": "new author", "title": "new title"}

    response = client.put(f"/books/{id}", json=updated_book)

    assert response.json == {"error": f"no book with id:{id}"}


def test_delete_book_correct_id(client):
    id = 1

    response = client.delete(f"/books/{id}")

    assert response.json == {"id": 1, "author": "Brown", "title": "Origin"}


def test_delete_book_incorrect_id(client):
    id = "asd"

    response = client.delete(f"/books/{id}")

    assert response.status_code == 422


def test_delete_book_id_not_in_collection(client):
    id = 100

    response = client.delete(f"/books/{id}")

    assert response.json == {"error": f"no book with id:{id}"}
