from flask import current_app, request, g
from flask_httpauth import HTTPBasicAuth
from collections import namedtuple
from itsdangerous import \
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from libs.error_code import AuthFailed, Forbidden

auth = HTTPBasicAuth()
User = namedtuple("user", ["uid", "ac_type", "scope"])


def verify_auth_token(token):
	s = Serializer(current_app.config['SECRET_KEY'])
	try:
		data = s.loads(token)
	# token 有误
	except BadSignature:
		raise AuthFailed(msg='token is valid', error_code=1002)
	# token 过期
	except SignatureExpired:
		raise AuthFailed(msg='token is expired', error_code=1003)
	uid = data['uid']
	ac_type = data['type']
	scope = data['scope']

	return User(uid, ac_type, scope)


@auth.verify_password
def verify_password(token, password):
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
    return True