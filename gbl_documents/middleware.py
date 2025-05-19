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
            '/favicon.ico',
            '/vendor/',
            '/documents/',      
            '/contracts/',
            '/dashboard/',
            '/ajax/filter-vendors/',
            '/api/token/',
            '/api/token/refresh/',
        
        ]
    
    def __call__(self, request):
        path = request.path_info

    # Bypass for DRF/REST API
        if path.startswith('/api/') or request.headers.get('Authorization', '').startswith('Bearer'):
            return self.get_response(request)

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
