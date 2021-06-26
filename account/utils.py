def get_user_from_request(request):
	user = None
	if request.user.is_authenticated:
		user = request.user
	return user

