from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from django.shortcuts import render # redering templates
from rest_framework import viewsets,permissions,generics,status #base class for modelviewsets,to restict view,provide view (createapiview,retriveupdatedestryapiview), for http response status code(403,201)
from rest_framework_simplejwt.views import TokenObtainPairView #return jwt token on login
from rest_framework.permissions import IsAuthenticated #retrict view to authenticated  only
from rest_framework.response import Response #return json response from views
from .models import Task,Priority,AuditLog
from .serializers import TaskSerializers,PrioritySerializers,AuditLogSerializers,UserSerializers,RegisterationSerializers,CustomTokenObtainPairSerializer #to convert db obj to/from json
from django.contrib.auth.models import User#default model for authentication
import logging #to log sys msg
from django.http import JsonResponse #return json res in custom login_view

logger=logging.getLogger(__name__)
def login_view(request):
    logger.info("Login API was called")
    return JsonResponse({"message":"Login attempt recevied"}) #logs msg and return json res. used for testing

class TaskViewSet(viewsets.ModelViewSet): # provide crud opr
    queryset=Task.objects.all() #only login user can access
    serializer_class=TaskSerializers #use all tasks in db
    permission_classes=[permissions.IsAuthenticated] # used taskserializer to validate data
    filter_backends=[DjangoFilterBackend] # en filtering tasks using query param
    filterset_fields=['status','priority_level','due_date']
    def get_queryset(self): #ad see all tasks user see his only
        if self.request.user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=self.request.user)
    def perform_create(self, serializer): #created tasks auto assign to loggedin user
        serializer.save(assigned_to=self.request.user)
    def create(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        if not serializer.is_valid(): #show err if form invalid
            print("Invalid data:",serializer.errors)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer) #creates task and return success res
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#only acceessible to admin
class PriorityViewSet(viewsets.ModelViewSet):
    queryset=Priority.objects.all()
    serializer_class=PrioritySerializers
    permission_classes=[permissions.IsAdminUser]

#only acceessible to admin
class AuditLogViewSet(viewsets.ModelViewSet):
    queryset=AuditLog.objects.all().order_by('-timestamp')
    serializer_class=AuditLogSerializers
    permission_classes=[permissions.IsAdminUser]

# list all users to the admin not to user
class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializers
    permission_classes=[permissions.IsAdminUser]

#handle users register via POST
class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterationSerializers
    permission_classes=[] #allows anyone to register

#handle get,put,post and delete for task
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializers
    permission_classes = [IsAuthenticated]
#user delete own task and admin can any.
    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        if request.user != task.assigned_to and not request.user.is_staff:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)

# custom jWT token with role info
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer