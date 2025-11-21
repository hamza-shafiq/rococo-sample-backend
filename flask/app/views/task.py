from flask_restx import Namespace, Resource
from flask import request
from app.helpers.response import get_success_response, get_failure_response, parse_request_body, validate_required_fields
from app.helpers.decorators import login_required
from common.app_config import config
from common.services import TaskService
from common.models.task import Task

# Create the task blueprint
task_api = Namespace('tasks', description="Task related APIs")


@task_api.route('')
class Tasks(Resource):

    @task_api.param(
        'completed', 'Filter by completion status: true (completed), false (incomplete), or omit for all',
        type='boolean'
    )
    @login_required()
    def get(self, person):
        """Get all tasks for the current user, optionally filtered by completion status.

        Query parameters:
        - completed (optional): Filter by completion status
          - true: Show only completed tasks
          - false: Show only incomplete tasks
          - omitted: Show all tasks
        """
        completed_param = request.args.get('completed')
        completed = None
        if completed_param is not None:
            if isinstance(completed_param, str):
                completed = completed_param.lower() == 'true'
            else:
                completed = bool(completed_param)

        task_service = TaskService(config)
        tasks = task_service.get_tasks_by_person_id(person.entity_id, completed=completed)

        return get_success_response(tasks=[task.as_dict() for task in tasks])

    @task_api.expect(
        {'type': 'object', 'properties': {
            'title': {'type': 'string'},
        }}
    )
    @login_required()
    def post(self, person):
        """
        Create a new task
        """
        parsed_body = parse_request_body(request, ['title'])
        validate_required_fields(parsed_body)

        task = Task()
        task.person_id = person.entity_id
        task.title = parsed_body['title']
        task.completed = False

        task_service = TaskService(config)
        task = task_service.save_task(task)

        return get_success_response(task=task.as_dict())


@task_api.route('/<string:task_id>')
class TaskById(Resource):

    @login_required()
    def get(self, person, task_id):
        """Get a specific task by ID"""
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id, person.entity_id)

        if not task:
            return get_failure_response(message="Task not found", status_code=404)

        return get_success_response(task=task.as_dict())

    @task_api.expect(
        {'type': 'object', 'properties': {
            'title': {'type': 'string'},
            'completed': {'type': 'string'},
        }}
    )
    @login_required()
    def put(self, person, task_id):
        """Update a task (title and/or completed status)"""
        parsed_body = parse_request_body(request, ['title', 'completed'], default_value=None)

        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id, person.entity_id)

        if not task:
            return get_failure_response(message="Task not found", status_code=404)

        # Update title if provided
        if 'title' in parsed_body and parsed_body['title'] is not None:
            validate_required_fields({'title': parsed_body['title']})
            task.title = parsed_body['title']

        # Update completed status if provided
        if 'completed' in parsed_body and parsed_body['completed'] is not None:
            task.completed = parsed_body['completed'] is True or str(parsed_body['completed']).lower() == 'true'

        task = task_service.save_task(task)

        return get_success_response(task=task.as_dict())

    @login_required()
    def delete(self, person, task_id):
        """Delete a task"""
        task_service = TaskService(config)
        task = task_service.get_task_by_id(task_id, person.entity_id)

        if not task:
            return get_failure_response(message="Task not found", status_code=404)

        task_service.delete_task(task)

        return get_success_response(message="Task deleted successfully")
