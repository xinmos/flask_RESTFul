from libs.redprint import Redprint

api = Redprint('book')

@api.route('', methods=["get"])
def get_book():
	return 'get book'