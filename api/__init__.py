import os

import config
from celery.result import AsyncResult
from flask import jsonify, request
from flask_restful import Api, Resource
from tasks import celery
from tasks.celery_task import import_file_task
from werkzeug.utils import secure_filename

api = Api(prefix=config.as_dict()['DevConfig'].API_PREFIX)


class HomeAPI(Resource):
    def get(self):
        return jsonify({"message": "Hello World!"})


class UploaderAPI(Resource):
    def post(self):
        file = request.files["file"]
        # send in 30 seconds
        # task_result = import_file_task.apply_async(args=[file], countdown=30)
        task_result = import_file_task.delay(file)
        return jsonify({"task_id": task_result.id}, 200)


class UploadAPI(Resource):
    def post(self):
        file = request.files["file"]
        if not file.filename:
            raise LookupError()
        filename = secure_filename(file.filename)
        file_path = os.path.join(config.as_dict()[config.CURRENT_ENV].UPLOAD_FOLDER, filename)
        file.save(file_path)
        task_result = import_file_task.apply_async(args=[file_path], queue='high_priority', priority=0, countdown=10)
        return {"task_id": task_result.id}, 200

import json
class TaskStatusAPI(Resource):
    def get(self, task_id):
        if task_id:
            job = AsyncResult(task_id, app=celery)
            print(f"Task id {task_id} with state {job.state} and result {job.result}")
            if job.state == 'PROGRESS':
                return json.dumps(dict(
                    state=job.state,
                    progress=float(job.result['current'] * 1.0 / job.result['total']),
                ))
            elif job.state == 'PENDING':
                return json.dumps(dict(
                    state=job.state,
                    progress=0.0,
                ))
            elif job.state == 'SUCCESS':
                return dict(
                    state=job.state,
                    progress=1.0,
                    result=job.result
                )
        return '{}'


# data processing endpoint
api.add_resource(HomeAPI, "/")
api.add_resource(UploaderAPI, "/uploader")
api.add_resource(UploadAPI, "/upload")
api.add_resource(TaskStatusAPI, "/tasks/<string:task_id>")
