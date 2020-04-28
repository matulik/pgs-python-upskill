from flask import jsonify, Blueprint, request, Response
from upapp.user.models import User, Skill

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


@bp.route('/user/<int:user_id>', methods=('GET', 'DELETE'))
def user_by_id(user_id):
    if request.method == 'GET':
        return User.user(user_id=user_id)

    elif request.method == 'DELETE':
        pass


