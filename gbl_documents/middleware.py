from django.shortcuts import redirect
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin

class RestrictUserMiddleware(MiddlewareMixin):
    login_url = '/login/'

    def process_request(self, request):
        path = request.path

        public_paths = [
            "/login/", "/logout", "/api", "/admin", "/media", "/static", "/password_reset_view", "/email_verify", "/change_password","/favicon.ico"
        ]

        if any(path.startswith(p) for p in public_paths):
            return None

        if not request.user.is_authenticated:
            if not path.startswith('/accounts/login/'):
                return redirect_to_login(request.get_full_path(), self.login_url)

        if path == '/accounts/login/' and request.user.is_authenticated:
            return redirect('user:user_vendor_list')  
        if path.startswith('/user/vendor/') and not request.user.is_superuser:
            messages.error(request, "You do not have permission to access this section.")
            raise Http404("Page not found")

        return None
