#defines db tables 
from django.db import models # orm sys for defining db tables
from django.contrib.auth.models import User # builtin user model for assigning tasks and tracking logs 

class Priority(models.Model): #riority level
    level=models.CharField(max_length=20)
    class Meta:
        verbose_name_plural = "Priorities" #instead of prioritys will show priorities
    def __str__(self): #str reprsantation for panel and shell
        return self.level # instead of priority obj 1 will show high
    
class Task(models.Model): #user assigd tasks
    STATUS_CHOICES=[
        ('TODO','To Do'),
        ('INPROGRESS','In Progress'),
        ('DONE','Done')
    ]
    #fields for user assignment and task
    title=models.CharField(max_length=255) #task title(required)
    description=models.TextField(blank=True) # optional
    status=models.CharField(max_length=20, choices=STATUS_CHOICES,default='TODO') # field using dropdown
    due_date=models.DateField(null=True,blank=True) #allows NULL in db and is optional
    assigned_to=models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks') #if user it deleted, so there tasks are also. let you access tasks from user
    #auto generate time stamp
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    priority_level = models.CharField(max_length=20,default="Medium", choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]) # dropdown for priority level

    def __str__(self):
        return self.title

# logs task actions with timestamp and user info 
class AuditLog(models.Model): #tracks who did what and when
    user= models.ForeignKey(User,on_delete=models.SET_NULL, null=True) #logs user actions. if user is remove keep log but set user as null 
    task=models.ForeignKey(Task,on_delete=models.SET_NULL, null=True,blank=True) # connects log to task, can be empty
    action=models.CharField(max_length=100) #description of what happen
    timestamp=models.DateTimeField(auto_now_add=True) # record time  of action

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}" #display str in given fromat