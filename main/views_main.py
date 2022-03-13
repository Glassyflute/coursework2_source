from flask import Blueprint, render_template, request
from utils import PostsManager
# import logging
POST_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"

main_blueprint = Blueprint("main_blueprint", __name__, template_folder="templates")
# logging.basicConfig(filename="basic.log", level=logging.INFO)


@main_blueprint.route("/")
def page_index():
    # logging.info("Запрошена главная страница")
    posts_manager = PostsManager(POST_PATH, COMMENTS_PATH)
    posts_data = posts_manager.load_posts_from_json()

    return render_template("index.html", posts_data=posts_data)


@main_blueprint.route("/posts/<int:postid>")
def page_post_page_with_comments(postid):
    # logging.info("Запрошена полная страница поста по идентификатору поста
    # с комментариями")
    posts_manager = PostsManager(POST_PATH, COMMENTS_PATH)
    post_data = posts_manager.get_post_by_pk(postid)
    post_comments = posts_manager.get_comments_by_post_id(postid)
    comments_number = len(post_comments)

    return render_template("post.html", post_data=post_data,
                           post_comments=post_comments,
                           comments_number=comments_number)


@main_blueprint.route("/search")
def page_search():
    # logging.info("Запрошена лента с постами по вхождению поискового термина")
    search_term = request.values.get("q")
    posts_manager = PostsManager(POST_PATH, COMMENTS_PATH)
    search_output = posts_manager.search_for_posts(search_term)
    search_results_num = len(search_output)

    if search_results_num > 10:
        return "Слишком много вариантов. Рекомендуем использовать" \
               "другой поисковый термин."

    return render_template("search.html", search_output=search_output,
                           search_results_num=search_results_num)


@main_blueprint.route("/users/<username>")
def page_posts_by_user(username):
    # logging.info("Запрошена лента с постами пользователя")
    posts_manager = PostsManager(POST_PATH, COMMENTS_PATH)
    user_posts = posts_manager.get_posts_by_user(username)

    return render_template("user-feed.html", user_posts=user_posts)

