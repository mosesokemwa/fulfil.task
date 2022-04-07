import time
import celery
from flask import jsonify, request
from flask_restful import Api, Resource
import config
from werkzeug.utils import secure_filename
import os

from tasks.celery_task import import_file_task
from celery import current_app as celery_app


api = Api(prefix=config.API_PREFIX)

class HomeAPI(Resource):
    def get(self):
        return jsonify({'message': 'Hello World!'})

class UploaderAPI(Resource):
    def post(self):
        file = request.files["file"]
        # send in 30 seconds
        print("-------------file------------")
        print(file)
        task_result = import_file_task.apply_async(args=[file], countdown=30)
        return jsonify({"task_id": task_result.id})

class UploadAPI(Resource):
    def post(self):
        file = request.files["file"]
        if not file.filename:
            raise LookupError()
        filename = secure_filename(file.filename)
        file_path = os.path.join(config.UPLOAD_FOLDER, filename)
        file.save(file_path)

        task_result = import_file_task.apply_async(args=[file_path], countdown=30)
        return {"task_id": task_result.id}, 201


class TaskStatusAPI(Resource):
    def get(self, task_id):
        # task = celery.AsyncResult(task_id)
        task = celery_app.tasks['import_file_task'].AsyncResult(task_id)
        return jsonify(task.result)


class TaskStatusResultAPI(Resource):
    def get(self, task_id):
        task = celery.AsyncResult(task_id)
        if task.state in ["FAILURE", "PENDING"]:
            response = {
                "task_id": task_id,
                "state": task.state,
                "progression": "None",
                "info": str(task.info),
            }
            return jsonify(response)
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
        return jsonify(response)


# data processing endpoint
api.add_resource(HomeAPI, '/')
api.add_resource(UploaderAPI, "/uploader")
api.add_resource(UploadAPI, "/upload")
api.add_resource(TaskStatusAPI, "/tasks/<string:task_id>")
api.add_resource(TaskStatusResultAPI, "/tasks/<string:task_id>")