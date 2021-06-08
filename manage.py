from werkzeug.exceptions import HTTPException

from api import create_app
from libs.error import APIException
from libs.error_code import ServerError


app = create_app()


# 捕获未知异常
@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # TODO log
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e
    pass

if __name__ == '__main__':
    app.run(debug=True)