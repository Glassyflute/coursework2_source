from flask import Flask, send_from_directory

# импортируем блюпринт
from api_folder.views_api import api_blueprint
from main.views_main import main_blueprint

POST_PATH = "data/data.json"
COMMENTS_PATH = "data/comments.json"

app = Flask(__name__)

# регистрируем блюпринты
app.register_blueprint(main_blueprint)
app.register_blueprint(api_blueprint, url_prefix="/api")

# доступ к папке uploads, чтобы внешний клиент видел - в текущем задании не требуется
# @app.route("/uploads/<path:path>")
# def static_dir(path):
#     return send_from_directory("uploads", path)

if __name__ == "__main__":
    app.run()
