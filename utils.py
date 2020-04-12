def get_token_from_request(request):
    try:
        token = request.META['HTTP_AUTHORIZATION']
        if token[0] == '{':
            return token
        else:
            return token[7:]
    except (IndexError, KeyError):
        return None
