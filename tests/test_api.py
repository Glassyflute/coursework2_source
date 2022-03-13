import pytest
from app import app


def test_app_posts():
    response = app.test_client().get("/api/posts")
    assert response.status_code == 200, "Страница не запрошена"
    assert response.data is not None, "Не возвращаются данные"

    # ниже проверка типа данных - список
    assert isinstance(response.json, list)

    # проверка на наличие нужных ключей
    posts_keys = [
        "poster_name", "poster_avatar", "pic", "content", "views_count",
        "likes_count", "pk"
    ]

    for dict_item in response.json:
        post_data_keys = list(dict_item.keys())

        for i in range(len(post_data_keys)):
            assert post_data_keys[i] in posts_keys


def test_app_posts_by_pk():
    response = app.test_client().get("/api/posts/2")
    assert response.status_code == 200, "Страница не запрошена"
    assert response.json.get("poster_name") == "johnny", "Словарь не возвращается"

    # ниже проверка типа данных - словарь
    assert isinstance(response.json, dict)

    # проверка на наличие нужных ключей
    post_keys = [
        "poster_name", "poster_avatar", "pic", "content", "views_count",
        "likes_count", "pk"
    ]
    selected_dict = response.json
    for key_value in selected_dict.keys():
        if key_value in post_keys:
            assert True


def test_app_posts_by_absent_pk():
    response = app.test_client().get("/api/posts/32443534")
    assert response.status_code == 500, "Страница не запрошена"

