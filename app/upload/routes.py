
from app.upload import bp
from celery.result import AsyncResult

from app.celery_task import import_file_task


@bp.route("/", methods=['GET'])
def index():
    return "<h1>Welcome to uploads home page!</h1>"

@bp.route("/import", methods=['POST'])
def import_file():
    # send in 30 seconds
    task_result = import_file_task.apply_async(args=["products.csv"], countdown=30)
    return {"task_id": task_result.id}


@bp.route("/task_status/<task_id>", methods=['GET'])
def task_status(task_id):
    task = AsyncResult(task_id)
    if task.state in ['FAILURE', 'PENDING']:
        response = {
            'task_id': task_id,
            'state': task.state,
            'progression': "None",
            'info': str(task.info)
        }
        return response
    current = task.info.get('current', 0)
    total = task.info.get('total', 1)
    # display a percentage of the task's progress
    progression = (int(current) / int(total)) * 100
    response = {
        'task_id': task_id,
        'state': task.state,
        'progression': progression,
        'info': "None"
    }
    return response
