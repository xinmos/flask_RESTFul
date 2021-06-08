from flask import current_app, jsonify

from libs.enums import ClientTypeEnum
from libs.redprint import Redprint
from models.user import User
from validators.forms import ClientForm

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

api = Redprint("token")

@api.route('', methods=["post"])
def get_token():
	form = ClientForm().validate_for_api()
	promise = {
		ClientTypeEnum.USER_EMAIL: User.verify,
	}
	identity = promise[form.type.data](
		form.account.data,
		form.secret.data
	)
	expiration = current_app.config['TOKEN_EXPIRATION']
	token = generator_auth_token(identity['uid'],
								 form.type.data,
								 identity['scope'],
								 expiration=expiration)
	t = {
		'token': token.decode('utf-8')
	}
	return jsonify(t), 201

def generator_auth_token(uid, ac_type, scope=None,
                         expiration=7200):
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope': scope
    })