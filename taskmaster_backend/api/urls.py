#inside api/
from django.urls import path, include #define individual url pattern, include other urlconfs
from rest_framework.routers import DefaultRouter #auto gnerate routes for viewsets without defining
from .views import TaskViewSet, PriorityViewSet, AuditLogViewSet, UserViewSet,RegisterView,CustomTokenObtainPairView #my custom views
from rest_framework_simplejwt.views import(TokenObtainPairView,TokenRefreshView,) #jwt-authview provided by drf simplejwt
#register endpoints /api/...../
router = DefaultRouter() #autogenerate url patterns for viewsets
router.register(r'tasks', TaskViewSet)
router.register(r'priorities', PriorityViewSet)
router.register(r'users', UserViewSet)
#maps url to view
urlpatterns = [ #main url pattern
    path('', include(router.urls)), # includes all viewsets registerd into to root of API'/api'from urls.py
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), #return access & refresh token+username is_staff flag, used in feS
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'), #allow client to refresh ccess token using refresh, used to stay logged in without entering pwd
    path('register/',RegisterView.as_view(),name='register'), #public endpoint to allow user signup, no require authentication
]