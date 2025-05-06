from django.shortcuts import redirect
from django.contrib import messages

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [
            '/login/',
            '/admin/',
            '/logout/',
            '/api/',
            '/media/',
            '/static/',
            '/password_reset_view/',
            '/email_verify/',
            '/change_password/',
            '/favicon.ico',
        ]
    
    def __call__(self, request):
        path = request.path_info
        
        if any(path.startswith(url) for url in self.exempt_urls):
            return self.get_response(request)
            
        if request.user.is_authenticated:
            if path.startswith('/dashboard/') and not request.user.is_superuser:
                messages.error(request, "You do not have permission to access this section.")
                return redirect('dashboard')
            return self.get_response(request)
            
        login_url = f"/login/?next={request.path}" if request.path != '/login/' else '/dashboard/'
        return redirect(login_url)

    async def __acall__(self, request):
        path = request.path_info
        
        if any(path.startswith(url) for url in self.exempt_urls):
            return await self.get_response(request)
            
        if request.user.is_authenticated:
            if path.startswith('/dashboard/') and not request.user.is_superuser:
                messages.error(request, "You do not have permission to access this section.")
                return redirect('login')
            return await self.get_response(request)
            
        login_url = f"/login/?next={request.path}" if request.path != '/login/' else '/dashboard/'
        return redirect(login_url)
