from flask import Flask, Blueprint, render_template, send_from_directory

# импортируем блюпринт
from api_folder.views_api import api_blueprint
from main.views_main import main_blueprint

POST_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"
# UPLOAD_FOLDER = "uploads/img"

app = Flask(__name__)

# регистрируем блюпринты
app.register_blueprint(main_blueprint)
app.register_blueprint(api_blueprint)


# # доступ к папке uploads, чтобы внешний клиент видел
# @app.route("/uploads/<path:path>")
# def static_dir(path):
#     return send_from_directory("uploads", path)


app.run()
