"""
Module to create a Celery instance for background task processing in Flask applications.
"""

from celery import Celery


def make_celery(app):
    """
    Create a Celery instance using the provided Flask app.

    Parameters:
        app (Flask): The Flask application instance.

    Returns:
        Celery: The Celery application instance.
    """
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        """
        A subclass of Celery's Task class that automatically creates a Flask application 
        context before executing the task.
        """

        abstract = True

        def __call__(self, *args, **kwargs):
            """
            Execute the task within a Flask application context.

            Parameters:
                *args: Positional arguments to be passed to the task.
                **kwargs: Keyword arguments to be passed to the task.

            Returns:
                Any: The result of executing the task.
            """
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
