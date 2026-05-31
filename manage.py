import os
import sys
import json
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import JsonResponse
from django.urls import path
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv()

# 1. Configure Django Settings
if not settings.configured:
    settings.configure(
        DEBUG=os.getenv('DJANGO_DEBUG', 'False') == 'True',
        SECRET_KEY=os.getenv('DJANGO_SECRET_KEY', 'fallback-secret-key-for-dev-only'),
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
        # Email Configuration
        EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
        EMAIL_HOST='smtp.gmail.com',
        EMAIL_PORT=587,
        EMAIL_USE_TLS=True,
        EMAIL_HOST_USER=os.getenv('EMAIL_USER'),
        EMAIL_HOST_PASSWORD=os.getenv('EMAIL_PASS'),
    )

# 2. The Contact View Logic
@csrf_exempt
def contact_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('user_name')
            email = data.get('user_email')
            message = data.get('message')

            if not all([name, email, message]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            print(f'[RECV] Mission briefing from: {name}')

            # Send the email
            send_mail(
                subject=f'New Portfolio Mission: {name}',
                message=f'Commander Andrew,\n\nYou have received a new mission briefing:\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[os.getenv('RECEIVER_EMAIL', settings.EMAIL_HOST_USER)],
                fail_silently=False,
            )

            print(f'[SUCCESS] Transmission relayed to {settings.EMAIL_HOST_USER}')
            return JsonResponse({'message': 'Transmission successful!'}, status=200)

        except Exception as e:
            print(f'[CRITICAL] Signal Error: {str(e)}')
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

# 3. URL Routing
urlpatterns = [
    path('contact/', contact_view),
]

# 4. Main Execution
if __name__ == "__main__":
    execute_from_command_line(sys.argv)