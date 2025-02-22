from flask import Blueprint, render_template, request, jsonify
from utils import PostsManager
# import logging
POST_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"

api_blueprint = Blueprint("api_blueprint", __name__, template_folder="templates")
# logging.basicConfig(filename="basic.log", level=logging.INFO)


@api_blueprint.route("/posts")
def get_api_posts():
    # logging.info("Запрашивается страница с постами")
    posts_manager = PostsManager(POST_PATH, COMMENTS_PATH)
    posts_from_json = posts_manager.load_posts_from_json()

    return jsonify(posts_from_json)


@api_blueprint.route("/posts/<int:postid>")
def get_single_api_post(postid):
    # logging.info("Запрашивается страница поста по идентификатору")
    posts_manager = PostsManager(POST_PATH, COMMENTS_PATH)
    post_from_json = posts_manager.get_post_by_pk(postid)
    post_as_dict = post_from_json[0]

    return jsonify(post_as_dict)

