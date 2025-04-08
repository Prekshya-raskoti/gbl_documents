
def current_path(request):
    return {
        'current_path': request.path,
        'current_url_name': request.resolver_match.url_name if request.resolver_match else ''
    }
