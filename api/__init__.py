from config import setting, secure
from datetime import date

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder

from libs.error_code import ServerError


class JSONEncoder(_JSONEncoder):
	# python 中有无法序列化的对象时会再次调用 default，递归调用
	def default(self, o):
		if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
			return dict(o)
			# 兼容其他的序列化
		if isinstance(o, date):
			return o.strftime('%Y-%m-%d')
		return ServerError()

class Flask(_Flask):
	json_encoder = JSONEncoder

def register_blueprint(app):
	from api.v1 import create_blueprint_v1
	app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')

def register_plugin(app):
	from models.base import db
	db.init_app(app)
	with app.app_context():
		db.create_all()

def create_app():
	app = Flask(__name__)
	app.config.from_object(setting)
	app.config.from_object(secure)

	register_blueprint(app)
	register_plugin(app)

	return app