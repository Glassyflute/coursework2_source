# это бэкап всех методов класса - драфт и идеи.
# используемые для решения в курсовой методы находятся в файле utils
# др доп идеи бэкапятся здесь

import json
from json import JSONDecodeError
from exceptions import DataWriteError, NoFilePathPosts, NoFilePathComments
from pprint import pprint as pp


class PostsManager:
    """
    Класс для обработки постов. Загружает для чтения данные из json по ссылкам
     (path и comments), ищет посты по query-запросу,
     перезаписывает данные в json
    """
    def __init__(self, path, comments):
        if not path:
            raise NoFilePathPosts("Некорректно указан путь к файлу постов")
        if not comments:
            raise NoFilePathComments("Некорректно указан путь к файлу комментариев")

        self.path = path
        self.comments = comments

    def load_posts_from_json(self):
        """
        Загружает для чтения данные из json по ссылке (path)
        :return:
        """
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                posts_data = json.load(file)
            return posts_data
        except FileNotFoundError:
            print("Файл с данными постов не найден")
        except JSONDecodeError:
            print("Ошибка в чтении файла json с данными постов")

    def load_comments_from_json(self):
        """
        возвращает посты с комментариями из файла json
        :return:
        """
        try:
            with open(self.comments, "r", encoding="utf-8") as file:
                comments_data = json.load(file)
            return comments_data
        except FileNotFoundError:
            print("Файл с комментариями не найден")
        except JSONDecodeError:
            print("Ошибка в чтении файла json с комментариями")





    def get_posts_all(self):
        """
        возвращает посты с данными и комментариями из файлов json
        :return:
        """
        posts_data = self.load_posts_from_json()
        all_posts = []

        for post in posts_data:
            all_post_data = []
            post_id = int(post["pk"])
            all_post_data.append(post)
            comments_selected = self.get_comments_by_post_id(post_id)

            for comment in comments_selected:
                all_post_data.append(comment)

            all_posts.append(all_post_data)

        return all_posts

    def get_post_data_all(self, post_id):
        """
        возвращает пост с данными и комментариями из файлов json
        :return:
        """
        posts_data = self.load_posts_from_json()
        all_post_data = []

        for post in posts_data:
            post_id_ = int(post["pk"])
            if post_id_ == int(post_id):
                all_post_data.append(post)
                comments_selected = self.get_comments_by_post_id(post_id_)
                for comment in comments_selected:
                    all_post_data.append(comment)

        return all_post_data


    def get_all_post_data_by_id(self, post_id):
        """
        возвращает 2 списка: данные поста по id, комментарии к этому посту
        :param post_id:
        :return:
        """
        post_by_id = self.get_post_by_pk(post_id)
        comments_by_id = self.get_comments_by_post_id(post_id)

        return post_by_id, comments_by_id





    def search_for_posts(self, query):
        """
        возвращает список словарей по вхождению query
        :param query:
        :return:
        """
        if not query:
            return []
        else:
            query_lower = query.lower()
            posts_selected = []

            posts_data = self.load_posts_from_json()
            for post in posts_data:
                search_text = post["content"].lower()
                if query_lower in search_text:
                    posts_selected.append(post)
            return posts_selected

    def search_for_posts_full(self, query):
        """
        возвращает список словарей по вхождению query в содержимом поста или комментариях
        :param query:
        :return:
        """
        query_lower = query.lower()

        posts_selected = []
        post_id_list = []

        posts_data = self.load_posts_from_json()
        for post in posts_data:
            search_text = post["content"].lower()
            if query_lower in search_text:
                selected_post_id = int(post["pk"])
                post_id_list.append(selected_post_id)

        comments_data = self.load_comments_from_json()
        for comment in comments_data:
            search_text = comment["comment"].lower()
            if query_lower in search_text:
                selected_comment_by_post_id = int(comment["post_id"])
                post_id_list.append(selected_comment_by_post_id)

        post_id_set = set(post_id_list)
        post_id_list_formatted = list(post_id_set)

        for id_value in post_id_list_formatted:
            selected_post = self.get_post_data_all(id_value)
            posts_selected.append(selected_post)

        return posts_selected







    def get_posts_by_user(self, user_name):
        """
        возвращает посты определенного пользователя
        :param user_name:
        :return:
        """
        user_name_lower = user_name.lower()
        posts_selected = []

        posts_data = self.load_posts_from_json()
        for post in posts_data:
            search_text = post["poster_name"].lower()
            if user_name_lower in search_text:
                posts_selected.append(post)
        return posts_selected

    def get_post_by_pk(self, pk):
        """
        возвращает один пост по его идентификатору
        :return:
        """
        post_id_number = int(pk)
        posts_selected = []

        posts_data = self.load_posts_from_json()
        for post in posts_data:
            search_text = int(post["pk"])
            if post_id_number == search_text:
                posts_selected.append(post)
        return posts_selected

    def get_comments_by_post_id(self, post_id):
        """
        возвращает комментарии определенного поста по id поста
        :param post_id:
        :return:
        """
        post_id_number = int(post_id)
        comments_selected = []

        comments_data = self.load_comments_from_json()
        for comment in comments_data:
            search_text = int(comment["post_id"])
            if post_id_number == search_text:
                comments_selected.append(comment)
        return comments_selected


    def overwrite_json_data(self, posts_data):
        """
        перезаписывает данные в json
        :param posts_data:
        :return:
        """
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(posts_data, file, ensure_ascii=False)
        except FileNotFoundError:
            print("Файл не найден")

    def add_post_to_json_list(self, new_post):
        """
        добавляет новый пост в файл json со списком постов в формате словарей
        :param new_post:
        :return:
        """
        posts_data = self.load_posts_from_json()
        try:
            posts_data.append(new_post)
            self.overwrite_json_data(posts_data)
        except DataWriteError:
            print("Данные не были перезаписаны в файл json")


