import os
from flask import request
from app.upload import bp
from celery.result import AsyncResult

from app.celery_task import import_file_task
from config import Config

from werkzeug.utils import secure_filename


@bp.route("/", methods=["GET"])
def index():
    return "<h1>Welcome to uploads home page!</h1>"


@bp.route("/uploader", methods=["POST"])
def import_file():
    file = request.files["file"]
    # send in 30 seconds
    task_result = import_file_task.apply_async(args=[file], countdown=30)
    return {"task_id": task_result.id}


@bp.route("/upload", methods=["GET", "POST"])
def upload_file():
    print("-----------request.files----------")
    print(request.files)
    if request.method == "POST":
        try:
            file = request.files["file"]
            if not file.filename:
                # return 'No file found'
                raise LookupError()
            filename = secure_filename(file.filename)
            file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(file_path)

            task_result = import_file_task.apply_async(args=[file_path], countdown=30)
            return {"task_id": task_result.id}, 201
        except LookupError:
            return "No file provided", 400


@bp.route("/task_status/<task_id>", methods=["GET"])
def task_status(task_id):
    task = AsyncResult(task_id)
    print("-----------task----------")
    print(task.info.get("total", 1))
    if task.state in ["FAILURE", "PENDING"]:
        response = {
            "task_id": task_id,
            "state": task.state,
            "progression": "None",
            "info": str(task.info),
        }
        return response
    current = task.info.get("current", 0)
    total = task.info.get("total", 1)
    # display a percentage of the task's progress
    progression = (int(current) / int(total)) * 100
    response = {
        "task_id": task_id,
        "state": task.state,
        "progression": progression,
        "info": "None",
    }
    return response
