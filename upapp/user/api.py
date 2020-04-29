from flask import jsonify, Blueprint, request, Response
from upapp.user.models import User, Skill, UserDoesNotExists, UserCreationFailed, FileUploadFiled

bp = Blueprint('user', __name__, url_prefix='/api')


@bp.route('/user', methods=('GET', 'POST'))
def user():
    if request.method == 'GET':
        return User.all()

    elif request.method == 'POST':
        try:
            crated_user = User.create(request.get_json())
            return crated_user, 201
        except KeyError:
            return 500
    else:
        # TODO: - raise exception
        pass


@bp.route('/user/<int:user_id>', methods=('GET', 'DELETE', 'POST'))
def user_by_id(user_id):
    if request.method == 'GET':
        try:
            return User.user(user_id=user_id)
        except (UserDoesNotExists, UserCreationFailed):
            return 'User doesnt exist', 204

    elif request.method == 'DELETE':
        try:
            User.delete(user_id)
            # TODO: - what should be returned?
            return '', 204
        except UserDoesNotExists:
            return 'User doesnt exist', 404

    elif request.method == 'POST':
        try:
            if 'file' not in request.files:
                return 'No file', 500
            file = request.files['file']
            url = User.upload(user_id=user_id, file=file)
            return url, 200
        except FileUploadFiled:
            return 'Upload filed', 500

    else:
        return {}, 404
