from app.api import api
from app.exceptions import ValidationError
from app.main import main
from flask import request, jsonify, render_template


@main.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response= jsonify({'error': 'Not Found'})
        response.status_code=404
        return response
    return render_template('404.html'), 404


@main.errorhandler(500)
def server_error(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response= jsonify({'error': 'Internal Server Error'})
        response.status_code=500
        return response
    return render_template('500.html'), 500


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def unauthorized(message):
    response = jsonify({'error': 'Unauthorized', 'message': message})
    response.status_code = 401
    return response


def bad_request(message):
    response = jsonify({'error': 'Bad Request', 'message': message})
    response.status_code = 400
    return response


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])



