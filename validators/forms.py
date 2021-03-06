from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from validators.base import BaseForm
from libs.enums import ClientTypeEnum
from models.user import User


class ClientForm(BaseForm):
	account = StringField(validators=[DataRequired(), length(
		min=1, max=32
	)])
	secret = StringField()
	type = IntegerField(validators=[DataRequired()])

	def validate_type(self, value):
		try:
			client = ClientTypeEnum(value.data)
		except ValueError as e:
			raise e
		self.type.data = client

class UserEmailForm(ClientForm):
	account = StringField(validators=[
		Email(message='validate email')
	])
	secret = StringField(validators=[
		DataRequired(),
		Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
	])
	nickname = StringField(validators=[DataRequired(),
									   length(min=2, max=22)])

	def validate_account(self, value):
		if User.query.filter_by(email=value.data).first():
			raise ValidationError(message='账号已经存在')
