import pytest
from utils import PostsManager
from exceptions import NoFilePathPosts, NoFilePathComments
POST_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"


class TestPostsManager:
    def test_init_nofilepathposts(self):
        with pytest.raises(NoFilePathPosts):
            posts_manager = PostsManager("", COMMENTS_PATH)

    def test_init_nofilepathcomments(self):
        with pytest.raises(NoFilePathComments):
            posts_manager = PostsManager(POST_PATH, "")

    def test_load_posts_from_json(self):
        posts_manager = PostsManager(POST_PATH, COMMENTS_PATH)
        posts_data = posts_manager.load_posts_from_json()
        assert isinstance(posts_data, list), "Проблема с загрузкой данных из json"
        assert len(posts_data) >= 1, "Пустой список, данные не получены из json"
        assert len(posts_data[0]) >= 1, "Пустой словарь в списке, данные " \
                                        "не получены из json"

    def test_load_comments_from_json(self):
        posts_manager = PostsManager(POST_PATH, COMMENTS_PATH)
        comments_data = posts_manager.load_comments_from_json()
        assert isinstance(comments_data, list), "Проблема с загрузкой данных из json"
        assert len(comments_data) >= 1, "Пустой список, данные не получены из json"
        assert len(comments_data[0]) >= 1, "Пустой словарь в списке, данные " \
                                           "не получены из json"

    def test_search_for_posts(self):
        posts_manager = PostsManager(POST_PATH, COMMENTS_PATH)
        search_output = None
        search_result_a = posts_manager.search_for_posts("а")
        if search_result_a:
            search_output = search_result_a
            assert len(search_output) >= 1, "Поиск в постах не работает"
        if not search_result_a:
            assert len(search_output) == 0, "Поиск в постах не работает"

    def test_get_posts_by_user(self):
        posts_manager = PostsManager(POST_PATH, COMMENTS_PATH)
        search_output = None
        search_result_a = posts_manager.get_posts_by_user("a")
        if search_result_a:
            search_output = search_result_a
            assert len(search_output) >= 1, "Поиск по части имени пользователя " \
                                            "не работает"
        if not search_result_a:
            assert len(search_output) == 0, "Поиск по части имени пользователя " \
                                            "не работает"

    def test_get_post_by_pk(self):
        posts_manager = PostsManager(POST_PATH, COMMENTS_PATH)
        search_output = None
        search_result = posts_manager.get_post_by_pk(2)
        if search_result:
            search_output = search_result
            assert len(search_output) == 1, "Поиск по идентификатору поста не работает"
        if not search_result:
            assert len(search_output) == 0, "Поиск по идентификатору поста не работает"

    def test_get_comments_by_post_id(self):
        posts_manager = PostsManager(POST_PATH, COMMENTS_PATH)
        search_output = None
        search_result = posts_manager.get_comments_by_post_id(2)
        if search_result:
            search_output = search_result
            assert len(search_output) >= 1, "Поиск комментариев по " \
                                            "идентификатору поста не работает"
        if not search_result:
            assert len(search_output) == 0, "Поиск комментариев по " \
                                            "идентификатору поста не работает"