POST_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"

posts_manager = PostsManager(POST_PATH, COMMENTS_PATH)

# pp(posts_manager.load_posts_from_json())
# print(len(posts_manager.load_posts_from_json()))
# print("===")
# pp(posts_manager.load_comments_from_json())
# print(len(posts_manager.load_comments_from_json()))
# print("=======")
#
# pp(posts_manager.get_post_by_pk(2))
# pp(posts_manager.get_post_by_pk(3))
# print("-- post by pk done --")
#
# pp(posts_manager.get_comments_by_post_id(3))
# print(len(posts_manager.get_comments_by_post_id(3)))
#
# pp(posts_manager.get_comments_by_post_id(4))
# print(len(posts_manager.get_comments_by_post_id(4)))
# print("-- post by post id done --")
#
#
# pp(posts_manager.get_posts_by_user("johnny"))
# pp(posts_manager.get_posts_by_user("leo"))
# print("======= by user done === ")
#
# pp(posts_manager.search_for_posts("тром"))
# pp(posts_manager.search_for_posts("Раньше"))
# pp(posts_manager.search_for_posts(""))
# print("----- search by query done ---- ")


# pp(posts_manager.get_all_post_data_by_id(2))
# print(len(posts_manager.get_all_post_data_by_id(2)))
# post_full_data = posts_manager.get_all_post_data_by_id(2)
#
# # post without comments - in list
# print(post_full_data[0])
# # comments for the post in list
# print(post_full_data[1])
#
# print("=== BREAK ================")

# pp(posts_manager.get_posts_all())
# print(len(posts_manager.get_posts_all()))
# print("fffffffffffffffffff")


# pp(posts_manager.get_post_data_all(1))
# print(len(posts_manager.get_post_data_all(1)))

# pp(posts_manager.search_for_posts_full("где"))
# pp(posts_manager.search_for_posts_full("класс"))
# pp(posts_manager.search_for_posts_full("лампочка"))


###################################################################
# def test_xxxxx(test_input_1, test_input_2, expected):
#     assert xxxx(test_input_1, test_input_2) == expected
#
#

# Протестируйте эндпоинт GET /api/posts , проверьте, что
# 	• возвращается список
# 	• у элементов есть нужные ключи
# Не проверяйте количество элементов в списке, так как оно может меняться
# Протестируйте эндпоинт GET /api/posts/<post_id> , проверьте, что
# 	• возвращается словарь
# 	• у элемента есть нужные ключи
# Не проверяйте данные в полученном словаре, это не обязательно.

# import pytest
# from utils import PostsManager
# from exceptions import NoFilePathPosts, NoFilePathComments
# from app import app
#
#
# def test_app_posts():
#     response = app.test_client().get("/api/posts")
#     assert response.status_code == 200, "Страница не запрошена"
#     assert response.data is not None, "Не возвращаются данные"
#     # ниже проверка типа данных - список
#     assert isinstance(response.json, list)
#
#     # проверка на наличие нужных ключей
#     posts_keys = [
#         "poster_name", "poster_avatar", "pic", "content", "views_count",
#         "likes_count", "pk"
#     ]
#     for item in response.json:
#         post_data_keys = item.keys()
#         if post_data_keys != posts_keys:
#             assert False
#
#
# def test_app_posts_by_pk():
#     response = app.test_client().get("/api/posts/2")
#     assert response.status_code == 200, "Страница не запрошена"
#     assert response.json.get("poster_name") == "johnny", "Словарь не возвращается"
#     # ниже проверка типа данных - словарь
#     assert isinstance(response.json, dict)
#
#     # проверка на наличие нужных ключей
#     post_keys = [
#         "poster_name", "poster_avatar", "pic", "content", "views_count",
#         "likes_count", "pk"
#     ]
#     for item in response.json:
#         post_data_keys = item.keys()
#         if post_data_keys != post_keys:
#             assert False
#
#
# def test_app_posts_by_absent_pk():
#     response = app.test_client().get("/api/posts/32443534")
#     assert response.status_code == 404, "Страница не запрошена"


############

# @pytest.mark.parametrize(
#     "pk, status_code",
#     [
#         (2, 200),
#         (32443534, 500)
#     ]
# )
# def test_app_posts_by_pk(pk, status_code):
#     response = app.test_client().get(f"/api/posts/{pk}")
#     assert response.status_code == status_code
#
#
#     # ниже проверка типа данных - словарь
#     assert isinstance(response.json, dict)

    # проверка на наличие нужных ключей
    # post_keys = [
    #     "poster_name", "poster_avatar", "pic", "content", "views_count",
    #     "likes_count", "pk"
    # ]
    # for item in response:
    #     post_data_keys = item.keys()
    #     if post_data_keys != post_keys:
    #         assert False


# for key_value in post_keys:
#     assert response.json.get(key_value) == selected_dict[key_value]

# if post_data_keys != posts_keys:
#     assert False

# for i in range(len(posts_keys)):
#     assert post_data_keys[i] == posts_keys[i]

