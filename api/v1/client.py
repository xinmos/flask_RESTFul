from libs.enums import ClientTypeEnum
from libs.error_code import Success
from libs.redprint import Redprint
from models.user import User
from validators.forms import ClientForm, UserEmailForm

api = Redprint('client')

@api.route('/register', methods=['post'])
def create_client():
	form = ClientForm().validate_for_api()
	promise = {
		ClientTypeEnum.USER_EMAIL: __register_user_by_email
	}
	promise[form.type.data]()
	return Success()

def __register_user_by_email():
	# 必须用data = data指定，否者会报错
	form = UserEmailForm().validate_for_api()
	User.register_by_email(form.nickname.data,
						   form.account.data,
						   form.secret.data)