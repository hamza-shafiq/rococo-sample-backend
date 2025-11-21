from flask_restx import Namespace, Resource
from flask import request
from app.helpers.response import get_success_response, get_failure_response, parse_request_body, validate_required_fields
from app.helpers.decorators import login_required
from common.app_config import config
from common.services import PersonService

# Create the organization blueprint
person_api = Namespace('person', description="Person-related APIs")


@person_api.route('/me')
class Me(Resource):
    
    @login_required()
    def get(self, person):
        return get_success_response(person=person.as_dict())

    @person_api.expect(
        {'type': 'object', 'properties': {
            'first_name': {'type': 'string'},
            'last_name': {'type': 'string'}
        }}
    )
    @login_required()
    def put(self, person):
        """Update the current user's name"""
        parsed_body = parse_request_body(request, ['first_name', 'last_name'], default_value=None)

        # At least one field must be provided
        if parsed_body.get('first_name') is None and parsed_body.get('last_name') is None:
            return get_failure_response(message="At least one of 'first_name' or 'last_name' must be provided")

        # Validate provided fields
        if parsed_body.get('first_name') is not None:
            validate_required_fields({'first_name': parsed_body['first_name']})
            person.first_name = parsed_body['first_name']

        if parsed_body.get('last_name') is not None:
            validate_required_fields({'last_name': parsed_body['last_name']})
            person.last_name = parsed_body['last_name']

        person_service = PersonService(config)
        person = person_service.save_person(person)

        return get_success_response(person=person.as_dict())
