import os
import sys
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import JsonResponse, HttpResponse
from django.urls import path, re_path
from django.views.static import serve

# 1. Configure Django Settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY='development-secret-key',
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=['*'],
        INSTALLED_APPS=[
            'corsheaders',
        ],
        MIDDLEWARE=[
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.common.CommonMiddleware',
        ],
        CORS_ALLOW_ALL_ORIGINS=True,
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR],
        }],
    )

# 2. Simple View to serve index.html
def home_view(request):
    with open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
        return HttpResponse(f.read())

# 3. URL Routing
urlpatterns = [
    path('', home_view),
    # Serve assets (images)
    re_path(r'^assets/(?P<path>.*)$', serve, {'document_root': os.path.join(BASE_DIR, 'assets')}),
]

# 4. Main Execution
if __name__ == "__main__":
    execute_from_command_line(sys.argv)