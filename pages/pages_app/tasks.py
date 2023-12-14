from pages.celery import app

def sendtask(task_name, *args, **kwargs):
    # Send the task message to the queue of the receiver app
    app.send_task(task_name, args=args, kwargs=kwargs)
