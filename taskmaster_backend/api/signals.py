#cretes logs and send mails on task activity
from django.db.models.signals import post_save, post_delete # sigm=nal fired after model instance is saved or del
from django.dispatch import receiver #deco that connects signal to funt
from django.core.mail import send_mail #utility to send mail
from .models import Task, AuditLog # models

#triggered when task is create /update
@receiver(post_save, sender=Task)
def handle_task_save(sender, instance, created, **kwargs): #tasks obj was save, created true update false
    action = "created" if created else "updated" #dyn sets action created or updated

    # Creates auditlog record
    AuditLog.objects.create(
        user=instance.assigned_to,#user assign to task 
        task=instance,#task obj
        action=f"Task {action}: {instance.title}"
    )

    # Send email notification
    if instance.assigned_to and instance.assigned_to.email: #send if task is assigned to user has valid mail
        send_mail(
            subject=f"[Task Master] Task {action}: {instance.title}",
            message=f"Hi {instance.assigned_to.username},\n\n"
                    f"The task titled '{instance.title}' has been {action}.\n\n"
                    f"Status: {instance.status}\nDue: {instance.due_date}\nPriority: {instance.priority_level}",
            from_email='shrutimahadik2102@gmail.com',
            recipient_list=[instance.assigned_to.email],
            fail_silently=True,  # avoid crashing if fails
        )
#triggered after task del
@receiver(post_delete, sender=Task)
def handle_task_delete(sender, instance, **kwargs):
    # del log entry
    if instance.assigned_to:
        AuditLog.objects.create(
            user=instance.assigned_to,
            task=None,
            action=f"Task deleted: {instance.title}"
        ) # store in sudit log but null task as alreday del
        if instance.assigned_to.email:
            #message in this format will be sent
            send_mail(
                subject=f"[Task Master] Task deleted: {instance.title}",
                message=f"Hi {instance.assigned_to.username},\n\n"
                        f"The task titled '{instance.title}' has been deleted.",
                from_email='shrutimahadik2102@gmail.com',
                recipient_list=[instance.assigned_to.email],
                fail_silently=True,
            )