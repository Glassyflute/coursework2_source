import json
from json import JSONDecodeError
from exceptions import NoFilePathPosts, NoFilePathComments


class PostsManager:
    """
    Класс для обработки постов. Загружает для чтения данные из json по ссылкам
     (path и comments), ищет посты по query-запросу,
     возвращает посты определенного пользователя, пост по его идентификатору,
     комментарии к посту по идентификатору поста
    """
    def __init__(self, path, comments):
        if not path:
            raise NoFilePathPosts("Некорректно указан путь к файлу постов")
        if not comments:
            raise NoFilePathComments("Некорректно указан путь к файлу комментариев")

        self.path = path
        self.comments = comments

    # get_posts_all() заменена двумя функциями ниже для получения данных по постам
    # и комментариям из файлов json

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
        Загружает для чтения все комментарии к постам из файла json
        по ссылке (comments)
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

    def get_posts_by_user(self, user_name):
        """
        возвращает посты определенного пользователя (по вхождению строки)
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
        возвращает комментарии к посту по идентификатору поста
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

