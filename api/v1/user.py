import time

from flask import jsonify, g

from libs.error_code import DeleteSuccess
from libs.redprint import Redprint
from libs.token_auth import auth
from models.base import db
from models.user import User

api = Redprint('user')

@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
	user = User.query.filter_by(id=uid).first_or_404()
	return jsonify(user)

@api.route('/<int:uid>', methods=['DELETE'])
@auth.login_required
def super_delete_user(uid):
	pass

@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
	# 超权问题：自己应该只能删除自己
	uid = g.user.uid
	# g 为flask自带全局变量，是线程隔离的
	with db.auto_commit():
		User.query.filter_by(id=uid).first_or_404()
	return DeleteSuccess()

@api.route('', methods=['GET'])
@auth.login_required
def get_user():
	uid = g.user.uid
	user = User.query.filter_by(id=uid).first_or_404()
	return jsonify(user)

