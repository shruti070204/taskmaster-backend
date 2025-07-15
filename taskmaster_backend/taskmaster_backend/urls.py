#project level
from django.contrib import admin #buitin admin mod acess to admin.site.urls
from django.urls import path,include # define individual url routes, includes url patterns from other apps
from django.http import HttpResponse #retun simp res directly from view func
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def home(request):
    return HttpResponse("""
        <html>
            <head>
                <style>
                    body{margin: 0;height: 100vh;display: flex;justify-content: center;align-items: center;flex-direction: column;}
                    button{padding: 10px 20px;font-size: 16px;cursor: pointer;}
                </style>
            </head>
            <body>
                <h1> Welcome to Django Admin Panel !!! </h1>
                <button onclick="location.href='/admin/'">Go To Admin Panel </button>
            </body>
        </html>
            
    """)

urlpatterns = [
    path('',home), #binds root url / to home view
    path('admin/', admin.site.urls), #en jango interface at url /admin/
    path('api/', include('api.urls')), #this connects to app's url
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 