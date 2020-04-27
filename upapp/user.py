from flask import Blueprint

bp = Blueprint('user', __name__, url_prefix='/api')


@bp.route('/user/', methods=('GET', 'POST'))
def user():
    return 'User'


@bp.route('/user/<int:user_id>', methods=('GET', 'DELETE'))
def user_by_id(user_id):
    return 'User id {user_id}'.format(user_id=user_id)
